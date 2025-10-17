import sys
import os
import json
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from experiment_runner.results import (
    ResultsAnalyzer,
    SummaryAnalyzer,
    DifferencesAnalyzer,
    create_combined_report,
    save_results_to_file,
)


class RQ2DirectoryFinder:
    """Utility class for dynamic results directory detection in RQ2"""

    def __init__(self, config_module):
        self.config = config_module

    def find_results_directory(self, experiment_dir, combined_only=False):
        """Find latest results directory matching current config pattern

        Args:
            experiment_dir: Directory to search in
            combined_only: If True, only search _combined directories

        Returns:
            tuple: (directory_name, mismatch_info) where:
            - directory_name: str or None if no directory found
            - mismatch_info: dict with details about pattern mismatch (None if no mismatch)
        """
        if not os.path.exists(experiment_dir):
            return None, None

        # Build pattern from current config values
        # results_{ANY_LLM}_{RATIO}_ROWS_{TD_RATIO}_TD_PUBLIC_{REATTEMPT}_REATTEMPT
        import re

        base_pattern = f"results_.*_{self.config.RATIO_OF_ROWS_TO_RUN}_ROWS_{self.config.TEST_DRIVEN_RATIO}_TD_PUBLIC_{self.config.REATTEMPT_MAX_NUM}_REATTEMPT"

        if combined_only:
            # Only look for _combined directories
            pattern = f"{base_pattern}_combined"
        else:
            # Only look for regular directories (exclude _combined)
            pattern = f"{base_pattern}$"

        regex = re.compile(pattern)

        # Find all matching directories with metadata
        candidates = []
        for item in os.listdir(experiment_dir):
            if regex.match(item) and os.path.isdir(os.path.join(experiment_dir, item)):
                dir_path = os.path.join(experiment_dir, item)

                # Collect metadata for selection
                mtime = os.path.getmtime(dir_path)
                has_summary = os.path.exists(os.path.join(dir_path, "summary.json"))

                candidates.append(
                    {
                        "name": item,
                        "path": dir_path,
                        "mtime": mtime,
                        "has_summary": has_summary,
                    }
                )

        if not candidates:
            # No directories match current config - collect mismatch info
            available_dirs = [
                item
                for item in os.listdir(experiment_dir)
                if item.startswith("results_")
            ]
            if available_dirs:
                mismatch_info = {
                    "expected_pattern": pattern,
                    "available_directories": available_dirs,
                    "current_config": {
                        "RATIO": self.config.RATIO_OF_ROWS_TO_RUN,
                        "TD_RATIO": self.config.TEST_DRIVEN_RATIO,
                        "REATTEMPT": self.config.REATTEMPT_MAX_NUM,
                    },
                }
                return None, mismatch_info
            return None, None

        # Sort by: 1) has summary.json, 2) newest modification time
        candidates.sort(key=lambda x: (x["has_summary"], x["mtime"]), reverse=True)
        return candidates[0]["name"], None


