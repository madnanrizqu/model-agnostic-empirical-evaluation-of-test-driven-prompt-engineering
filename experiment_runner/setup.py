import sys
import os
import pandas as pd
import json
from datetime import datetime
from abc import ABC, abstractmethod

# Add the root directory to sys.path for imports
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from llm_module import ModelSolutionGenerator
from prompt_module import PromptModule
from llm_module import LLMConfigManager
from solution_formatter_module import SolutionFormatter


class BaseGetSolutionSetup:
    """Shared solution generation setup with strategic customization points"""

    def __init__(
        self, research_question, dataset_name, language, config_module, **kwargs
    ):
        """Initialize with research question parameterization and extension points"""
        self.research_question = research_question  # "rq1", "rq2", etc.
        self.dataset_name = dataset_name
        self.language = language
        self.config = config_module
        self.root_dir = ROOT_DIR

        # Extract common parameters from config
        self.test_driven = kwargs.get("test_driven", False)
        self.test_driven_ratio = kwargs.get(
            "test_driven_ratio", getattr(config_module, "TEST_DRIVEN_RATIO", 1.0)
        )
        self.llm_to_use = kwargs.get(
            "llm_to_use", getattr(config_module, "LLM_TO_USE", "OPEN_LLM")
        )

        # Initialize core components
        self._init_core_components()

        # Strategic extension point for RQ-specific customizations
        self._apply_rq_customizations(**kwargs)

        # Initialize result directory
        self._init_result_dir()

    def _init_core_components(self):
        """Initialize core components - can be overridden for custom behavior"""
        # Get LLM configuration
        self.llm_config = self._get_llm_config()

        # Initialize prompt module
        self.prompt_module = PromptModule(
            language=self.language,
            test_driven=self.test_driven,
            test_driven_ratio=self.test_driven_ratio,
        )

        # Initialize LLM module
        self.llm_module = ModelSolutionGenerator(
            self.llm_config,
            options={
                "temp_results_dir_prefix": self._get_output_path(),
                "dataset_prompt_template": self.prompt_module.get_prompt_template(),
                "max_retries": 2,  # On get better larger max retries so that no hard to regenerate error happens
            },
        )

    def _apply_rq_customizations(self, **kwargs):
        """Override point for RQ-specific initialization logic"""
        pass

    def _get_llm_config(self):
        """Override point for custom LLM selection logic"""
        manager = LLMConfigManager()

        # Check if llm_to_use is a specific LLM key (like "CHATGPT_4O") or a type (like "OPEN_LLM")
        if self.llm_to_use in manager.llm_configurations:
            # It's a specific LLM key, use get_llm_config()
            return manager.get_llm_config(self.llm_to_use)
        else:
            # It's a type, use get_llm_config_by_type()
            return manager.get_llm_config_by_type(self.llm_to_use)

    def _customize_result_dir_name(self):
        """Override point for custom result directory naming"""
        return getattr(self.config, "RESULT_DIR_NAME", "results")

    def _post_dataset_load_hook(self, dataset):
        """Override point for dataset post-processing"""
        return dataset

    def _pre_generation_hook(self, formatted_df):
        """Override point for pre-generation processing"""
        return formatted_df

    def _init_result_dir(self):
        """Initialize result directory with customizable naming"""
        self.results_dir = os.path.join(
            ROOT_DIR,
            self.research_question,
            self._get_adjusted_dataset_name(),
            self._customize_result_dir_name(),
        )

        # Create results directory if it doesn't exist
        os.makedirs(self.results_dir, exist_ok=True)

    def _get_original_dataset_name(self):
        """Get the original dataset name without any modifications"""
        return self.dataset_name

    def _get_adjusted_dataset_name(self):
        """Returns dataset name with 'td' suffix if test_driven is True"""
        if self.test_driven:
            return f"{self.dataset_name}_td"
        return self.dataset_name

    def _load_dataset(self):
        """Load the original dataset with post-processing hook"""
        csv_path = os.path.join(
            self.root_dir, "datasets", f"{self._get_original_dataset_name()}.csv"
        )
        dataset = pd.read_csv(csv_path)
        return self._post_dataset_load_hook(dataset)

    def _get_output_path(self):
        """Get the output path for results"""
        return os.path.join(
            self.root_dir,
            f"{self.research_question}/{self._get_adjusted_dataset_name()}/{self._customize_result_dir_name()}",
        )

    def _determine_indices(self, ratio_of_rows, total_rows, start_index=None):
        """Determine the start and end indices for dataset processing"""
        if ratio_of_rows == "ALL":
            calculated_start_index = start_index if start_index is not None else 0
            return calculated_start_index, None
        else:
            # Convert decimal ratio to actual number of rows
            try:
                ratio = float(ratio_of_rows)
                if not 0 <= ratio <= 1:
                    raise ValueError("Ratio must be between 0 and 1")

                if start_index is not None:
                    # When start_index is provided, calculate end_index based on ratio from start_index
                    rows_to_process = int(total_rows * ratio)
                    calculated_start_index = start_index
                    calculated_end_index = min(
                        start_index + rows_to_process - 1, total_rows - 1
                    )
                    print(
                        f"Processing {rows_to_process} rows from index {calculated_start_index} to {calculated_end_index}"
                    )
                else:
                    # Original behavior: start from 0
                    calculated_start_index = 0
                    calculated_end_index = int(total_rows * ratio) - 1
                    if calculated_end_index < 0:
                        calculated_end_index = 0
                    print(
                        f"Processing {ratio*100:.1f}% of dataset ({calculated_end_index+1} rows)"
                    )

            except ValueError as e:
                if "Ratio must be between 0 and 1" in str(e):
                    raise

            return calculated_start_index, calculated_end_index

    def generate_solutions(self, ratio_of_rows=None, start_index=None):
        """Generate solutions for the dataset with customization hooks"""
        if ratio_of_rows is None:
            ratio_of_rows = getattr(self.config, "RATIO_OF_ROWS_TO_RUN", 0.1)

        original_df = self._load_dataset()
        output_path = self._get_output_path()

        formatted_df = self.prompt_module.format_dataset(
            original_df=original_df,
            dataset_name=self._get_original_dataset_name(),
        )

        # Apply pre-generation hook
        formatted_df = self._pre_generation_hook(formatted_df)

        # Save the formatted dataset for inspection
        formatted_csv_path = os.path.join(
            output_path,
            f"tmp_{self._get_adjusted_dataset_name()}.csv",
        )
        formatted_df.to_csv(formatted_csv_path, index=False)
        print(f"Formatted dataset saved to: {formatted_csv_path}")

        # Use new _determine_indices method that supports start_index
        calculated_start_index, end_index = self._determine_indices(
            ratio_of_rows, len(formatted_df), start_index
        )

        results, errors = self.llm_module.generate_solution_for_dataset(
            dataset_name=self._get_adjusted_dataset_name(),
            dataset_numpy_frame=formatted_df,
            start_index=calculated_start_index,
            end_index=end_index,
        )

        # Calculate expected total tasks for metadata
        if calculated_start_index is not None and end_index is not None:
            expected_total = end_index - calculated_start_index + 1
        elif end_index is not None:
            expected_total = end_index + 1
        else:
            expected_total = len(formatted_df) - (calculated_start_index or 0)

        # Save metadata file
        metadata = {
            "expected_total": expected_total,
            "dataset_rows": len(formatted_df),
            "original_dataset_rows": len(original_df),
            "ratio_of_rows": ratio_of_rows,
            "start_index": calculated_start_index,
            "end_index": end_index,
            "generation_errors_count": len(errors),
            "successful_generations_count": len(results),
            "dataset_name": self._get_adjusted_dataset_name(),
            "original_dataset_name": self._get_original_dataset_name(),
            "research_question": self.research_question,
            "test_driven": self.test_driven,
            "llm_to_use": self.llm_to_use,
            "timestamp": datetime.now().isoformat(),
        }

        with open(
            os.path.join(
                output_path, f"{self._get_adjusted_dataset_name()}_metadata.json"
            ),
            "w",
        ) as f:
            json.dump(metadata, f, indent=4)

        # Save results
        with open(
            os.path.join(
                output_path, f"{self._get_adjusted_dataset_name()}_errors.json"
            ),
            "w",
        ) as f:
            json.dump(errors, f, indent=4)
        with open(
            os.path.join(
                output_path, f"{self._get_adjusted_dataset_name()}_solution.json"
            ),
            "w",
        ) as f:
            json.dump(results, f, indent=4)

        print(
            f"Metadata saved: expected_total={expected_total}, generation_errors={len(errors)}"
        )

        return results, errors


