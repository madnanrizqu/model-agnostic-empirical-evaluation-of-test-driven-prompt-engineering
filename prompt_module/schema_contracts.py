"""
Schema Contract System for Dataset Formatters

This module provides explicit schema contracts that define input/output requirements
for dataset formatters, enabling validation and self-documentation through composition.
"""

from dataclasses import dataclass
from typing import List, Optional, Any, Callable
import pandas as pd


@dataclass
class ColumnContract:
    """Contract definition for a single column in a dataset"""

    name: str
    required: bool = True
    data_type: type = str
    description: str = ""
    validator: Optional[Callable[[pd.Series], bool]] = None

    def validate(self, series: pd.Series) -> List[str]:
        """Validate a pandas Series against this column contract"""
        errors = []

        # Check data type if specified
        if self.data_type != str:  # Skip string type checking as it's default
            try:
                if self.data_type == int:
                    pd.to_numeric(series, errors="raise")
                elif self.data_type == float:
                    pd.to_numeric(series, errors="raise", downcast="float")
            except (ValueError, TypeError):
                errors.append(
                    f"Column '{self.name}' contains invalid {self.data_type.__name__} values"
                )

        # Run custom validator if provided
        if self.validator:
            try:
                if not self.validator(series):
                    errors.append(f"Column '{self.name}' failed custom validation")
            except Exception as e:
                errors.append(f"Column '{self.name}' validator error: {str(e)}")

        return errors


@dataclass
class SchemaContract:
    """Contract definition for dataset schema with input/output requirements"""

    input_columns: List[ColumnContract]
    output_columns: List[ColumnContract]
    dataset_type: str
    language: str = "any"
    description: str = ""

    def validate_input(self, df: pd.DataFrame) -> List[str]:
        """Validate input DataFrame against input contract"""
        errors = []

        # Check for missing required columns
        for col in self.input_columns:
            if col.required and col.name not in df.columns:
                errors.append(f"Required input column '{col.name}' missing")
            elif col.name in df.columns:
                # Validate column content
                column_errors = col.validate(df[col.name])
                errors.extend(column_errors)

        # Check for completely empty DataFrame
        if df.empty:
            errors.append("Input DataFrame is empty")

        return errors

    def validate_output(self, df: pd.DataFrame) -> List[str]:
        """Validate output DataFrame against output contract"""
        errors = []

        # Check for missing required output columns
        for col in self.output_columns:
            if col.required and col.name not in df.columns:
                errors.append(f"Required output column '{col.name}' missing")
            elif col.name in df.columns:
                # Validate column content
                column_errors = col.validate(df[col.name])
                errors.extend(column_errors)

        # Check for completely empty DataFrame
        if df.empty:
            errors.append("Output DataFrame is empty")

        return errors

    def get_required_input_columns(self) -> List[str]:
        """Get list of required input column names"""
        return [col.name for col in self.input_columns if col.required]

    def get_required_output_columns(self) -> List[str]:
        """Get list of required output column names"""
        return [col.name for col in self.output_columns if col.required]


class DatasetValidator:
    """Standalone validator that can be composed with any formatter"""

    def __init__(self, schema_contract: SchemaContract):
        self.schema_contract = schema_contract

    def _validate_input(self, df: pd.DataFrame) -> Optional[str]:
        """Validate input DataFrame and return error message if invalid"""
        errors = self.schema_contract.validate_input(df)
        if errors:
            error_msg = f"Input validation failed:\n"
            error_msg += "\n".join(f"  - {error}" for error in errors)
            error_msg += f"\nRequired columns: {self.schema_contract.get_required_input_columns()}"
            error_msg += f"\nAvailable columns: {list(df.columns)}"
            return error_msg
        return None

    def _validate_output(self, df: pd.DataFrame) -> Optional[str]:
        """Validate output DataFrame and return error message if invalid"""
        errors = self.schema_contract.validate_output(df)
        if errors:
            error_msg = f"Output validation failed:\n"
            error_msg += "\n".join(f"  - {error}" for error in errors)
            error_msg += f"\nRequired output columns: {self.schema_contract.get_required_output_columns()}"
            error_msg += f"\nActual output columns: {list(df.columns)}"
            return error_msg
        return None

    def validate_and_transform(self, formatter, df: pd.DataFrame) -> pd.DataFrame:
        """Validate input, transform data, then validate output"""
        # Input validation
        input_error = self._validate_input(df)
        if input_error:
            raise ValueError(f"{formatter.__class__.__name__}: {input_error}")

        # Transform data
        try:
            result = formatter._transform_dataset(df)
        except Exception as e:
            raise ValueError(
                f"Transformation failed in {formatter.__class__.__name__}: {str(e)}"
            )

        # Output validation
        output_error = self._validate_output(result)
        if output_error:
            raise ValueError(f"{formatter.__class__.__name__}: {output_error}")

        return result