class RQ2SummaryAnalyzer(SummaryAnalyzer):
    """RQ2-specific summary analyzer with dynamic results directory detection"""

    def __init__(self, rq_dir, results_folder, config_module=None, combined_only=False):
        """Initialize with optional config module for pattern-based detection"""
        super().__init__(rq_dir, results_folder)
        self.directory_finder = RQ2DirectoryFinder(config_module)
        self.combined_only = combined_only

    def compare_summaries(self, use_remediation=False):
        """Compare summary.json files with dynamic results directory detection"""
        subdirs = [
            d
            for d in os.listdir(self.rq_dir)
            if os.path.isdir(os.path.join(self.rq_dir, d))
            and not d.endswith("_td")
            and d not in ["__pycache__", "logs", "results_all"]
            and (
                (self.combined_only and d.endswith("_combined"))
                or (
                    not self.combined_only
                    and not d.endswith("_combined")
                    and not d.endswith("_second_half")
                )
            )
        ]

        if not subdirs:
            print(f"No base directories found in {self.rq_dir}")
            return None

        print(f"Found {len(subdirs)} base directories to compare")
        print(f"Using dynamic results directory detection for RQ2")
        if use_remediation:
            print("Using remediation results for comparison")
        else:
            print("Using first attempt results for comparison")

        comparison_count = 0
        single_summary_count = 0
        td_better_count = 0
        td_same_count = 0
        td_worse_count = 0

        # Track incomplete directories for re-execution guidance
        missing_td_dirs = []
        missing_summary_files = []
        missing_accuracy_data = []
        partial_completion_dirs = []
        successful_comparisons = []
        config_mismatch_dirs = []

        detailed_results = {}

        for subdir in sorted(subdirs):
            # Check if corresponding _td directory exists
            td_dir = f"{subdir}_td"
            if not os.path.isdir(os.path.join(self.rq_dir, td_dir)):
                print(f"Warning: No matching {td_dir} directory found for {subdir}")
                missing_td_dirs.append(subdir)
                continue

            base_dir = os.path.join(self.rq_dir, subdir)
            td_dir_path = os.path.join(self.rq_dir, td_dir)

            # Dynamic results directory detection
            base_results_folder, base_mismatch = (
                self.directory_finder.find_results_directory(
                    base_dir, self.combined_only
                )
            )
            td_results_folder, td_mismatch = (
                self.directory_finder.find_results_directory(
                    td_dir_path, self.combined_only
                )
            )

            # Check for config mismatches
            if base_mismatch or td_mismatch:
                mismatch_details = {
                    "subdir": subdir,
                    "base_mismatch": base_mismatch,
                    "td_mismatch": td_mismatch,
                }
                config_mismatch_dirs.append(mismatch_details)
                print(f"Warning: Config mismatch detected for {subdir}")
                continue

            # Skip if no results directories found
            if not base_results_folder or not td_results_folder:
                missing_summary_files.append(
                    {"subdir": subdir, "missing": ["results directory not found"]}
                )
                continue

            base_summary_path = os.path.join(
                base_dir, base_results_folder, "summary.json"
            )
            td_summary_path = os.path.join(
                td_dir_path, td_results_folder, "summary.json"
            )

            base_data = self._load_summary(base_summary_path)
            td_data = self._load_summary(td_summary_path)

            if base_data is None or td_data is None:
                missing_files = []
                if base_data is None:
                    missing_files.append(f"base ({base_summary_path})")
                if td_data is None:
                    missing_files.append(f"td ({td_summary_path})")
                missing_summary_files.append(
                    {"subdir": subdir, "missing": missing_files}
                )
                continue

            # Extract accuracy for comparison
            base_acc_result = self.extract_accuracy(
                base_data, use_remediation, base_summary_path
            )
            td_acc_result = self.extract_accuracy(
                td_data, use_remediation, td_summary_path
            )

            base_acc = base_acc_result["value"]
            td_acc = td_acc_result["value"]

            if base_acc is not None and td_acc is not None:
                # Check for generation errors to determine if this is truly complete
                base_has_gen_errors = self._check_generation_errors(
                    base_dir, subdir, base_results_folder
                )
                td_has_gen_errors = self._check_generation_errors(
                    td_dir_path, td_dir, td_results_folder
                )

                # Only consider as successful if no significant generation errors occurred
                if not base_has_gen_errors and not td_has_gen_errors:
                    # Track successful comparison (fully complete experiments)
                    successful_comparisons.append(subdir)
                    comparison_count += 1
                else:
                    # Track as partial completion due to generation errors
                    partial_completion_dirs.append(
                        {
                            "subdir": subdir,
                            "base_gen_errors": base_has_gen_errors,
                            "td_gen_errors": td_has_gen_errors,
                            "base_dir": base_dir,
                            "td_dir": td_dir_path,
                        }
                    )
                    print(
                        f"Directory {subdir} has generation errors - marked as partial completion"
                    )
                    continue

                if td_acc > base_acc:
                    td_better_count += 1
                    status = "better"
                elif td_acc == base_acc:
                    td_same_count += 1
                    status = "same"
                else:
                    td_worse_count += 1
                    status = "worse"

                detailed_results[subdir] = {
                    "status": status,
                    "base_accuracy": base_acc,
                    "td_accuracy": td_acc,
                    "using_remediation": use_remediation,
                    "base_summary_path": base_summary_path,
                    "td_summary_path": td_summary_path,
                    "base_dir": base_dir,
                    "td_dir": td_dir_path,
                }
            else:
                # Track directories with missing accuracy data
                missing_acc = []
                if base_acc is None:
                    missing_acc.append("base")
                if td_acc is None:
                    missing_acc.append("td")
                missing_accuracy_data.append(
                    {
                        "subdir": subdir,
                        "missing": missing_acc,
                        "base_summary_path": base_summary_path,
                        "td_summary_path": td_summary_path,
                    }
                )

        # Print final summary (using base class methods)
        print(
            f"\n\033[94mCompleted {comparison_count} comparisons and {single_summary_count} single summaries\033[0m"
        )

        if comparison_count > 0:
            print(
                f"\033[92mTest-driven (TD) results were better in {td_better_count} out of {comparison_count} comparisons\033[0m"
            )
            print(
                f"\033[93mTest-driven (TD) results were same in {td_same_count} out of {comparison_count} comparisons\033[0m"
            )
            print(
                f"\033[91mTest-driven (TD) results were worse in {td_worse_count} out of {comparison_count} comparisons\033[0m"
            )

            # Calculate statistics
            statistics_data = self.calculate_statistics(detailed_results)

            # Print statistics (using base class method)
            print(f"\n\033[94mAccuracy Statistics:\033[0m")
            print(
                f"\033[94mTotal increase: {statistics_data['total_increase']:.2f}\033[0m"
            )
            print(
                f"\033[94mAverage increase: {statistics_data['avg_increase']:.2f} (95% CI: [{statistics_data['confidence_interval'][0]:.2f}, {statistics_data['confidence_interval'][1]:.2f}])\033[0m"
            )
            print(
                f"\033[94mMedian increase: {statistics_data['median_increase']:.2f}\033[0m"
            )
            print(
                f"\033[94mStandard deviation: {statistics_data['std_dev']:.2f}\033[0m"
            )
            print(
                f"\033[94mRange: {statistics_data['min_increase']:.2f} to {statistics_data['max_increase']:.2f}\033[0m"
            )
            print(
                f"\033[94mInterquartile range: {statistics_data['percentile_25']:.2f} to {statistics_data['percentile_75']:.2f}\033[0m"
            )

            if statistics_data["improved_count"] > 0:
                print(
                    f"\033[94mAverage improvement percentage: {statistics_data['avg_improvement_pct']:.2f}%\033[0m"
                )
            if statistics_data["worsened_count"] > 0:
                print(
                    f"\033[94mAverage regression percentage: {statistics_data['avg_regression_pct']:.2f}%\033[0m"
                )

            # Print top increases
            if statistics_data["sorted_increases_desc"]:
                print(f"\n\033[92mTop 5 Increases:\033[0m")
                for item in statistics_data["sorted_increases_desc"][:5]:
                    print(
                        f"\033[92m  {item['benchmark']}: {item['base_accuracy']:.2f} → {item['td_accuracy']:.2f} (change: {item['increase']:+.2f})\033[0m"
                    )

            # Print top regressions
            if statistics_data["sorted_regressions_asc"]:
                print(f"\n\033[91mTop 5 Regressions:\033[0m")
                for item in statistics_data["sorted_regressions_asc"][:5]:
                    print(
                        f"\033[91m  {item['benchmark']}: {item['base_accuracy']:.2f} → {item['td_accuracy']:.2f} (change: {item['increase']:+.2f})\033[0m"
                    )
        else:
            print(
                "\033[93mNo TD comparisons were possible (no matching _td directories with valid summaries)\033[0m"
            )

        # Print incomplete directories analysis
        self._print_incomplete_directories_analysis(
            len(subdirs),
            missing_td_dirs,
            missing_summary_files,
            missing_accuracy_data,
            partial_completion_dirs,
            successful_comparisons,
            config_mismatch_dirs,
        )

        summary_result = {
            "total_comparisons": comparison_count,
            "td_better": td_better_count,
            "td_same": td_same_count,
            "td_worse": td_worse_count,
            "using_remediation": use_remediation,
            "details": detailed_results,
            "rq_dir": self.rq_dir,
            "results_folder": "dynamic",  # Indicate dynamic detection was used
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "incomplete_directories": {
                "missing_td_dirs": missing_td_dirs,
                "missing_summary_files": missing_summary_files,
                "missing_accuracy_data": missing_accuracy_data,
                "partial_completion_dirs": partial_completion_dirs,
                "successful_comparisons": successful_comparisons,
                "config_mismatch_dirs": config_mismatch_dirs,
                "total_directories": len(subdirs),
            },
        }

        # Add statistics to the summary result
        if comparison_count > 0:
            summary_result["accuracy_statistics"] = statistics_data

        return summary_result

    def _print_incomplete_directories_analysis(
        self,
        total_dirs,
        missing_td_dirs,
        missing_summary_files,
        missing_accuracy_data,
        partial_completion_dirs,
        successful_comparisons,
        config_mismatch_dirs,
    ):
        """Print detailed analysis of incomplete experiment directories including config mismatches"""
        print(f"\n\033[96m{'='*60}\033[0m")
        print(f"\033[96mINCOMPLETE DIRECTORIES ANALYSIS\033[0m")
        print(f"\033[96m{'='*60}\033[0m")

        total_incomplete = (
            len(missing_td_dirs)
            + len(missing_summary_files)
            + len(missing_accuracy_data)
            + len(partial_completion_dirs)
            + len(config_mismatch_dirs)
        )
        completion_rate = (
            (len(successful_comparisons) / total_dirs * 100) if total_dirs > 0 else 0
        )
        print(
            f"\033[94mCompletion Status: {len(successful_comparisons)}/{total_dirs} directories ({completion_rate:.1f}%)\033[0m"
        )
        print(f"\033[94mIncomplete Directories: {total_incomplete}\033[0m\n")

        # Config Mismatch Directories (new category)
        if config_mismatch_dirs:
            print(
                f"\033[91m🚫 Config Mismatch Directories ({len(config_mismatch_dirs)} dirs):\033[0m"
            )
            for mismatch in config_mismatch_dirs[:5]:  # Show first 5
                subdir = mismatch["subdir"]
                base_mismatch = mismatch.get("base_mismatch")
                td_mismatch = mismatch.get("td_mismatch")

                if base_mismatch:
                    available = (
                        base_mismatch["available_directories"][0]
                        if base_mismatch["available_directories"]
                        else "none"
                    )
                    print(f"\033[91m   {subdir}: Found {available}\033[0m")
                elif td_mismatch:
                    available = (
                        td_mismatch["available_directories"][0]
                        if td_mismatch["available_directories"]
                        else "none"
                    )
                    print(f"\033[91m   {subdir}_td: Found {available}\033[0m")

            if len(config_mismatch_dirs) > 5:
                print(f"\033[91m   ... and {len(config_mismatch_dirs) - 5} more\033[0m")

            # Show config fix suggestion
            if config_mismatch_dirs:
                first_mismatch = config_mismatch_dirs[0]
                mismatch_info = first_mismatch.get(
                    "base_mismatch"
                ) or first_mismatch.get("td_mismatch")
                if mismatch_info and mismatch_info["available_directories"]:
                    # Try to parse config from first available directory
                    available_dir = mismatch_info["available_directories"][0]
                    print(
                        f"\n\033[93m💡 Fix: Update config to match existing results:\033[0m"
                    )

                    # Extract values from directory name pattern
                    import re

                    match = re.search(
                        r"_(\d+\.?\d*)_ROWS_(\d+\.?\d*)_TD_PUBLIC_(\d+)_REATTEMPT",
                        available_dir,
                    )
                    if match:
                        found_ratio, found_td_ratio, found_reattempt = match.groups()
                        current_config = mismatch_info["current_config"]

                        if str(found_td_ratio) != str(current_config["TD_RATIO"]):
                            print(
                                f"\033[93m   TEST_DRIVEN_RATIO = {found_td_ratio} (currently {current_config['TD_RATIO']})\033[0m"
                            )
                        if str(found_reattempt) != str(current_config["REATTEMPT"]):
                            print(
                                f"\033[93m   REATTEMPT_MAX_NUM = {found_reattempt} (currently {current_config['REATTEMPT']})\033[0m"
                            )
            print()

        # Call parent method for other categories (if they exist)
        if (
            missing_td_dirs
            or missing_summary_files
            or missing_accuracy_data
            or partial_completion_dirs
        ):
            # Show other incomplete categories using base analyzer logic
            if missing_td_dirs:
                print(
                    f"\033[91m❌ Missing TD Directories ({len(missing_td_dirs)} dirs):\033[0m"
                )
                for subdir in missing_td_dirs[:5]:
                    print(
                        f"\033[91m   {subdir}: No matching {subdir}_td directory\033[0m"
                    )
                if len(missing_td_dirs) > 5:
                    print(f"\033[91m   ... and {len(missing_td_dirs) - 5} more\033[0m")
                print()

        # Show successful comparisons
        if successful_comparisons:
            print(
                f"\n\033[92m✅ Successful Comparisons ({len(successful_comparisons)} dirs):\033[0m"
            )
            shown_dirs = successful_comparisons[:10]
            print(f"\033[92m   {', '.join(shown_dirs)}\033[0m")
            if len(successful_comparisons) > 10:
                print(
                    f"\033[92m   ... and {len(successful_comparisons) - 10} more\033[0m"
                )

        print(f"\033[96m{'='*60}\033[0m\n")


