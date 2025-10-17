#!/usr/bin/env python3
"""
Retry script for failed generation attempts using existing infrastructure.

This script uses the built-in regenerate_failed_reported_rows() method to:
1. Load failed attempts from errors.json
2. Regenerate solutions only for failed IDs
3. Automatically merge with existing successful results
4. Update solution and error files

Usage:
    python scripts/retry_error_generation.py --errors-file path/to/errors.json --experiment-dir path/to/experiment/

Note: Run this script from the thesis root directory.
"""

import sys
import os
import json
import argparse
from pathlib import Path

# Add the thesis directory to Python path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)  # Go up one level from scripts/ to thesis/
sys.path.append(ROOT_DIR)


def detect_rq_from_path(experiment_dir):
    """Detect which RQ directory the experiment belongs to"""
    experiment_path = Path(experiment_dir)
    parts = experiment_path.parts

    # Look for rq1, rq2, or rq2_difficulties in the path
    for part in parts:
        if part in ["rq1", "rq2"]:
            return part


def get_setup_class(rq_name):
    """Dynamically import GetSolutionSetup from the correct RQ module"""
    if rq_name == "rq1":
        from rq1.get_solution_setup import GetSolutionSetup

        return GetSolutionSetup
    else:  # rq2
        from rq2.get_solution_setup import GetSolutionSetup

        return GetSolutionSetup


def load_errors_from_file(errors_file_path):
    """Load failed generation attempts from errors.json file"""
    print(f"Loading errors from: {errors_file_path}")

    with open(errors_file_path, "r") as f:
        errors = json.load(f)

    print(f"Found {len(errors)} failed generation attempts")
    return errors


def extract_experiment_info_from_path(experiment_dir):
    """Extract dataset name and LLM configuration from experiment directory path"""
    experiment_path = Path(experiment_dir)

    # Extract from directory structure: rq2/human_eval_chatgpt4omini_td/results_*/
    parts = experiment_path.parts

    # Find the experiment directory (should contain dataset name and LLM info)
    experiment_name = None
    for part in parts:
        if any(dataset in part for dataset in ["human_eval", "mbpp", "code_contests"]):
            experiment_name = part
            break

    if not experiment_name:
        raise ValueError(
            f"Could not extract experiment info from path: {experiment_dir}"
        )

    # Parse experiment name (e.g., "human_eval_chatgpt4omini_td")
    if "_td" in experiment_name:
        dataset_part = experiment_name.replace("_td", "")
        test_driven = True
    else:
        dataset_part = experiment_name
        test_driven = False

    # Extract base dataset name and LLM identifier
    if "chatgpt4omini" in experiment_name:
        dataset_name = dataset_part.replace("_chatgpt4omini", "")
        llm_key = "CHATGPT_4O_MINI"
    elif "chatgpt4o" in experiment_name:
        dataset_name = dataset_part.replace("_chatgpt4o", "")
        llm_key = "CHATGPT_4O"
    elif "claude35sonnet" in experiment_name:
        dataset_name = dataset_part.replace("_claude35sonnet", "")
        llm_key = "CLAUDE_35_SONNET"
    elif "claude35haiku" in experiment_name:
        dataset_name = dataset_part.replace("_claude35haiku", "")
        llm_key = "CLAUDE_35_HAIKU"
    elif "qwen25coder32b" in experiment_name:
        dataset_name = dataset_part.replace("_qwen25coder32b", "")
        llm_key = "QWEN_2_5_CODER_32B_OR"
    elif "qwen25coder7b" in experiment_name:
        dataset_name = dataset_part.replace("_qwen25coder7b", "")
        llm_key = "QWEN_7B_CODER"
    else:
        raise ValueError(
            f"Could not identify LLM from experiment name: {experiment_name}"
        )

    # Handle experiment variants like _second_half, _combined, etc.
    # These are not part of the actual dataset file name
    if dataset_name.endswith("_second_half"):
        dataset_name = dataset_name.replace("_second_half", "")
    elif dataset_name.endswith("_combined"):
        dataset_name = dataset_name.replace("_combined", "")

    return dataset_name, llm_key, test_driven, experiment_name