# Standard output contract that all formatters should produce
# Refer to docs/solution_generation_pipeline.md
# Formatter is used as an input to the llm_module
STANDARD_OUTPUT_CONTRACT = [
    ColumnContract(
        name="task_id",
        required=True,
        data_type=int,
        description="Numeric task identifier for tracking and testing",
    ),
    ColumnContract(
        name="prompt",
        required=True,
        data_type=str,
        description="Formatted prompt text for LLM input with sections",
    ),
    ColumnContract(
        name="test",
        required=True,
        data_type=str,
        description="Executable test code for solution validation",
    ),
    ColumnContract(
        name="context",
        required=False,
        data_type=str,
        description="Additional context information (optional)",
    ),
]


# Python contracts
HUMANEVAL_INPUT_CONTRACT = [
    ColumnContract("task_id", description="Original HumanEval task identifier"),
    ColumnContract(
        "prompt", description="Function prompt with docstring and signature"
    ),
    ColumnContract(
        "canonical_solution", required=False, description="Reference solution"
    ),
    ColumnContract("test", description="Test cases for validation"),
    ColumnContract(
        "entry_point", required=False, description="Function entry point name"
    ),
]

MBPP_SANITIZED_INPUT_CONTRACT = [
    ColumnContract("task_id", data_type=int, description="Numeric problem identifier"),
    ColumnContract("prompt", description="Problem description text"),
    ColumnContract("test_list", description="Array of test assertion strings"),
    ColumnContract("source_file", required=False, description="Source notebook file"),
    ColumnContract("code", required=False, description="Reference solution code"),
    ColumnContract(
        "test_imports", required=False, description="Required import statements"
    ),
    ColumnContract(
        "split", required=False, description="Dataset split (train/test/validation)"
    ),
]

