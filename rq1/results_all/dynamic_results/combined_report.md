# Combined Analysis Report

Generated: 2025-08-10 16:42:29

**LLMs:** Multiple (6 models) | **Research Question:** rq2

## Summary (First Attempt Only)

Total comparisons: 15

* Test-driven (TD) results were better in 11 out of 15 comparisons (73.3%)
* Test-driven (TD) results were same in 4 out of 15 comparisons (26.7%)
* Test-driven (TD) results were worse in 0 out of 15 comparisons (0.0%)

### Accuracy Statistics

* Total increase: 335.00
* Average increase: 22.33 (95% CI: [12.97, 31.70])
* Median increase: 25.00
* Standard deviation: 18.50
* Range: 0.00 to 60.00
* Interquartile range: 0.00 to 30.00
* Benchmarks improved: 11 (73.3%)
* Benchmarks worsened: 0 (0.0%)
* Benchmarks unchanged: 4 (26.7%)
* Average improvement percentage: 73.38%

#### Top 5 Increases

* mbpp_sanitized_chatgpt4o: 40.00 → 100.00 (change: +60.00)
* mbpp_sanitized_qwen25coder32b: 30.00 → 80.00 (change: +50.00)
* mbpp_sanitized_qwen257b: 40.00 → 80.00 (change: +40.00)
* code_contests_claude35sonnet: 0.00 → 30.00 (change: +30.00)
* mbpp_sanitized_claude35sonnet: 70.00 → 100.00 (change: +30.00)

#### Top 5 Regressions

* code_contests_qwen25coder32b: 0.00 → 0.00 (change: +0.00)
* human_eval_chatgpt4o: 100.00 → 100.00 (change: +0.00)
* human_eval_claude35haiku: 100.00 → 100.00 (change: +0.00)
* human_eval_qwen257b: 100.00 → 100.00 (change: +0.00)
* mbpp_sanitized_chatgpt4omini: 70.00 → 80.00 (change: +10.00)

## Summary (With Remediation)

Total comparisons: 15

* Test-driven (TD) results were better in 6 out of 15 comparisons (40.0%)
* Test-driven (TD) results were same in 9 out of 15 comparisons (60.0%)
* Test-driven (TD) results were worse in 0 out of 15 comparisons (0.0%)

### Accuracy Statistics (With Remediation)

* Total increase: 120.00
* Average increase: 8.00 (95% CI: [0.79, 15.21])
* Median increase: 0.00
* Standard deviation: 14.24
* Range: 0.00 to 50.00
* Interquartile range: 0.00 to 10.00
* Benchmarks improved: 6 (40.0%)
* Benchmarks worsened: 0 (0.0%)
* Benchmarks unchanged: 9 (60.0%)
* Average improvement percentage: 48.02%

#### Top 5 Increases (With Remediation)

* mbpp_sanitized_qwen25coder32b: 30.00 → 80.00 (change: +50.00)
* mbpp_sanitized_chatgpt4omini: 70.00 → 100.00 (change: +30.00)
* code_contests_chatgpt4o: 20.00 → 30.00 (change: +10.00)
* code_contests_claude35sonnet: 70.00 → 80.00 (change: +10.00)
* code_contests_qwen25coder32b: 0.00 → 10.00 (change: +10.00)

#### Top 5 Regressions (With Remediation)

* human_eval_chatgpt4o: 100.00 → 100.00 (change: +0.00)
* human_eval_chatgpt4omini: 100.00 → 100.00 (change: +0.00)
* human_eval_claude35haiku: 100.00 → 100.00 (change: +0.00)
* human_eval_claude35sonnet: 100.00 → 100.00 (change: +0.00)
* human_eval_qwen257b: 100.00 → 100.00 (change: +0.00)

## Detailed Comparisons (First Attempt Only)

### code_contests_chatgpt4o vs code_contests_chatgpt4o_td

Accuracy comparison: **TD is better** - 30.00 vs 10.00

