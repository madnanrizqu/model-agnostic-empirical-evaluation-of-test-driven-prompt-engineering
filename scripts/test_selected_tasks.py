#!/usr/bin/env python3
"""
Selective test execution script for regenerated solutions.

This script runs tests only for specific task IDs (like newly regenerated solutions)
and merges the results with existing test results, preserving all previous test outcomes.

Usage:
    python test_single_regenerated.py --experiment-dir path/to/experiment/ --task-ids 69
"""

import sys
import os
import json
import argparse
from pathlib import Path

# Add the thesis directory to Python path
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from solution_formatter_module import SolutionFormatter
from test_runner_module.main import TestRunner


def detect_rq_from_path(experiment_dir):
    """Detect which RQ directory the experiment belongs to"""
    experiment_path = Path(experiment_dir)
    parts = experiment_path.parts

    # Look for rq1, rq2, or rq2_difficulties in the path
    for part in parts:
        if part in ["rq1", "rq2"]:
            return part


def get_test_setup_class(rq_name):
    """Dynamically import TestSolutionSetup from the correct RQ module"""
    if rq_name == "rq1":
        from rq1.test_solution_setup import TestSolutionSetup

        return TestSolutionSetup
    else:  # rq2
        from rq2.test_solution_setup import TestSolutionSetup

        return TestSolutionSetup


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
        llm_key = "QWEN_2_5_CODER_32B"
    elif "qwen25coder7b" in experiment_name:
        dataset_name = dataset_part.replace("_qwen25coder7b", "")
        llm_key = "QWEN_7B_CODER"
    else:
        raise ValueError(
            f"Could not identify LLM from experiment name: {experiment_name}"
        )

    return dataset_name, llm_key, test_driven, experiment_name


def load_existing_results(results_dir):
    """Load existing test results if they exist"""
    results = {"passed": {}, "fails": {}, "errors": {}, "summary": {}}

    result_files = {
        "passed": "runner_passed.json",
        "fails": "runner_fails.json",
        "errors": "runner_errors.json",
        "summary": "summary.json",
    }

    for key, filename in result_files.items():
        filepath = os.path.join(results_dir, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    results[key] = json.load(f)
                print(f"   Loaded existing {key}: {filepath}")
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"   Warning: Could not load {filepath}, starting fresh")
                results[key] = {}
        else:
            print(f"   No existing {key} file found, starting fresh")

    return results


def merge_test_results(existing_results, new_results):
    """Merge new test results with existing results"""
    print("   Merging test results...")

    # Merge each result type
    for result_type in ["passed", "fails", "errors"]:
        existing_data = existing_results[result_type]
        new_data = getattr(
            new_results,
            f"{result_type}s" if result_type == "passed" else result_type,
            {},
        )  # Add "s" only for "passed"

        # Merge LLM-specific results
        for llm_name, llm_results in new_data.items():
            if llm_name not in existing_data:
                existing_data[llm_name] = []

            # Remove any existing results for the same task_ids to avoid duplicates
            new_task_ids = {result.get("task_id") for result in llm_results}
            existing_data[llm_name] = [
                result
                for result in existing_data[llm_name]
                if result.get("task_id") not in new_task_ids
            ]

            # Add new results
            existing_data[llm_name].extend(llm_results)

            # To make sure any addition in proper order
            existing_data[llm_name].sort(key=lambda x: x.get("task_id"))

            print(
                f"   Merged {len(llm_results)} new {result_type} results for {llm_name}"
            )

    return existing_results


def save_merged_results(merged_results, updated_summary, results_dir):
    """Save merged results back to files"""
    print("   Saving merged results...")

    # Save each result type
    result_files = {
        "passed": "runner_passed.json",
        "fails": "runner_fails.json",
        "errors": "runner_errors.json",
    }

    for key, filename in result_files.items():
        filepath = os.path.join(results_dir, filename)
        with open(filepath, "w") as f:
            json.dump(merged_results[key], f, indent=2)
        print(f"   Saved merged {key}: {filepath}")

    # Save updated summary
    summary_filepath = os.path.join(results_dir, "summary.json")
    with open(summary_filepath, "w") as f:
        json.dump(updated_summary, f, indent=2)
    print(f"   Saved updated summary: {summary_filepath}")


