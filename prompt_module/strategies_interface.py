from abc import ABC, abstractmethod
import pandas as pd
from typing import Optional


class DatasetFormatterInterface(ABC):
    """Abstract base class for dataset formatters with optional validation via composition"""

    def __init__(self, test_driven: bool = False, test_driven_ratio: int = 1):
        """Initialize formatter with test-driven development options

        Args:
            test_driven: Whether to format for test-driven development
            test_driven_ratio: Ratio of public tests to use for TDD
        """
        self.test_driven = test_driven
        self.test_driven_ratio = test_driven_ratio
        self.validator: Optional["DatasetValidator"] = None  # Composed, not inherited

    def set_validator(self, validator: "DatasetValidator"):
        """Optionally add validation via composition

        Args:
            validator: DatasetValidator instance to use for input/output validation
        """
        self.validator = validator

    def format_dataset(self, original_df: pd.DataFrame) -> pd.DataFrame:
        """Format dataset with optional validation

        Args:
            original_df: The original dataset DataFrame

        Returns:
            Formatted DataFrame

        Raises:
            ValueError: If validation is enabled and fails
        """
        if self.validator:
            # Use validator's validate_and_transform method
            return self.validator.validate_and_transform(self, original_df)
        else:
            # Just transform without validation (backward compatible)
            return self._transform_dataset(original_df)

    @abstractmethod
    def _transform_dataset(self, original_df: pd.DataFrame) -> pd.DataFrame:
        """Core transformation logic - implement dataset-specific formatting

        This method should contain the core formatting logic without validation,
        as validation is handled by the optional validator.

        Args:
            original_df: The original dataset DataFrame

        Returns:
            Transformed DataFrame with standardized columns
        """
        pass

    def _combine_prompt_and_test(self, row, test_column_name="test_public"):
        """Combine prompt and test for test-driven approach

        Uses ### Test header format

        Args:
            row: The row from the DataFrame.
            test_column_name: The name of the column containing the test code.
        """
        prompt = row["prompt"]
        test = row[test_column_name]
        test_lines = test.split("\n")
        # Remove empty lines at start and end
        test_lines = [line for line in test_lines if line.strip()]
        # Format test with section header
        formatted_test = "### Test\n" + "\n".join(test_lines)
        return prompt + "\n\n" + formatted_test

    def _combine_prompt_and_test_public(self, row, test_column_name="test"):
        """Combine prompt and test for test-driven public private

        Uses ### Test header format

        Args:
            row: The row from the DataFrame.
            test_column_name: The name of the column containing the test code.
        """
        prompt = row["prompt"]
        test = row[test_column_name]
        test_lines = test.split("\n")
        # Remove empty lines at start and end
        test_lines = [line for line in test_lines if line.strip()]
        # Format test with section header
        formatted_test = "### Test\n" + "\n".join(test_lines)
        return prompt + "\n\n" + formatted_test
