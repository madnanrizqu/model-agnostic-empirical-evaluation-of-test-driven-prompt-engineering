import subprocess
import re
from test_runner_module.strategies.common_strategies import (
    CommonLanguageBaseStrategy,
    CommonTestResultCollectionStrategy,
)
from test_runner_module.strategies_interface import (
    NonCommonConfigValidationStrategy,
    NonCommonAttributesInitiatorStrategy,
    TestExecutionStrategy,
)


class PythonPreparationStrategy(CommonLanguageBaseStrategy):
    """Preparation strategy specifically for Python code"""

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
        """Test run llm output code before execution and handle syntax errors"""
        print(f"Test run for task: {task_id}")

        stdin_validation = self._validate_stdin_usage(solution)
        if not stdin_validation["is_safe"]:
            mock_process = type(
                "obj",
                (object,),
                {
                    "stderr": f"Code contains forbidden stdin patterns: {', '.join(stdin_validation['violations'])}",
                    "stdout": "Please rewrite without sys.stdin.read(), input(), or main() functions",
                },
            )()

            self._record_prep_failure(
                runner_context=runner_context,
                process=mock_process,
                compile_status="Fail: Stdin validation",
                task_id=task_id,
                prompt=prompt,
                llm_name=llm_name,
                solution=solution,
                test_content=test_content,
                context=context,
                attempt_num=attempt_num,
            )

            return {
                "success": False,
                "fail_status": "Fail: Contains stdin usage",
                "stderr": mock_process.stderr,
                "stdout": mock_process.stdout,
            }

        llm_output_process = subprocess.run(
            [runner_context.test_runner_binary, runner_context.llm_output_file],
            cwd=runner_context.test_runner_dir,
            capture_output=True,
            text=True,
        )
        if llm_output_process.returncode != 0:
            self._record_prep_failure(
                runner_context=runner_context,
                process=llm_output_process,
                compile_status="Fail: LLM file",
                task_id=task_id,
                prompt=prompt,
                llm_name=llm_name,
                solution=solution,
                test_content=test_content,
                context=context,
                attempt_num=attempt_num,
            )
            return {
                "success": False,
                "fail_status": "Fail: LLM file",
                "stderr": llm_output_process.stderr,
                "stdout": llm_output_process.stdout,
            }

        return {"success": True}

    def _validate_stdin_usage(self, code):
        """Validate that code doesn't contain forbidden stdin usage patterns"""
        forbidden_patterns = [
            (r"sys\.stdin\.read\s*\(", "sys.stdin.read()"),
            (r"input\s*\(", "input()"),
            (r"sys\.stdin\.", "sys.stdin access"),
            (r'if\s+__name__\s*==\s*["\']__main__["\']', "main execution block"),
            (r"def\s+main\s*\(", "main() function definition"),
        ]

        violations = []
        for pattern, description in forbidden_patterns:
            if re.search(pattern, code, re.MULTILINE):
                violations.append(description)

        return {"is_safe": len(violations) == 0, "violations": violations}


class PythonTestExecutionStrategy(TestExecutionStrategy):
    """Test execution strategy specifically for Python code"""

    def execute_tests(
        self, task_id, prompt, llm_name, solution, test_content, runner_context
    ):
        """Execute tests for Python code"""
        print(f"\nProcessing task: {task_id}")
        print(f"LLM: {llm_name}")

        process = subprocess.run(
            [runner_context.test_runner_binary, runner_context.test_file],
            cwd=runner_context.test_runner_dir,
            capture_output=True,
            text=True,
        )

        return process


class PythonNonCommonConfigValidationStrategy(NonCommonConfigValidationStrategy):
    """Configuration validation strategy specific to Python"""

    @staticmethod
    def validate(config):
        """Validate configuration requirements specific to Python"""
        pass


class PythonNonCommonAttributesInitiatorStrategy(NonCommonAttributesInitiatorStrategy):
    """Attribute initialization strategy specific to Python"""

    @staticmethod
    def init(config, runner_context):
        """Initialize attributes specific to Python"""
        pass


class PythonTestResultCollectionStrategy(CommonTestResultCollectionStrategy):
    """Test collection strategy for Python programming language"""

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
        """Record and categorize the test execution result based on return codes"""
        has_test_failure = "AssertionError" in process.stderr

        self.save_result(
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
        )
