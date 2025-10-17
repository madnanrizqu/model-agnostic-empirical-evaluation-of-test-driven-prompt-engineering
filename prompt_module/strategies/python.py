import pandas as pd
import re
from ..strategies_interface import DatasetFormatterInterface
import json


class PythonAssertionExtractor:
    """Utility class for extracting and validating assertions from Python test code."""

    def __init__(self, test_driven_ratio=1):
        self.test_driven_ratio = test_driven_ratio

    def _extract_assertions(self, test_code: str) -> str:
        lines = test_code.splitlines()
        assertions = []
        in_assertion = False
        current_assertion = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("assert"):
                if in_assertion:
                    assertions.append(" ".join(current_assertion))
                    current_assertion = []
                in_assertion = True
                current_assertion.append(stripped)
            elif in_assertion:
                current_assertion.append(stripped)
                if stripped.endswith("]") or stripped.endswith(")"):
                    assertions.append(" ".join(current_assertion))
                    current_assertion = []
                    in_assertion = False
        if current_assertion:
            assertions.append(" ".join(current_assertion))
        res = "\n".join(assertions)
        self._validate_test_seq(res)
        return res

    def _validate_test_seq(self, test_seq: str) -> None:
        lines = test_seq.split("\n")
        invalid_lines = []
        for line in lines:
            if not line.strip().startswith("assert"):
                invalid_lines.append(line)
        if invalid_lines:
            error_message = "Invalid assertions found in test sequence:\n"
            for invalid_line in invalid_lines:
                error_message += f"{invalid_line}\n"
            raise ValueError(error_message)

    def _extract_test_seq_private_public(self, test_seq: str) -> tuple:
        lines = test_seq.split("\n")
        num_lines_to_extract = max(1, int(len(lines) * self.test_driven_ratio))
        public_part = "\n".join(lines[:num_lines_to_extract])
        private_part = "\n".join(lines[num_lines_to_extract:])
        return public_part, private_part


