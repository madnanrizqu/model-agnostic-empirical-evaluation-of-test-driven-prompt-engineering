import json
import os


class SummaryCalculator:
    """Standalone summary calculator that reuses TestRunner's calculation logic"""
    
    def __init__(self, max_attempt_num=5):
        self.max_attempt_num = max_attempt_num
    
    def calculate_summary(self, passeds, fails, errors, metadata=None, generation_errors=None, solutions=None):
        """Core summary calculation logic (extracted from TestRunner._generate_summary)"""
        if generation_errors is None:
            generation_errors = []
        
        # Get expected total from metadata, fallback to test execution count
        expected_total_from_metadata = (
            metadata.get("expected_total") if metadata else None
        )
        generation_errors_count = len(generation_errors)
        
        summary = {}
        for llm_name in passeds:
            # Get all passed tasks with attempt_num of 1
            first_attempt_passed = [
                item
                for item in passeds[llm_name]
                if item.get("attempt_num", 1) == 1
            ]
            pass_count = len(first_attempt_passed)
            
            # Get all failed tasks with attempt_num of 1
            first_attempt_fail = [
                item for item in fails.get(llm_name, []) if item.get("attempt_num", 1) == 1
            ]
            fail_count = len(first_attempt_fail)
            
            # Get all error tasks with attempt_num of 1
            error_attempt_fail = [
                item
                for item in errors.get(llm_name, [])
                if item.get("attempt_num", 1) == 1
            ]
            error_count = len(error_attempt_fail)
            
            # Calculate totals - use expected total from metadata if available
            test_execution_total = pass_count + fail_count + error_count
            if expected_total_from_metadata is not None:
                total = expected_total_from_metadata
                print(
                    f"Using expected total from metadata: {total} (tested: {test_execution_total}, generation_errors: {generation_errors_count})"
                )
            else:
                total = test_execution_total
                print(f"Using test execution total: {total} (no metadata available)")
            
            accuracy = (pass_count / total) * 100 if total > 0 else 0
            
            # Count unique tasks present in runner files
            passed_task_ids = set(item["task_id"] for item in passeds[llm_name])
            failed_task_ids = set(item["task_id"] for item in fails.get(llm_name, []))
            error_task_ids = set(item["task_id"] for item in errors.get(llm_name, []))
            
            # Total unique tasks that actually have runner entries
            all_runner_task_ids = passed_task_ids | failed_task_ids | error_task_ids
            unique_tasks_in_runner = len(all_runner_task_ids)
            
            # Get expected task IDs from solutions file to find missing ones
            expected_task_ids = set()
            if solutions:
                for entry in solutions:
                    if entry.get("llm_name") == llm_name:
                        expected_task_ids.add(entry["dataset_row_id"])
            
            # Find which specific tasks are missing from runner files
            missing_task_ids = sorted(list(expected_task_ids - all_runner_task_ids))
            missing_from_runner = len(missing_task_ids)
            
            summary[llm_name] = {
                "passed": pass_count,
                "failed": fail_count,
                "test_errors": error_count,
                "error": error_count,
                "generation_errors": generation_errors_count,
                "total": total,
                "accuracy": round(accuracy, 2),
                "runner_totals": {
                    "unique_tasks_in_runner": unique_tasks_in_runner,
                    "missing_from_runner": missing_from_runner,
                    "missing_task_ids": missing_task_ids,
                },
            }
            
            if self.max_attempt_num > 1:
                # Get all passed tasks with attempt_num > 1
                remediation_passed = [
                    item
                    for item in passeds[llm_name]
                    if item.get("attempt_num", 1) > 1
                ]
                pass_remediation_count = len(remediation_passed)
                
                # Calculate totals and accuracy for remediation attempts
                accuracy_remediation = (
                    ((pass_count + pass_remediation_count) / total) * 100
                    if total > 0
                    else 0
                )
                
                # Count tasks that ended up failed on the FINAL attempt
                final_failed = [
                    item
                    for item in fails.get(llm_name, [])
                    if item.get("attempt_num", 1) == self.max_attempt_num
                ]
                
                # Count tasks that ended up errored on the FINAL attempt
                final_errored = [
                    item
                    for item in errors.get(llm_name, [])
                    if item.get("attempt_num", 1) == self.max_attempt_num
                ]
                
                summary[llm_name]["remediation"] = {
                    "passed": pass_count + pass_remediation_count,
                    "failed": len(final_failed),
                    "error": len(final_errored),
                    "test_errors": len(final_errored),
                    "generation_errors": generation_errors_count,
                    "total": total,
                    "accuracy": round(accuracy_remediation, 2),
                }
        
        return summary
    
    def calculate_from_files(self, results_dir, dataset_name):
        """Load files and calculate summary using existing file structure"""
        passeds = self._load_json_file(results_dir, "runner_passed.json")
        fails = self._load_json_file(results_dir, "runner_fails.json")
        errors = self._load_json_file(results_dir, "runner_errors.json")
        metadata = self._load_json_file(results_dir, f"{dataset_name}_metadata.json")
        generation_errors = self._load_json_file(results_dir, f"{dataset_name}_errors.json")
        solutions = self._load_json_file(results_dir, f"{dataset_name}_solution.json")
        
        # Convert generation_errors from dict to list if needed
        if isinstance(generation_errors, dict):
            generation_errors = []
        if not isinstance(generation_errors, list):
            generation_errors = []
        
        return self.calculate_summary(passeds, fails, errors, metadata, generation_errors, solutions)
    
    def _load_json_file(self, results_dir, filename):
        """Load JSON file, return empty dict/list if file doesn't exist"""
        file_path = os.path.join(results_dir, filename)
        if not os.path.exists(file_path):
            return {} if filename.endswith('.json') else []
        
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {} if filename.endswith('.json') else []