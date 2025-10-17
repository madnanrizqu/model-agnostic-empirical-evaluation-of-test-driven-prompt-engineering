import pandas as pd
from typing import Optional
from .strategies_interface import DatasetFormatterInterface
from .strategies.default import DefaultFormatter
from .schema_contracts import ValidatedFormatterFactory
from textwrap import dedent


class PromptModule:
    """Module for handling prompts and dataset formatting"""

    def __init__(
        self, language: str, test_driven=False, test_driven_ratio=1, io_dataset=False
    ):
        """
        Initialize the PromptModule class.

        Args:
            language (str): The programming language for which to generate prompts
            test_driven (bool): Whether to use test-driven prompts
            test_driven_ratio (float): Ratio of test-driven examples
            io_dataset (bool): Whether dataset uses stdin/stdout (default: False)
        """
        self.language = language.lower()
        self.test_driven = test_driven
        self.io_dataset = io_dataset
        self._formatter_registry = {
            "human_eval": ValidatedFormatterFactory.create_humaneval_python_formatter(
                test_driven, test_driven_ratio
            ),
            "mbpp_sanitized": ValidatedFormatterFactory.create_mbpp_python_formatter(
                test_driven, test_driven_ratio
            ),
            "code_contests": ValidatedFormatterFactory.create_code_contests_formatter(
                test_driven, test_driven_ratio
            ),
        }
        self._default_formatter = DefaultFormatter()

    def get_prompt_template(self):
        """
        Generate a prompt template for the configured programming language.

        Returns:
            str: The formatted prompt template
        """
        # Build IO-specific instructions conditionally
        if self.io_dataset:
            if self.test_driven:
                io_instructions = """8. Do NOT use sys.stdin.read(), input(), or any stdin reading methods.
                9. If input is needed, it will be provided as function parameters - parse from those parameters.
                10. Use return statements for output values, do not use print() statements unless explicitly required."""
            else:
                io_instructions = """5. Do NOT use sys.stdin.read(), input(), or any stdin reading methods.
                6. If input is needed, it will be provided as function parameters - parse from those parameters.
                7. Use return statements for output values, do not use print() statements unless explicitly required."""
        else:
            io_instructions = ""

        if self.test_driven:
            template = f"""
                Your task is to write a {self.language} function to satisfy requirements specified by the users Prompt.
                Don't generate any thing else besides code and imports for the solution to the requirements.
                1. Look at the "###Prompt" section provided to understand the users requirements.
                2. Only import from standard libraries for the {self.language} language.
                3. The primary logic must utilize the same function "###Signature" section as provided by the user
                4. Don't assume anything from standard libraries and type imports will be available, include necessary imports for the code and provided function signature in "###Signature" section.
                5. Look at the "###Test" section provided to understand the users requirements.
                6. Do not write code to verify the solution with the provided tests. Only write code for the solution.
                7. Do not write code in order to satisfy the tests, primarily focus on satisfying the prompt.
                {io_instructions}
                Mark the start of the all imports and code with ===START=== tag.
                Then mark the end with ===END=== tag.
                Do not write any import or code before ===START===.
                """
        else:
            template = f"""
                Your task is to write a {self.language} function to satisfy requirements specified by the users Prompt.
                Don't generate any thing else besides code and imports for the solution to the requirements.
                1. Look at the "###Prompt" section provided to understand the users requirements.
                2. Only import from standard libraries for the {self.language} language.
                3. The primary logic must utilize the same function "###Signature" section as provided by the user
                4. Don't assume anything from standard libraries and type imports will be available, include necessary imports for the code and provided function signature in "###Signature" section.
                {io_instructions}
                Mark the start of the all imports and code with ===START=== tag.
                Then mark the end with ===END=== tag.
                Do not write any import or code before ===START===.
                """

        return dedent(template)

    def format_dataset(
        self,
        original_df: pd.DataFrame,
        dataset_name: str,
        fallback: Optional[pd.DataFrame] = None,
    ) -> pd.DataFrame:
        """
        Format dataset using dataset-specific formatter with fallback support

        Args:
            original_df: The original dataset to format
            dataset_name: The name of the dataset to determine formatting strategy
            fallback: Optional pre-formatted dataset to use if formatting fails or dataset not supported

        Returns:
            Formatted DataFrame
        """
        try:
            # Get the appropriate formatter for the dataset
            formatter = self._get_formatter(dataset_name)

            # If we have a supported formatter, use it
            if formatter != self._default_formatter:
                return formatter.format_dataset(original_df)

            # If dataset not supported and we have a fallback, use it
            if fallback is not None:
                print(
                    f"Warning: Dataset '{dataset_name}' not supported. Using fallback dataset."
                )
                return fallback.copy()

            # Otherwise, use default formatter (returns unchanged dataset)
            print(
                f"Warning: Dataset '{dataset_name}' not supported and no fallback provided. Returning original dataset."
            )
            return self._default_formatter.format_dataset(original_df)

        except Exception as e:
            print(f"Error formatting dataset: {e}")

            # If formatting fails and we have a fallback, use it
            if fallback is not None:
                print("Using fallback dataset due to formatting error.")
                return fallback.copy()

            # Otherwise, return original dataset
            print("No fallback available. Returning original dataset.")
            return original_df.copy()

    def _get_formatter(self, dataset_name: str) -> DatasetFormatterInterface:
        """Get the appropriate formatter for the given dataset"""
        return self._formatter_registry.get(
            dataset_name.lower(), self._default_formatter
        )

    def get_remediation_prompt(self, issue_string: str) -> str:
        """
        Generate a remediation prompt describing issues with the code.

        Args:
            issue_string (str): Description of the issues found in the code.

        Returns:
            str: Remediation prompt.
        """
        return f"### Remediation Message\nThis code is not correct as it led to the following issues:\n{issue_string}"