class HumanEvalPythonFormatter(DatasetFormatterInterface):
    """Formatter for Python HumanEval dataset"""

    def __init__(self, test_driven: bool = False, test_driven_ratio=1):
        """Initialize the formatter with test-driven option

        Args:
            test_driven: Whether to format for test-driven development (default: False)
        """
        super().__init__(test_driven, test_driven_ratio)
        self.assertion_extractor = PythonAssertionExtractor(test_driven_ratio)

    def _transform_dataset(self, original_df: pd.DataFrame) -> pd.DataFrame:
        """Transform HumanEval dataset with Python-specific formatting"""
        df = original_df.copy()

        if self.test_driven:
            return self._format_test_driven(df)
        else:
            return self._format_regular(df)

    def _format_regular(self, df: pd.DataFrame) -> pd.DataFrame:
        """Format for regular (non-test-driven) development"""
        # Remove double prompt for HumanEval/10
        df["prompt"] = df.apply(self._remove_double_prompt, axis=1)

        # Format prompt with sections (docstring and signature)
        df["prompt"] = df["prompt"].apply(self._format_prompt_with_sections)

        # Clean metadata from tests
        df["test"] = df["test"].apply(self._clean_metadata)

        # Add executing tests
        df["test"] = df.apply(self._add_executing_tests, axis=1)

        # Extract numeric part from task_id and convert to integer (only if it's still string)
        if df["task_id"].dtype == "object":
            df["task_id"] = df["task_id"].str.extract(r"(\d+)").astype(int)

        # Sort by task id
        df = df.sort_values(by="task_id")

        return df

    def _format_test_driven(self, df: pd.DataFrame) -> pd.DataFrame:
        """Format for test-driven development"""
        # Remove double prompt for HumanEval/10
        df["prompt"] = df.apply(self._remove_double_prompt, axis=1)

        # Format prompt with sections (docstring and signature)
        df["prompt"] = df["prompt"].apply(self._format_prompt_with_sections)

        # Clean metadata from tests
        df["test"] = df["test"].apply(self._clean_metadata)

        # Extract assertions and save to a new column "test_seq"
        df["test_seq"] = df["test"].apply(self.assertion_extractor._extract_assertions)

        # Extract a subset of assertions based on the ratio and save to a new column "test_seq_ratio"
        df["test_public"], df["test_private"] = zip(
            *df["test_seq"].apply(
                self.assertion_extractor._extract_test_seq_private_public
            )
        )

        # Combine prompt and test for test-driven approach
        df["prompt"] = df.apply(self._combine_prompt_and_test, axis=1)

        # Add executing tests
        df["test"] = df.apply(self._add_executing_tests, axis=1)

        # Extract numeric part from task_id and convert to integer (only if it's still string)
        if df["task_id"].dtype == "object":
            df["task_id"] = df["task_id"].str.extract(r"(\d+)").astype(int)

        # Sort by task id
        df = df.sort_values(by="task_id")

        return df

    def _format_prompt_with_sections(self, prompt_text):
        """Format prompt to extract docstring and signature into separate sections"""
        function_parts = []

        lines = prompt_text.split("\n")
        current_function = []
        in_function = False

        for line in lines:
            stripped = line.strip()

            # Skip import statements - we don't want them in the formatted output
            if stripped.startswith(("import ", "from ")):
                continue

            # Start of function definition
            if stripped.startswith("def "):
                if current_function:
                    function_parts.append(current_function)
                current_function = [line]
                in_function = True
                continue

            # Add to current function if we're inside one
            if in_function:
                current_function.append(line)
                # Check if we've reached the end of the function (empty line or next def)
                if not stripped and len(current_function) > 1:
                    # Check if this is truly the end by looking for docstring closure
                    docstring_closed = False
                    for func_line in current_function:
                        # Check both quote styles
                        if '"""' in func_line:
                            if func_line.count('"""') == 2:  # Single line docstring
                                docstring_closed = True
                                break
                            elif func_line.count('"""') == 1:
                                docstring_closed = not docstring_closed
                        elif "'''" in func_line:
                            if func_line.count("'''") == 2:  # Single line docstring
                                docstring_closed = True
                                break
                            elif func_line.count("'''") == 1:
                                docstring_closed = not docstring_closed

                    if docstring_closed:
                        in_function = False

        # Add the last function if exists
        if current_function:
            function_parts.append(current_function)

        # Process each function to extract signature and docstring
        formatted_functions = []
        for func_lines in function_parts:
            signature_line = func_lines[0]  # First line is always the def statement

            # Extract docstring
            docstring_lines = []
            in_docstring = False
            current_quote_marker = None  # Track which quote style we're using
            docstring_start_idx = -1

            for i, line in enumerate(func_lines[1:], 1):
                stripped = line.strip()
                quote_marker, quote_count = self._detect_docstring_quote(stripped)

                if quote_marker:
                    if not in_docstring:
                        # Starting a new docstring
                        in_docstring = True
                        current_quote_marker = quote_marker
                        docstring_start_idx = i

                        if quote_count == 2:
                            # Single-line docstring (opening and closing on same line)
                            docstring_lines.append(line)
                            break
                        else:
                            # Multi-line docstring (opening only)
                            docstring_lines.append(line)
                    else:
                        # We're already in a docstring - check if this closes it
                        if quote_marker == current_quote_marker:
                            # Found matching closing marker
                            docstring_lines.append(line)
                            break
                        else:
                            # Different quote marker inside docstring - treat as content
                            docstring_lines.append(line)
                elif in_docstring:
                    # Inside docstring, no quotes on this line
                    docstring_lines.append(line)

            # Format the function
            formatted_func = "### Prompt\n"

            if docstring_lines:
                # Clean up docstring formatting - remove both types of triple quotes
                cleaned_docstring = []
                for line in docstring_lines:
                    # Remove both types of triple quotes but keep the content
                    cleaned_line = line.replace('"""', "").replace("'''", "").rstrip()
                    cleaned_docstring.append(cleaned_line)

                # Remove empty lines at start and end
                while cleaned_docstring and not cleaned_docstring[0].strip():
                    cleaned_docstring.pop(0)
                while cleaned_docstring and not cleaned_docstring[-1].strip():
                    cleaned_docstring.pop()

                # Don't add triple quotes around the docstring content
                formatted_func += "\n".join(cleaned_docstring) + "\n\n"

            formatted_func += "### Signature\n"
            # Remove the extra colon - signature_line already ends with ':'
            formatted_func += signature_line.rstrip()

            formatted_functions.append(formatted_func)

        # Just return the formatted functions without imports
        result = "\n\n".join(formatted_functions)

        return result

    def _detect_docstring_quote(self, line: str) -> tuple:
        """
        Detect which docstring quote style is used in a line.

        Args:
            line: The line to check for docstring quotes

        Returns:
            Tuple of (quote_marker, count) where:
            - quote_marker is triple-double-quotes or triple-single-quotes or None
            - count is how many times the marker appears in the line
        """
        if '"""' in line:
            return '"""', line.count('"""')
        elif "'''" in line:
            return "'''", line.count("'''")
        return None, 0

    def _remove_double_prompt(self, row):
        """Remove isPalindrome function from HumanEval/10 task"""
        text = row["prompt"]
        task_id = row["task_id"]

        # Check if this is HumanEval/10 and contains isPalindrome
        if task_id == "HumanEval/10":
            # Find the start of isPalindrome function
            is_palindrome_start = text.find("def is_palindrome(string: str) -> bool:")
            # Find the start of make_palindrome function
            make_palindrome_start = text.find(
                "def make_palindrome(string: str) -> str:"
            )

            # Remove isPalindrome function by keeping only text before it and after make_palindrome
            if is_palindrome_start < make_palindrome_start:
                # Keep text before isPalindrome and from make_palindrome onwards
                before_is_palindrome = text[:is_palindrome_start].rstrip()
                from_make_palindrome = text[make_palindrome_start:]
                return before_is_palindrome + "\n\n" + from_make_palindrome

        return text

    def _clean_metadata(self, text):
        """Remove metadata from test strings"""
        if "METADATA" in text:
            def_position = text.find("def")
            return text[def_position:]
        return text

    def _add_executing_tests(self, row):
        """Add executing tests with proper imports"""
        text = row["test"]
        prompt = row["prompt"]

        # Extract function name from the formatted prompt (look in Signature section)
        signature_match = re.search(
            r"### Signature\s*\ndef (\w+)\(", prompt, re.MULTILINE
        )
        if signature_match:
            function_name = signature_match.group(1)
        else:
            # Fallback to original method if new format not found
            match = re.search(r"def (\w+)\(", prompt)
            if match:
                function_name = match.group(1)
            else:
                return text

        import_line = f"from llm_output import {function_name}\n\n"
        text = import_line + text
        return text + f"\ncheck({function_name})"