class BaseTestSolutionSetup:
    """Shared test solution setup with strategic customization points"""

    def __init__(self, research_question, dataset_name, config_module, **kwargs):
        """Initialize with research question parameterization"""
        self.research_question = research_question
        self.dataset_name = dataset_name
        self.config = config_module
        self.root_dir = ROOT_DIR

        # Extract configuration parameters
        self.llm_to_use = kwargs.get(
            "llm_to_use", getattr(config_module, "LLM_TO_USE", "OPEN_LLM")
        )

        # Extract test-driven parameters (explicit parameters take precedence over implicit detection)
        self.test_driven = kwargs.get("test_driven", False)
        self.test_driven_ratio = kwargs.get(
            "test_driven_ratio", getattr(config_module, "TEST_DRIVEN_RATIO", 1.0)
        )

        # Strategic extension point
        self._apply_test_customizations(**kwargs)

        # Initialize result directory
        self._init_result_dir()

    def _apply_test_customizations(self, **kwargs):
        """Override point for test-specific customizations"""
        pass

    def _get_custom_llm_module(self):
        """Override point for custom LLM module configuration"""
        return None  # Use default if not overridden

    def _customize_result_dir_name(self):
        """Override point for custom result directory naming"""
        return getattr(self.config, "RESULT_DIR_NAME", "results")

    def _init_result_dir(self):
        """Initialize result directory with customizable naming"""
        self.results_dir = os.path.join(
            ROOT_DIR,
            self.research_question,
            self.dataset_name,
            self._customize_result_dir_name(),
        )

        # Create results directory if it doesn't exist
        os.makedirs(self.results_dir, exist_ok=True)

    def get_standard_paths(self):
        """Get standardized paths for solutions and datasets"""
        solutions_path = os.path.join(
            self.results_dir, f"{self.dataset_name}_solution.json"
        )
        formatted_path = os.path.join(
            self.results_dir, f"{self.dataset_name}_solution_formatted.json"
        )
        dataset_path = os.path.join(self.results_dir, f"tmp_{self.dataset_name}.csv")

        return solutions_path, formatted_path, dataset_path

    def format_solutions(self, formatter):
        """Format solutions using the provided formatter"""
        solutions_path, formatted_path, _ = self.get_standard_paths()
        formatter.format_solutions_in_file(solutions_path, formatted_path)
        return formatted_path

    def get_base_config(self, language: str) -> dict:
        """Get base configuration that all test runners need with customization support"""
        _, formatted_path, dataset_path = self.get_standard_paths()

        # Use explicit test_driven parameters if provided, otherwise fallback to implicit detection
        # TODO: Remove implicit detection after migration - this is for backward compatibility, right now used in rq1
        if hasattr(self, "test_driven") and hasattr(self, "test_driven_ratio"):
            test_driven = self.test_driven
            test_driven_ratio = self.test_driven_ratio
        else:
            # Deprecated: implicit detection based on dataset name
            test_driven = self.dataset_name.endswith("_td")
            test_driven_ratio = getattr(self.config, "TEST_DRIVEN_RATIO", 1.0)

        prompt_module = PromptModule(
            language=language,
            test_driven=test_driven,
            test_driven_ratio=test_driven_ratio,
        )

        # Check for custom LLM module first
        custom_llm_module = self._get_custom_llm_module()
        if custom_llm_module:
            get_llm_module_func = lambda: custom_llm_module
        else:
            # Use default LLM configuration - same logic as _get_llm_config()
            manager = LLMConfigManager()
            if self.llm_to_use in manager.llm_configurations:
                llm_config = manager.get_llm_config(self.llm_to_use)
            else:
                llm_config = manager.get_llm_config_by_type(self.llm_to_use)

            get_llm_module_func = lambda: ModelSolutionGenerator(
                llm_config,
                options={
                    "temp_results_dir_prefix": self.results_dir,
                    "dataset_prompt_template": prompt_module.get_prompt_template(),
                    "max_retries": 0,  # On test better have no retries since test_runner already has remediation loop
                },
            )

        config = {
            "solutions_file": formatted_path,
            "dataset_file": dataset_path,
            "results_dir": self.results_dir,
            "language": language,
            "dataset_name": self.dataset_name,
            "max_attempt_num": getattr(self.config, "REATTEMPT_MAX_NUM", 5),
            "get_llm_module": get_llm_module_func,
            "formatter": SolutionFormatter(language),
            "prompt_module": prompt_module,
        }

        # Apply any custom configuration modifications
        return self._customize_base_config(config, language)

    def _customize_base_config(self, config: dict, language: str) -> dict:
        """Override point for customizing the base configuration"""
        return config
