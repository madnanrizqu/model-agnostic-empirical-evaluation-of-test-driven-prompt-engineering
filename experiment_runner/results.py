import os
import json
import sys
from pathlib import Path
from io import StringIO
import contextlib
from datetime import datetime
import statistics
import math
from scipy import stats
import pingouin as pg

# Add the root directory to sys.path for imports
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)


class ResultsAnalyzer:
    """Shared results analysis for all research questions with extension points"""

    def __init__(
        self, research_question, config_module, exclude_dirs=None, include_dirs=None
    ):
        """Initialize with research question parameterization"""
        self.research_question = research_question
        self.config = config_module
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.rq_dir = os.path.join(self.base_dir, "..", research_question)
        self.results_all_dir = os.path.join(self.rq_dir, "results_all")
        self.exclude_dirs = exclude_dirs or []
        self.include_dirs = include_dirs

        # Get result directory name from config
        self.results_folder = getattr(config_module, "RESULT_DIR_NAME", "results")

    def _ensure_dir_exists(self, dir_path):
        """Create directory if it doesn't exist."""
        os.makedirs(dir_path, exist_ok=True)

    def _load_summary(self, path):
        """Load a summary.json file if it exists."""
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: File not found: {path}")
            return None
        except json.JSONDecodeError:
            print(f"Warning: Could not parse JSON: {path}")
            return None

    def _load_metadata(self, path):
        """Load a metadata.json file if it exists."""
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Metadata file not found: {path}")
            return None
        except json.JSONDecodeError:
            print(f"Warning: Could not parse metadata JSON: {path}")
            return None

    def _load_generation_errors(self, path):
        """Load generation errors from *_errors.json file if it exists."""
        try:
            with open(path, "r") as f:
                errors = json.load(f)
                return errors if isinstance(errors, list) else []
        except FileNotFoundError:
            print(f"Warning: Generation errors file not found: {path}")
            return []
        except json.JSONDecodeError:
            print(f"Warning: Could not parse generation errors JSON: {path}")
            return []

    def _apply_custom_processing(self, data, processing_type="default"):
        """Extension point for RQ-specific result processing"""
        return data

    def _get_custom_summary_filters(self):
        """Extension point for custom summary filtering"""
        return {}

    def _collect_experiment_metadata(self):
        """Collect metadata from all experiment directories"""
        metadata_list = []

        # Find all subdirectories in the RQ directory
        if not os.path.exists(self.rq_dir):
            return metadata_list

        # Apply directory filtering based on include/exclude lists
        if self.include_dirs is not None:
            subdirs = [
                d
                for d in self.include_dirs
                if os.path.isdir(os.path.join(self.rq_dir, d)) and not d.endswith("_td")
            ]
        else:
            excluded_dirs = {"__pycache__", "logs", "results_all"} | set(
                self.exclude_dirs
            )
            subdirs = [
                d
                for d in os.listdir(self.rq_dir)
                if os.path.isdir(os.path.join(self.rq_dir, d))
                and not d.endswith("_td")
                and d not in excluded_dirs
            ]

        for subdir in subdirs:
            experiment_dir = os.path.join(self.rq_dir, subdir)
            results_dir = os.path.join(experiment_dir, self.results_folder)

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
        """Main function to run the combined analysis with extension support"""
        combined_filename = "combined_report"

        # Create timestamp for directory naming (filesystem-safe format)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create output directory without timestamp suffix
        output_dir = os.path.join(self.results_all_dir, self.results_folder)
        self._ensure_dir_exists(output_dir)

        # Create analyzers and run analyses
        summary_analyzer = SummaryAnalyzer(
            self.rq_dir, self.results_folder, self.exclude_dirs, self.include_dirs
        )

        # Run analysis for first attempt only
        print("\n=== First Attempt Analysis ===\n")
        summary_first_attempt = summary_analyzer.compare_summaries(
            use_remediation=False
        )

        # Run analysis with remediation
        print("\n=== Remediation Analysis ===\n")
        summary_remediation = summary_analyzer.compare_summaries(use_remediation=True)

        differences_analyzer = DifferencesAnalyzer(
            self.rq_dir, self.results_folder, self.exclude_dirs, self.include_dirs
        )

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

        # Apply custom processing to results
        summary_first_attempt = self._apply_custom_processing(
            summary_first_attempt, "summary_first"
        )
        summary_remediation = self._apply_custom_processing(
            summary_remediation, "summary_remediation"
        )
        differences_first_attempt = self._apply_custom_processing(
            differences_first_attempt, "differences_first"
        )
        differences_remediation = self._apply_custom_processing(
            differences_remediation, "differences_remediation"
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


class SummaryAnalyzer:
    """Class for analyzing summaries between base and TD directories."""

    def __init__(self, rq_dir, results_folder, exclude_dirs=None, include_dirs=None):
        """Initialize the analyzer with RQ directory and results folder."""
        self.rq_dir = rq_dir
        self.results_folder = results_folder
        self.exclude_dirs = exclude_dirs or []
        self.include_dirs = include_dirs

    def _load_summary(self, path):
        """Load a summary.json file if it exists."""
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: File not found: {path}")
            return None
        except json.JSONDecodeError:
            print(f"Warning: Could not parse JSON: {path}")
            return None

    def _load_metadata(self, path):
        """Load a metadata.json file if it exists."""
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Metadata file not found: {path}")
            return None
        except json.JSONDecodeError:
            print(f"Warning: Could not parse metadata JSON: {path}")
            return None

    def _load_generation_errors(self, path):
        """Load generation errors from *_errors.json file if it exists."""
        try:
            with open(path, "r") as f:
                errors = json.load(f)
                return errors if isinstance(errors, list) else []
        except FileNotFoundError:
            print(f"Warning: Generation errors file not found: {path}")
            return []
        except json.JSONDecodeError:
            print(f"Warning: Could not parse generation errors JSON: {path}")
            return []

    def _check_generation_errors(self, experiment_dir, dataset_name, results_folder):
        """
        Check if a directory has significant generation errors that prevented full dataset processing.
        Returns True if there are generation errors that make the experiment incomplete.
        """
        results_dir = os.path.join(experiment_dir, results_folder)

        # Use the actual dataset name as it appears in the directory (including _td if present)
        # The metadata files are named with the full dataset name including _td suffix

        # Load metadata to get expected total
        metadata_path = os.path.join(results_dir, f"{dataset_name}_metadata.json")
        metadata = self._load_metadata(metadata_path)

        # Load generation errors
        errors_path = os.path.join(results_dir, f"{dataset_name}_errors.json")
        generation_errors = self._load_generation_errors(errors_path)

        if metadata is None:
            # No metadata file means old experiment, assume complete for backward compatibility
            return len(generation_errors) > 0  # Any generation errors = incomplete

        expected_total = metadata.get("expected_total", 0)
        generation_error_count = len(generation_errors)

        # Zero-tolerance approach: Any generation errors make the experiment incomplete
        # This ensures complete experimental integrity
        is_incomplete = generation_error_count > 0

        if is_incomplete:
            print(
                f"  {dataset_name}: {generation_error_count}/{expected_total} generation errors - experiment incomplete (zero-tolerance policy)"
            )

        return is_incomplete

    def extract_accuracy(self, summary_data, use_remediation=False, file_path=None):
        """Extract accuracy value from summary data, optionally using remediation data."""
        result = {"value": None, "file_path": file_path}

        if not summary_data or not isinstance(summary_data, dict):
            return result

        for v in summary_data.values():
            if isinstance(v, dict):
                if (
                    use_remediation
                    and "remediation" in v
                    and "accuracy" in v["remediation"]
                ):
                    try:
                        result["value"] = float(v["remediation"]["accuracy"])
                        return result
                    except Exception:
                        return result
                elif "accuracy" in v and not use_remediation:
                    try:
                        result["value"] = float(v["accuracy"])
                        return result
                    except Exception:
                        return result
        return result

    def calculate_statistics(self, detailed_results):
        """Calculate accuracy change statistics from the detailed results."""
        if not detailed_results:
            return {
                "increases": [],
                "total_increase": 0,
                "avg_increase": 0,
                "median_increase": 0,
                "std_dev": 0,
                "min_increase": 0,
                "max_increase": 0,
                "percentile_25": 0,
                "percentile_75": 0,
                "improved_count": 0,
                "worsened_count": 0,
                "same_count": 0,
                "avg_improvement_pct": 0,
                "avg_regression_pct": 0,
                "confidence_interval": [0, 0],
                "sorted_increases_desc": [],
                "sorted_regressions_asc": [],
                "normality_test_stat": None,
                "normality_p_value": None,
                "is_normal": None,
                "significance_test_type": None,
                "significance_test_stat": None,
                "significance_p_value": None,
                "cohens_d": None,
                "effect_size_interpretation": None,
            }

        # Collect all accuracy increases/decreases
        increases = []
        benchmark_details = []

        for benchmark, details in detailed_results.items():
            base_acc = details.get("base_accuracy")
            td_acc = details.get("td_accuracy")

            if base_acc is not None and td_acc is not None:
                increase = td_acc - base_acc
                increases.append(increase)
                benchmark_details.append(
                    {
                        "benchmark": benchmark,
                        "base_accuracy": base_acc,
                        "td_accuracy": td_acc,
                        "increase": increase,
                        # Add percentage change relative to base
                        "pct_change": (
                            (increase / base_acc * 100) if base_acc > 0 else 0
                        ),
                    }
                )

        if not increases:
            return {
                "increases": [],
                "total_increase": 0,
                "avg_increase": 0,
                "median_increase": 0,
                "std_dev": 0,
                "min_increase": 0,
                "max_increase": 0,
                "percentile_25": 0,
                "percentile_75": 0,
                "improved_count": 0,
                "worsened_count": 0,
                "same_count": 0,
                "avg_improvement_pct": 0,
                "avg_regression_pct": 0,
                "confidence_interval": [0, 0],
                "sorted_increases_desc": [],
                "sorted_regressions_asc": [],
                "normality_test_stat": None,
                "normality_p_value": None,
                "is_normal": None,
                "significance_test_type": None,
                "significance_test_stat": None,
                "significance_p_value": None,
                "cohens_d": None,
                "effect_size_interpretation": None,
            }

        # Calculate basic statistics
        total_increase = sum(increases)
        avg_increase = statistics.mean(increases)
        median_increase = statistics.median(increases)

        # Calculate standard deviation
        std_dev = statistics.stdev(increases) if len(increases) > 1 else 0

        # Calculate min and max
        min_increase = min(increases)
        max_increase = max(increases)

        # Calculate percentiles
        sorted_increases = sorted(increases)
        if len(sorted_increases) >= 2:
            quartiles = statistics.quantiles(sorted_increases, n=4, method="inclusive")
            percentile_25 = quartiles[0]
            percentile_75 = quartiles[2]
        else:
            percentile_25 = min_increase
            percentile_75 = max_increase

        # Calculate IQR (Interquartile Range)
        interquartile_range = percentile_75 - percentile_25

        # Count improved/worsened/unchanged benchmarks
        improved_count = sum(1 for inc in increases if inc > 0)
        worsened_count = sum(1 for inc in increases if inc < 0)
        same_count = sum(1 for inc in increases if inc == 0)

        # Calculate average percentage improvement/regression
        improved_pcts = [
            detail["pct_change"]
            for detail in benchmark_details
            if detail["increase"] > 0
        ]
        regression_pcts = [
            detail["pct_change"]
            for detail in benchmark_details
            if detail["increase"] < 0
        ]

        avg_improvement_pct = statistics.mean(improved_pcts) if improved_pcts else 0
        avg_regression_pct = statistics.mean(regression_pcts) if regression_pcts else 0

        # Calculate 95% confidence interval for the mean using t-distribution
        if len(increases) > 1:
            confidence_interval = stats.t.interval(
                0.95,  # 95% confidence level
                len(increases) - 1,  # degrees of freedom
                loc=avg_increase,  # mean
                scale=stats.sem(increases),  # standard error of mean
            )
        else:
            confidence_interval = [avg_increase, avg_increase]

        # Statistical Tests: Step 1 - Normality Check
        if len(increases) > 2:
            normality_stat, normality_p = stats.shapiro(increases)
            normality_stat = float(normality_stat)
            normality_p = float(normality_p)
            is_normal = bool(normality_p > 0.05)
        else:
            # Not enough data for normality test
            normality_stat, normality_p = None, None
            is_normal = True

        # Statistical Tests: Step 2 - Significance Test (based on normality)
        if len(increases) > 1:
            base_accuracies = [detail["base_accuracy"] for detail in benchmark_details]
            td_accuracies = [detail["td_accuracy"] for detail in benchmark_details]

            if is_normal:
                # Use parametric paired t-test
                test_stat, test_p = stats.ttest_rel(td_accuracies, base_accuracies)
                test_stat = float(test_stat)
                test_p = float(test_p)
                test_type = "paired_t_test"
            else:
                # Use non-parametric Wilcoxon signed-rank test
                test_stat, test_p = stats.wilcoxon(td_accuracies, base_accuracies)
                test_stat = float(test_stat)
                test_p = float(test_p)
                test_type = "wilcoxon_signed_rank"
        else:
            test_stat, test_p = None, None
            test_type = None

        # Statistical Tests: Step 3 - Effect Size (Cohen's d)
        if len(increases) > 1:
            base_accuracies = [detail["base_accuracy"] for detail in benchmark_details]
            td_accuracies = [detail["td_accuracy"] for detail in benchmark_details]

            cohens_d = pg.compute_effsize(
                td_accuracies, base_accuracies, paired=True, eftype="cohen"
            )
            cohens_d = float(cohens_d)  # Convert to Python float

            # Interpret effect size
            if abs(cohens_d) < 0.2:
                effect_interpretation = "negligible"
            elif abs(cohens_d) < 0.5:
                effect_interpretation = "small"
            elif abs(cohens_d) < 0.8:
                effect_interpretation = "medium"
            else:
                effect_interpretation = "large"
        else:
            cohens_d = None
            effect_interpretation = None

        # Sort by increase (descending for increases, ascending for regressions)
        benchmark_details.sort(key=lambda x: x["increase"], reverse=True)
        sorted_increases_desc = benchmark_details.copy()  # All increases, sorted desc

        benchmark_details.sort(key=lambda x: x["increase"])
        sorted_regressions_asc = benchmark_details.copy()  # All regressions, sorted asc

        return {
            # Descriptive statistics
            "increases": increases,
            "total_increase": total_increase,
            "avg_increase": avg_increase,
            "median_increase": median_increase,
            "std_dev": std_dev,
            "min_increase": min_increase,
            "max_increase": max_increase,
            "percentile_25": percentile_25,
            "percentile_75": percentile_75,
            "interquartile_range": interquartile_range,
            "improved_count": improved_count,
            "worsened_count": worsened_count,
            "same_count": same_count,
            "avg_improvement_pct": avg_improvement_pct,
            "avg_regression_pct": avg_regression_pct,
            "confidence_interval": confidence_interval,
            "sorted_increases_desc": sorted_increases_desc,
            "sorted_regressions_asc": sorted_regressions_asc,
            # Advanced statistics
            "normality_test_stat": normality_stat,
            "normality_p_value": normality_p,
            "is_normal": is_normal,
            "significance_test_type": test_type,
            "significance_test_stat": test_stat,
            "significance_p_value": test_p,
            "cohens_d": cohens_d,
            "effect_size_interpretation": effect_interpretation,
        }

    def compare_summaries(self, use_remediation=False):
        """Compare summary.json files between base directories and their TD counterparts."""
        # Apply directory filtering based on include/exclude lists
        if self.include_dirs is not None:
            subdirs = [
                d
                for d in self.include_dirs
                if os.path.isdir(os.path.join(self.rq_dir, d)) and not d.endswith("_td")
            ]
        else:
            excluded_dirs = {"__pycache__", "logs", "results_all"} | set(
                self.exclude_dirs
            )
            subdirs = [
                d
                for d in os.listdir(self.rq_dir)
                if os.path.isdir(os.path.join(self.rq_dir, d))
                and not d.endswith("_td")
                and d not in excluded_dirs
            ]

        if not subdirs:
            print(f"No base directories found in {self.rq_dir}")
            return None

        print(f"Found {len(subdirs)} base directories to compare")
        print(f"Looking for summary.json files in '{self.results_folder}' folders")
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

            base_summary_path = os.path.join(
                base_dir, self.results_folder, "summary.json"
            )
            td_summary_path = os.path.join(
                td_dir_path, self.results_folder, "summary.json"
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
                    base_dir, subdir, self.results_folder
                )
                td_has_gen_errors = self._check_generation_errors(
                    td_dir_path, td_dir, self.results_folder
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

        # Print final summary
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

            # Print statistics
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
        )

        summary_result = {
            "total_comparisons": comparison_count,
            "td_better": td_better_count,
            "td_same": td_same_count,
            "td_worse": td_worse_count,
            "using_remediation": use_remediation,
            "details": detailed_results,
            "rq_dir": self.rq_dir,
            "results_folder": self.results_folder,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "incomplete_directories": {
                "missing_td_dirs": missing_td_dirs,
                "missing_summary_files": missing_summary_files,
                "missing_accuracy_data": missing_accuracy_data,
                "partial_completion_dirs": partial_completion_dirs,
                "successful_comparisons": successful_comparisons,
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
    ):
        """Print detailed analysis of incomplete experiment directories"""
        print(f"\n\033[96m{'='*60}\033[0m")
        print(f"\033[96mINCOMPLETE DIRECTORIES ANALYSIS\033[0m")
        print(f"\033[96m{'='*60}\033[0m")

        total_incomplete = (
            len(missing_td_dirs)
            + len(missing_summary_files)
            + len(missing_accuracy_data)
            + len(partial_completion_dirs)
        )
        completion_rate = (
            (len(successful_comparisons) / total_dirs * 100) if total_dirs > 0 else 0
        )

        print(
            f"\033[94mCompletion Status: {len(successful_comparisons)}/{total_dirs} directories ({completion_rate:.1f}%)\033[0m"
        )
        print(f"\033[94mIncomplete Directories: {total_incomplete}\033[0m\n")

        # Missing TD Directories
        if missing_td_dirs:
            print(
                f"\033[91m🔴 Missing TD Directories ({len(missing_td_dirs)} dirs need TD experiments):\033[0m"
            )
            for subdir in missing_td_dirs:
                print(f"   - {subdir}")
                rq_name = os.path.basename(self.rq_dir)
                print(
                    f"     \033[93mRun: python {rq_name}/{subdir}_td/get_solution.py\033[0m"
                )
            print()

        # Missing Summary Files
        if missing_summary_files:
            print(
                f"\033[93m🟡 Missing Summary Files ({len(missing_summary_files)} dirs need test execution):\033[0m"
            )
            for item in missing_summary_files:
                subdir = item["subdir"]
                missing = item["missing"]
                print(f"   - {subdir}: Missing {', '.join(missing)}")
                rq_name = os.path.basename(self.rq_dir)
                print(
                    f"     \033[93mRun: python {rq_name}/{subdir}/test_solution.py\033[0m"
                )
                if "td" in " ".join(missing):
                    print(
                        f"     \033[93mRun: python {rq_name}/{subdir}_td/test_solution.py\033[0m"
                    )
            print()

        # Missing Accuracy Data
        if missing_accuracy_data:
            print(
                f"\033[95m🟣 Missing Accuracy Data ({len(missing_accuracy_data)} dirs need investigation):\033[0m"
            )
            for item in missing_accuracy_data:
                subdir = item["subdir"]
                missing = item["missing"]
                print(f"   - {subdir}: Missing {', '.join(missing)} accuracy")
                print(
                    f"     \033[95mCheck: {item['base_summary_path'] if 'base' in missing else item['td_summary_path']}\033[0m"
                )
            print()

        # Partial Completion Due to Generation Errors
        if partial_completion_dirs:
            print(
                f"\033[93m🟠 Partial Completion ({len(partial_completion_dirs)} dirs have generation errors):\033[0m"
            )
            for item in partial_completion_dirs:
                subdir = item["subdir"]
                base_errors = item["base_gen_errors"]
                td_errors = item["td_gen_errors"]
                error_status = []
                if base_errors:
                    error_status.append("base")
                if td_errors:
                    error_status.append("td")
                print(f"   - {subdir}: Generation errors in {', '.join(error_status)}")
                rq_name = os.path.basename(self.rq_dir)
                print(
                    f"     \033[93mRe-run: python {rq_name}/{subdir}/get_solution.py\033[0m"
                )
                if td_errors:
                    print(
                        f"     \033[93mRe-run: python {rq_name}/{subdir}_td/get_solution.py\033[0m"
                    )
            print()

        # Success Summary
        if successful_comparisons:
            print(
                f"\033[92m✅ Successful Comparisons ({len(successful_comparisons)} dirs):\033[0m"
            )
            print(f"   {', '.join(successful_comparisons[:10])}")
            if len(successful_comparisons) > 10:
                print(f"   ... and {len(successful_comparisons) - 10} more")
            print()

        print(f"\033[96m{'='*60}\033[0m\n")


class DifferencesAnalyzer:
    """Class for analyzing differences between base and TD directories."""

    def __init__(self, rq_dir, results_folder, exclude_dirs=None, include_dirs=None):
        """Initialize the analyzer with RQ directory and results folder."""
        self.rq_dir = rq_dir
        self.results_folder = results_folder
        self.exclude_dirs = exclude_dirs or []
        self.include_dirs = include_dirs

    def _load_summary(self, path):
        """Load a summary.json file if it exists."""
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: File not found: {path}")
            return None
        except json.JSONDecodeError:
            print(f"Warning: Could not parse JSON: {path}")
            return None

    def extract_counts(self, summary_data, use_remediation=False):
        """
        Recursively extract passed, failed, and error counts from summary data and map to success, fail, error.
        If use_remediation is True, use the remediation statistics if available.
        Now includes generation errors in the error count for complete statistics.
        """
        counts = {
            "success": 0,
            "fail": 0,
            "error": 0,
            "generation_errors": 0,
            "test_errors": 0,
        }

        if not summary_data or not isinstance(summary_data, dict):
            return counts

        for llm_name, stats in summary_data.items():
            if not isinstance(stats, dict):
                continue

            if use_remediation and "remediation" in stats:
                counts["success"] += stats["remediation"].get("passed", 0)
                counts["fail"] += stats["remediation"].get("failed", 0)
                counts["error"] += stats["remediation"].get("error", 0)
                counts["test_errors"] += stats["remediation"].get("test_errors", 0)
                counts["generation_errors"] += stats["remediation"].get(
                    "generation_errors", 0
                )
            else:
                counts["success"] += stats.get("passed", 0)
                counts["fail"] += stats.get("failed", 0)
                counts["error"] += stats.get("error", 0)
                counts["test_errors"] += stats.get("test_errors", 0)
                counts["generation_errors"] += stats.get("generation_errors", 0)

        return counts

    def compare_counts(self, base_counts, td_counts):
        """Compare base and TD counts for success, fail, and error."""
        diffs = {}
        for k in base_counts:
            diffs[k] = td_counts[k] - base_counts[k]
        return diffs

    def extract_accuracy(self, summary_data, use_remediation=False, file_path=None):
        """Extract accuracy value from summary data (first key found)."""
        result = {"value": None, "file_path": file_path}

        if not summary_data or not isinstance(summary_data, dict):
            return result

        for v in summary_data.values():
            if isinstance(v, dict):
                if (
                    use_remediation
                    and "remediation" in v
                    and "accuracy" in v["remediation"]
                ):
                    try:
                        result["value"] = float(v["remediation"]["accuracy"])
                        return result
                    except Exception:
                        return result
                elif "accuracy" in v and not use_remediation:
                    try:
                        result["value"] = float(v["accuracy"])
                        return result
                    except Exception:
                        return result
        return result

    def load_json_ids(self, path, attempt_num=None):
        """
        Load a JSON file and return a set of task_ids. Handles dict or list structure.
        If attempt_num is provided, only consider entries with that attempt number.
        """
        ids = set()
        if not os.path.isfile(path):
            return ids
        try:
            with open(path, "r") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    for v in data.values():
                        if isinstance(v, list):
                            for entry in v:
                                if isinstance(entry, dict) and "task_id" in entry:
                                    if (
                                        attempt_num is None
                                        or entry.get("attempt_num", 1) == attempt_num
                                    ):
                                        ids.add(entry["task_id"])
                elif isinstance(data, list):
                    for entry in data:
                        if isinstance(entry, dict) and "task_id" in entry:
                            if (
                                attempt_num is None
                                or entry.get("attempt_num", 1) == attempt_num
                            ):
                                ids.add(entry["task_id"])
        except Exception as e:
            print(f"Error loading JSON from {path}: {e}")
        return ids

    def comprehensive_analysis(
        self, base_results_dir, td_results_dir, use_remediation=False
    ):
        """
        Perform comprehensive analysis of test results between base and TD directories.
        If use_remediation is True, consider all attempts rather than just first attempts.
        """
        # For remediation, we consider all attempts, so don't filter
        attempt_filter = 1 if not use_remediation else None

        base_passed_path = os.path.join(base_results_dir, "runner_passed.json")
        td_passed_path = os.path.join(td_results_dir, "runner_passed.json")
        base_fails_path = os.path.join(base_results_dir, "runner_fails.json")
        base_errors_path = os.path.join(base_results_dir, "runner_errors.json")
        td_fails_path = os.path.join(td_results_dir, "runner_fails.json")
        td_errors_path = os.path.join(td_results_dir, "runner_errors.json")

        # Load the task IDs from each file
        base_passed = self.load_json_ids(base_passed_path, attempt_filter)
        td_passed = self.load_json_ids(td_passed_path, attempt_filter)
        base_fails = self.load_json_ids(base_fails_path, attempt_filter)
        base_errors = self.load_json_ids(base_errors_path, attempt_filter)
        td_fails = self.load_json_ids(td_fails_path, attempt_filter)
        td_errors = self.load_json_ids(td_errors_path, attempt_filter)

        # Get the total number of tasks passed in each condition
        base_passed_count = len(base_passed)
        td_passed_count = len(td_passed)

        # Create a result structure with file paths for validation
        result = {
            "status": None,
            "improved_tasks": [],
            "regressed_tasks": [],
            "using_remediation": use_remediation,
            "file_paths": {
                "base_passed": base_passed_path,
                "td_passed": td_passed_path,
                "base_fails": base_fails_path,
                "base_errors": base_errors_path,
                "td_fails": td_fails_path,
                "td_errors": td_errors_path,
                "base_results_dir": base_results_dir,
                "td_results_dir": td_results_dir,
            },
        }

        # A task is improved only if it passes in TD but never passes in base
        improved_tasks = sorted(td_passed - base_passed)

        # A task is regressed only if it passes in base but never passes in TD
        regressed_tasks = sorted(base_passed - td_passed)

        result["improved_tasks"] = improved_tasks
        result["regressed_tasks"] = regressed_tasks

        if td_passed_count > base_passed_count:
            result["status"] = "better"
            print(
                "\033[92mTest Driven is better, tests that passed in TD but failed/errored in Base:\033[0m"
            )
            if improved_tasks:
                for tid in improved_tasks:
                    print(f"  task_id: {tid}")
            else:
                print("  None.")
        elif td_passed_count < base_passed_count:
            result["status"] = "worse"
            print(
                "\033[91mTest Driven is worse, tests that passed in Base but failed/errored in TD\033[0m"
            )
            if regressed_tasks:
                for tid in regressed_tasks:
                    print(f"  task_id: {tid}")
            else:
                print("  None.")
        else:
            result["status"] = "same"
            print(
                "\033[93mEquivalent Results, the number of passed tests is identical.\033[0m"
            )

        return result

    def run_analysis(self, use_remediation=False):
        """
        Run detailed differences analysis between base and TD directories.
        If use_remediation is True, use remediation data (all attempts) instead of first attempt only.
        """
        # Apply directory filtering based on include/exclude lists
        if self.include_dirs is not None:
            subdirs = [
                d
                for d in self.include_dirs
                if os.path.isdir(os.path.join(self.rq_dir, d)) and not d.endswith("_td")
            ]
        else:
            excluded_dirs = {"__pycache__", "logs", "results_all"} | set(
                self.exclude_dirs
            )
            subdirs = [
                d
                for d in os.listdir(self.rq_dir)
                if os.path.isdir(os.path.join(self.rq_dir, d))
                and not d.endswith("_td")
                and d not in excluded_dirs
            ]

        if not subdirs:
            print(f"No base directories found in {self.rq_dir}")
            return None

        print(f"Found {len(subdirs)} base directories to compare")
        print(
            f"Looking for runner_passed.json, runner_fails.json, runner_errors.json in '{self.results_folder}' folders"
        )
        if use_remediation:
            print("Using remediation results (all attempts)")
        else:
            print("Using first attempt results only")

        comparison_count = 0
        detailed_results = {}

        for subdir in sorted(subdirs):
            td_dir = f"{subdir}_td"
            base_results_dir = os.path.join(self.rq_dir, subdir, self.results_folder)
            td_results_dir = os.path.join(self.rq_dir, td_dir, self.results_folder)

            if not os.path.isdir(os.path.join(self.rq_dir, td_dir)):
                print(f"Warning: No matching {td_dir} directory found for {subdir}")
                continue
            if not os.path.isdir(base_results_dir):
                print(f"Warning: No '{self.results_folder}' folder in {subdir}")
                continue
            if not os.path.isdir(td_results_dir):
                print(f"Warning: No '{self.results_folder}' folder in {td_dir}")
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
                "results_folder": self.results_folder,
                "use_remediation": use_remediation,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
            "results": detailed_results,
        }

        return result_with_metadata

    def print_comparison(
        self,
        base_name,
        td_name,
        base_counts,
        td_counts,
        diffs,
        base_results_dir=None,
        td_results_dir=None,
        base_data=None,
        td_data=None,
        use_remediation=False,
    ):
        """Print detailed comparison between base and TD test results."""
        print(f"\n{'='*50}")
        print(f"Test Results Comparison: {base_name} vs {td_name}")
        if use_remediation:
            print("Using remediation results (all attempts)")
        else:
            print("Using first attempt results only")
        print(f"{'='*50}")
        print(f"{base_name}: {base_counts}")
        print(f"{td_name}: {td_counts}")
        print("Differences (TD - Base):", diffs)

        for k in diffs:
            if k == "success":
                if diffs[k] > 0:
                    print(
                        f"  TD has more {k}: {td_counts[k]} vs {base_counts[k]} (+{diffs[k]})"
                    )
                elif diffs[k] < 0:
                    print(
                        f"  TD has fewer {k}: {td_counts[k]} vs {base_counts[k]} ({diffs[k]})"
                    )
                else:
                    print(f"  TD has same {k}: {td_counts[k]} vs {base_counts[k]}")
            else:  # fail or error
                if diffs[k] > 0:
                    print(
                        f"  TD has more {k}: {td_counts[k]} vs {base_counts[k]} (+{diffs[k]})"
                    )
                elif diffs[k] < 0:
                    print(
                        f"  TD has fewer {k}: {td_counts[k]} vs {base_counts[k]} ({diffs[k]})"
                    )
                else:
                    print(f"  TD has same {k}: {td_counts[k]} vs {base_counts[k]}")

        # Print accuracy comparison if available
        base_summary_path = (
            os.path.join(base_results_dir, "summary.json") if base_results_dir else None
        )
        td_summary_path = (
            os.path.join(td_results_dir, "summary.json") if td_results_dir else None
        )

        comparison_result = {
            "using_remediation": use_remediation,
            "base_results_dir": base_results_dir,
            "td_results_dir": td_results_dir,
            "base_summary_path": base_summary_path,
            "td_summary_path": td_summary_path,
        }

        base_acc_result = self.extract_accuracy(
            base_data, use_remediation, base_summary_path
        )
        td_acc_result = self.extract_accuracy(td_data, use_remediation, td_summary_path)

        base_acc = base_acc_result["value"]
        td_acc = td_acc_result["value"]

        if base_acc is not None and td_acc is not None:
            comparison_result["base_accuracy"] = base_acc
            comparison_result["td_accuracy"] = td_acc

            if td_acc > base_acc:
                comparison_result["accuracy_status"] = "better"
                print(
                    f"\033[92mTD has better accuracy: {td_acc:.2f} vs {base_acc:.2f}\033[0m"
                )
            elif td_acc == base_acc:
                comparison_result["accuracy_status"] = "same"
                print(
                    f"\033[93mTD has same accuracy: {td_acc:.2f} vs {base_acc:.2f}\033[0m"
                )
            else:
                comparison_result["accuracy_status"] = "worse"
                print(
                    f"\033[91mTD has worse accuracy: {td_acc:.2f} vs {base_acc:.2f}\033[0m"
                )

        analysis_result = self.comprehensive_analysis(
            base_results_dir, td_results_dir, use_remediation
        )
        comparison_result.update(analysis_result)
        comparison_result["counts"] = {
            "base": base_counts,
            "td": td_counts,
            "diff": diffs,
        }

        return comparison_result


def _create_incomplete_directories_report_section(summary_data):
    """Create markdown section for incomplete directories analysis."""
    if "incomplete_directories" not in summary_data:
        return ""

    incomplete = summary_data["incomplete_directories"]
    total_dirs = incomplete["total_directories"]
    successful = len(incomplete["successful_comparisons"])
    completion_rate = (successful / total_dirs * 100) if total_dirs > 0 else 0

    report = "## Incomplete Directories Analysis\n\n"
    report += f"**Completion Status:** {successful}/{total_dirs} directories ({completion_rate:.1f}%)\n\n"

    total_incomplete = (
        len(incomplete["missing_td_dirs"])
        + len(incomplete["missing_summary_files"])
        + len(incomplete["missing_accuracy_data"])
        + len(incomplete.get("partial_completion_dirs", []))
        + len(incomplete.get("config_mismatch_dirs", []))
    )

    if total_incomplete == 0:
        report += "🎉 **All directories are complete!** No re-execution needed.\n\n"
        return report

    report += f"**Incomplete Directories:** {total_incomplete}\n\n"

    # Missing TD Directories
    if incomplete["missing_td_dirs"]:
        report += f"### 🔴 Missing TD Directories ({len(incomplete['missing_td_dirs'])} dirs need TD experiments)\n\n"
        for subdir in incomplete["missing_td_dirs"]:
            # Get research question from summary data
            rq_dir = summary_data.get("rq_dir", "").split("/")[-1] or "rq1"
            report += f"- **{subdir}**\n"
            report += f"  ```bash\n"
            report += f"  python {rq_dir}/{subdir}_td/get_solution.py\n"
            report += f"  python {rq_dir}/{subdir}_td/test_solution.py\n"
            report += f"  ```\n\n"

    # Missing Summary Files
    if incomplete["missing_summary_files"]:
        report += f"### 🟡 Missing Summary Files ({len(incomplete['missing_summary_files'])} dirs need test execution)\n\n"
        for item in incomplete["missing_summary_files"]:
            subdir = item["subdir"]
            missing = item["missing"]
            rq_dir = summary_data.get("rq_dir", "").split("/")[-1] or "rq1"
            report += f"- **{subdir}**: Missing {', '.join(missing)}\n"
            report += f"  ```bash\n"
            if "base" in " ".join(missing):
                report += f"  python {rq_dir}/{subdir}/test_solution.py\n"
            if "td" in " ".join(missing):
                report += f"  python {rq_dir}/{subdir}_td/test_solution.py\n"
            report += f"  ```\n\n"

    # Missing Accuracy Data
    if incomplete["missing_accuracy_data"]:
        report += f"### 🟣 Missing Accuracy Data ({len(incomplete['missing_accuracy_data'])} dirs need investigation)\n\n"
        for item in incomplete["missing_accuracy_data"]:
            subdir = item["subdir"]
            missing = item["missing"]
            report += f"- **{subdir}**: Missing {', '.join(missing)} accuracy\n"
            report += f"  Check summary.json format in results directory\n\n"

    # Config Mismatch Directories
    if incomplete.get("config_mismatch_dirs"):
        config_dirs = incomplete["config_mismatch_dirs"]
        report += f"### 🔵 Config Mismatch Directories ({len(config_dirs)} dirs need config update or re-execution)\n\n"

        for mismatch in config_dirs:
            subdir = mismatch["subdir"]
            mismatch_info = mismatch.get("base_mismatch") or mismatch.get("td_mismatch")

            if mismatch_info and mismatch_info.get("available_directories"):
                available_dir = mismatch_info["available_directories"][0]
                current_config = mismatch_info["current_config"]

                # Extract config values from directory name
                import re

                match = re.search(
                    r"_(\d+\.?\d*)_ROWS_(\d+\.?\d*)_TD_PUBLIC_(\d+)_REATTEMPT",
                    available_dir,
                )
                if match:
                    found_ratio, found_td_ratio, found_reattempt = match.groups()

                    report += f"- **{subdir}**: Expected `{current_config['RATIO']}_ROWS` but found `{found_ratio}_ROWS`\n"
                    report += f"  ```bash\n"
                    report += f"  # Option 1: Update config to match existing results\n"
                    report += f"  RATIO_OF_ROWS_TO_RUN = {found_ratio}\n"
                    report += f"  \n"
                    report += f"  # Option 2: Re-run with current config\n"
                    rq_dir = summary_data.get("rq_dir", "").split("/")[-1] or "rq2"
                    report += f"  python {rq_dir}/{subdir}/get_solution.py\n"
                    report += f"  python {rq_dir}/{subdir}_td/get_solution.py\n"
                    report += f"  ```\n\n"
                else:
                    # Fallback if regex doesn't match
                    report += f"- **{subdir}**: Config mismatch detected\n"
                    report += f"  Available: {available_dir}\n"
                    report += f"  Expected pattern: {mismatch_info.get('expected_pattern', 'N/A')}\n\n"
            else:
                # Fallback if no mismatch info available
                report += f"- **{subdir}**: Config mismatch detected (details unavailable)\n\n"

    # Partial Completion Due to Generation Errors
    if incomplete.get("partial_completion_dirs"):
        partial_dirs = incomplete["partial_completion_dirs"]
        report += f"### 🟠 Partial Completion ({len(partial_dirs)} dirs have generation errors)\n\n"
        for item in partial_dirs:
            subdir = item["subdir"]
            base_errors = item.get("base_gen_errors", False)
            td_errors = item.get("td_gen_errors", False)
            error_status = []
            if base_errors:
                error_status.append("base")
            if td_errors:
                error_status.append("td")
            rq_dir = summary_data.get("rq_dir", "").split("/")[-1] or "rq1"
            report += (
                f"- **{subdir}**: Generation errors in {', '.join(error_status)}\n"
            )
            report += f"  ```bash\n"
            report += f"  python {rq_dir}/{subdir}/get_solution.py\n"
            if td_errors:
                report += f"  python {rq_dir}/{subdir}_td/get_solution.py\n"
            report += f"  ```\n\n"

    # Successful Comparisons Summary
    if incomplete["successful_comparisons"]:
        report += f"### ✅ Successful Comparisons ({len(incomplete['successful_comparisons'])} dirs)\n\n"
        success_list = incomplete["successful_comparisons"]
        if len(success_list) <= 10:
            report += f"{', '.join(success_list)}\n\n"
        else:
            report += (
                f"{', '.join(success_list[:10])}, and {len(success_list) - 10} more\n\n"
            )

    return report


def _create_metadata_section(llm_info, summary_data, differences_data):
    """Create comprehensive metadata section for the report."""
    report = "## Experiment Metadata\n\n"

    # LLM Configuration
    report += "**LLM Configuration:**\n"
    if llm_info["llm_config_keys"]:
        if len(llm_info["llm_config_keys"]) == 1:
            report += f"- Configuration Key: {llm_info['llm_config_keys'][0]}\n"
        else:
            report += (
                f"- Configuration Keys: {', '.join(llm_info['llm_config_keys'])}\n"
            )
    if llm_info["llm_name"]:
        report += f"- Model Name: {llm_info['llm_name']}\n"
    else:
        report += "- Model Name: Unknown\n"

    # Dataset Configuration
    report += "**Dataset Configuration:**\n"
    if llm_info["research_question"]:
        report += f"- Research Question: {llm_info['research_question']}\n"
    if llm_info["dataset_coverage"]:
        coverage_pct = float(llm_info["dataset_coverage"]) * 100
        report += f"- Dataset Coverage: {llm_info['dataset_coverage']} ({coverage_pct}% of problems)\n"

    # Display all datasets and their problem counts
    if llm_info["datasets_info"]:
        dataset_coverage = llm_info.get("dataset_coverage")
        coverage_ratio = float(dataset_coverage) if dataset_coverage else None

        if len(llm_info["datasets_info"]) == 1:
            # Single dataset - show inline with tested count
            dataset_name, info = next(iter(llm_info["datasets_info"].items()))
            total_problems = info["problems"]
            if coverage_ratio:
                tested_problems = int(total_problems * coverage_ratio)
                report += f"- Total Problems in Dataset: {total_problems} ({tested_problems} tested)\n"
            else:
                report += f"- Total Problems in Dataset: {total_problems}\n"
        else:
            # Multiple datasets - show detailed breakdown with tested counts
            total_problems = sum(
                info["problems"] for info in llm_info["datasets_info"].values()
            )
            report += f"- Total Problems Across All Datasets: {total_problems}\n"

            if coverage_ratio:
                total_tested = sum(
                    int(info["problems"] * coverage_ratio)
                    for info in llm_info["datasets_info"].values()
                )
                report += f"- Total Problems Tested: {total_tested}\n"

            report += "- Datasets:\n"
            for dataset_name, info in sorted(llm_info["datasets_info"].items()):
                original_name = info.get("original_name", dataset_name)
                problems_count = info["problems"]

                if coverage_ratio:
                    tested_count = int(problems_count * coverage_ratio)
                    dataset_display = (
                        f"{problems_count} problems ({tested_count} tested)"
                    )
                else:
                    dataset_display = f"{problems_count} problems"

                if original_name != dataset_name:
                    report += f"  * {original_name}: {dataset_display}\n"
                else:
                    report += f"  * {dataset_name}: {dataset_display}\n"

    if llm_info["test_driven_ratio"]:
        report += f"- Test-Driven Ratio: {llm_info['test_driven_ratio']}\n"
    if llm_info["max_reattempts"]:
        report += f"- Max Reattempts: {llm_info['max_reattempts']}\n"
    report += "\n"

    return report


def _extract_llm_info_from_data(summary_data, metadata_list=None):
    """
    Extract and aggregate LLM information from summary data and metadata.
    Returns dict with aggregated llm_names, dataset info, and other metadata.
    """
    llm_info = {
        "llm_name": None,
        "llm_config_keys": set(),  # Collect all unique LLMs
        "research_question": None,
        "dataset_coverage": None,
        "test_driven_ratio": None,
        "max_reattempts": None,
        "results_directory": None,
        "generation_timestamp": None,
        "datasets_info": {},  # Dict of {dataset_name: {problems: count, original_name: name}}
    }

    # Extract LLM name from summary data (uses the key from summary.json)
    if summary_data and isinstance(summary_data, dict):
        for llm_name in summary_data.keys():
            if isinstance(summary_data[llm_name], dict):
                llm_info["llm_name"] = llm_name
                break

    # Extract and aggregate metadata from all metadata files
    if metadata_list:
        for metadata in metadata_list:
            if metadata:
                # Collect unique LLM config keys
                llm_key = metadata.get("llm_to_use")
                if llm_key:
                    llm_info["llm_config_keys"].add(llm_key)

                # Use first valid values for common fields
                if not llm_info["research_question"]:
                    llm_info["research_question"] = metadata.get("research_question")
                if not llm_info["dataset_coverage"]:
                    llm_info["dataset_coverage"] = metadata.get("ratio_of_rows")
                if not llm_info["generation_timestamp"]:
                    llm_info["generation_timestamp"] = metadata.get("timestamp")

                # Collect dataset information
                dataset_name = metadata.get("dataset_name")
                original_dataset_name = metadata.get("original_dataset_name")
                dataset_rows = metadata.get("dataset_rows")

                if dataset_name and dataset_rows:
                    # Use original dataset name as the key to avoid duplicates
                    # For example: human_eval_chatgpt4o -> human_eval
                    key = original_dataset_name or dataset_name
                    if key not in llm_info["datasets_info"]:
                        llm_info["datasets_info"][key] = {
                            "problems": dataset_rows,
                            "original_name": original_dataset_name or dataset_name,
                        }

    # Convert set to sorted list for consistent output
    llm_info["llm_config_keys"] = sorted(list(llm_info["llm_config_keys"]))

    return llm_info


def save_results_to_file(dir_path, filename, content, format="md"):
    """Save results to a file in the specified directory."""
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, f"{filename}.{format}")

    with open(file_path, "w") as f:
        f.write(content)

    print(f"Results saved to {file_path}")


