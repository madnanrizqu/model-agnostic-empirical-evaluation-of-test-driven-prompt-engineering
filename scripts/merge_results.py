#!/usr/bin/env python3
"""
Results Merger Script

Merges first half and second half results into a complete dataset using the same
summary calculation logic as TestRunner via SummaryCalculator.
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Add the thesis directory to Python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from test_runner_module.summary_calculator import SummaryCalculator


def detect_rq_from_path(base_dir):
    """Detect which RQ directory this experiment belongs to"""
    base_path = Path(base_dir)
    parts = base_path.parts

    # Look for rq1 or rq2 in the path
    for part in parts:
        if part in ["rq1", "rq2"]:
            return part


def get_config_module(rq_name):
    """Dynamically import config from the correct RQ module"""
    if rq_name == "rq1":
        import config.rq1 as config

        return config
    else:  # rq2
        import config.rq2 as config

        return config


def find_results_directory(experiment_dir, config):
    """Find results directory inside experiment directory using config pattern"""
    if not os.path.exists(experiment_dir):
        return None

    import re

    # Build pattern from current config values
    base_pattern = f"results_.*_{config.RATIO_OF_ROWS_TO_RUN}_ROWS_{config.TEST_DRIVEN_RATIO}_TD_PUBLIC_{config.REATTEMPT_MAX_NUM}_REATTEMPT"
    pattern = f"{base_pattern}(?:_combined|_second_half)?"
    regex = re.compile(pattern)

    # Find matching directories
    for item in os.listdir(experiment_dir):
        if regex.match(item) and os.path.isdir(os.path.join(experiment_dir, item)):
            return os.path.join(experiment_dir, item)

    return None


def load_json_file(file_path):
    """Load JSON file, return empty dict/list if file doesn't exist"""
    if not os.path.exists(file_path):
        return {}

    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not load {file_path}: {e}")
        return {}


def merge_runner_files(first_dir, second_dir, filename):
    """Merge runner files from two directories by LLM name"""
    first_file = os.path.join(first_dir, filename)
    second_file = os.path.join(second_dir, filename)

    first_data = load_json_file(first_file)
    second_data = load_json_file(second_file)

    # Merge by LLM name (each file has structure: {"llm_name": [array_of_results]})
    merged = {}
    for llm_name in set(first_data.keys()) | set(second_data.keys()):
        merged[llm_name] = first_data.get(llm_name, []) + second_data.get(llm_name, [])

    return merged


def merge_solution_files(first_dir, second_dir, first_name, second_name):
    """Merge solution files (arrays) from two directories"""
    first_file = os.path.join(first_dir, first_name)
    second_file = os.path.join(second_dir, second_name)

    first_data = load_json_file(first_file)
    second_data = load_json_file(second_file)

    # Solution files are arrays, not dicts
    if not isinstance(first_data, list):
        first_data = []
    if not isinstance(second_data, list):
        second_data = []

    return first_data + second_data


def merge_metadata(first_dir, second_dir, first_name, second_name, rq_name="rq2"):
    """Merge metadata files from two directories"""
    first_file = os.path.join(first_dir, first_name)
    second_file = os.path.join(second_dir, second_name)

    first_metadata = load_json_file(first_file)
    second_metadata = load_json_file(second_file)

    # Combine key metadata fields
    combined_metadata = {
        "expected_total": (
            first_metadata.get("expected_total", 0)
            + second_metadata.get("expected_total", 0)
        ),
        "dataset_rows": (
            first_metadata.get("dataset_rows", 0)
            + second_metadata.get("dataset_rows", 0)
        ),
        "original_dataset_rows": first_metadata.get(
            "original_dataset_rows", 0
        ),  # Should be same
        "ratio_of_rows": "1.0",
        "start_index": first_metadata.get("start_index", 0),
        "end_index": second_metadata.get("end_index"),
        "generation_errors_count": (
            first_metadata.get("generation_errors_count", 0)
            + second_metadata.get("generation_errors_count", 0)
        ),
        "successful_generations_count": (
            first_metadata.get("successful_generations_count", 0)
            + second_metadata.get("successful_generations_count", 0)
        ),
        "research_question": first_metadata.get("research_question", rq_name),
        "test_driven": first_metadata.get("test_driven", False),
        "llm_to_use": first_metadata.get("llm_to_use", "UNKNOWN"),
        "merged_from": [first_name, second_name],
        "timestamp": first_metadata.get("timestamp", ""),
    }

    return combined_metadata