class MbppPythonFormatter(DatasetFormatterInterface):
    """Formatter for Python MBPP dataset"""

    def __init__(self, test_driven: bool = False, test_driven_ratio=1):
        """Initialize the formatter with test-driven option

        Args:
            test_driven: Whether to format for test-driven development (default: False)
            test_driven_ratio: Ratio of public tests to use for test-driven development (default: 1)
        """
        super().__init__(test_driven, test_driven_ratio)
        self.assertion_extractor = PythonAssertionExtractor(test_driven_ratio)

    def _transform_dataset(self, original_df: pd.DataFrame) -> pd.DataFrame:
        """Transform MBPP dataset with Python-specific formatting"""
        df = original_df.copy()

        if self.test_driven:
            return self._format_test_driven(df)
        else:
            return self._format_regular(df)

    def _format_regular(self, df: pd.DataFrame) -> pd.DataFrame:
        """Format for regular (non-test-driven) development based on format_mbpp_sanitized.py"""
        # Column validation is now handled by the schema contract system

        # Save original test_list
        df["ori_test_list"] = df["test_list"]

        # Extract function name from code
        df["func_name"] = df["code"].apply(self._extract_function_name)

        # Format prompt with sections (prompt and signature)
        df["prompt"] = df.apply(self._format_prompt_with_sections, axis=1)

        # Replace escaped single quotes with triple quotes in test_list
        df["test_list"] = df["test_list"].str.replace(r"\'", '"""')

        # Format to testing environment compatible test cases
        df["test_list"] = df.apply(self._apply_format_to_test_list, axis=1)

        # Handle edge cases
        self._handle_edge_cases(df)

        # Add 'import math' only if it exists in test_imports
        df["test_list"] = df.apply(self._add_math_import, axis=1)

        # Formats to follow llm module - rename test_list to test
        df = df.rename(columns={"test_list": "test"})

        # Add executing tests
        df["test"] = df.apply(self._add_executing_tests, axis=1)

        # Add context column as JSON with function name
        df["context"] = df["func_name"].apply(
            lambda func_name: json.dumps({"function_name": func_name})
        )

        # Sort by task id
        df = df.sort_values(by="task_id")

        return df

    def _format_test_driven(self, df: pd.DataFrame) -> pd.DataFrame:
        """Format for test-driven development based on format_mbpp_sanitized_td.py"""
        # Save original test_list
        df["ori_test_list"] = df["test_list"]

        # Extract function name from code
        df["func_name"] = df["code"].apply(self._extract_function_name)

        # Format prompt with sections (prompt and signature)
        df["prompt"] = df.apply(self._format_prompt_with_sections, axis=1)

        # Replace escaped single quotes with triple quotes in test_list
        df["test_list"] = df["test_list"].str.replace(r"\'", '"""')

        # Format to testing environment compatible test cases
        df["test_list"] = df.apply(self._apply_format_to_test_list, axis=1)

        # Handle edge cases
        self._handle_edge_cases(df)

        # Add 'import math' only if it exists in test_imports
        df["test_list"] = df.apply(self._add_math_import, axis=1)

        # Formats to follow llm module - rename test_list to test
        df = df.rename(columns={"test_list": "test"})

        # Extract assertions and save to a new column "test_seq"
        df["test_seq"] = df["test"].apply(self.assertion_extractor._extract_assertions)

        # Extract a subset of assertions based on the ratio and save to a new column "test_seq_ratio"
        df["test_public"], df["test_private"] = zip(
            *df["test_seq"].apply(
                self.assertion_extractor._extract_test_seq_private_public
            )
        )

        # Combine prompt and test for test-driven approach
        df["prompt"] = df.apply(self._combine_prompt_and_test, axis=1)

        # Add executing tests
        df["test"] = df.apply(self._add_executing_tests, axis=1)

        # Add context column as JSON with function name
        df["context"] = df["func_name"].apply(
            lambda func_name: json.dumps({"function_name": func_name})
        )

        # Sort by task id
        df = df.sort_values(by="task_id")

        return df

    def _extract_function_name(self, code):
        """Extract function name from code"""
        # Initialize function name as None
        func_name = None
        # Look through all lines
        for line in code.split("\n"):
            if line.strip().startswith("def "):
                # Extract everything between 'def ' and '('
                # Keep overwriting func_name to get the last one
                func_name = line.strip()[4:].split("(")[0]
        return func_name

    def _format_prompt_with_sections(self, row):
        """Format prompt to have sections with original prompt content and function signature"""
        prompt_text = row["prompt"]
        code = row["code"]

        # Extract function signature from code
        signature_line = None
        for line in code.split("\n"):
            stripped = line.strip()
            if stripped.startswith("def "):
                signature_line = stripped
                break

        # Format the sections
        formatted_prompt = "### Prompt\n"
        formatted_prompt += prompt_text + "\n\n"
        formatted_prompt += "### Signature\n"
        if signature_line:
            formatted_prompt += signature_line

        return formatted_prompt

    def _format_to_check_function(self, test_string, func_name):
        """Format test string to check function"""
        # Clean the string and split by 'assert'
        # Find the first instance of 'assert' and check the character before it
        assert_pos = test_string.find("assert")
        quote_char = test_string[assert_pos - 1] if assert_pos > 0 else "'"
        # Split by newlines first to handle each assertion separately
        lines = test_string.strip("[]").split("\n")
        cleaned_lines = []
        for line in lines:
            # Find quote char for each line
            assert_pos = line.find("assert")
            if assert_pos > 0:
                line_quote_char = line[assert_pos - 1]
                cleaned_lines.append(line.strip().replace(line_quote_char, ""))
        cleaned = " ".join(cleaned_lines)
        assertions = [a.strip() for a in cleaned.split("assert") if a.strip()]

        formatted_lines = []
        for assertion in assertions:
            # Replace func name and replace with 'candidate'
            formatted = "assert " + assertion.replace(func_name, "candidate", 1)
            formatted_lines.append(f"    {formatted}")

        check_function = "def check(candidate):\n"
        check_function += "\n".join(formatted_lines)

        return check_function

    def _apply_format_to_test_list(self, row):
        """Apply format to test list"""
        test_list = row["test_list"]
        func_name = row["func_name"]
        return self._format_to_check_function(test_list, func_name)

    def _handle_edge_cases(self, df):
        """Handle edge cases for specific task IDs"""
        # Replace test_list for task_id 563
        df.loc[
            df["task_id"] == 563, "test_list"
        ] = """
def check(candidate):
    assert extract_values("Python", "PHP", "Java") == ["Python", "PHP", "Java"]
    assert extract_values("python", "program", "language") == ["python", "program", "language"]
    assert extract_values("red", "blue", "green", "yellow") == ["red", "blue", "language", "yellow"]
"""
        # Replace test_list for task_id 725
        df.loc[
            df["task_id"] == 725, "test_list"
        ] = """
def check(candidate):
    assert extract_quotation('Cortex "A53" Based "multi" tasking "Processor"') == ['A53', 'multi', 'Processor']
    assert extract_quotation('Cast your "favorite" entertainment "apps"') == ['favorite', 'apps']
    assert extract_quotation('Watch content "4k Ultra HD" resolution with "HDR 10" Support') == ['4k Ultra HD', 'HDR 10']
    assert extract_quotation("Watch content '4k Ultra HD' resolution with 'HDR 10' Support") == []
"""

    def _add_math_import(self, row):
        """Add math import if needed"""
        # Check if test_imports column exists and has a value
        if (
            "test_imports" in row
            and pd.notna(row["test_imports"])
            and "math" in str(row["test_imports"])
        ):
            return "import math\n" + row["test_list"]
        return row["test_list"]

    def _add_executing_tests(self, row):
        """Add executing tests with proper imports"""
        text = row["test"]

        # Extract function name from prompt
        function_name = row["func_name"]

        import_line = f"from llm_output import {function_name}\n\n"
        text = import_line + text
        return text + f"\n\ncheck({function_name})"