def retry_failed_generations(errors_file_path, experiment_dir):
    """
    Retry failed generations using existing infrastructure

    Args:
        errors_file_path: Path to the errors.json file
        experiment_dir: Path to the experiment directory
    """
    # Detect which RQ this experiment belongs to
    rq_name = detect_rq_from_path(experiment_dir)
    print(f"Detected research question: {rq_name}")

    # Get the appropriate GetSolutionSetup class
    GetSolutionSetup = get_setup_class(rq_name)

    # Load failed attempts
    failed_rows = load_errors_from_file(errors_file_path)

    if not failed_rows:
        print("No failed attempts found. Nothing to retry.")
        return

    # Extract experiment configuration
    dataset_name, llm_key, test_driven, directory_name = (
        extract_experiment_info_from_path(experiment_dir)
    )

    print(f"Experiment configuration:")
    print(f"  Dataset: {dataset_name}")
    print(f"  LLM: {llm_key}")
    print(f"  Test-driven: {test_driven}")
    print(f"  Directory: {directory_name}")

    # Setup the generation configuration (same as original experiment)
    setup = GetSolutionSetup(
        dataset_name=dataset_name,
        language="python",  # Assuming Python for RQ2 experiments
        llm_to_use=llm_key,
        test_driven=test_driven,
        directory_name=directory_name,
    )

    # Load and format the dataset (same as normal generation flow)
    print("Loading and formatting dataset...")
    original_df = setup._load_dataset()
    formatted_df = setup.prompt_module.format_dataset(
        original_df=original_df,
        dataset_name=dataset_name,
    )

    print(f"Dataset formatted: {len(original_df)} -> {len(formatted_df)} rows")

    # Use existing retry mechanism with formatted dataset
    print(f"Retrying {len(failed_rows)} failed generations...")
    new_results, new_errors = setup.llm_module.regenerate_failed_reported_rows(
        failed_rows, formatted_df
    )

    print(f"Retry completed:")
    print(f"  New successful generations: {len(new_results)}")
    print(f"  New failed attempts: {len(new_errors)}")

    # The regenerate_failed_reported_rows method automatically handles:
    # - Saving progress incrementally
    # - Updating result files
    # - Merging with existing solutions

    # Manually merge the new results with existing solution file
    if new_results:
        print("✅ Successfully generated new solutions!")
        print("   Merging with existing solutions...")

        # Load existing solutions
        solutions_path = os.path.join(
            setup.results_dir, f"{directory_name}_solution.json"
        )
        try:
            with open(solutions_path, "r") as f:
                existing_solutions = json.load(f)
        except FileNotFoundError:
            existing_solutions = []

        # Add new results
        existing_solutions.extend(new_results)

        # Sort it
        existing_solutions.sort(key=lambda x: x["dataset_row_id"])

        # Save merged results
        with open(solutions_path, "w") as f:
            json.dump(existing_solutions, f, indent=4)

        print(
            f"   Merged {len(new_results)} new solutions with {len(existing_solutions) - len(new_results)} existing solutions."
        )
        print(f"   Total solutions: {len(existing_solutions)}")

    # Update errors file (remove successfully retried errors)
    if new_results:
        successful_ids = {result["dataset_row_id"] for result in new_results}

        # Load existing errors
        errors_path = os.path.join(setup.results_dir, f"{directory_name}_errors.json")
        try:
            with open(errors_path, "r") as f:
                existing_errors = json.load(f)
        except FileNotFoundError:
            existing_errors = []

        # Remove successfully retried errors
        remaining_errors = [
            err
            for err in existing_errors
            if err["dataset_row_id"] not in successful_ids
        ]

        # Add any new errors from retry
        if new_errors:
            remaining_errors.extend(new_errors)

        # Save updated errors
        with open(errors_path, "w") as f:
            json.dump(remaining_errors, f, indent=4)

        print(
            f"   Updated errors file: removed {len(existing_errors) - len(remaining_errors)} successfully retried errors."
        )

    if new_errors:
        print("⚠️  Some retries still failed. Check updated errors file.")

    return new_results, new_errors


def main():
    parser = argparse.ArgumentParser(description="Retry failed generation attempts")
    parser.add_argument(
        "--errors-file",
        required=True,
        help="Path to the errors.json file containing failed attempts",
    )
    parser.add_argument(
        "--experiment-dir",
        required=True,
        help="Path to the experiment directory (containing the results)",
    )

    args = parser.parse_args()

    # Validate inputs
    if not os.path.exists(args.errors_file):
        print(f"Error: Errors file not found: {args.errors_file}")
        sys.exit(1)

    if not os.path.exists(args.experiment_dir):
        print(f"Error: Experiment directory not found: {args.experiment_dir}")
        sys.exit(1)

    try:
        retry_failed_generations(args.errors_file, args.experiment_dir)
    except Exception as e:
        print(f"Error during retry: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
