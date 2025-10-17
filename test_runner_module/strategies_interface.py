from abc import ABC, abstractmethod


# Strategy interfaces
class CodePreparationStrategy(ABC):
    """Strategy interface for preparing code before execution"""

    @abstractmethod
    def prepare_code(
        self,
        task_id,
        prompt,
        llm_name,
        solution,
        test_content,
        context,
        runner_context,
        attempt_num,
    ):
        """Prepare code for execution and return success status"""
        pass

    @abstractmethod
    def _record_prep_failure(
        self,
        runner_context,
        process,
        compile_status,
        task_id,
        prompt,
        llm_name,
        solution,
        test_content,
        context,
        attempt_num,
    ):
        """Record compilation failures to the appropriate results collection"""
        pass


class NonCommonConfigValidationStrategy(ABC):
    """Strategy interface for validating language-specific configuration"""

    @staticmethod
    @abstractmethod
    def validate(config):
        """Validate language-specific configuration parameters"""
        pass


class NonCommonAttributesInitiatorStrategy(ABC):
    """Strategy interface for initializing language-specific attributes"""

    @staticmethod
    @abstractmethod
    def init(config, runner_context):
        """Initialize language-specific attributes in the runner context"""
        pass


class TestExecutionStrategy(ABC):
    """Strategy interface for executing tests on prepared code"""

    @abstractmethod
    def execute_tests(
        self, task_id, prompt, llm_name, solution, test_content, runner_context
    ):
        """Execute tests and return the process result"""
        pass


class TestResultCollectionStrategy(ABC):
    """Strategy interface for collecting tests results on prepared code"""

    @abstractmethod
    def record_result(
        self,
        process,
        task_id,
        prompt,
        llm_name,
        solution,
        test_content,
        context,
        runner_context,
        attempt_num,
    ):
        """Execute tests and return the process result"""
        pass

    @abstractmethod
    def save_result(
        self,
        has_test_failure,
        process,
        task_id,
        prompt,
        llm_name,
        solution,
        test_content,
        context,
        runner_context,
        attempt_num,
    ):
        """Execute tests and return the save processed result"""
        pass