class CodeContestsPythonFormatter(DatasetFormatterInterface):
    """Formatter for Code Contests dataset with I/O test conversion"""

    def __init__(self, test_driven=False, test_driven_ratio=1):
        super().__init__(test_driven, test_driven_ratio)
        self.assertion_extractor = PythonAssertionExtractor(test_driven_ratio)

    def _parse_numpy_array_string(self, array_string):
        """Parse numpy array string format to extract input/output pairs"""
        if not array_string or pd.isna(array_string):
            return []

        try:
            # Method 1: Use ast.literal_eval after preprocessing
            import ast
            import re

            # Replace array calls with just the list content, handling multiline strings
            # Use DOTALL flag to match across newlines
            pattern = r"array\((\[.*?\]), dtype=object\)"
            cleaned = re.sub(pattern, r"\1", str(array_string), flags=re.DOTALL)

            # Escape newlines for ast.literal_eval (convert actual newlines to \n literals)
            escaped = (
                cleaned.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
            )

            # Parse the cleaned dictionary
            parsed = ast.literal_eval(escaped)

            if isinstance(parsed, dict) and "input" in parsed and "output" in parsed:
                inputs = parsed["input"]
                outputs = parsed["output"]

                # Ensure they're lists
                if not isinstance(inputs, list):
                    inputs = [inputs]
                if not isinstance(outputs, list):
                    outputs = [outputs]

                # Pair up inputs and outputs
                test_cases = []
                for i in range(min(len(inputs), len(outputs))):
                    test_cases.append((inputs[i], outputs[i]))

                return test_cases

        except Exception as e:
            # Method 2: Fallback to controlled eval if ast fails
            try:
                safe_dict = {
                    "array": lambda x, dtype=None: x,
                    "object": object,
                    "__builtins__": {},
                }
                parsed = eval(str(array_string), safe_dict)

                if (
                    isinstance(parsed, dict)
                    and "input" in parsed
                    and "output" in parsed
                ):
                    inputs = parsed["input"]
                    outputs = parsed["output"]

                    # Ensure they're lists
                    if not isinstance(inputs, list):
                        inputs = [inputs]
                    if not isinstance(outputs, list):
                        outputs = [outputs]

                    # Pair up inputs and outputs
                    test_cases = []
                    for i in range(min(len(inputs), len(outputs))):
                        test_cases.append((inputs[i], outputs[i]))

                    return test_cases

            except Exception:
                pass

        # If all methods fail, return empty list
        return []

    def _parse_test_data(self, test_string):
        """Parse test data from numpy array string format"""
        return self._parse_numpy_array_string(test_string)

    def _aggregate_all_tests(self, row):
        """Combine public_tests, private_tests, and generated_tests"""
        all_test_cases = []

        # Parse each test source
        for test_column in ["public_tests", "private_tests", "generated_tests"]:
            if test_column in row and not pd.isna(row[test_column]):
                test_cases = self._parse_test_data(row[test_column])
                all_test_cases.extend(test_cases)

        return all_test_cases

    def _create_competitive_programming_test(self, test_cases):
        """Convert I/O test cases to Python function assertions"""
        if not test_cases:
            return "# No test cases available"

        assertions = []
        for input_str, output_str in test_cases:
            # Escape special characters for valid Python string literals
            input_escaped = (
                input_str.replace("\\", "\\\\")
                .replace('"', '\\"')
                .replace("\n", "\\n")
                .replace("\r", "\\r")
                .replace("\t", "\\t")
            )
            output_escaped = (
                output_str.replace("\\", "\\\\")
                .replace('"', '\\"')
                .replace("\n", "\\n")
                .replace("\r", "\\r")
                .replace("\t", "\\t")
            )

            assertion = (
                f'    assert solve_problem("{input_escaped}") == "{output_escaped}"'
            )
            assertions.append(assertion)

        # Generate check(candidate) function wrapper
        test_code = "from llm_output import solve_problem\n\n"
        test_code += "def check(candidate):\n"
        test_code += "\n".join(assertions)
        test_code += "\n\ncheck(solve_problem)"

        return test_code

    def _generate_function_signature(self):
        """Generate standard competitive programming function signature"""
        return "def solve_problem(input_str: str) -> str:"

    def _format_problem_description(self, description):
        """Format problem description into ### Prompt section"""
        if pd.isna(description):
            return "No description available"

        # Clean description text and ensure proper formatting
        cleaned_description = str(description).strip()
        return cleaned_description

    def _create_prompt_sections(self, description, signature):
        """Create formatted prompt with ### sections"""
        prompt = "### Prompt\n"
        prompt += self._format_problem_description(description)
        prompt += "\n\n### Signature\n"
        prompt += signature

        return prompt

    def _transform_dataset(self, df):
        """Main transformation method following schema contract"""
        result_df = df.copy()

        if self.test_driven:
            return self._format_test_driven(result_df)
        else:
            return self._format_regular(result_df)

    def _format_regular(self, df):
        """Format for regular (non-test-driven) development"""
        return self._format_dataset_common(df, test_driven=False)

    def _format_test_driven(self, df):
        """Format for test-driven development"""
        return self._format_dataset_common(df, test_driven=True)

    def _format_dataset_common(self, df, test_driven=False):
        """Common formatting logic for both regular and test-driven modes"""
        result_df = df.copy()

        for idx, row in result_df.iterrows():
            # 1. Parse and aggregate all test data
            all_tests = self._aggregate_all_tests(row)

            # 2. Convert I/O tests to Python assertions
            test_code = self._create_competitive_programming_test(all_tests)

            # 3. Format base prompt sections
            prompt = self._create_prompt_sections(
                row["description"], self._generate_function_signature()
            )

            # 4. Add mandatory columns while preserving original ones
            result_df.at[idx, "task_id"] = idx  # Use row index as task_id
            result_df.at[idx, "test"] = test_code

            # Add context column as JSON with function name and difficulty information
            import json

            difficulty = row.get("difficulty", None)
            difficulty_labels = {1: "EASY", 2: "MEDIUM", 3: "HARD"}
            result_df.at[idx, "context"] = json.dumps(
                {
                    "function_name": "solve_problem",
                    "difficulty": int(difficulty),
                    "difficulty_label": difficulty_labels.get(
                        difficulty, f"LEVEL_{difficulty}"
                    ),
                }
            )

            # 5. Test-driven specific processing
            if test_driven:
                # Extract assertions for test-driven prompt inclusion
                test_seq = self.assertion_extractor._extract_assertions(test_code)

                # Split tests into public and private based on ratio
                test_public, test_private = (
                    self.assertion_extractor._extract_test_seq_private_public(test_seq)
                )

                # Set up data for superclass method
                result_df.at[idx, "prompt"] = prompt
                result_df.at[idx, "test_seq"] = test_seq
                result_df.at[idx, "test_public"] = test_public
                result_df.at[idx, "test_private"] = test_private

                # Use superclass method to combine prompt with visible tests
                if test_public.strip():
                    result_df.at[idx, "prompt"] = self._combine_prompt_and_test(
                        result_df.iloc[idx]
                    )
            else:
                # Regular mode - just use the base prompt
                result_df.at[idx, "prompt"] = prompt

        return result_df
