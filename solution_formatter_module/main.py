import json
from typing import Optional
from .strategies_interface import FormattingStrategy
from .strategies.python import (
    PythonFormattingStrategy,
    PythonMultiMarkerFormattingStrategy,
)


class SolutionFormatter:
    """A class for formatting code solutions by standardizing function names."""

    # Strategy registry
    _strategies = {
        "python": lambda: PythonFormattingStrategy(),
    }

    _strategies_multi_marker = {
        "python": lambda: PythonMultiMarkerFormattingStrategy(),
    }

    def __init__(
        self,
        language: str,
        start_marker: str = "===START===",
        end_marker: str = "===END===",
        use_multi_marker: bool = False,
    ):
        """
        Initialize a solution formatter for a specific language.

        Args:
            language: Programming language of the code (required)
            start_marker: Marker indicating where code begins
            end_marker: Marker indicating where code ends
        """
        self.start_marker = start_marker
        self.end_marker = end_marker

        # Get the appropriate strategy for the language
        language = language.lower()
        if language not in self._strategies:
            raise ValueError(f"Unsupported language: {language}")

        if use_multi_marker:
            self.strategy = self._strategies_multi_marker[language]()
        else:
            self.strategy = self._strategies[language]()

    def format_solution(
        self, solution: str, prompt: str, context: Optional[str] = None
    ) -> str:
        """
        Format the solution using the selected formatting strategy.

        Args:
            solution: The solution string containing code markers
            prompt: The original prompt text
            context: Additional context information

        Returns:
            Formatted code block with renamed function
        """
        return self.strategy.format_code_block(
            solution, self.start_marker, self.end_marker, prompt, context
        )

    def format_solutions_in_file(
        self, input_json_path: str, output_json_path: Optional[str] = None
    ) -> None:
        """
        Apply format_solution to all solutions in a generation results JSON file

        Args:
            input_json_path: Path to the input JSON file with generation results
            output_json_path: Path for the output file. If None, will overwrite the input file
        """
        print(f"Reading solutions from {input_json_path}")

        with open(input_json_path, "r") as f:
            solutions = json.load(f)

        print(f"Found {len(solutions)} solutions to format")

        # Apply formatting to each solution
        for i, entry in enumerate(solutions):
            original = entry["solution"]
            prompt = entry["prompt"]
            context = entry.get("context")
            task_id = entry.get("dataset_row_id", i)

            try:
                entry["solution"] = self.format_solution(original, prompt, context)
                print(
                    f"Formatted solution {i+1}/{len(solutions)} for task ID {task_id}"
                )
            except ValueError as e:
                entry["solution"] = str(e)
                print(
                    f"Error formatting solution {i+1}/{len(solutions)} for task ID {task_id}: {str(e)}"
                )

        # Determine output path
        output_path = output_json_path if output_json_path else input_json_path

        # Write the formatted solutions back to file
        with open(output_path, "w") as f:
            json.dump(solutions, f, indent=2)

        print(f"Formatted solutions written to {output_path}")