def test_specific_tasks(experiment_dir, task_ids, llm_names=None):
    """
    Run tests only for specific task IDs and merge with existing results

    Args:
        experiment_dir: Path to the experiment directory
        task_ids: List of task IDs to test
        llm_names: Optional list of LLM names to filter (if None, test all)
    """
    print(f"Testing specific task IDs: {task_ids}")
    print(f"Experiment directory: {experiment_dir}")

    # Detect which RQ this experiment belongs to
    rq_name = detect_rq_from_path(experiment_dir)
    print(f"Detected research question: {rq_name}")

    # Get the appropriate TestSolutionSetup class
    TestSolutionSetup = get_test_setup_class(rq_name)

    # Extract experiment configuration
    dataset_name, llm_key, test_driven, directory_name = (
        extract_experiment_info_from_path(experiment_dir)
    )

    print(f"Experiment configuration:")
    print(f"  Dataset: {dataset_name}")
    print(f"  LLM: {llm_key}")
    print(f"  Test-driven: {test_driven}")
    print(f"  Directory: {directory_name}")

    # Setup test configuration (same as normal test pipeline)
    setup = TestSolutionSetup(
        dataset_name=dataset_name,
        llm_to_use=llm_key,
        directory_name=directory_name,
        test_driven=test_driven,
    )

    # Format solutions (required step)
    print("Formatting solutions...")
    formatter = SolutionFormatter("python")  # Assuming Python for RQ2
    setup.format_solutions(formatter)

    # Load existing results
    print("Loading existing test results...")
    existing_results = load_existing_results(setup.results_dir)

    # Configure TestRunner with selective task IDs
    print(f"Configuring TestRunner for task IDs: {task_ids}")
    config = setup.get_base_config("python")
    config.update(
        {
            "needs_compilation": False,
            "test_runner_dir": os.path.join(ROOT_DIR, "languages/python"),
            "llm_output_file": "llm_output.py",
            "test_file": "llm_output_test.py",
            "test_runner_binary": "python",
            "selected_task_id": task_ids,  # Filter to only test specific task IDs
        }
    )

    if llm_names:
        config["selected_llm"] = llm_names

    # Execute selective tests
    print("Executing tests...")
    runner = TestRunner(config)
    test_summary = runner.run()

    print(f"Selective test completed:")
    print(f"  Tested {len(task_ids)} task IDs")

    # Merge results
    print("Merging with existing results...")
    merged_results = merge_test_results(existing_results, runner)

    # Update TestRunner's internal state with merged results so _generate_summary() sees all results
    print("Updating TestRunner internal state with merged results...")

    # Fix key name mismatch: TestRunner expects "task_id" but merged results might have "dataset_row_id"
    def normalize_keys_for_testrunner(results_dict):
        """Ensure all result items have 'task_id' field for TestRunner compatibility"""
        for llm_name, items in results_dict.items():
            for item in items:
                if "dataset_row_id" in item and "task_id" not in item:
                    item["task_id"] = item["dataset_row_id"]
                # Debug: check what keys we have
                if llm_name == "openai/gpt-4o-mini-2024-07-18" and len(items) > 0:
                    print(f"   Sample keys in {llm_name} results: {list(item.keys())}")
                    break
        return results_dict

    # Normalize the merged results
    merged_results["passed"] = normalize_keys_for_testrunner(merged_results["passed"])
    merged_results["fails"] = normalize_keys_for_testrunner(merged_results["fails"])
    merged_results["errors"] = normalize_keys_for_testrunner(merged_results["errors"])

    runner.passeds = merged_results["passed"]
    runner.fails = merged_results["fails"]
    runner.errors = merged_results["errors"]

    # Use TestRunner's built-in summary generation (which loads metadata and handles all logic correctly)
    print("Generating updated summary using TestRunner's built-in logic...")
    updated_summary = runner._generate_summary()

    # Save merged results
    save_merged_results(merged_results, updated_summary, setup.results_dir)

    print("✅ Selective testing and result merging completed!")
    print(f"Updated summary:")
    for llm_name, stats in updated_summary.items():
        print(
            f"  {llm_name}: {stats['passed']}/{stats['total']} passed ({stats['accuracy']}%)"
        )

    return updated_summary


def main():
    parser = argparse.ArgumentParser(
        description="Test specific regenerated solutions and merge results"
    )
    parser.add_argument(
        "--experiment-dir",
        required=True,
        help="Path to the experiment directory (containing the results)",
    )
    parser.add_argument(
        "--task-ids",
        required=True,
        nargs="+",
        type=int,
        help="Task IDs to test (space-separated integers)",
    )
    parser.add_argument(
        "--llm-names", nargs="*", help="Optional: Filter to specific LLM names"
    )

    args = parser.parse_args()

    # Validate inputs
    if not os.path.exists(args.experiment_dir):
        print(f"Error: Experiment directory not found: {args.experiment_dir}")
        sys.exit(1)

    try:
        test_specific_tasks(args.experiment_dir, args.task_ids, args.llm_names)
    except Exception as e:
        print(f"Error during selective testing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
