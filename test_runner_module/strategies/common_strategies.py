from test_runner_module.strategies_interface import (
    CodePreparationStrategy,
    TestResultCollectionStrategy,
)


class CommonLanguageBaseStrategy(CodePreparationStrategy):
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
        print(f"Compile {compile_status}")

        fail_data = {
            "task_id": task_id,
            "prompt": prompt,
            "llm_name": llm_name,
            "error": process.stderr + process.stdout,
            "solution": solution,
            "test_content": test_content,
            "context": context,
            "attempt_num": attempt_num,
        }

        if "Fail" in compile_status:
            if llm_name not in runner_context.fails:
                runner_context.fails[llm_name] = []
            runner_context.fails[llm_name].append(fail_data)
        elif "Error" in compile_status:
            if llm_name not in runner_context.errors:
                runner_context.errors[llm_name] = []
            runner_context.errors[llm_name].append(fail_data)


class CommonTestResultCollectionStrategy(TestResultCollectionStrategy):
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
        if process.returncode == 0:
            print("Passed")
            passed_data = {
                "task_id": task_id,
                "prompt": prompt,
                "llm_name": llm_name,
                "solution": solution,
                "test_content": test_content,
                "context": context,
                "attempt_num": attempt_num,
            }
            runner_context.passeds[llm_name].append(passed_data)
        elif process.returncode != 0 and has_test_failure:
            print("Fail")
            fail_data = {
                "task_id": task_id,
                "prompt": prompt,
                "llm_name": llm_name,
                "error": process.stderr + process.stdout,
                "solution": solution,
                "test_content": test_content,
                "context": context,
                "attempt_num": attempt_num,
            }
            runner_context.fails[llm_name].append(fail_data)
        elif (
            process.returncode != 0
            and process.stderr == "Fail: attempt has reached limit"
        ):
            print("Max attempt reached")
            pass
        else:
            print("Error")
            error_data = {
                "task_id": task_id,
                "prompt": prompt,
                "llm_name": llm_name,
                "error": process.stderr + process.stdout,
                "solution": solution,
                "test_content": test_content,
                "context": context,
                "attempt_num": attempt_num,
            }
            runner_context.errors[llm_name].append(error_data)
