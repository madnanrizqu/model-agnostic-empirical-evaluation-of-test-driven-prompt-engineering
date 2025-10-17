import json
import os
import time
import shutil
import logging
import pandas as pd

from test_runner_module.utils import TimeoutExecutor
from test_runner_module.summary_calculator import SummaryCalculator

from test_runner_module.strategies.python import (
    PythonNonCommonAttributesInitiatorStrategy,
    PythonNonCommonConfigValidationStrategy,
    PythonPreparationStrategy,
    PythonTestExecutionStrategy,
    PythonTestResultCollectionStrategy,
)


class TestRunner:
    """Test runner that uses strategy pattern for language-specific test operations"""

    def __init__(self, config=None):
        if not config:
            raise ValueError("Configuration is required")

        self._setup_temp_directory(config)
        self._validate_common_config(config)
        self._setup_strategies(config)
        self.non_common_config_validator_strategy.validate(config)
        self._init_common_attributes(config)
        self.non_common_attributes_initiator_strategy.init(
            config=config, runner_context=self
        )

    def _setup_temp_directory(self, config):
        """Set up temporary subdirectory for test execution isolation"""
        self.temp_subdir = None
        self.original_test_runner_dir = None

        timestamp = int(time.time() * 1000000)
        # Use directory_name if available, fallback to dataset_name
        dir_name = config.get("directory_name") or config.get("dataset_name", "unknown")
        self.temp_subdir = f"{dir_name}_{timestamp}"

        # Get base language directory (e.g., languages/python)
        self.original_test_runner_dir = config.get("test_runner_dir")

        # Create temp subdirectory inside language directory
        self.test_runner_dir = os.path.join(
            self.original_test_runner_dir, self.temp_subdir
        )
        os.makedirs(self.test_runner_dir, exist_ok=True)

        # Update config to use temp subdirectory
        config["test_runner_dir"] = self.test_runner_dir

        print(f"Using temp directory: {self.test_runner_dir}")

    def _validate_common_config(self, config):
        """Validate the common configuration parameters required by all language types"""
        required_keys = [
            "get_llm_module",
            "formatter",
            "test_runner_dir",
            "solutions_file",
            "dataset_file",
            "llm_output_file",
            "test_file",
            "results_dir",
            "test_runner_binary",
        ]

        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required configuration key: {key}")

    def _init_common_attributes(self, config):
        """Initialize common attributes used by the test runner"""
        # llm module for reattempt
        self.get_llm_module = config.get("get_llm_module")
        self.formatter = config.get("formatter")
        self.prompt_module = config.get("prompt_module")
        self.max_attempt_num = config.get("max_attempt_num", 1)
        # Initialize SummaryCalculator with same max_attempt_num
        self.summary_calculator = SummaryCalculator(
            max_attempt_num=self.max_attempt_num
        )
        # Common attributes
        self.test_runner_dir = config.get("test_runner_dir")
        self.solutions_file = config["solutions_file"]
        self.dataset_file = config["dataset_file"]
        self.llm_output_file = config["llm_output_file"]
        self.test_file = config["test_file"]
        self.results_dir = config["results_dir"]
        self.test_runner_binary = config["test_runner_binary"]
        self.main_file = config.get("main_file", "")
        # Add timeout configuration with default value
        self.execution_timeout = config.get("execution_timeout", 30)

        # Optional filters
        self.selected_task_id = config.get("selected_task_id", [])
        self.selected_llm = config.get("selected_llm", [])

        # Results storage
        self.passeds = {}
        self.fails = {}
        self.errors = {}
        self.dataset = None

    def _setup_strategies(self, config):
        """Set up the appropriate strategies based on language configuration"""
        language = config.get("language", "").lower()

        # Create a mapping of language to strategy implementations
        language_strategies = {
            "python": {
                "config_validator": PythonNonCommonConfigValidationStrategy(),
                "attributes_initiator": PythonNonCommonAttributesInitiatorStrategy(),
                "preparation": PythonPreparationStrategy(),
                "execution": PythonTestExecutionStrategy(),
                "result_collection": PythonTestResultCollectionStrategy(),
            },
        }

        if language not in language_strategies:
            raise ValueError(f"Unsupported language: {language}")
        else:
            strategies = language_strategies[language]
            self.non_common_config_validator_strategy = strategies["config_validator"]
            self.non_common_attributes_initiator_strategy = strategies[
                "attributes_initiator"
            ]
            self.preparation_strategy = strategies["preparation"]
            self.execution_strategy = strategies["execution"]
            self.result_collection_strategy = strategies["result_collection"]

    def _read_dataset(self):
        """Read and parse the dataset from CSV using pandas"""
        self.dataset = pd.read_csv(self.dataset_file)

    def _write_to_file(self, content, file_path):
        """Write content to a file at the specified path"""
        with open(file_path, "w") as f:
            f.write(content)

    def _cleanup(self):
        """Clean up temporary directory after execution"""
        if self.temp_subdir and self.original_test_runner_dir:
            temp_path = os.path.join(self.original_test_runner_dir, self.temp_subdir)
            if os.path.exists(temp_path):
                try:
                    shutil.rmtree(temp_path)
                    print(f"Cleaned up temp directory: {temp_path}")
                except Exception as e:
                    print(
                        f"Warning: Failed to clean up temp directory {temp_path}: {e}"
                    )

    def _get_test_for_task(self, task_id):
        """Retrieve test cases for a specific task ID from the dataset"""
        task_row = self.dataset[self.dataset["task_id"] == task_id].iloc[0]
        return task_row["test"]

    def _process_solution(self, entry, index):
        """Process a single solution entry using the configured strategies"""
        task_id = entry["dataset_row_id"]
        original_prompt = entry["prompt"]
        llm_name = entry["llm_name"]
        original_solution = entry["solution"]
        context = entry.get("context")

        # Initialize result data structures
        if llm_name not in self.passeds:
            self.passeds[llm_name] = []
        if llm_name not in self.fails:
            self.fails[llm_name] = []
        if llm_name not in self.errors:
            self.errors[llm_name] = []

        # Mutable variables are defined here that
        # could be updated when code remediation is
        # executed after test failure
        process = None
        attempt_num = 0
        llm_module = self.get_llm_module()
        remediation_message = None
        solution = original_solution
        record_prompt = original_prompt
        while attempt_num < self.max_attempt_num:
            attempt_num += 1
            if attempt_num > 1:
                task_row = self.dataset[self.dataset["task_id"] == task_id].iloc[0]

                # If first remediation create messages based on
                # original prompt and original solution
                if attempt_num == 2:
                    llm_module.store_messages(
                        llm_module.create_messages(
                            prompt=original_prompt, assistant_answer=solution
                        )
                    )
                else:
                    llm_module.store_messages(
                        llm_module.extend_messages(
                            llm_module.get_stored_messages(),
                            new_content=solution,
                            role="assistant",
                        )
                    )

                new_messages = llm_module.extend_messages(
                    llm_module.get_stored_messages(),
                    self.prompt_module.get_remediation_prompt(remediation_message),
                )

                # The prompt to store in records for results analysis.
                # Should append the latest remediation prompt
                record_prompt = original_prompt + "\n" + new_messages[-1]["content"]

                # Stores for next loop
                llm_module.store_messages(new_messages)

                results, _ = llm_module.get_solution_with_existing_messages(
                    new_messages, task_row
                )

                try:
                    solution = self.formatter.format_solution(
                        results[0]["solution"], original_prompt, context
                    )
                except Exception as e:
                    # Store formatting failure occurrence to file
                    self._record_formatting_failure(
                        task_id=task_id,
                        prompt=record_prompt,
                        llm_name=llm_name,
                        error_message=str(e),
                        solution=solution,
                        context=context,
                        attempt_num=attempt_num,
                    )

                    print(f"Error formatting solution attempt no: {attempt_num}")
                    remediation_message = str(e)
                    print("Remediation message: ", remediation_message)
                    # Formatting failed, reattempt
                    continue

            # Write solution and test files
            self._write_to_file(
                solution, os.path.join(self.test_runner_dir, self.llm_output_file)
            )
            test_content = self._get_test_for_task(task_id)
            self._write_to_file(
                test_content, os.path.join(self.test_runner_dir, self.test_file)
            )

            # Use strategy to prepare the code for execution
            preparation_result = self.preparation_strategy.prepare_code(
                task_id,
                record_prompt,
                llm_name,
                solution,
                test_content,
                context,
                self,
                attempt_num,
            )

            if not preparation_result.get("success", False):
                print("Preparation fail attempt no: ", attempt_num)
                remediation_message = preparation_result.get(
                    "stderr", ""
                ) + preparation_result.get("stdout", "")

                print("Remediation message: ", remediation_message)
                # Preparation failed, either reattempt or if max attempt continue to next task
                continue

            process = TimeoutExecutor.execute_with_timeout(
                self.execution_strategy.execute_tests,
                self.execution_timeout,
                task_id,
                record_prompt,
                llm_name,
                solution,
                test_content,
                self,
            )

            if process.returncode == 0:
                self.result_collection_strategy.record_result(
                    process,
                    task_id,
                    record_prompt,
                    llm_name,
                    solution,
                    test_content,
                    context,
                    runner_context=self,
                    attempt_num=attempt_num,
                )
                break
            else:
                print("Execution fail attempt no: ", attempt_num)
                # Update the remediation message with latest error
                remediation_message = process.stderr + process.stdout
                print("Remediation message: ", remediation_message)

                self.result_collection_strategy.record_result(
                    process,
                    task_id,
                    record_prompt,
                    llm_name,
                    solution,
                    test_content,
                    context,
                    runner_context=self,
                    attempt_num=attempt_num,
                )
                # Execution failed, reattempt
                continue

    def _load_metadata_file(self, results_dir, dataset_name):
        """Load metadata file if it exists."""
        metadata_path = os.path.join(results_dir, f"{dataset_name}_metadata.json")
        try:
            with open(metadata_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Metadata file not found: {metadata_path}")
            return None
        except json.JSONDecodeError:
            print(f"Warning: Could not parse metadata JSON: {metadata_path}")
            return None

    def _load_generation_errors_file(self, results_dir, dataset_name):
        """Load generation errors file if it exists."""
        errors_path = os.path.join(results_dir, f"{dataset_name}_errors.json")
        try:
            with open(errors_path, "r") as f:
                errors = json.load(f)
                return errors if isinstance(errors, list) else []
        except FileNotFoundError:
            print(f"Warning: Generation errors file not found: {errors_path}")
            return []
        except json.JSONDecodeError:
            print(f"Warning: Could not parse generation errors JSON: {errors_path}")
            return []

    def _record_formatting_failure(
        self, task_id, prompt, llm_name, error_message, solution, context, attempt_num
    ):
        """Record formatting failures that occur during solution processing"""
        failure_data = {
            "task_id": task_id,
            "prompt": prompt,
            "llm_name": llm_name,
            "error": f"Formatting failure: {error_message}",
            "solution": solution,
            "test_content": "",  # Empty since formatting happens before test generation
            "context": context,
            "attempt_num": attempt_num,
        }

        # Ensure llm_name exists in fails dict (should already exist from line 256)
        if llm_name not in self.fails:
            self.fails[llm_name] = []

        self.fails[llm_name].append(failure_data)

    def _generate_summary(self):
        """Generate statistical summary of test execution results (delegates to SummaryCalculator)"""
        # Extract dataset name from dataset file path
        dataset_file_name = os.path.basename(self.dataset_file)
        dataset_name = dataset_file_name.replace("tmp_", "").replace(".csv", "")

        # Load metadata and generation errors
        metadata = self._load_metadata_file(self.results_dir, dataset_name)
        generation_errors = self._load_generation_errors_file(
            self.results_dir, dataset_name
        )

        # Delegate to SummaryCalculator with in-memory data
        return self.summary_calculator.calculate_summary(
            passeds=self.passeds,
            fails=self.fails,
            errors=self.errors,
            metadata=metadata,
            generation_errors=generation_errors,
            solutions=self.solutions,
        )

    def _print_summary(self, summary):
        """Print formatted summary of test execution results to console"""
        print("\nTest Execution Summary:")
        print("-" * 50)
        for llm_name, stats in summary.items():
            print(f"\nModel: {llm_name}")
            print(f"Expected Total: {stats['total']}")
            print(f"Generation Errors: {stats.get('generation_errors', 0)}")

            test_execution_total = stats["passed"] + stats["failed"] + stats["error"]
            print(
                f"Test Execution: {test_execution_total} (passed: {stats['passed']}, failed: {stats['failed']}, errors: {stats['error']})"
            )
            print(
                f"Accuracy: {stats['accuracy']}% ({stats['passed']}/{stats['total']} expected tasks)"
            )

            # Print remediation statistics if available
            if "remediation" in stats:
                print("\nRemediation Results:")
                remediation_test_total = (
                    stats["remediation"]["passed"]
                    - stats.get("generation_errors", 0)
                    + stats["remediation"]["failed"]
                    + stats["remediation"]["error"]
                )
                print(f"  Expected Total: {stats['remediation']['total']}")
                print(
                    f"  Generation Errors: {stats['remediation'].get('generation_errors', 0)}"
                )
                print(
                    f"  Test Execution: {remediation_test_total} (passed: {stats['remediation']['passed'] - stats.get('generation_errors', 0)}, failed: {stats['remediation']['failed']}, errors: {stats['remediation']['error']})"
                )
                print(
                    f"  Final Passed (including remediation): {stats['remediation']['passed']}"
                )
                print(
                    f"  Accuracy: {round(stats['remediation']['accuracy'], 2)}% ({stats['remediation']['passed']}/{stats['remediation']['total']} expected tasks)"
                )
        print("-" * 50)

    def _save_results(self, summary):
        """Save test execution results and summary to JSON files"""
        results_dir = getattr(self, "results_dir", ".")

        # Create directory if it doesn't exist
        os.makedirs(results_dir, exist_ok=True)

        fails_file = os.path.join(results_dir, "runner_fails.json")
        errors_file = os.path.join(results_dir, "runner_errors.json")
        passed_file = os.path.join(results_dir, "runner_passed.json")
        summary_file = os.path.join(results_dir, "summary.json")

        with open(fails_file, "w") as f:
            json.dump(self.fails, f, indent=2)

        with open(errors_file, "w") as f:
            json.dump(self.errors, f, indent=2)

        with open(passed_file, "w") as f:
            json.dump(self.passeds, f, indent=2)

        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

    def run(self):
        """Main execution method to process all solutions and generate reports"""
        try:
            self._read_dataset()

            with open(self.solutions_file) as f:
                self.solutions = json.load(f)

            for idx, entry in enumerate(self.solutions):
                is_task_selected = (
                    len(self.selected_task_id) == 0
                    or entry["dataset_row_id"] in self.selected_task_id
                )
                is_llm_selected = (
                    len(self.selected_llm) == 0
                    or entry["llm_name"] in self.selected_llm
                )

                if is_task_selected and is_llm_selected:
                    self._process_solution(entry, idx)

            summary = self._generate_summary()

            self._print_summary(summary)
            self._save_results(summary)

            return summary
        finally:
            # Always clean up temp directory, regardless of success or failure
            self._cleanup()
