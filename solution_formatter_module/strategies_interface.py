from abc import ABC, abstractmethod


class FormattingStrategy(ABC):
    """Abstract base class for code formatting strategies"""

    @abstractmethod
    def format_code_block(
        self, code_block, start_marker, end_marker, prompt, context=None
    ):
        """Format a code block according to language-specific rules

        Args:
            code_block: The code block containing markers
            start_marker: Marker indicating where code begins
            end_marker: Marker indicating where code ends
            prompt: The original prompt text
            context: Additional context information

        Returns:
            Formatted code block
        """
        pass