def create_combined_report(
    summary_first_attempt,
    summary_remediation,
    differences_first_attempt,
    differences_remediation,
    metadata_list=None,
):
    """Create a combined report with summary and differences results."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Extract LLM information from the first available summary data
    summary_data_for_llm = summary_first_attempt.get("details", {})
    if summary_data_for_llm:
        # Get the first experiment's summary data for LLM extraction
        first_experiment = list(summary_data_for_llm.values())[0]
        first_summary_path = first_experiment.get("base_summary_path", "")
        if first_summary_path and os.path.exists(first_summary_path):
            try:
                with open(first_summary_path, "r") as f:
                    sample_summary = json.load(f)
            except:
                sample_summary = {}
        else:
            sample_summary = {}
    else:
        sample_summary = {}

    llm_info = _extract_llm_info_from_data(sample_summary, metadata_list)

    # Create the combined report content
    report = f"# Combined Analysis Report\n\n"
    report += f"Generated: {timestamp}\n\n"

    # Add lean experiment configuration
    if (
        llm_info["llm_name"]
        or llm_info["llm_config_keys"]
        or llm_info["research_question"]
    ):
        # Determine LLM display based on single vs multiple LLMs
        if llm_info["llm_config_keys"] and len(llm_info["llm_config_keys"]) > 1:
            llm_count = len(llm_info["llm_config_keys"])
            llm_display = f"Multiple ({llm_count} models)"
            llm_label = "LLMs"
        else:
            llm_display = llm_info["llm_name"] or "Unknown"
            llm_label = "LLM"

        rq_display = llm_info["research_question"] or "Unknown"
        report += (
            f"**{llm_label}:** {llm_display} | **Research Question:** {rq_display}\n\n"
        )

    # Add summary section for first attempt
    report += "## Summary (First Attempt Only)\n\n"
    total = summary_first_attempt["total_comparisons"]
    if total > 0:
        report += f"Total comparisons: {total}\n\n"
        report += f"* Test-driven (TD) results were better in {summary_first_attempt['td_better']} out of {total} comparisons ({(summary_first_attempt['td_better']/total)*100:.1f}%)\n"
        report += f"* Test-driven (TD) results were same in {summary_first_attempt['td_same']} out of {total} comparisons ({(summary_first_attempt['td_same']/total)*100:.1f}%)\n"
        report += f"* Test-driven (TD) results were worse in {summary_first_attempt['td_worse']} out of {total} comparisons ({(summary_first_attempt['td_worse']/total)*100:.1f}%)\n\n"

        # Add accuracy statistics section if available
        if "accuracy_statistics" in summary_first_attempt:
            stats = summary_first_attempt["accuracy_statistics"]
            report += "### Accuracy Statistics\n\n"
            report += f"* Total increase: {stats['total_increase']:.2f}\n"
            report += f"* Average increase: {stats['avg_increase']:.2f} (95% CI: [{stats['confidence_interval'][0]:.2f}, {stats['confidence_interval'][1]:.2f}])\n"
            report += f"* Median increase: {stats['median_increase']:.2f}\n"
            report += f"* Standard deviation: {stats['std_dev']:.2f}\n"
            report += (
                f"* Range: {stats['min_increase']:.2f} to {stats['max_increase']:.2f}\n"
            )
            report += f"* Interquartile range: {stats['percentile_25']:.2f} to {stats['percentile_75']:.2f}\n"
            report += f"* Benchmarks improved: {stats['improved_count']} ({(stats['improved_count']/total)*100:.1f}%)\n"
            report += f"* Benchmarks worsened: {stats['worsened_count']} ({(stats['worsened_count']/total)*100:.1f}%)\n"
            report += f"* Benchmarks unchanged: {stats['same_count']} ({(stats['same_count']/total)*100:.1f}%)\n"

            if stats["improved_count"] > 0:
                report += f"* Average improvement percentage: {stats['avg_improvement_pct']:.2f}%\n"
            if stats["worsened_count"] > 0:
                report += f"* Average regression percentage: {stats['avg_regression_pct']:.2f}%\n"

            # Add statistical test results
            if (
                stats.get("normality_test_stat") is not None
                or stats.get("significance_test_stat") is not None
            ):
                report += "\n#### Statistical Tests\n\n"

                # Normality test
                if stats.get("normality_test_stat") is not None:
                    normality_stat = stats["normality_test_stat"]
                    normality_p = stats["normality_p_value"]
                    is_normal = "Yes" if stats.get("is_normal", False) else "No"
                    report += f"* **Normality Test (Shapiro-Wilk)**: statistic={normality_stat:.4f}, p-value={normality_p:.4f}, Normal={is_normal}\n"

                # Significance test
                if stats.get("significance_test_stat") is not None:
                    test_stat = stats["significance_test_stat"]
                    test_p = stats["significance_p_value"]
                    test_type = stats.get("significance_test_type", "unknown")

                    if test_type == "paired_t_test":
                        test_name = "Paired t-test"
                    elif test_type == "wilcoxon_signed_rank":
                        test_name = "Wilcoxon signed-rank test"
                    else:
                        test_name = f"{test_type.replace('_', ' ').title()} test"

                    report += f"* **{test_name}**: statistic={test_stat:.4f}, p-value={test_p:.4f}\n"

                # Effect size
                if stats.get("cohens_d") is not None:
                    cohens_d = stats["cohens_d"]
                    effect_interpretation = stats.get(
                        "effect_size_interpretation", "unknown"
                    )
                    report += f"* **Effect Size (Cohen's d)**: {cohens_d:.4f} ({effect_interpretation} effect)\n"

                # Interpretation
                if stats.get("significance_p_value") is not None:
                    p_val = stats["significance_p_value"]
                    if p_val < 0.001:
                        significance = "highly significant (p < 0.001)"
                    elif p_val < 0.01:
                        significance = "very significant (p < 0.01)"
                    elif p_val < 0.05:
                        significance = "significant (p < 0.05)"
                    else:
                        significance = "not significant (p ≥ 0.05)"
                    report += f"* **Interpretation**: Results are {significance}\n"

                report += "\n"
            else:
                report += "\n"

            # Add top increases
            if stats["sorted_increases_desc"]:
                report += "#### Top 5 Increases\n\n"
                for item in stats["sorted_increases_desc"][:5]:
                    report += f"* {item['benchmark']}: {item['base_accuracy']:.2f} → {item['td_accuracy']:.2f} (change: {item['increase']:+.2f})\n"
                report += "\n"

            # Add top regressions
            if stats["sorted_regressions_asc"]:
                report += "#### Top 5 Regressions\n\n"
                for item in stats["sorted_regressions_asc"][:5]:
                    report += f"* {item['benchmark']}: {item['base_accuracy']:.2f} → {item['td_accuracy']:.2f} (change: {item['increase']:+.2f})\n"
                report += "\n"
    else:
        report += "No comparisons were made for first attempts.\n\n"

    # Add summary section for remediation
    report += "## Summary (With Remediation)\n\n"
    total_remediation = summary_remediation["total_comparisons"]
    if total_remediation > 0:
        report += f"Total comparisons: {total_remediation}\n\n"
        report += f"* Test-driven (TD) results were better in {summary_remediation['td_better']} out of {total_remediation} comparisons ({(summary_remediation['td_better']/total_remediation)*100:.1f}%)\n"
        report += f"* Test-driven (TD) results were same in {summary_remediation['td_same']} out of {total_remediation} comparisons ({(summary_remediation['td_same']/total_remediation)*100:.1f}%)\n"
        report += f"* Test-driven (TD) results were worse in {summary_remediation['td_worse']} out of {total_remediation} comparisons ({(summary_remediation['td_worse']/total_remediation)*100:.1f}%)\n\n"

        # Add accuracy statistics section if available
        if "accuracy_statistics" in summary_remediation:
            stats = summary_remediation["accuracy_statistics"]
            report += "### Accuracy Statistics (With Remediation)\n\n"
            report += f"* Total increase: {stats['total_increase']:.2f}\n"
            report += f"* Average increase: {stats['avg_increase']:.2f} (95% CI: [{stats['confidence_interval'][0]:.2f}, {stats['confidence_interval'][1]:.2f}])\n"
            report += f"* Median increase: {stats['median_increase']:.2f}\n"
            report += f"* Standard deviation: {stats['std_dev']:.2f}\n"
            report += (
                f"* Range: {stats['min_increase']:.2f} to {stats['max_increase']:.2f}\n"
            )
            report += f"* Interquartile range: {stats['percentile_25']:.2f} to {stats['percentile_75']:.2f}\n"
            report += f"* Benchmarks improved: {stats['improved_count']} ({(stats['improved_count']/total_remediation)*100:.1f}%)\n"
            report += f"* Benchmarks worsened: {stats['worsened_count']} ({(stats['worsened_count']/total_remediation)*100:.1f}%)\n"
            report += f"* Benchmarks unchanged: {stats['same_count']} ({(stats['same_count']/total_remediation)*100:.1f}%)\n"

            if stats["improved_count"] > 0:
                report += f"* Average improvement percentage: {stats['avg_improvement_pct']:.2f}%\n"
            if stats["worsened_count"] > 0:
                report += f"* Average regression percentage: {stats['avg_regression_pct']:.2f}%\n"

            # Add statistical test results
            if (
                stats.get("normality_test_stat") is not None
                or stats.get("significance_test_stat") is not None
            ):
                report += "\n#### Statistical Tests\n\n"

                # Normality test
                if stats.get("normality_test_stat") is not None:
                    normality_stat = stats["normality_test_stat"]
                    normality_p = stats["normality_p_value"]
                    is_normal = "Yes" if stats.get("is_normal", False) else "No"
                    report += f"* **Normality Test (Shapiro-Wilk)**: statistic={normality_stat:.4f}, p-value={normality_p:.4f}, Normal={is_normal}\n"

                # Significance test
                if stats.get("significance_test_stat") is not None:
                    test_stat = stats["significance_test_stat"]
                    test_p = stats["significance_p_value"]
                    test_type = stats.get("significance_test_type", "unknown")

                    if test_type == "paired_t_test":
                        test_name = "Paired t-test"
                    elif test_type == "wilcoxon_signed_rank":
                        test_name = "Wilcoxon signed-rank test"
                    else:
                        test_name = f"{test_type.replace('_', ' ').title()} test"

                    report += f"* **{test_name}**: statistic={test_stat:.4f}, p-value={test_p:.4f}\n"

                # Effect size
                if stats.get("cohens_d") is not None:
                    cohens_d = stats["cohens_d"]
                    effect_interpretation = stats.get(
                        "effect_size_interpretation", "unknown"
                    )
                    report += f"* **Effect Size (Cohen's d)**: {cohens_d:.4f} ({effect_interpretation} effect)\n"

                # Interpretation
                if stats.get("significance_p_value") is not None:
                    p_val = stats["significance_p_value"]
                    if p_val < 0.001:
                        significance = "highly significant (p < 0.001)"
                    elif p_val < 0.01:
                        significance = "very significant (p < 0.01)"
                    elif p_val < 0.05:
                        significance = "significant (p < 0.05)"
                    else:
                        significance = "not significant (p ≥ 0.05)"
                    report += f"* **Interpretation**: Results are {significance}\n"

                report += "\n"
            else:
                report += "\n"

            # Add top increases
            if stats["sorted_increases_desc"]:
                report += "#### Top 5 Increases (With Remediation)\n\n"
                for item in stats["sorted_increases_desc"][:5]:
                    report += f"* {item['benchmark']}: {item['base_accuracy']:.2f} → {item['td_accuracy']:.2f} (change: {item['increase']:+.2f})\n"
                report += "\n"

            # Add top regressions
            if stats["sorted_regressions_asc"]:
                report += "#### Top 5 Regressions (With Remediation)\n\n"
                for item in stats["sorted_regressions_asc"][:5]:
                    report += f"* {item['benchmark']}: {item['base_accuracy']:.2f} → {item['td_accuracy']:.2f} (change: {item['increase']:+.2f})\n"
                report += "\n"
    else:
        report += "No comparisons were made with remediation.\n\n"

    # Add detailed comparison section for first attempt
    report += "## Detailed Comparisons (First Attempt Only)\n\n"
    detailed_results = differences_first_attempt.get("results", {})
    for dir_name, details in detailed_results.items():
        report += f"### {dir_name} vs {dir_name}_td\n\n"

        if "base_accuracy" in details and "td_accuracy" in details:
            base_acc = details["base_accuracy"]
            td_acc = details["td_accuracy"]
            status = details["accuracy_status"]

            report += f"Accuracy comparison: "
            if status == "better":
                report += f"**TD is better** - {td_acc:.2f} vs {base_acc:.2f}\n\n"
            elif status == "same":
                report += f"**TD is same** - {td_acc:.2f} vs {base_acc:.2f}\n\n"
            else:
                report += f"**TD is worse** - {td_acc:.2f} vs {base_acc:.2f}\n\n"

        if "counts" in details:
            counts = details["counts"]
            report += f"Test counts:\n"
            report += f"* Base: {counts['base']}\n"
            report += f"* TD: {counts['td']}\n"
            report += f"* Difference: {counts['diff']}\n\n"

        # Add improved/regressed tasks
        if "improved_tasks" in details and details["improved_tasks"]:
            report += "**Improvements** - Tests that passed in TD but failed/errored in Base:\n"
            for task in details["improved_tasks"]:
                report += f"* task_id: {task}\n"
            report += "\n"

        if "regressed_tasks" in details and details["regressed_tasks"]:
            report += "**Regressions** - Tests that passed in Base but failed/errored in TD:\n"
            for task in details["regressed_tasks"]:
                report += f"* task_id: {task}\n"
            report += "\n"

        report += "---\n\n"

    # Add detailed comparison section for remediation
    report += "## Detailed Comparisons (With Remediation)\n\n"
    detailed_remediation = differences_remediation.get("results", {})
    for dir_name, details in detailed_remediation.items():
        report += f"### {dir_name} vs {dir_name}_td\n\n"

        if "base_accuracy" in details and "td_accuracy" in details:
            base_acc = details["base_accuracy"]
            td_acc = details["td_accuracy"]
            status = details["accuracy_status"]

            report += f"Accuracy comparison (with remediation): "
            if status == "better":
                report += f"**TD is better** - {td_acc:.2f} vs {base_acc:.2f}\n\n"
            elif status == "same":
                report += f"**TD is same** - {td_acc:.2f} vs {base_acc:.2f}\n\n"
            else:
                report += f"**TD is worse** - {td_acc:.2f} vs {base_acc:.2f}\n\n"

        if "counts" in details:
            counts = details["counts"]
            report += f"Test counts (with remediation):\n"
            report += f"* Base: {counts['base']}\n"
            report += f"* TD: {counts['td']}\n"
            report += f"* Difference: {counts['diff']}\n\n"

        # Add improved/regressed tasks
        if "improved_tasks" in details and details["improved_tasks"]:
            report += "**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:\n"
            for task in details["improved_tasks"]:
                report += f"* task_id: {task}\n"
            report += "\n"

        if "regressed_tasks" in details and details["regressed_tasks"]:
            report += "**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:\n"
            for task in details["regressed_tasks"]:
                report += f"* task_id: {task}\n"
            report += "\n"

        report += "---\n\n"

    # Add incomplete directories section
    report += _create_incomplete_directories_report_section(summary_first_attempt)

    # Add comprehensive metadata section
    report += _create_metadata_section(
        llm_info, summary_first_attempt, differences_first_attempt
    )

    return report