class RQ2DifferencesAnalyzer(DifferencesAnalyzer):
    """RQ2-specific differences analyzer with dynamic results directory detection"""

    def __init__(self, rq_dir, results_folder, config_module=None, combined_only=False):
        """Initialize with optional config module for pattern-based detection"""
        super().__init__(rq_dir, results_folder)
        self.directory_finder = RQ2DirectoryFinder(config_module)
        self.combined_only = combined_only

    def run_analysis(self, use_remediation=False):
        """Run detailed differences analysis with dynamic results directory detection"""
        subdirs = [
            d
            for d in os.listdir(self.rq_dir)
            if os.path.isdir(os.path.join(self.rq_dir, d))
            and not d.endswith("_td")
            and d not in ["__pycache__", "logs", "results_all"]
            and (
                (self.combined_only and d.endswith("_combined"))
                or (
                    not self.combined_only
                    and not d.endswith("_combined")
                    and not d.endswith("_second_half")
                )
            )
        ]

        if not subdirs:
            print(f"No base directories found in {self.rq_dir}")
            return None

        print(f"Found {len(subdirs)} base directories to compare")
        print(
            f"Looking for runner_passed.json, runner_fails.json, runner_errors.json using dynamic directory detection"
        )
        if use_remediation:
            print("Using remediation results (all attempts)")
        else:
            print("Using first attempt results only")

        comparison_count = 0
        detailed_results = {}

        for subdir in sorted(subdirs):
            td_dir = f"{subdir}_td"
            base_dir = os.path.join(self.rq_dir, subdir)
            td_dir_path = os.path.join(self.rq_dir, td_dir)

            if not os.path.isdir(td_dir_path):
                print(f"Warning: No matching {td_dir} directory found for {subdir}")
                continue

            # Dynamic results directory detection
            base_results_folder, base_mismatch = (
                self.directory_finder.find_results_directory(
                    base_dir, self.combined_only
                )
            )
            td_results_folder, td_mismatch = (
                self.directory_finder.find_results_directory(
                    td_dir_path, self.combined_only
                )
            )

            # Skip directories with config mismatches or no results found
            # These are already tracked in the summary analysis
            if (
                base_mismatch
                or td_mismatch
                or not base_results_folder
                or not td_results_folder
            ):
                print(
                    f"Warning: Config mismatch or no results directory found for {subdir}"
                )
                continue

            base_results_dir = os.path.join(base_dir, base_results_folder)
            td_results_dir = os.path.join(td_dir_path, td_results_folder)

            if not os.path.isdir(base_results_dir):
                print(f"Warning: No results folder found in {subdir}")
                continue
            if not os.path.isdir(td_results_dir):
                print(f"Warning: No results folder found in {td_dir}")
                continue

            base_summary_path = os.path.join(base_results_dir, "summary.json")
            td_summary_path = os.path.join(td_results_dir, "summary.json")

            if os.path.isfile(base_summary_path) and os.path.isfile(td_summary_path):
                base_data = self._load_summary(base_summary_path)
                td_data = self._load_summary(td_summary_path)

                if base_data is not None and td_data is not None:
                    base_counts = self.extract_counts(base_data, use_remediation)
                    td_counts = self.extract_counts(td_data, use_remediation)
                    diffs = self.compare_counts(base_counts, td_counts)

                    comparison_result = self.print_comparison(
                        subdir,
                        td_dir,
                        base_counts,
                        td_counts,
                        diffs,
                        base_results_dir,
                        td_results_dir,
                        base_data,
                        td_data,
                        use_remediation,
                    )

                    detailed_results[subdir] = comparison_result
                    comparison_count += 1

        if comparison_count == 0:
            print("\n\033[91mNo valid result folders found for any comparisons.\033[0m")
        else:
            print(
                f"\n\033[94mCompleted {comparison_count} comprehensive analyses.\033[0m"
            )

        # Add metadata to the detailed results
        result_with_metadata = {
            "metadata": {
                "rq_dir": self.rq_dir,
                "results_folder": "dynamic",  # Indicate dynamic detection was used
                "use_remediation": use_remediation,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
            "results": detailed_results,
        }

        return result_with_metadata


class RQ2ResultsAnalyzer(ResultsAnalyzer):
    """RQ2-specific results analyzer with dynamic results directory detection"""

    def __init__(self, research_question, config_module, combined_only=False):
        """Initialize with directory finder for dynamic detection"""
        super().__init__(research_question, config_module)
        self.directory_finder = RQ2DirectoryFinder(config_module)
        self.combined_only = combined_only

    def _collect_experiment_metadata(self):
        """Collect metadata from all experiment directories using dynamic detection"""
        metadata_list = []

        # Find all subdirectories in the RQ directory
        if not os.path.exists(self.rq_dir):
            return metadata_list

        subdirs = [
            d
            for d in os.listdir(self.rq_dir)
            if os.path.isdir(os.path.join(self.rq_dir, d))
            and not d.endswith("_td")
            and d not in ["__pycache__", "logs", "results_all"]
            and (
                (self.combined_only and d.endswith("_combined"))
                or (
                    not self.combined_only
                    and not d.endswith("_combined")
                    and not d.endswith("_second_half")
                )
            )
        ]

        for subdir in subdirs:
            experiment_dir = os.path.join(self.rq_dir, subdir)
            # Use dynamic results directory detection
            results_folder, mismatch_info = (
                self.directory_finder.find_results_directory(
                    experiment_dir, self.combined_only
                )
            )

            # Skip directories with config mismatches or no results found
            # These are already tracked in the summary analysis
            if not results_folder:
                continue

            results_dir = os.path.join(experiment_dir, results_folder)

            if os.path.exists(results_dir):
                # Look for metadata file - try different patterns
                metadata_patterns = [f"{subdir}_metadata.json", "metadata.json"]

                for pattern in metadata_patterns:
                    metadata_path = os.path.join(results_dir, pattern)
                    if os.path.exists(metadata_path):
                        metadata = self._load_metadata(metadata_path)
                        if metadata:
                            metadata_list.append(metadata)
                        break

        return metadata_list

    def run_analysis(self):
        """Main function to run the combined analysis with RQ2-specific analyzers"""
        combined_filename = "combined_report"

        # Create output directory with dynamic naming based on config
        combined_suffix = "_combined" if self.combined_only else ""
        output_dir_name = f"results_dynamic_llm_{self.config.RATIO_OF_ROWS_TO_RUN}_ROWS_{self.config.TEST_DRIVEN_RATIO}_TD_PUBLIC_{self.config.REATTEMPT_MAX_NUM}_REATTEMPT{combined_suffix}"
        output_dir = os.path.join(self.results_all_dir, output_dir_name)
        self._ensure_dir_exists(output_dir)

        # Create RQ2-specific analyzers
        summary_analyzer = RQ2SummaryAnalyzer(
            self.rq_dir, "dynamic", self.config, self.combined_only
        )
        differences_analyzer = RQ2DifferencesAnalyzer(
            self.rq_dir, "dynamic", self.config, self.combined_only
        )

        # Run analysis for first attempt only
        print("\n=== First Attempt Analysis ===\n")
        summary_first_attempt = summary_analyzer.compare_summaries(
            use_remediation=False
        )

        # Run analysis with remediation
        print("\n=== Remediation Analysis ===\n")
        summary_remediation = summary_analyzer.compare_summaries(use_remediation=True)

        # Run detailed analysis for first attempt only
        print("\n=== Detailed First Attempt Analysis ===\n")
        differences_first_attempt = differences_analyzer.run_analysis(
            use_remediation=False
        )

        # Run detailed analysis with remediation
        print("\n=== Detailed Remediation Analysis ===\n")
        differences_remediation = differences_analyzer.run_analysis(
            use_remediation=True
        )

        # Collect metadata from experiment directories
        metadata_list = self._collect_experiment_metadata()

        # Create and save combined report
        combined_report = create_combined_report(
            summary_first_attempt,
            summary_remediation,
            differences_first_attempt,
            differences_remediation,
            metadata_list,
        )
        save_results_to_file(output_dir, combined_filename, combined_report)

        # Save individual reports as well
        save_results_to_file(
            output_dir,
            "first_attempt_summary",
            json.dumps(summary_first_attempt, indent=2),
            "json",
        )
        save_results_to_file(
            output_dir,
            "remediation_summary",
            json.dumps(summary_remediation, indent=2),
            "json",
        )
        save_results_to_file(
            output_dir,
            "first_attempt_details",
            json.dumps(differences_first_attempt, indent=2),
            "json",
        )
        save_results_to_file(
            output_dir,
            "remediation_details",
            json.dumps(differences_remediation, indent=2),
            "json",
        )

        # Print the combined report to console
        print("\n\n" + combined_report)