# Javascript contracts
HUMANEVAL_JS_INPUT_CONTRACT = [
    ColumnContract(
        "name",
        description="Task identifier with language suffix (e.g., HumanEval_0_js)",
    ),
    ColumnContract("language", description="Programming language code (js)"),
    ColumnContract("prompt", description="JavaScript function prompt with comments"),
    ColumnContract("tests", description="JavaScript test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

MBPP_JS_INPUT_CONTRACT = [
    ColumnContract(
        "name", description="Task identifier with language suffix (e.g., mbpp_3_js)"
    ),
    ColumnContract("language", description="Programming language code (js)"),
    ColumnContract("prompt", description="JavaScript function prompt with comments"),
    ColumnContract("tests", description="JavaScript test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

# Typescript contracts
HUMANEVAL_TS_INPUT_CONTRACT = [
    ColumnContract(
        "name",
        description="Task identifier with language suffix (e.g., HumanEval_0_ts)",
    ),
    ColumnContract("language", description="Programming language code (ts)"),
    ColumnContract("prompt", description="TypeScript function prompt with types"),
    ColumnContract("tests", description="TypeScript test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

MBPP_TS_INPUT_CONTRACT = [
    ColumnContract(
        "name", description="Task identifier with language suffix (e.g., mbpp_3_ts)"
    ),
    ColumnContract("language", description="Programming language code (ts)"),
    ColumnContract("prompt", description="TypeScript function prompt with types"),
    ColumnContract("tests", description="TypeScript test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

HUMANEVAL_CPP_INPUT_CONTRACT = [
    ColumnContract(
        "name",
        description="Task identifier with language suffix (e.g., HumanEval_0_cpp)",
    ),
    ColumnContract("language", description="Programming language code (cpp)"),
    ColumnContract("prompt", description="C++ function prompt with headers"),
    ColumnContract("tests", description="C++ test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

# Cpp contracts
MBPP_CPP_INPUT_CONTRACT = [
    ColumnContract(
        "name", description="Task identifier with language suffix (e.g., mbpp_3_cpp)"
    ),
    ColumnContract("language", description="Programming language code (cpp)"),
    ColumnContract("prompt", description="C++ function prompt with headers"),
    ColumnContract("tests", description="C++ test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

# C# contracts
HUMANEVAL_CSHARP_INPUT_CONTRACT = [
    ColumnContract(
        "name",
        description="Task identifier with language suffix (e.g., HumanEval_0_has_close_elements)",
    ),
    ColumnContract("language", description="Programming language code (cs)"),
    ColumnContract("prompt", description="C# class and method prompt with using statements"),
    ColumnContract("tests", description="C# test code block with Debug.Assert statements"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

MBPP_CSHARP_INPUT_CONTRACT = [
    ColumnContract(
        "name", description="Task identifier with language suffix (e.g., mbpp_3_is_not_prime)"
    ),
    ColumnContract("language", description="Programming language code (cs)"),
    ColumnContract("prompt", description="C# class and method prompt with using statements"),
    ColumnContract("tests", description="C# test code block with Debug.Assert statements"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

# Go contracts
HUMANEVAL_GO_INPUT_CONTRACT = [
    ColumnContract(
        "name",
        description="Task identifier with language suffix (e.g., HumanEval_0_go)",
    ),
    ColumnContract("language", description="Programming language code (go)"),
    ColumnContract("prompt", description="Go function prompt with package declaration"),
    ColumnContract("tests", description="Go test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

MBPP_GO_INPUT_CONTRACT = [
    ColumnContract(
        "name", description="Task identifier with language suffix (e.g., mbpp_3_go)"
    ),
    ColumnContract("language", description="Programming language code (go)"),
    ColumnContract("prompt", description="Go function prompt with package declaration"),
    ColumnContract("tests", description="Go test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

# Rust contracts
HUMANEVAL_RS_INPUT_CONTRACT = [
    ColumnContract(
        "name",
        description="Task identifier with language suffix (e.g., HumanEval_0_rs)",
    ),
    ColumnContract("language", description="Programming language code (rs)"),
    ColumnContract("prompt", description="Rust function prompt with ownership syntax"),
    ColumnContract("tests", description="Rust test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

MBPP_RS_INPUT_CONTRACT = [
    ColumnContract(
        "name", description="Task identifier with language suffix (e.g., mbpp_3_rs)"
    ),
    ColumnContract("language", description="Programming language code (rs)"),
    ColumnContract("prompt", description="Rust function prompt with ownership syntax"),
    ColumnContract("tests", description="Rust test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

# Julia contracts
HUMANEVAL_JL_INPUT_CONTRACT = [
    ColumnContract(
        "name",
        description="Task identifier with language suffix (e.g., HumanEval_0_jl)",
    ),
    ColumnContract("language", description="Programming language code (jl)"),
    ColumnContract("prompt", description="Julia function prompt with type annotations"),
    ColumnContract("tests", description="Julia test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

MBPP_JL_INPUT_CONTRACT = [
    ColumnContract(
        "name", description="Task identifier with language suffix (e.g., mbpp_3_jl)"
    ),
    ColumnContract("language", description="Programming language code (jl)"),
    ColumnContract("prompt", description="Julia function prompt with type annotations"),
    ColumnContract("tests", description="Julia test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

# Perl contracts
HUMANEVAL_PL_INPUT_CONTRACT = [
    ColumnContract(
        "name",
        description="Task identifier with language suffix (e.g., HumanEval_0_pl)",
    ),
    ColumnContract("language", description="Programming language code (pl)"),
    ColumnContract("prompt", description="Perl function prompt with subroutines"),
    ColumnContract("tests", description="Perl test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

MBPP_PL_INPUT_CONTRACT = [
    ColumnContract(
        "name", description="Task identifier with language suffix (e.g., mbpp_3_pl)"
    ),
    ColumnContract("language", description="Programming language code (pl)"),
    ColumnContract("prompt", description="Perl function prompt with subroutines"),
    ColumnContract("tests", description="Perl test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

# Racket contracts
HUMANEVAL_RKT_INPUT_CONTRACT = [
    ColumnContract(
        "name",
        description="Task identifier with language suffix (e.g., HumanEval_0_rkt)",
    ),
    ColumnContract("language", description="Programming language code (rkt)"),
    ColumnContract("prompt", description="Racket function prompt with S-expressions"),
    ColumnContract("tests", description="Racket test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

MBPP_RKT_INPUT_CONTRACT = [
    ColumnContract(
        "name", description="Task identifier with language suffix (e.g., mbpp_3_rkt)"
    ),
    ColumnContract("language", description="Programming language code (rkt)"),
    ColumnContract("prompt", description="Racket function prompt with S-expressions"),
    ColumnContract("tests", description="Racket test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

# PHP contracts
HUMANEVAL_PHP_INPUT_CONTRACT = [
    ColumnContract(
        "name",
        description="Task identifier with language suffix (e.g., HumanEval_0_php)",
    ),
    ColumnContract("language", description="Programming language code (php)"),
    ColumnContract("prompt", description="PHP function prompt with function syntax"),
    ColumnContract("tests", description="PHP test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

MBPP_PHP_INPUT_CONTRACT = [
    ColumnContract(
        "name", description="Task identifier with language suffix (e.g., mbpp_3_php)"
    ),
    ColumnContract("language", description="Programming language code (php)"),
    ColumnContract("prompt", description="PHP function prompt with function syntax"),
    ColumnContract("tests", description="PHP test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

# Scala contracts
HUMANEVAL_SCALA_INPUT_CONTRACT = [
    ColumnContract(
        "name",
        description="Task identifier with language suffix (e.g., HumanEval_0_scala)",
    ),
    ColumnContract("language", description="Programming language code (scala)"),
    ColumnContract("prompt", description="Scala function prompt with object/def syntax"),
    ColumnContract("tests", description="Scala test code block with main method"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

MBPP_SCALA_INPUT_CONTRACT = [
    ColumnContract(
        "name", description="Task identifier with language suffix (e.g., mbpp_3_scala)"
    ),
    ColumnContract("language", description="Programming language code (scala)"),
    ColumnContract("prompt", description="Scala function prompt with object/def syntax"),
    ColumnContract("tests", description="Scala test code block with main method"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

# R contracts
HUMANEVAL_R_INPUT_CONTRACT = [
    ColumnContract(
        "name",
        description="Task identifier with language suffix (e.g., HumanEval_0_r)",
    ),
    ColumnContract("language", description="Programming language code (r)"),
    ColumnContract("prompt", description="R function prompt with function syntax"),
    ColumnContract("tests", description="R test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

MBPP_R_INPUT_CONTRACT = [
    ColumnContract(
        "name", description="Task identifier with language suffix (e.g., mbpp_3_r)"
    ),
    ColumnContract("language", description="Programming language code (r)"),
    ColumnContract("prompt", description="R function prompt with function syntax"),
    ColumnContract("tests", description="R test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

# Ruby contracts
HUMANEVAL_RB_INPUT_CONTRACT = [
    ColumnContract(
        "name",
        description="Task identifier with language suffix (e.g., HumanEval_0_rb)",
    ),
    ColumnContract("language", description="Programming language code (rb)"),
    ColumnContract("prompt", description="Ruby function prompt with def syntax"),
    ColumnContract("tests", description="Ruby test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

MBPP_RB_INPUT_CONTRACT = [
    ColumnContract(
        "name", description="Task identifier with language suffix (e.g., mbpp_3_rb)"
    ),
    ColumnContract("language", description="Programming language code (rb)"),
    ColumnContract("prompt", description="Ruby function prompt with def syntax"),
    ColumnContract("tests", description="Ruby test code block"),
    ColumnContract("doctests", required=False, description="Documentation tests"),
    ColumnContract("original", required=False, description="Original source reference"),
    ColumnContract(
        "prompt_terminology", required=False, description="Terminology used in prompt"
    ),
    ColumnContract("stop_tokens", required=False, description="Generation stop tokens"),
]

# Code Contests contracts
CODE_CONTESTS_INPUT_CONTRACT = [
    ColumnContract("name", description="Problem identifier from Code Contests dataset"),
    ColumnContract("description", description="Problem description text for algorithmic challenge"),
    ColumnContract("public_tests", description="Public test cases as numpy array string"),
    ColumnContract("private_tests", required=False, description="Private test cases as numpy array string"),
    ColumnContract("generated_tests", required=False, description="Generated test cases as numpy array string"),
    ColumnContract("solutions", required=False, description="Reference solutions array"),
    ColumnContract("difficulty", required=False, data_type=int, description="Problem difficulty level"),
    ColumnContract("source", required=False, data_type=int, description="Problem source identifier"),
]


def create_schema_contract(
    input_columns: List[ColumnContract],
    dataset_type: str,
    language: str = "any",
    description: str = "",
) -> SchemaContract:
    """Helper function to create a schema contract with standard output"""
    return SchemaContract(
        input_columns=input_columns,
        output_columns=STANDARD_OUTPUT_CONTRACT,
        dataset_type=dataset_type,
        language=language,
        description=description,
    )


HUMANEVAL_SCHEMA_CONTRACT = create_schema_contract(
    HUMANEVAL_INPUT_CONTRACT,
    "human_eval",
    "python",
    "Original HumanEval dataset with Python problems",
)

MBPP_SANITIZED_SCHEMA_CONTRACT = create_schema_contract(
    MBPP_SANITIZED_INPUT_CONTRACT,
    "mbpp_sanitized",
    "python",
    "MBPP Sanitized dataset with Python problems",
)

HUMANEVAL_JS_SCHEMA_CONTRACT = create_schema_contract(
    HUMANEVAL_JS_INPUT_CONTRACT,
    "human_eval_js",
    "javascript",
    "HumanEval dataset translated to JavaScript via MultiPL-E",
)

MBPP_JS_SCHEMA_CONTRACT = create_schema_contract(
    MBPP_JS_INPUT_CONTRACT,
    "mbpp_js",
    "javascript",
    "MBPP dataset translated to JavaScript via MultiPL-E",
)

HUMANEVAL_TS_SCHEMA_CONTRACT = create_schema_contract(
    HUMANEVAL_TS_INPUT_CONTRACT,
    "human_eval_ts",
    "typescript",
    "HumanEval dataset translated to TypeScript via MultiPL-E",
)

MBPP_TS_SCHEMA_CONTRACT = create_schema_contract(
    MBPP_TS_INPUT_CONTRACT,
    "mbpp_ts",
    "typescript",
    "MBPP dataset translated to TypeScript via MultiPL-E",
)

HUMANEVAL_CPP_SCHEMA_CONTRACT = create_schema_contract(
    HUMANEVAL_CPP_INPUT_CONTRACT,
    "human_eval_cpp",
    "cpp",
    "HumanEval dataset translated to C++ via MultiPL-E",
)

MBPP_CPP_SCHEMA_CONTRACT = create_schema_contract(
    MBPP_CPP_INPUT_CONTRACT,
    "mbpp_cpp",
    "cpp",
    "MBPP dataset translated to C++ via MultiPL-E",
)

HUMANEVAL_CSHARP_SCHEMA_CONTRACT = create_schema_contract(
    HUMANEVAL_CSHARP_INPUT_CONTRACT,
    "human_eval_cs",
    "csharp",
    "HumanEval dataset translated to C# via MultiPL-E",
)

MBPP_CSHARP_SCHEMA_CONTRACT = create_schema_contract(
    MBPP_CSHARP_INPUT_CONTRACT,
    "mbpp_cs",
    "csharp",
    "MBPP dataset translated to C# via MultiPL-E",
)

HUMANEVAL_GO_SCHEMA_CONTRACT = create_schema_contract(
    HUMANEVAL_GO_INPUT_CONTRACT,
    "human_eval_go",
    "go",
    "HumanEval dataset translated to Go via MultiPL-E",
)

MBPP_GO_SCHEMA_CONTRACT = create_schema_contract(
    MBPP_GO_INPUT_CONTRACT,
    "mbpp_go",
    "go",
    "MBPP dataset translated to Go via MultiPL-E",
)

HUMANEVAL_RS_SCHEMA_CONTRACT = create_schema_contract(
    HUMANEVAL_RS_INPUT_CONTRACT,
    "human_eval_rs",
    "rust",
    "HumanEval dataset translated to Rust via MultiPL-E",
)

MBPP_RS_SCHEMA_CONTRACT = create_schema_contract(
    MBPP_RS_INPUT_CONTRACT,
    "mbpp_rs",
    "rust",
    "MBPP dataset translated to Rust via MultiPL-E",
)

HUMANEVAL_JL_SCHEMA_CONTRACT = create_schema_contract(
    HUMANEVAL_JL_INPUT_CONTRACT,
    "human_eval_jl",
    "julia",
    "HumanEval dataset translated to Julia via MultiPL-E",
)

MBPP_JL_SCHEMA_CONTRACT = create_schema_contract(
    MBPP_JL_INPUT_CONTRACT,
    "mbpp_jl",
    "julia",
    "MBPP dataset translated to Julia via MultiPL-E",
)

HUMANEVAL_PL_SCHEMA_CONTRACT = create_schema_contract(
    HUMANEVAL_PL_INPUT_CONTRACT,
    "human_eval_pl",
    "perl",
    "HumanEval dataset translated to Perl via MultiPL-E",
)

MBPP_PL_SCHEMA_CONTRACT = create_schema_contract(
    MBPP_PL_INPUT_CONTRACT,
    "mbpp_pl",
    "perl",
    "MBPP dataset translated to Perl via MultiPL-E",
)

HUMANEVAL_RKT_SCHEMA_CONTRACT = create_schema_contract(
    HUMANEVAL_RKT_INPUT_CONTRACT,
    "human_eval_rkt",
    "racket",
    "HumanEval dataset translated to Racket via MultiPL-E",
)

MBPP_RKT_SCHEMA_CONTRACT = create_schema_contract(
    MBPP_RKT_INPUT_CONTRACT,
    "mbpp_rkt",
    "racket",
    "MBPP dataset translated to Racket via MultiPL-E",
)

HUMANEVAL_SCALA_SCHEMA_CONTRACT = create_schema_contract(
    HUMANEVAL_SCALA_INPUT_CONTRACT,
    "human_eval_scala",
    "scala",
    "HumanEval dataset translated to Scala via MultiPL-E",
)

MBPP_SCALA_SCHEMA_CONTRACT = create_schema_contract(
    MBPP_SCALA_INPUT_CONTRACT,
    "mbpp_scala",
    "scala",
    "MBPP dataset translated to Scala via MultiPL-E",
)

HUMANEVAL_PHP_SCHEMA_CONTRACT = create_schema_contract(
    HUMANEVAL_PHP_INPUT_CONTRACT,
    "human_eval_php",
    "php",
    "HumanEval dataset translated to PHP via MultiPL-E",
)

MBPP_PHP_SCHEMA_CONTRACT = create_schema_contract(
    MBPP_PHP_INPUT_CONTRACT,
    "mbpp_php",
    "php",
    "MBPP dataset translated to PHP via MultiPL-E",
)

HUMANEVAL_R_SCHEMA_CONTRACT = create_schema_contract(
    HUMANEVAL_R_INPUT_CONTRACT,
    "human_eval_r",
    "r",
    "HumanEval dataset translated to R via MultiPL-E",
)

MBPP_R_SCHEMA_CONTRACT = create_schema_contract(
    MBPP_R_INPUT_CONTRACT,
    "mbpp_r",
    "r",
    "MBPP dataset translated to R via MultiPL-E",
)

HUMANEVAL_RB_SCHEMA_CONTRACT = create_schema_contract(
    HUMANEVAL_RB_INPUT_CONTRACT,
    "human_eval_rb",
    "ruby",
    "HumanEval dataset translated to Ruby via MultiPL-E",
)

MBPP_RB_SCHEMA_CONTRACT = create_schema_contract(
    MBPP_RB_INPUT_CONTRACT,
    "mbpp_rb",
    "ruby",
    "MBPP dataset translated to Ruby via MultiPL-E",
)

CODE_CONTESTS_SCHEMA_CONTRACT = create_schema_contract(
    CODE_CONTESTS_INPUT_CONTRACT,
    "code_contests",
    "python",
    "Code Contests dataset with competitive programming problems",
)


class ValidatedFormatterFactory:
    """Factory for creating formatters with validation enabled"""

    @staticmethod
    def create_humaneval_python_formatter(test_driven=False, test_driven_ratio=1):
        """Create HumanEval Python formatter with validation"""
        from .strategies.python import HumanEvalPythonFormatter

        formatter = HumanEvalPythonFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(HUMANEVAL_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    @staticmethod
    def create_mbpp_python_formatter(test_driven=False, test_driven_ratio=1):
        """Create MBPP Python formatter with validation"""
        from .strategies.python import MbppPythonFormatter

        formatter = MbppPythonFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(MBPP_SANITIZED_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    @staticmethod
    def create_humaneval_js_formatter(test_driven=False, test_driven_ratio=1):
        """Create HumanEval JavaScript formatter with validation"""
        from .strategies.javascript import HumanEvalJavaScriptFormatter

        formatter = HumanEvalJavaScriptFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(HUMANEVAL_JS_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    @staticmethod
    def create_mbpp_js_formatter(test_driven=False, test_driven_ratio=1):
        """Create MBPP JavaScript formatter with validation"""
        from .strategies.javascript import MbppJavaScriptFormatter

        formatter = MbppJavaScriptFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(MBPP_JS_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    # TypeScript formatters
    @staticmethod
    def create_humaneval_ts_formatter(test_driven=False, test_driven_ratio=1):
        """Create HumanEval TypeScript formatter with validation"""
        from .strategies.typescript import HumanEvalTypeScriptFormatter

        formatter = HumanEvalTypeScriptFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(HUMANEVAL_TS_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    @staticmethod
    def create_mbpp_ts_formatter(test_driven=False, test_driven_ratio=1):
        """Create MBPP TypeScript formatter with validation"""
        from .strategies.typescript import MbppTypeScriptFormatter

        formatter = MbppTypeScriptFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(MBPP_TS_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    # C++ formatters
    @staticmethod
    def create_humaneval_cpp_formatter(test_driven=False, test_driven_ratio=1):
        """Create HumanEval C++ formatter with validation"""
        from .strategies.cpp import HumanEvalCppFormatter

        formatter = HumanEvalCppFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(HUMANEVAL_CPP_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    @staticmethod
    def create_mbpp_cpp_formatter(test_driven=False, test_driven_ratio=1):
        """Create MBPP C++ formatter with validation"""
        from .strategies.cpp import MbppCppFormatter

        formatter = MbppCppFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(MBPP_CPP_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    # C# formatters
    @staticmethod
    def create_humaneval_csharp_formatter(test_driven=False, test_driven_ratio=1):
        """Create HumanEval C# formatter with validation"""
        from .strategies.csharp import HumanEvalCSharpFormatter

        formatter = HumanEvalCSharpFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(HUMANEVAL_CSHARP_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    @staticmethod
    def create_mbpp_csharp_formatter(test_driven=False, test_driven_ratio=1):
        """Create MBPP C# formatter with validation"""
        from .strategies.csharp import MbppCSharpFormatter

        formatter = MbppCSharpFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(MBPP_CSHARP_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    # Go formatters
    @staticmethod
    def create_humaneval_go_formatter(test_driven=False, test_driven_ratio=1):
        """Create HumanEval Go formatter with validation"""
        from .strategies.go import HumanEvalGoFormatter

        formatter = HumanEvalGoFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(HUMANEVAL_GO_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    @staticmethod
    def create_mbpp_go_formatter(test_driven=False, test_driven_ratio=1):
        """Create MBPP Go formatter with validation"""
        from .strategies.go import MbppGoFormatter

        formatter = MbppGoFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(MBPP_GO_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    # Rust formatters
    @staticmethod
    def create_humaneval_rs_formatter(test_driven=False, test_driven_ratio=1):
        """Create HumanEval Rust formatter with validation"""
        from .strategies.rust import HumanEvalRustFormatter

        formatter = HumanEvalRustFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(HUMANEVAL_RS_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    @staticmethod
    def create_mbpp_rs_formatter(test_driven=False, test_driven_ratio=1):
        """Create MBPP Rust formatter with validation"""
        from .strategies.rust import MbppRustFormatter

        formatter = MbppRustFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(MBPP_RS_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    # Julia formatters
    @staticmethod
    def create_humaneval_jl_formatter(test_driven=False, test_driven_ratio=1):
        """Create HumanEval Julia formatter with validation"""
        from .strategies.julia import HumanEvalJuliaFormatter

        formatter = HumanEvalJuliaFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(HUMANEVAL_JL_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    @staticmethod
    def create_mbpp_jl_formatter(test_driven=False, test_driven_ratio=1):
        """Create MBPP Julia formatter with validation"""
        from .strategies.julia import MbppJuliaFormatter

        formatter = MbppJuliaFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(MBPP_JL_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    # Perl formatters
    @staticmethod
    def create_humaneval_pl_formatter(test_driven=False, test_driven_ratio=1):
        """Create HumanEval Perl formatter with validation"""
        from .strategies.perl import HumanEvalPerlFormatter

        formatter = HumanEvalPerlFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(HUMANEVAL_PL_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    @staticmethod
    def create_mbpp_pl_formatter(test_driven=False, test_driven_ratio=1):
        """Create MBPP Perl formatter with validation"""
        from .strategies.perl import MbppPerlFormatter

        formatter = MbppPerlFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(MBPP_PL_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    # Racket formatters
    @staticmethod
    def create_humaneval_rkt_formatter(test_driven=False, test_driven_ratio=1):
        """Create HumanEval Racket formatter with validation"""
        from .strategies.racket import HumanEvalRacketFormatter

        formatter = HumanEvalRacketFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(HUMANEVAL_RKT_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    @staticmethod
    def create_mbpp_rkt_formatter(test_driven=False, test_driven_ratio=1):
        """Create MBPP Racket formatter with validation"""
        from .strategies.racket import MbppRacketFormatter

        formatter = MbppRacketFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(MBPP_RKT_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    # PHP formatters
    @staticmethod
    def create_humaneval_php_formatter(test_driven=False, test_driven_ratio=1):
        """Create HumanEval PHP formatter with validation"""
        from .strategies.php import HumanEvalPhpFormatter

        formatter = HumanEvalPhpFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(HUMANEVAL_PHP_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    @staticmethod
    def create_mbpp_php_formatter(test_driven=False, test_driven_ratio=1):
        """Create MBPP PHP formatter with validation"""
        from .strategies.php import MbppPhpFormatter

        formatter = MbppPhpFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(MBPP_PHP_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    # R formatters
    @staticmethod
    def create_humaneval_r_formatter(test_driven=False, test_driven_ratio=1):
        """Create HumanEval R formatter with validation"""
        from .strategies.r import HumanEvalRFormatter

        formatter = HumanEvalRFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(HUMANEVAL_R_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    @staticmethod
    def create_mbpp_r_formatter(test_driven=False, test_driven_ratio=1):
        """Create MBPP R formatter with validation"""
        from .strategies.r import MbppRFormatter

        formatter = MbppRFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(MBPP_R_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    # Scala formatters
    @staticmethod
    def create_humaneval_scala_formatter(test_driven=False, test_driven_ratio=1):
        """Create HumanEval Scala formatter with validation"""
        from .strategies.scala import HumanEvalScalaFormatter

        formatter = HumanEvalScalaFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(HUMANEVAL_SCALA_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    @staticmethod
    def create_mbpp_scala_formatter(test_driven=False, test_driven_ratio=1):
        """Create MBPP Scala formatter with validation"""
        from .strategies.scala import MbppScalaFormatter

        formatter = MbppScalaFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(MBPP_SCALA_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    # Ruby formatters
    @staticmethod
    def create_humaneval_rb_formatter(test_driven=False, test_driven_ratio=1):
        """Create HumanEval Ruby formatter with validation"""
        from .strategies.ruby import HumanEvalRubyFormatter

        formatter = HumanEvalRubyFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(HUMANEVAL_RB_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    @staticmethod
    def create_mbpp_rb_formatter(test_driven=False, test_driven_ratio=1):
        """Create MBPP Ruby formatter with validation"""
        from .strategies.ruby import MbppRubyFormatter

        formatter = MbppRubyFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(MBPP_RB_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter

    @staticmethod
    def create_code_contests_formatter(test_driven=False, test_driven_ratio=1):
        """Create Code Contests Python formatter with validation"""
        from .strategies.python import CodeContestsPythonFormatter

        formatter = CodeContestsPythonFormatter(
            test_driven=test_driven, test_driven_ratio=test_driven_ratio
        )
        validator = DatasetValidator(CODE_CONTESTS_SCHEMA_CONTRACT)
        formatter.set_validator(validator)
        return formatter