def save_merged_results(
    output_dir,
    merged_passeds,
    merged_fails,
    merged_errors,
    combined_solutions,
    combined_solutions_formatted,
    combined_metadata,
    summary,
    experiment_name,
    is_td,
):
    """Save all merged results to output directory"""
    os.makedirs(output_dir, exist_ok=True)

    # Save runner files
    with open(os.path.join(output_dir, "runner_passed.json"), "w") as f:
        json.dump(merged_passeds, f, indent=2)

    with open(os.path.join(output_dir, "runner_fails.json"), "w") as f:
        json.dump(merged_fails, f, indent=2)

    with open(os.path.join(output_dir, "runner_errors.json"), "w") as f:
        json.dump(merged_errors, f, indent=2)

    # Save solution files
    solution_suffix = "_td" if is_td else ""
    with open(
        os.path.join(
            output_dir, f"{experiment_name}_combined{solution_suffix}_solution.json"
        ),
        "w",
    ) as f:
        json.dump(combined_solutions, f, indent=2)

    with open(
        os.path.join(
            output_dir,
            f"{experiment_name}_combined{solution_suffix}_solution_formatted.json",
        ),
        "w",
    ) as f:
        json.dump(combined_solutions_formatted, f, indent=2)

    # Save metadata and summary
    with open(
        os.path.join(
            output_dir, f"{experiment_name}_combined{solution_suffix}_metadata.json"
        ),
        "w",
    ) as f:
        json.dump(combined_metadata, f, indent=2)

    with open(os.path.join(output_dir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)


def merge_experiment_results(
    first_dir, second_dir, output_dir, experiment_name, is_td=False, rq_name="rq2"
):
    """Merge first and second half results for any experiment directory"""

    print(f"Merging results from:")
    print(f"  First half: {first_dir}")
    print(f"  Second half: {second_dir}")
    print(f"  Output: {output_dir}")

    # 1. Merge runner files
    print("\n1. Merging runner files...")
    merged_passeds = merge_runner_files(first_dir, second_dir, "runner_passed.json")
    merged_fails = merge_runner_files(first_dir, second_dir, "runner_fails.json")
    merged_errors = merge_runner_files(first_dir, second_dir, "runner_errors.json")

    print(f"   Merged passed results for LLMs: {list(merged_passeds.keys())}")
    for llm_name in merged_passeds:
        print(f"     {llm_name}: {len(merged_passeds[llm_name])} passed")

    # 2. Merge solution files
    print("\n2. Merging solution files...")
    first_suffix = "_td" if is_td else ""
    second_suffix = "_second_half_td" if is_td else "_second_half"

    combined_solutions = merge_solution_files(
        first_dir,
        second_dir,
        f"{experiment_name}{first_suffix}_solution.json",
        f"{experiment_name}{second_suffix}_solution.json",
    )

    combined_solutions_formatted = merge_solution_files(
        first_dir,
        second_dir,
        f"{experiment_name}{first_suffix}_solution_formatted.json",
        f"{experiment_name}{second_suffix}_solution_formatted.json",
    )

    print(f"   Combined solutions: {len(combined_solutions)} total")
    print(f"   Combined formatted solutions: {len(combined_solutions_formatted)} total")

    # 3. Merge metadata
    print("\n3. Merging metadata...")
    combined_metadata = merge_metadata(
        first_dir,
        second_dir,
        f"{experiment_name}{first_suffix}_metadata.json",
        f"{experiment_name}{second_suffix}_metadata.json",
        rq_name,
    )

    print(f"   Expected total: {combined_metadata['expected_total']}")

    # 4. Calculate summary using SummaryCalculator (same logic as TestRunner)
    print("\n4. Calculating summary using SummaryCalculator...")
    calculator = SummaryCalculator(max_attempt_num=5)
    summary = calculator.calculate_summary(
        passeds=merged_passeds,
        fails=merged_fails,
        errors=merged_errors,
        metadata=combined_metadata,
        generation_errors=[],  # Combine if needed
        solutions=combined_solutions,
    )

    print(f"   Summary calculated for LLMs: {list(summary.keys())}")
    for llm_name, stats in summary.items():
        print(
            f"     {llm_name}: {stats['accuracy']}% accuracy ({stats['passed']}/{stats['total']})"
        )
        if "remediation" in stats:
            print(
                f"       Remediation: {stats['remediation']['accuracy']}% accuracy ({stats['remediation']['passed']}/{stats['remediation']['total']})"
            )

    # 5. Save merged results
    print("\n5. Saving merged results...")
    save_merged_results(
        output_dir,
        merged_passeds,
        merged_fails,
        merged_errors,
        combined_solutions,
        combined_solutions_formatted,
        combined_metadata,
        summary,
        experiment_name,
        is_td,
    )

    print(f"\n✅ Merge completed! Results saved to: {output_dir}")
    return summary


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Merge first half and second half results into complete dataset",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Merge base results
  python scripts/merge_results.py --base-dir rq1/human_eval_chatgpt4omini
  python scripts/merge_results.py --base-dir rq2/human_eval_chatgpt4omini

  # Merge test-driven results
  python scripts/merge_results.py --base-dir rq1/human_eval_chatgpt4omini --is-td
        """,
    )
    parser.add_argument(
        "--base-dir",
        required=True,
        help="Base experiment directory (e.g., rq1/human_eval_chatgpt4omini or rq2/human_eval_chatgpt4omini)",
    )
    parser.add_argument(
        "--is-td",
        action="store_true",
        help="Merge test-driven results instead of base results",
    )

    args = parser.parse_args()

    # Detect which RQ this experiment belongs to
    rq_name = detect_rq_from_path(args.base_dir)
    print(f"Detected research question: {rq_name}")

    # Get the appropriate config module
    config = get_config_module(rq_name)

    # Extract experiment name from base directory
    experiment_name = os.path.basename(args.base_dir)

    # Determine directory paths based on base_dir and is_td flag
    if args.is_td:
        first_half_exp_dir = f"{args.base_dir}_td"
        second_half_exp_dir = f"{args.base_dir}_second_half_td"
        combined_exp_dir = f"{args.base_dir}_combined_td"
        result_type = "Test-Driven"
    else:
        first_half_exp_dir = args.base_dir
        second_half_exp_dir = f"{args.base_dir}_second_half"
        combined_exp_dir = f"{args.base_dir}_combined"
        result_type = "Base"

    print(f"🚀 Merging {result_type} results for: {experiment_name}")
    print(f"   First half: {first_half_exp_dir}")
    print(f"   Second half: {second_half_exp_dir}")
    print(f"   Combined output: {combined_exp_dir}")

    # Find results directories inside experiment directories
    first_half_results_dir = find_results_directory(first_half_exp_dir, config)
    second_half_results_dir = find_results_directory(second_half_exp_dir, config)

    if not first_half_results_dir:
        print(f"❌ Error: No results directory found in {first_half_exp_dir}")
        return

    if not second_half_results_dir:
        print(f"❌ Error: No results directory found in {second_half_exp_dir}")
        return

    # Create combined output directory structure
    os.makedirs(combined_exp_dir, exist_ok=True)

    # Generate output results directory name based on config pattern
    base_pattern = f"results_.*_{config.RATIO_OF_ROWS_TO_RUN}_ROWS_{config.TEST_DRIVEN_RATIO}_TD_PUBLIC_{config.REATTEMPT_MAX_NUM}_REATTEMPT"
    combined_results_dirname = f"results_CHATGPT_4O_MINI_{config.RATIO_OF_ROWS_TO_RUN}_ROWS_{config.TEST_DRIVEN_RATIO}_TD_PUBLIC_{config.REATTEMPT_MAX_NUM}_REATTEMPT_combined"
    combined_results_dir = os.path.join(combined_exp_dir, combined_results_dirname)

    print(f"   Results directories found:")
    print(f"     First half: {first_half_results_dir}")
    print(f"     Second half: {second_half_results_dir}")
    print(f"     Combined output: {combined_results_dir}")

    # Perform merge
    summary = merge_experiment_results(
        first_half_results_dir,
        second_half_results_dir,
        combined_results_dir,
        experiment_name,
        args.is_td,
        rq_name,
    )

    print(f"\n📊 Final Summary:")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