Test counts:
* Base: {'success': 1, 'fail': 8, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 3, 'fail': 5, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* Difference: {'success': 2, 'fail': -3, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 4.0
* task_id: 6.0

---

### code_contests_claude35sonnet vs code_contests_claude35sonnet_td

Accuracy comparison: **TD is better** - 30.00 vs 0.00

Test counts:
* Base: {'success': 0, 'fail': 5, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* TD: {'success': 3, 'fail': 2, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* Difference: {'success': 3, 'fail': -3, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2.0
* task_id: 3.0
* task_id: 5.0

---

### code_contests_qwen25coder32b vs code_contests_qwen25coder32b_td

Accuracy comparison: **TD is same** - 0.00 vs 0.00

Test counts:
* Base: {'success': 0, 'fail': 8, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 0, 'fail': 5, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* Difference: {'success': 0, 'fail': -3, 'error': 3, 'generation_errors': 0, 'test_errors': 3}

---

### human_eval_chatgpt4o vs human_eval_chatgpt4o_td

Accuracy comparison: **TD is same** - 100.00 vs 100.00

Test counts:
* Base: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 0, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

---

### human_eval_chatgpt4omini vs human_eval_chatgpt4omini_td

Accuracy comparison: **TD is better** - 100.00 vs 75.00

Test counts:
* Base: {'success': 3, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 1, 'fail': -1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2

---

### human_eval_claude35haiku vs human_eval_claude35haiku_td

Accuracy comparison: **TD is same** - 100.00 vs 100.00

Test counts:
* Base: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 0, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

---

### human_eval_claude35sonnet vs human_eval_claude35sonnet_td

Accuracy comparison: **TD is better** - 100.00 vs 75.00

Test counts:
* Base: {'success': 3, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 1, 'fail': -1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2

---

### human_eval_qwen257b vs human_eval_qwen257b_td

Accuracy comparison: **TD is same** - 100.00 vs 100.00

Test counts:
* Base: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 0, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

---

### human_eval_qwen25coder32b vs human_eval_qwen25coder32b_td

Accuracy comparison: **TD is better** - 100.00 vs 75.00

Test counts:
* Base: {'success': 3, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 1, 'fail': -1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2

---

### mbpp_sanitized_chatgpt4o vs mbpp_sanitized_chatgpt4o_td

Accuracy comparison: **TD is better** - 100.00 vs 40.00

Test counts:
* Base: {'success': 4, 'fail': 5, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 10, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 6, 'fail': -5, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 4
* task_id: 6
* task_id: 7
* task_id: 8
* task_id: 12

---

### mbpp_sanitized_chatgpt4omini vs mbpp_sanitized_chatgpt4omini_td

Accuracy comparison: **TD is better** - 80.00 vs 70.00

Test counts:
* Base: {'success': 7, 'fail': 2, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 8, 'fail': 0, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* Difference: {'success': 1, 'fail': -2, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 6
* task_id: 14

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 9

---

### mbpp_sanitized_claude35haiku vs mbpp_sanitized_claude35haiku_td

Accuracy comparison: **TD is better** - 80.00 vs 60.00

Test counts:
* Base: {'success': 6, 'fail': 3, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 8, 'fail': 2, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 2, 'fail': -1, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 3
* task_id: 6

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 8

---

### mbpp_sanitized_claude35sonnet vs mbpp_sanitized_claude35sonnet_td

Accuracy comparison: **TD is better** - 100.00 vs 70.00

Test counts:
* Base: {'success': 7, 'fail': 2, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 10, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 3, 'fail': -2, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 4
* task_id: 6

---

### mbpp_sanitized_qwen257b vs mbpp_sanitized_qwen257b_td

Accuracy comparison: **TD is better** - 80.00 vs 40.00

Test counts:
* Base: {'success': 4, 'fail': 5, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 8, 'fail': 1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 4, 'fail': -4, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 4
* task_id: 9
* task_id: 11
* task_id: 14

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 7

---

### mbpp_sanitized_qwen25coder32b vs mbpp_sanitized_qwen25coder32b_td

Accuracy comparison: **TD is better** - 80.00 vs 30.00

Test counts:
* Base: {'success': 3, 'fail': 6, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 8, 'fail': 1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 5, 'fail': -5, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 4
* task_id: 7
* task_id: 9
* task_id: 12

---

## Detailed Comparisons (With Remediation)

### code_contests_chatgpt4o vs code_contests_chatgpt4o_td

Accuracy comparison (with remediation): **TD is better** - 30.00 vs 20.00

Test counts (with remediation):
* Base: {'success': 2, 'fail': 7, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 3, 'fail': 5, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* Difference: {'success': 1, 'fail': -2, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 4.0
* task_id: 6.0

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 0.0

---

### code_contests_claude35sonnet vs code_contests_claude35sonnet_td

Accuracy comparison (with remediation): **TD is better** - 80.00 vs 70.00

Test counts (with remediation):
* Base: {'success': 7, 'fail': 2, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* TD: {'success': 8, 'fail': 1, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* Difference: {'success': 1, 'fail': -1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2.0
* task_id: 7.0

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 0.0

---

### code_contests_qwen25coder32b vs code_contests_qwen25coder32b_td

Accuracy comparison (with remediation): **TD is better** - 10.00 vs 0.00

Test counts (with remediation):
* Base: {'success': 0, 'fail': 8, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 1, 'fail': 4, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* Difference: {'success': 1, 'fail': -4, 'error': 3, 'generation_errors': 0, 'test_errors': 3}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 4.0

---

### human_eval_chatgpt4o vs human_eval_chatgpt4o_td

Accuracy comparison (with remediation): **TD is same** - 100.00 vs 100.00

Test counts (with remediation):
* Base: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 0, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

---

### human_eval_chatgpt4omini vs human_eval_chatgpt4omini_td

Accuracy comparison (with remediation): **TD is same** - 100.00 vs 100.00

Test counts (with remediation):
* Base: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 0, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

---

### human_eval_claude35haiku vs human_eval_claude35haiku_td

Accuracy comparison (with remediation): **TD is same** - 100.00 vs 100.00

Test counts (with remediation):
* Base: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 0, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

---

### human_eval_claude35sonnet vs human_eval_claude35sonnet_td

Accuracy comparison (with remediation): **TD is same** - 100.00 vs 100.00

Test counts (with remediation):
* Base: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 0, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

---

### human_eval_qwen257b vs human_eval_qwen257b_td

Accuracy comparison (with remediation): **TD is same** - 100.00 vs 100.00

Test counts (with remediation):
* Base: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 0, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

---

### human_eval_qwen25coder32b vs human_eval_qwen25coder32b_td

Accuracy comparison (with remediation): **TD is same** - 100.00 vs 100.00

Test counts (with remediation):
* Base: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 4, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 0, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

---

### mbpp_sanitized_chatgpt4o vs mbpp_sanitized_chatgpt4o_td

Accuracy comparison (with remediation): **TD is same** - 100.00 vs 100.00

Test counts (with remediation):
* Base: {'success': 10, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 10, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 0, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

---

### mbpp_sanitized_chatgpt4omini vs mbpp_sanitized_chatgpt4omini_td

Accuracy comparison (with remediation): **TD is better** - 100.00 vs 70.00

Test counts (with remediation):
* Base: {'success': 7, 'fail': 2, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 10, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 3, 'fail': -2, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 6
* task_id: 14

---

### mbpp_sanitized_claude35haiku vs mbpp_sanitized_claude35haiku_td

Accuracy comparison (with remediation): **TD is same** - 100.00 vs 100.00

Test counts (with remediation):
* Base: {'success': 10, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 10, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 0, 'fail': -1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

---

### mbpp_sanitized_claude35sonnet vs mbpp_sanitized_claude35sonnet_td

Accuracy comparison (with remediation): **TD is same** - 100.00 vs 100.00

Test counts (with remediation):
* Base: {'success': 10, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 10, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 0, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

---

### mbpp_sanitized_qwen257b vs mbpp_sanitized_qwen257b_td

Accuracy comparison (with remediation): **TD is better** - 80.00 vs 70.00

Test counts (with remediation):
* Base: {'success': 7, 'fail': 4, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 8, 'fail': 1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 1, 'fail': -3, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 4
* task_id: 9

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 6
* task_id: 7

---

### mbpp_sanitized_qwen25coder32b vs mbpp_sanitized_qwen25coder32b_td

Accuracy comparison (with remediation): **TD is better** - 80.00 vs 30.00

Test counts (with remediation):
* Base: {'success': 3, 'fail': 6, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 8, 'fail': 1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 5, 'fail': -5, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 4
* task_id: 7
* task_id: 9
* task_id: 12

---

## Incomplete Directories Analysis

**Completion Status:** 15/15 directories (100.0%)

🎉 **All directories are complete!** No re-execution needed.

## Experiment Metadata

**LLM Configuration:**
- Configuration Keys: CHATGPT_4O, CHATGPT_4O_MINI, CLAUDE_35_HAIKU, CLAUDE_35_SONNET, QWEN_2_5_7B, QWEN_2_5_CODER_32B
- Model Name: openai/gpt-4o-2024-11-20
**Dataset Configuration:**
- Research Question: rq2
- Dataset Coverage: 0.025 (2.5% of problems)
- Total Problems Across All Datasets: 995
- Total Problems Tested: 24
- Datasets:
  * code_contests: 404 problems (10 tested)
  * human_eval: 164 problems (4 tested)
  * mbpp_sanitized: 427 problems (10 tested)

