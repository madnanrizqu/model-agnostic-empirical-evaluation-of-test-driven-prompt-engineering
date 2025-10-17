import re
from ..strategies_interface import FormattingStrategy
import json


class PythonFormattingStrategy(FormattingStrategy):
    def format_code_block(self, code_block, start_marker, end_marker, prompt, context):
        # Extract the code block between markers
        start_idx = code_block.find(start_marker) + len(start_marker)
        end_idx = code_block.find(end_marker)

        if start_idx == -1 - len(start_marker) or end_idx == -1:
            raise ValueError("Warning: Code markers not found in code block")

        extracted_code = code_block[start_idx:end_idx].strip()

        # Find the function definition and rename it to the context name
        # Look for function definition pattern: def function_name(
        def_match = re.search(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", extracted_code)

        if def_match and context:
            original_function_name = def_match.group(1)

            # Parse JSON context to extract function name with fallback
            try:
                context_data = json.loads(context)
                new_function_name = context_data.get(
                    "function_name", original_function_name
                )
            except (json.JSONDecodeError, TypeError):
                # Backward compatibility fallback for existing simple string contexts
                new_function_name = (
                    context.strip()
                    if isinstance(context, str)
                    else original_function_name
                )

            # Replace the function name in the code
            extracted_code = extracted_code.replace(
                f"def {original_function_name}(", f"def {new_function_name}("
            )

        return extracted_code


class PythonMultiMarkerFormattingStrategy(FormattingStrategy):
    def format_code_block(self, code_block, start_marker, end_marker, prompt, context):
        # Extract the code block between markers
        def find_code_blocks(block, s_marker, e_marker):
            start_pos = block.find(s_marker)
            if start_pos == -1:
                return -1 - len(s_marker), -1, s_marker
            start_idx = start_pos + len(s_marker)
            end_idx = block.find(e_marker, start_idx)
            return start_idx, end_idx, s_marker

        start_markers = [f"{start_marker}\n```python", start_marker, "```python"]
        end_markers = [f"```\n{end_marker}", end_marker, "\n```"]

        for i in range(min(len(start_markers), len(end_markers))):
            start_idx, end_idx, used_start = find_code_blocks(
                code_block, start_markers[i], end_markers[i]
            )

            # If this marker pair found both start and end, use it
            if start_idx != -1 - len(start_markers[i]) and end_idx != -1:
                break

        if start_idx == -1 - len(used_start) or end_idx == -1:
            raise ValueError("Warning: Code markers not found in code block")

        extracted_code = code_block[start_idx:end_idx].strip()

        # Find the function definition and rename it to the context name
        # Look for function definition pattern: def function_name(
        def_match = re.search(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", extracted_code)

        if def_match and context:
            original_function_name = def_match.group(1)

            # Parse JSON context to extract function name with fallback
            try:
                context_data = json.loads(context)
                new_function_name = context_data.get(
                    "function_name", original_function_name
                )
            except (json.JSONDecodeError, TypeError):
                # Backward compatibility fallback for existing simple string contexts
                new_function_name = (
                    context.strip()
                    if isinstance(context, str)
                    else original_function_name
                )

            # Replace the function name in the code
            extracted_code = extracted_code.replace(
                f"def {original_function_name}(", f"def {new_function_name}("
            )

        return extracted_code
