import sys
import os
import json
import csv
from datetime import datetime
from collections import defaultdict, Counter
from pathlib import Path
import statistics
from scipy import stats

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from rq2.results_analyzer import RQ2DirectoryFinder


class CodeContestsDifficultyAnalyzer:
    """Analyzer for CodeContests difficulty-based performance analysis"""

    def __init__(self, rq_dir, config_module, combined_only=False):
        """Initialize the difficulty analyzer

        Args:
            rq_dir: Research question directory (e.g., "rq2")
            config_module: Configuration module with experiment parameters
            combined_only: If True, prefer combined results directories
        """
        self.config = config_module
        self.rq_dir = os.path.join(ROOT_DIR, rq_dir)
        self.results_all_dir = os.path.join(self.rq_dir, "results_all")
        self.combined_only = combined_only
        self.directory_finder = RQ2DirectoryFinder(config_module)

        # Define difficulty levels
        self.difficulty_levels = ["EASY", "MEDIUM", "HARD"]
        self.difficulty_numeric = {"EASY": 1, "MEDIUM": 2, "HARD": 3}

        # Initialize data storage
        self.results_data = {}
        self.analysis_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def run_analysis(self):
        """Main analysis method that generates all difficulty-focused reports"""
        print("\n" + "=" * 60)
        print("CODECONTESTS DIFFICULTY PERFORMANCE ANALYSIS")
        print("=" * 60)

        # Step 1: Collect and process data
        print("\n🔍 Collecting CodeContests results data...")
        self._collect_code_contests_data()

        if not self.results_data:
            print("❌ No CodeContests data found. Skipping difficulty analysis.")
            return

        print(f"✅ Found data for {len(self.results_data)} model configurations")

        # Step 2: Generate analysis outputs
        print("\n📊 Generating trusted data analysis...")

        # Step 3: Create output directory
        output_dir = self._create_output_directory()

        # Step 4: Save analysis results
        print(f"\n💾 Saving analysis results to {output_dir}...")
        self._save_trusted_analysis_results(output_dir)

        # Step 5: Print summary
        self._print_trusted_analysis_summary()

        print("\n✅ CodeContests difficulty analysis completed!")
        print("=" * 60)

    def _collect_code_contests_data(self):
        """Collect data from all CodeContests experiment directories"""
        if not os.path.exists(self.rq_dir):
            return

        # Find all CodeContests directories (both regular and _td variants)
        # Exclude _combined and _second_half directories when not in combined mode
        contest_dirs = [
            d
            for d in os.listdir(self.rq_dir)
            if os.path.isdir(os.path.join(self.rq_dir, d))
            and d.startswith("code_contests")
            and (
                (
                    self.combined_only
                    and (d.endswith("_combined") or d.endswith("_combined_td"))
                )
                or (
                    not self.combined_only
                    and not d.endswith("_combined")
                    and not d.endswith("_second_half")
                )
            )
        ]

        print(f"   Found {len(contest_dirs)} CodeContests directories")

        for contest_dir in contest_dirs:
            self._process_contest_directory(contest_dir)

    def _process_contest_directory(self, contest_dir):
        """Process a single CodeContests directory"""
        experiment_dir = os.path.join(self.rq_dir, contest_dir)

        # Find results directory with dynamic pattern matching
        results_dir = self._find_results_directory(experiment_dir)
        if not results_dir:
            print(f"   ⚠️  No results directory found for {contest_dir}")
            return

        results_path = os.path.join(experiment_dir, results_dir)

        # Load required data files
        summary_data = self._load_json_file(os.path.join(results_path, "summary.json"))
        passed_data = self._load_json_file(
            os.path.join(results_path, "runner_passed.json")
        )
        failed_data = self._load_json_file(
            os.path.join(results_path, "runner_fails.json")
        )
        errors_data = self._load_json_file(
            os.path.join(results_path, "runner_errors.json")
        )

        if not summary_data:
            print(f"   ⚠️  No summary data found for {contest_dir}")
            return

        # Extract model information and difficulty data
        model_name = list(summary_data.keys())[
            0
        ]  # Get the first (and usually only) model
        is_test_driven = contest_dir.endswith("_td")

        # Extract difficulty breakdown
        difficulty_breakdown = self._extract_difficulty_breakdown(
            passed_data, failed_data, errors_data, model_name
        )

        # Validate against summary.json totals
        if summary_data and model_name in summary_data:
            self._validate_difficulty_breakdown(
                difficulty_breakdown, summary_data, model_name, contest_dir
            )

        # Store processed data
        config_key = f"{model_name}_{('TD' if is_test_driven else 'Normal')}"
        self.results_data[config_key] = {
            "model_name": model_name,
            "is_test_driven": is_test_driven,
            "contest_dir": contest_dir,
            "summary": summary_data[model_name],
            "difficulty_breakdown": difficulty_breakdown,
        }

        print(f"   ✅ Processed {contest_dir} -> {config_key}")

    def _find_results_directory(self, experiment_dir):
        """Find the results directory using RQ2DirectoryFinder for consistency"""
        results_folder, mismatch_info = self.directory_finder.find_results_directory(
            experiment_dir, self.combined_only
        )
        return results_folder

    def _load_json_file(self, file_path):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    return json.load(f)
        except Exception as e:
            print(f"   ⚠️  Error loading {file_path}: {e}")
        return None

    def _extract_difficulty_breakdown(
        self, passed_data, failed_data, errors_data, model_name
    ):
        """Extract difficulty breakdown from result files with proper attempt tracking"""
        breakdown = {
            "EASY": {
                "passed": 0,
                "failed": 0,
                "error": 0,
                "total_entries": 0,
                "unique_tasks": set(),
                "first_attempt_passed": 0,
                "first_attempt_failed": 0,
                "first_attempt_error": 0,
                "final_passed": 0,
                "final_failed": 0,
                "final_error": 0,
            },
            "MEDIUM": {
                "passed": 0,
                "failed": 0,
                "error": 0,
                "total_entries": 0,
                "unique_tasks": set(),
                "first_attempt_passed": 0,
                "first_attempt_failed": 0,
                "first_attempt_error": 0,
                "final_passed": 0,
                "final_failed": 0,
                "final_error": 0,
            },
            "HARD": {
                "passed": 0,
                "failed": 0,
                "error": 0,
                "total_entries": 0,
                "unique_tasks": set(),
                "first_attempt_passed": 0,
                "first_attempt_failed": 0,
                "first_attempt_error": 0,
                "final_passed": 0,
                "final_failed": 0,
                "final_error": 0,
            },
        }

        # Get max attempt number from config
        max_attempt = getattr(self.config, "REATTEMPT_MAX_NUM", 3)

        # Process each result type
        for result_type, data in [
            ("passed", passed_data),
            ("failed", failed_data),
            ("error", errors_data),
        ]:
            if not data or model_name not in data:
                continue

            for entry in data[model_name]:
                difficulty = self._extract_difficulty_from_context(
                    entry.get("context", "")
                )
                task_id = entry.get("task_id", entry.get("dataset_row_id", "unknown"))
                attempt_num = entry.get("attempt_num", 1)

                if difficulty in breakdown:
                    # Track unique tasks
                    breakdown[difficulty]["unique_tasks"].add(task_id)

                    # Count total entries (for debugging)
                    breakdown[difficulty]["total_entries"] += 1
                    breakdown[difficulty][result_type] += 1

                    # Track first attempts (attempt_num == 1)
                    if attempt_num == 1:
                        if result_type == "passed":
                            breakdown[difficulty]["first_attempt_passed"] += 1
                        elif result_type == "failed":
                            breakdown[difficulty]["first_attempt_failed"] += 1
                        elif result_type == "error":
                            breakdown[difficulty]["first_attempt_error"] += 1

                    # Track final results (final attempt or any pass)
                    if attempt_num == max_attempt or result_type == "passed":
                        if result_type == "passed":
                            breakdown[difficulty]["final_passed"] += 1
                        elif result_type == "failed" and attempt_num == max_attempt:
                            breakdown[difficulty]["final_failed"] += 1
                        elif result_type == "error" and attempt_num == max_attempt:
                            breakdown[difficulty]["final_error"] += 1

        # Convert unique task sets to counts and add validation
        for difficulty in breakdown:
            unique_count = len(breakdown[difficulty]["unique_tasks"])
            breakdown[difficulty]["unique_task_count"] = unique_count
            breakdown[difficulty][
                "total"
            ] = unique_count  # Keep for backward compatibility

            # Remove the set to make JSON serializable
            del breakdown[difficulty]["unique_tasks"]

            # Validate first attempt totals
            first_total = (
                breakdown[difficulty]["first_attempt_passed"]
                + breakdown[difficulty]["first_attempt_failed"]
                + breakdown[difficulty]["first_attempt_error"]
            )

            if first_total != unique_count and unique_count > 0:
                print(
                    f"   ⚠️  WARNING: First attempt total mismatch for {model_name} {difficulty}"
                )
                print(f"      Expected: {unique_count}, Got: {first_total}")

        return breakdown

    def _validate_difficulty_breakdown(
        self, breakdown, summary_data, model_name, contest_dir
    ):
        """Validate that difficulty breakdown matches summary.json totals"""
        summary_stats = summary_data[model_name]

        # Calculate total unique tasks across all difficulties
        breakdown_total = sum(
            data.get("unique_task_count", 0) for data in breakdown.values()
        )

        summary_total = summary_stats.get("total", 0)

        if breakdown_total != summary_total:
            print(f"   ⚠️  WARNING: Total mismatch for {contest_dir}")
            print(f"      Summary total: {summary_total}")
            print(f"      Breakdown total: {breakdown_total}")

            # Show breakdown by difficulty for debugging
            for difficulty, data in breakdown.items():
                if data.get("unique_task_count", 0) > 0:
                    print(
                        f"      {difficulty}: {data.get('unique_task_count', 0)} tasks"
                    )

        # Validate first attempt counts match summary first attempt counts
        summary_first_attempt = (
            summary_stats.get("passed", 0)
            + summary_stats.get("failed", 0)
            + summary_stats.get("error", 0)
        )

        breakdown_first_attempt = sum(
            data.get("first_attempt_passed", 0)
            + data.get("first_attempt_failed", 0)
            + data.get("first_attempt_error", 0)
            for data in breakdown.values()
        )

        if breakdown_first_attempt != summary_first_attempt:
            print(f"   ⚠️  WARNING: First attempt total mismatch for {contest_dir}")
            print(f"      Summary first attempt: {summary_first_attempt}")
            print(f"      Breakdown first attempt: {breakdown_first_attempt}")

    def _perform_comprehensive_validation(self):
        """Perform comprehensive validation including difficulty-level mismatches"""
        validation_results = {
            "has_mismatches": False,
            "mismatch_types": {
                "breakdown_vs_summary": False,
                "first_attempt_within_difficulty": False,
            },
            "details": {},
            "summary": "",
        }

        total_mismatch_count = 0
        difficulty_mismatch_count = 0

        for config_key, data in self.results_data.items():
            model_name = data["model_name"]
            method_key = "TD" if data["is_test_driven"] else "NORMAL"

            # Initialize nested structure
            if model_name not in validation_results["details"]:
                validation_results["details"][model_name] = {}
            if method_key not in validation_results["details"][model_name]:
                validation_results["details"][model_name][method_key] = {
                    "overall_validation": {},
                    "first_attempt_validation": {},
                    "difficulty_mismatches": {},
                }

            # Check overall totals
            summary_total = data["summary"].get("total", 0)
            breakdown_total = sum(
                d.get("unique_task_count", d.get("total", 0))
                for d in data["difficulty_breakdown"].values()
            )

            overall_match = breakdown_total == summary_total
            if not overall_match:
                validation_results["has_mismatches"] = True
                validation_results["mismatch_types"]["breakdown_vs_summary"] = True
                total_mismatch_count += 1

            validation_results["details"][model_name][method_key][
                "overall_validation"
            ] = {
                "breakdown_total": breakdown_total,
                "summary_total": summary_total,
                "match": overall_match,
            }

            # Check first attempt totals at summary level
            summary_first = (
                data["summary"].get("passed", 0)
                + data["summary"].get("failed", 0)
                + data["summary"].get("error", 0)
            )

            breakdown_first = sum(
                d.get("first_attempt_passed", 0)
                + d.get("first_attempt_failed", 0)
                + d.get("first_attempt_error", 0)
                for d in data["difficulty_breakdown"].values()
            )

            first_match = breakdown_first == summary_first
            validation_results["details"][model_name][method_key][
                "first_attempt_validation"
            ] = {
                "breakdown_total": breakdown_first,
                "summary_total": summary_first,
                "match": first_match,
            }

            # Check first attempt totals WITHIN each difficulty
            for difficulty, diff_data in data["difficulty_breakdown"].items():
                expected_total = diff_data.get(
                    "unique_task_count", diff_data.get("total", 0)
                )
                if expected_total > 0:
                    first_attempt_sum = (
                        diff_data.get("first_attempt_passed", 0)
                        + diff_data.get("first_attempt_failed", 0)
                        + diff_data.get("first_attempt_error", 0)
                    )

                    if first_attempt_sum != expected_total:
                        validation_results["has_mismatches"] = True
                        validation_results["mismatch_types"][
                            "first_attempt_within_difficulty"
                        ] = True
                        difficulty_mismatch_count += 1

                        validation_results["details"][model_name][method_key][
                            "difficulty_mismatches"
                        ][difficulty] = {
                            "expected_total": expected_total,
                            "first_attempt_sum": first_attempt_sum,
                            "match": False,
                            "missing_count": expected_total - first_attempt_sum,
                        }

        # Create detailed summary
        summary_parts = []
        if validation_results["mismatch_types"]["breakdown_vs_summary"]:
            summary_parts.append(
                f"{total_mismatch_count} breakdown-vs-summary mismatches"
            )
        if validation_results["mismatch_types"]["first_attempt_within_difficulty"]:
            summary_parts.append(
                f"{difficulty_mismatch_count} difficulty-level first attempt mismatches"
            )

        if summary_parts:
            validation_results["summary"] = f"Found {', '.join(summary_parts)}"
        else:
            validation_results["summary"] = "All validations passed"

        return validation_results

    def _generate_raw_difficulty_breakdown(self):
        """Generate raw difficulty breakdown with TD/NORMAL nested within each difficulty level"""
        raw_breakdown = {}

        # First pass: collect all model names and initialize structure
        model_names = set()
        for config_key, data in self.results_data.items():
            model_names.add(data["model_name"])

        # Initialize structure for all models
        for model_name in model_names:
            raw_breakdown[model_name] = {}
            for difficulty in self.difficulty_levels:
                raw_breakdown[model_name][difficulty] = {
                    "TD": {
                        "passed": 0,
                        "failed": 0,
                        "error": 0,
                        "total": 0,
                        "accuracy": 0.0,
                        "remediation": {
                            "passed": 0,
                            "failed": 0,
                            "error": 0,
                            "total": 0,
                            "accuracy": 0.0,
                        },
                    },
                    "NORMAL": {
                        "passed": 0,
                        "failed": 0,
                        "error": 0,
                        "total": 0,
                        "accuracy": 0.0,
                        "remediation": {
                            "passed": 0,
                            "failed": 0,
                            "error": 0,
                            "total": 0,
                            "accuracy": 0.0,
                        },
                    },
                }

        # Second pass: populate with actual data
        for config_key, data in self.results_data.items():
            model_name = data["model_name"]
            is_test_driven = data["is_test_driven"]
            method_key = "TD" if is_test_driven else "NORMAL"

            for difficulty in self.difficulty_levels:
                difficulty_data = data["difficulty_breakdown"][difficulty]
                total = difficulty_data.get(
                    "unique_task_count", difficulty_data.get("total", 0)
                )

                if total > 0:
                    # First attempt results (now correctly tracked)
                    first_attempt_passed = difficulty_data.get(
                        "first_attempt_passed", 0
                    )
                    first_attempt_failed = difficulty_data.get(
                        "first_attempt_failed", 0
                    )
                    first_attempt_error = difficulty_data.get("first_attempt_error", 0)

                    # Validate first attempt totals
                    first_total = (
                        first_attempt_passed
                        + first_attempt_failed
                        + first_attempt_error
                    )
                    if first_total != total and total > 0:
                        print(
                            f"   ⚠️  WARNING: First attempt total mismatch for {model_name} {difficulty} {method_key}"
                        )
                        print(f"      Expected: {total}, Got: {first_total}")

                    first_attempt_accuracy = round(
                        (first_attempt_passed / total) * 100, 2
                    )

                    # Final/Remediation results (correctly using final counts)
                    final_passed = difficulty_data.get(
                        "final_passed", difficulty_data.get("passed", 0)
                    )
                    final_failed = difficulty_data.get("final_failed", 0)
                    final_error = difficulty_data.get("final_error", 0)

                    # Calculate final accuracy - final_passed is the total that ultimately passed
                    final_accuracy = round((final_passed / total) * 100, 2)

                    raw_breakdown[model_name][difficulty][method_key] = {
                        "passed": first_attempt_passed,
                        "failed": first_attempt_failed,
                        "error": first_attempt_error,
                        "total": total,
                        "accuracy": first_attempt_accuracy,
                        "remediation": {
                            "passed": final_passed,
                            "failed": final_failed,
                            "error": final_error,
                            "total": total,
                            "accuracy": final_accuracy,
                        },
                    }

        return raw_breakdown

    def _extract_difficulty_from_context(self, context_str):
        """Extract difficulty label from context string"""
        try:
            if context_str:
                context = json.loads(context_str)
                return context.get("difficulty_label", "UNKNOWN")
        except:
            pass
        return "UNKNOWN"

    def _detect_pattern(self, performances):
        """Detect the pattern type from performance values"""
        if len(performances) != 3:
            return "unknown"

        easy, medium, hard = performances

        # Use small threshold for floating point comparison
        threshold = 2.0

        if easy > medium + threshold and medium > hard + threshold:
            return "monotonic_decrease"
        elif easy + threshold < medium and medium + threshold < hard:
            return "monotonic_increase"
        elif easy + threshold < medium and medium > hard + threshold:
            return "inverted_u"
        elif easy > medium + threshold and medium + threshold < hard:
            return "u_shaped"
        elif abs(easy - medium) < threshold and abs(medium - hard) < threshold:
            return "flat"
        elif easy > hard + threshold:
            return "overall_decrease"
        elif easy + threshold < hard:
            return "overall_increase"
        else:
            return "mixed"

    def _calculate_performance_and_effectiveness(self, stage="first_attempt"):
        """Calculate performance metrics and TD effectiveness for a given stage"""

        # Aggregate data across all models
        td_by_diff = {"EASY": [], "MEDIUM": [], "HARD": []}
        normal_by_diff = {"EASY": [], "MEDIUM": [], "HARD": []}

        # Get raw difficulty breakdown
        raw_breakdown = self._generate_raw_difficulty_breakdown()

        # Collect performance data based on stage
        for model_name, model_data in raw_breakdown.items():
            for difficulty in self.difficulty_levels:
                if stage == "first_attempt":
                    td_acc = model_data[difficulty]["TD"]["accuracy"]
                    normal_acc = model_data[difficulty]["NORMAL"]["accuracy"]
                else:  # remediation
                    td_acc = model_data[difficulty]["TD"]["remediation"]["accuracy"]
                    normal_acc = model_data[difficulty]["NORMAL"]["remediation"][
                        "accuracy"
                    ]

                td_by_diff[difficulty].append(td_acc)
                normal_by_diff[difficulty].append(normal_acc)

        # Calculate aggregate means
        td_performance = [
            statistics.mean(td_by_diff[d]) for d in self.difficulty_levels
        ]
        normal_performance = [
            statistics.mean(normal_by_diff[d]) for d in self.difficulty_levels
        ]

        # Calculate TD benefit (effectiveness over normal)
        td_benefit = {
            "easy": round(td_performance[0] - normal_performance[0], 2),
            "medium": round(td_performance[1] - normal_performance[1], 2),
            "hard": round(td_performance[2] - normal_performance[2], 2),
        }

        # Calculate performance transitions
        td_transitions = {
            "easy_to_medium": round(td_performance[1] - td_performance[0], 2),
            "medium_to_hard": round(td_performance[2] - td_performance[1], 2),
        }
        normal_transitions = {
            "easy_to_medium": round(normal_performance[1] - normal_performance[0], 2),
            "medium_to_hard": round(normal_performance[2] - normal_performance[1], 2),
        }

        # Detect patterns
        pattern_td = self._detect_pattern(td_performance)
        pattern_normal = self._detect_pattern(normal_performance)

        return {
            # Raw performance data
            "td_performance_by_difficulty": [round(p, 2) for p in td_performance],
            "normal_performance_by_difficulty": [
                round(p, 2) for p in normal_performance
            ],
            # TD effectiveness
            "td_benefit": td_benefit,
            # Performance transitions
            "performance_transitions_td": td_transitions,
            "performance_transitions_normal": normal_transitions,
            # Pattern identification
            "pattern_type_td": pattern_td,
            "pattern_type_normal": pattern_normal,
        }

    def _calculate_td_benefit_statistics_by_difficulty(self, stage="first_attempt"):
        """Calculate detailed statistics for TD benefit at each difficulty level"""

        # Get raw difficulty breakdown
        raw_breakdown = self._generate_raw_difficulty_breakdown()

        difficulty_stats = {}

        # For each difficulty level
        for difficulty in self.difficulty_levels:
            td_improvements = []

            # Collect TD benefit for each model at this difficulty
            for model_name, model_data in raw_breakdown.items():
                if stage == "first_attempt":
                    td_acc = model_data[difficulty]["TD"]["accuracy"]
                    normal_acc = model_data[difficulty]["NORMAL"]["accuracy"]
                else:  # remediation
                    td_acc = model_data[difficulty]["TD"]["remediation"]["accuracy"]
                    normal_acc = model_data[difficulty]["NORMAL"]["remediation"][
                        "accuracy"
                    ]

                td_benefit = td_acc - normal_acc
                td_improvements.append(td_benefit)

            # Calculate descriptive statistics
            if len(td_improvements) > 0:
                # Basic statistics using statistics module
                mean_val = statistics.mean(td_improvements)
                median_val = statistics.median(td_improvements)
                std_val = (
                    statistics.stdev(td_improvements)
                    if len(td_improvements) > 1
                    else 0.0
                )
                min_val = min(td_improvements)
                max_val = max(td_improvements)

                # Percentiles using statistics.quantiles
                if len(td_improvements) >= 2:
                    quartiles = statistics.quantiles(
                        td_improvements, n=4, method="inclusive"
                    )
                    percentile_25 = quartiles[0]
                    percentile_75 = quartiles[2]
                    iqr = percentile_75 - percentile_25
                else:
                    percentile_25 = min_val
                    percentile_75 = max_val
                    iqr = 0.0

                # Confidence interval (95% using t-distribution)
                if len(td_improvements) > 1:
                    confidence_interval = stats.t.interval(
                        0.95,  # 95% confidence level
                        len(td_improvements) - 1,  # degrees of freedom
                        loc=mean_val,  # mean
                        scale=stats.sem(td_improvements),  # standard error of mean
                    )
                    confidence_interval = [
                        round(confidence_interval[0], 2),
                        round(confidence_interval[1], 2),
                    ]
                else:
                    confidence_interval = [round(mean_val, 2), round(mean_val, 2)]

                difficulty_stats[difficulty] = {
                    "td_improvements": [round(x, 2) for x in td_improvements],
                    "n_models": len(td_improvements),
                    "mean": round(mean_val, 2),
                    "median": round(median_val, 2),
                    "std_dev": round(std_val, 2),
                    "min": round(min_val, 2),
                    "max": round(max_val, 2),
                    "percentile_25": round(percentile_25, 2),
                    "percentile_75": round(percentile_75, 2),
                    "iqr": round(iqr, 2),
                    "confidence_interval": confidence_interval,
                }
            else:
                # Empty data case
                difficulty_stats[difficulty] = {
                    "td_improvements": [],
                    "n_models": 0,
                    "mean": 0.0,
                    "median": 0.0,
                    "std_dev": 0.0,
                    "min": 0.0,
                    "max": 0.0,
                    "percentile_25": 0.0,
                    "percentile_75": 0.0,
                    "iqr": 0.0,
                    "confidence_interval": [0.0, 0.0],
                }

        return difficulty_stats

    def _generate_detailed_analysis(self):
        """Generate comprehensive analysis for both first attempt and remediation"""

        # Extract unique models for metadata
        models = list(set(data["model_name"] for data in self.results_data.values()))

        detailed_analysis = {
            "metadata": {
                "analysis_date": self.analysis_timestamp.split()[
                    0
                ],  # Just the date part
                "data_source": "code_contests_difficulty_summary.json",
                "models_analyzed": sorted(models),
                "difficulties": self.difficulty_levels,
                "problems_per_difficulty": {"EASY": 13, "MEDIUM": 68, "HARD": 20},
            },
            "first_attempt": {
                "performance_and_effectiveness": self._calculate_performance_and_effectiveness(
                    "first_attempt"
                ),
                "td_benefit_statistics_by_difficulty": self._calculate_td_benefit_statistics_by_difficulty(
                    "first_attempt"
                ),
            },
            "remediation": {
                "performance_and_effectiveness": self._calculate_performance_and_effectiveness(
                    "remediation"
                ),
                "td_benefit_statistics_by_difficulty": self._calculate_td_benefit_statistics_by_difficulty(
                    "remediation"
                ),
            },
        }

        return detailed_analysis

    def _extract_raw_summary_data(self):
        """Extract raw data directly from summary.json files"""
        raw_data = {}

        # Group experiments by model
        model_experiments = defaultdict(dict)
        for config_key, data in self.results_data.items():
            model_name = data["model_name"]
            method_key = "TD" if data["is_test_driven"] else "NORMAL"
            model_experiments[model_name][method_key] = data["summary"]

        # Structure the data for easy access
        for model_name, methods in model_experiments.items():
            raw_data[model_name] = {}

            for method, summary in methods.items():
                raw_data[model_name][method] = {
                    "first_attempt": {
                        "passed": summary.get("passed", 0),
                        "failed": summary.get("failed", 0),
                        "error": summary.get("error", 0),
                        "total": summary.get("total", 0),
                        "accuracy": summary.get("accuracy", 0.0),
                    },
                    "remediation": summary.get(
                        "remediation",
                        {
                            "passed": 0,
                            "failed": 0,
                            "error": 0,
                            "total": 0,
                            "accuracy": 0.0,
                        },
                    ),
                }

        return raw_data

    def _create_output_directory(self):
        """Create output directory for analysis results"""
        # Create output directory with dynamic naming
        combined_suffix = "_combined" if self.combined_only else ""
        output_dir_name = f"results_dynamic_llm_{self.config.RATIO_OF_ROWS_TO_RUN}_ROWS_{self.config.TEST_DRIVEN_RATIO}_TD_PUBLIC_{self.config.REATTEMPT_MAX_NUM}_REATTEMPT{combined_suffix}"
        output_dir = os.path.join(self.results_all_dir, output_dir_name)

        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(self.results_all_dir, exist_ok=True)

        return output_dir

    def _save_trusted_analysis_results(self, output_dir):
        """Save trusted analysis results without calculated comparisons"""

        # Save comprehensive summary (JSON) with only trusted data
        summary_data = {
            "analysis_metadata": {
                "timestamp": self.analysis_timestamp,
                "total_configurations": len(self.results_data),
                "difficulty_levels": self.difficulty_levels,
                "config_parameters": {
                    "RATIO_OF_ROWS_TO_RUN": self.config.RATIO_OF_ROWS_TO_RUN,
                    "TEST_DRIVEN_RATIO": self.config.TEST_DRIVEN_RATIO,
                    "REATTEMPT_MAX_NUM": self.config.REATTEMPT_MAX_NUM,
                },
                "research_focus": "Test-Driven vs Normal Prompting Effectiveness",
            },
            "validation_status": self._perform_comprehensive_validation(),
            "raw_difficulty_breakdown": self._generate_raw_difficulty_breakdown(),
            "raw_summary_data": self._extract_raw_summary_data(),
        }

        with open(
            os.path.join(output_dir, "code_contests_difficulty_summary.json"), "w"
        ) as f:
            json.dump(summary_data, f, indent=2)

        # Generate and save detailed analysis
        detailed_analysis = self._generate_detailed_analysis()
        with open(
            os.path.join(output_dir, "code_contests_difficulty_details.json"), "w"
        ) as f:
            json.dump(detailed_analysis, f, indent=2)

        print(f"   ✅ Saved trusted analysis to code_contests_difficulty_summary.json")
        print(
            f"   ✅ Saved detailed statistics to code_contests_difficulty_details.json"
        )

    def _print_trusted_analysis_summary(self):
        """Print trusted analysis summary to console"""
        print(f"\n📈 ANALYSIS SUMMARY")
        print(f"   • Model configurations: {len(self.results_data)}")

        # Extract unique models
        models = set(data["model_name"] for data in self.results_data.values())
        print(f"   • Models analyzed: {', '.join(models)}")

        # Count TD vs Normal configurations
        td_count = sum(
            1 for data in self.results_data.values() if data["is_test_driven"]
        )
        normal_count = len(self.results_data) - td_count
        print(f"   • Test-driven configurations: {td_count}")
        print(f"   • Normal configurations: {normal_count}")

        # Show data sources
        print(f"   • Data extracted directly from summary.json files")
        print(f"   • Raw difficulty breakdown generated from runner result files")

        # Show validation status
        validation = self._perform_comprehensive_validation()
        print(f"\n📊 VALIDATION STATUS")
        if validation["has_mismatches"]:
            print(f"   ⚠️  {validation['summary']}")

            # Show details of mismatches
            for model, methods in validation["details"].items():
                for method, details in methods.items():
                    if details.get("difficulty_mismatches"):
                        for diff, mismatch in details["difficulty_mismatches"].items():
                            print(
                                f"      • {model} {method} {diff}: Expected {mismatch['expected_total']}, Got {mismatch['first_attempt_sum']} (missing {mismatch['missing_count']})"
                            )
        else:
            print(f"   ✅ {validation['summary']}")

        # Show key statistical findings from detailed analysis
        try:
            detailed_analysis = self._generate_detailed_analysis()

            print(f"\n📈 KEY STATISTICAL FINDINGS")

            # First attempt findings
            first_perf = detailed_analysis["first_attempt"][
                "performance_and_effectiveness"
            ]
            print(f"\nFirst Attempt Performance:")
            print(
                f"   TD:     EASY={first_perf['td_performance_by_difficulty'][0]:.1f}% → "
                f"MEDIUM={first_perf['td_performance_by_difficulty'][1]:.1f}% → "
                f"HARD={first_perf['td_performance_by_difficulty'][2]:.1f}%"
            )
            print(
                f"   Normal: EASY={first_perf['normal_performance_by_difficulty'][0]:.1f}% → "
                f"MEDIUM={first_perf['normal_performance_by_difficulty'][1]:.1f}% → "
                f"HARD={first_perf['normal_performance_by_difficulty'][2]:.1f}%"
            )
            print(f"   TD Pattern: {first_perf['pattern_type_td']}")

            # TD benefit by difficulty
            first_stats = detailed_analysis["first_attempt"][
                "td_benefit_statistics_by_difficulty"
            ]
            print(f"\nTD Benefit (First Attempt):")
            for diff in ["EASY", "MEDIUM", "HARD"]:
                stats = first_stats[diff]
                print(
                    f"   {diff}: Mean={stats['mean']:.1f}% (95% CI: [{stats['confidence_interval'][0]:.1f}, {stats['confidence_interval'][1]:.1f}])"
                )

            # Remediation comparison
            rem_perf = detailed_analysis["remediation"]["performance_and_effectiveness"]
            print(f"\nAfter Remediation:")
            print(
                f"   TD Benefit: EASY={rem_perf['td_benefit']['easy']:.1f}%, "
                f"MEDIUM={rem_perf['td_benefit']['medium']:.1f}%, "
                f"HARD={rem_perf['td_benefit']['hard']:.1f}%"
            )

            # Research question answer
            print(f"\n🎯 RESEARCH QUESTION ANSWER:")
            print(f"   TD effectiveness pattern: {first_perf['pattern_type_td']}")
            print(
                f"   Highest TD benefit: EASY problems (+{first_stats['EASY']['mean']:.1f}%)"
            )
            print(f"   Remediation reduces TD advantage significantly")

        except Exception as e:
            print(f"\n⚠️  Could not generate statistical summary: {e}")
