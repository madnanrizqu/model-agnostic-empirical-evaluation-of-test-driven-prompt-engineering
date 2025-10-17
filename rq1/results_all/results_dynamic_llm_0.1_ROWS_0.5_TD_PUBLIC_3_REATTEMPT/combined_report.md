# Combined Analysis Report

Generated: 2025-08-14 07:45:21

**LLMs:** Multiple (6 models) | **Research Question:** rq2

## Summary (First Attempt Only)

Total comparisons: 15

* Test-driven (TD) results were better in 11 out of 15 comparisons (73.3%)
* Test-driven (TD) results were same in 2 out of 15 comparisons (13.3%)
* Test-driven (TD) results were worse in 2 out of 15 comparisons (13.3%)

### Accuracy Statistics

* Total increase: 167.39
* Average increase: 11.16 (95% CI: [-0.60, 22.92])
* Median increase: 11.91
* Standard deviation: 23.24
* Range: -43.75 to 47.62
* Interquartile range: 0.00 to 30.95
* Benchmarks improved: 11 (73.3%)
* Benchmarks worsened: 2 (13.3%)
* Benchmarks unchanged: 2 (13.3%)
* Average improvement percentage: 73.19%
* Average regression percentage: -34.38%

#### Top 5 Increases

* mbpp_sanitized_chatgpt4o: 45.24 → 92.86 (change: +47.62)
* mbpp_sanitized_qwen25coder32b: 23.81 → 57.14 (change: +33.33)
* human_eval_chatgpt4o: 68.75 → 100.00 (change: +31.25)
* mbpp_sanitized_chatgpt4omini: 38.10 → 69.05 (change: +30.95)
* code_contests_claude35sonnet: 12.50 → 37.50 (change: +25.00)

#### Top 5 Regressions

* human_eval_claude35haiku: 100.00 → 56.25 (change: -43.75)
* human_eval_claude35sonnet: 100.00 → 75.00 (change: -25.00)
* code_contests_qwen25coder32b: 22.50 → 22.50 (change: +0.00)
* human_eval_qwen25coder32b: 87.50 → 87.50 (change: +0.00)
* human_eval_chatgpt4omini: 87.50 → 93.75 (change: +6.25)

## Summary (With Remediation)

Total comparisons: 15

* Test-driven (TD) results were better in 9 out of 15 comparisons (60.0%)
* Test-driven (TD) results were same in 2 out of 15 comparisons (13.3%)
* Test-driven (TD) results were worse in 4 out of 15 comparisons (26.7%)

### Accuracy Statistics (With Remediation)

* Total increase: 90.61
* Average increase: 6.04 (95% CI: [0.97, 11.11])
* Median increase: 6.25
* Standard deviation: 10.02
* Range: -6.25 to 23.81
* Interquartile range: -2.50 to 11.91
* Benchmarks improved: 9 (60.0%)
* Benchmarks worsened: 4 (26.7%)
* Benchmarks unchanged: 2 (13.3%)
* Average improvement percentage: 25.94%
* Average regression percentage: -6.61%

#### Top 5 Increases (With Remediation)

* mbpp_sanitized_chatgpt4omini: 61.90 → 85.71 (change: +23.81)
* mbpp_sanitized_qwen25coder32b: 45.24 → 69.05 (change: +23.81)
* code_contests_chatgpt4o: 20.00 → 35.00 (change: +15.00)
* mbpp_sanitized_claude35sonnet: 85.71 → 97.62 (change: +11.91)
* mbpp_sanitized_qwen25coder7b: 57.14 → 69.05 (change: +11.91)

#### Top 5 Regressions (With Remediation)

* human_eval_chatgpt4omini: 100.00 → 93.75 (change: -6.25)
* human_eval_claude35haiku: 100.00 → 93.75 (change: -6.25)
* human_eval_qwen25coder32b: 100.00 → 93.75 (change: -6.25)
* code_contests_qwen25coder32b: 32.50 → 30.00 (change: -2.50)
* human_eval_chatgpt4o: 100.00 → 100.00 (change: +0.00)

## Detailed Comparisons (First Attempt Only)

### code_contests_chatgpt4o vs code_contests_chatgpt4o_td

Accuracy comparison: **TD is better** - 25.00 vs 10.00

Test counts:
* Base: {'success': 4, 'fail': 34, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* TD: {'success': 10, 'fail': 23, 'error': 7, 'generation_errors': 0, 'test_errors': 7}
* Difference: {'success': 6, 'fail': -11, 'error': 5, 'generation_errors': 0, 'test_errors': 5}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 1.0
* task_id: 3.0
* task_id: 4.0
* task_id: 10.0
* task_id: 24.0
* task_id: 30.0
* task_id: 38.0

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 23.0

---

### code_contests_claude35sonnet vs code_contests_claude35sonnet_td

Accuracy comparison: **TD is better** - 37.50 vs 12.50

Test counts:
* Base: {'success': 5, 'fail': 19, 'error': 11, 'generation_errors': 0, 'test_errors': 11}
* TD: {'success': 15, 'fail': 11, 'error': 11, 'generation_errors': 0, 'test_errors': 11}
* Difference: {'success': 10, 'fail': -8, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2.0
* task_id: 3.0
* task_id: 4.0
* task_id: 5.0
* task_id: 6.0
* task_id: 15.0
* task_id: 24.0
* task_id: 26.0
* task_id: 30.0
* task_id: 34.0
* task_id: 35.0
* task_id: 36.0
* task_id: 38.0

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 10.0
* task_id: 22.0
* task_id: 32.0

---

### code_contests_qwen25coder32b vs code_contests_qwen25coder32b_td

Accuracy comparison: **TD is same** - 22.50 vs 22.50

Test counts:
* Base: {'success': 9, 'fail': 25, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* TD: {'success': 9, 'fail': 22, 'error': 5, 'generation_errors': 0, 'test_errors': 5}
* Difference: {'success': 0, 'fail': -3, 'error': 2, 'generation_errors': 0, 'test_errors': 2}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 0.0
* task_id: 1.0
* task_id: 24.0
* task_id: 26.0
* task_id: 38.0
* task_id: 39.0

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 15.0
* task_id: 19.0
* task_id: 22.0
* task_id: 29.0
* task_id: 32.0
* task_id: 34.0

---

### human_eval_chatgpt4o vs human_eval_chatgpt4o_td

Accuracy comparison: **TD is better** - 100.00 vs 68.75

Test counts:
* Base: {'success': 11, 'fail': 5, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 16, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 5, 'fail': -5, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 6
* task_id: 7
* task_id: 8
* task_id: 9
* task_id: 12

---

### human_eval_chatgpt4omini vs human_eval_chatgpt4omini_td

Accuracy comparison: **TD is better** - 93.75 vs 87.50

Test counts:
* Base: {'success': 14, 'fail': 1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 15, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 1, 'fail': 0, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 9

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 10

---

### human_eval_claude35haiku vs human_eval_claude35haiku_td

Accuracy comparison: **TD is worse** - 56.25 vs 100.00

Test counts:
* Base: {'success': 16, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 9, 'fail': 6, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': -7, 'fail': 6, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 2
* task_id: 4
* task_id: 5
* task_id: 7
* task_id: 10
* task_id: 12
* task_id: 14

---

### human_eval_claude35sonnet vs human_eval_claude35sonnet_td

Accuracy comparison: **TD is worse** - 75.00 vs 100.00

Test counts:
* Base: {'success': 16, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 12, 'fail': 4, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': -4, 'fail': 4, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 0
* task_id: 1
* task_id: 7
* task_id: 15

---

### human_eval_qwen25coder32b vs human_eval_qwen25coder32b_td

Accuracy comparison: **TD is same** - 87.50 vs 87.50

Test counts:
* Base: {'success': 14, 'fail': 2, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 14, 'fail': 2, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 0, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 8

---

### human_eval_qwen25coder7b vs human_eval_qwen25coder7b_td

Accuracy comparison: **TD is better** - 93.75 vs 87.50

Test counts:
* Base: {'success': 14, 'fail': 2, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 15, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 1, 'fail': -1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2

---

### mbpp_sanitized_chatgpt4o vs mbpp_sanitized_chatgpt4o_td

Accuracy comparison: **TD is better** - 92.86 vs 45.24

Test counts:
* Base: {'success': 19, 'fail': 20, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* TD: {'success': 39, 'fail': 2, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 20, 'fail': -18, 'error': -2, 'generation_errors': 0, 'test_errors': -2}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 4
* task_id: 6
* task_id: 7
* task_id: 8
* task_id: 18
* task_id: 19
* task_id: 20
* task_id: 57
* task_id: 59
* task_id: 64
* task_id: 66
* task_id: 67
* task_id: 68
* task_id: 70
* task_id: 71
* task_id: 72
* task_id: 74
* task_id: 77
* task_id: 84

---

### mbpp_sanitized_chatgpt4omini vs mbpp_sanitized_chatgpt4omini_td

Accuracy comparison: **TD is better** - 69.05 vs 38.10

Test counts:
* Base: {'success': 16, 'fail': 21, 'error': 5, 'generation_errors': 0, 'test_errors': 5}
* TD: {'success': 29, 'fail': 10, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* Difference: {'success': 13, 'fail': -11, 'error': -2, 'generation_errors': 0, 'test_errors': -2}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 3
* task_id: 6
* task_id: 14
* task_id: 18
* task_id: 57
* task_id: 58
* task_id: 61
* task_id: 63
* task_id: 65
* task_id: 68
* task_id: 69
* task_id: 74
* task_id: 82
* task_id: 85
* task_id: 86

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 17
* task_id: 75
* task_id: 84

---

### mbpp_sanitized_claude35haiku vs mbpp_sanitized_claude35haiku_td

Accuracy comparison: **TD is better** - 66.67 vs 59.52

Test counts:
* Base: {'success': 25, 'fail': 10, 'error': 7, 'generation_errors': 0, 'test_errors': 7}
* TD: {'success': 28, 'fail': 11, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* Difference: {'success': 3, 'fail': 1, 'error': -4, 'generation_errors': 0, 'test_errors': -4}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 6
* task_id: 8
* task_id: 18
* task_id: 63
* task_id: 68
* task_id: 71
* task_id: 82

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 11
* task_id: 58
* task_id: 72
* task_id: 77
* task_id: 85

---

### mbpp_sanitized_claude35sonnet vs mbpp_sanitized_claude35sonnet_td

Accuracy comparison: **TD is better** - 80.95 vs 59.52

Test counts:
* Base: {'success': 25, 'fail': 13, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* TD: {'success': 34, 'fail': 4, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* Difference: {'success': 9, 'fail': -9, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 4
* task_id: 6
* task_id: 57
* task_id: 59
* task_id: 61
* task_id: 63
* task_id: 72
* task_id: 74
* task_id: 75
* task_id: 80
* task_id: 86

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 12
* task_id: 58
* task_id: 84

---

### mbpp_sanitized_qwen25coder32b vs mbpp_sanitized_qwen25coder32b_td

Accuracy comparison: **TD is better** - 57.14 vs 23.81

Test counts:
* Base: {'success': 10, 'fail': 27, 'error': 5, 'generation_errors': 0, 'test_errors': 5}
* TD: {'success': 24, 'fail': 14, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* Difference: {'success': 14, 'fail': -13, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 7
* task_id: 16
* task_id: 19
* task_id: 20
* task_id: 58
* task_id: 59
* task_id: 62
* task_id: 68
* task_id: 69
* task_id: 71
* task_id: 72
* task_id: 75
* task_id: 77
* task_id: 79
* task_id: 82
* task_id: 85

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 57
* task_id: 86

---

### mbpp_sanitized_qwen25coder7b vs mbpp_sanitized_qwen25coder7b_td

Accuracy comparison: **TD is better** - 69.05 vs 57.14

Test counts:
* Base: {'success': 24, 'fail': 16, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* TD: {'success': 29, 'fail': 10, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* Difference: {'success': 5, 'fail': -6, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 7
* task_id: 19
* task_id: 59
* task_id: 68
* task_id: 70
* task_id: 79
* task_id: 84
* task_id: 86

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 63
* task_id: 64
* task_id: 69

---

## Detailed Comparisons (With Remediation)

### code_contests_chatgpt4o vs code_contests_chatgpt4o_td

Accuracy comparison (with remediation): **TD is better** - 35.00 vs 20.00

Test counts (with remediation):
* Base: {'success': 8, 'fail': 31, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 14, 'fail': 25, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 6, 'fail': -6, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 1.0
* task_id: 5.0
* task_id: 6.0
* task_id: 10.0
* task_id: 22.0
* task_id: 24.0
* task_id: 36.0

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 23.0

---

### code_contests_claude35sonnet vs code_contests_claude35sonnet_td

Accuracy comparison (with remediation): **TD is better** - 50.00 vs 47.50

Test counts (with remediation):
* Base: {'success': 19, 'fail': 11, 'error': 10, 'generation_errors': 0, 'test_errors': 10}
* TD: {'success': 20, 'fail': 10, 'error': 10, 'generation_errors': 0, 'test_errors': 10}
* Difference: {'success': 1, 'fail': -1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2.0
* task_id: 13.0
* task_id: 24.0
* task_id: 35.0
* task_id: 36.0

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 10.0
* task_id: 25.0
* task_id: 31.0
* task_id: 32.0

---

### code_contests_qwen25coder32b vs code_contests_qwen25coder32b_td

Accuracy comparison (with remediation): **TD is worse** - 30.00 vs 32.50

Test counts (with remediation):
* Base: {'success': 13, 'fail': 22, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* TD: {'success': 12, 'fail': 20, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* Difference: {'success': -1, 'fail': -2, 'error': 2, 'generation_errors': 0, 'test_errors': 2}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 0.0
* task_id: 1.0
* task_id: 4.0
* task_id: 8.0
* task_id: 24.0
* task_id: 26.0
* task_id: 38.0
* task_id: 39.0

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 5.0
* task_id: 14.0
* task_id: 15.0
* task_id: 22.0
* task_id: 28.0
* task_id: 29.0
* task_id: 31.0
* task_id: 32.0
* task_id: 34.0

---

### human_eval_chatgpt4o vs human_eval_chatgpt4o_td

Accuracy comparison (with remediation): **TD is same** - 100.00 vs 100.00

Test counts (with remediation):
* Base: {'success': 16, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 16, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 0, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

---

### human_eval_chatgpt4omini vs human_eval_chatgpt4omini_td

Accuracy comparison (with remediation): **TD is worse** - 93.75 vs 100.00

Test counts (with remediation):
* Base: {'success': 16, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 15, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': -1, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 10

---

### human_eval_claude35haiku vs human_eval_claude35haiku_td

Accuracy comparison (with remediation): **TD is worse** - 93.75 vs 100.00

Test counts (with remediation):
* Base: {'success': 16, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 15, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': -1, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 10

---

### human_eval_claude35sonnet vs human_eval_claude35sonnet_td

Accuracy comparison (with remediation): **TD is same** - 100.00 vs 100.00

Test counts (with remediation):
* Base: {'success': 16, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 16, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 0, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

---

### human_eval_qwen25coder32b vs human_eval_qwen25coder32b_td

Accuracy comparison (with remediation): **TD is worse** - 93.75 vs 100.00

Test counts (with remediation):
* Base: {'success': 16, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 15, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': -1, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 10

---

### human_eval_qwen25coder7b vs human_eval_qwen25coder7b_td

Accuracy comparison (with remediation): **TD is better** - 93.75 vs 87.50

Test counts (with remediation):
* Base: {'success': 14, 'fail': 2, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 15, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 1, 'fail': -1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2

---

### mbpp_sanitized_chatgpt4o vs mbpp_sanitized_chatgpt4o_td

Accuracy comparison (with remediation): **TD is better** - 95.24 vs 88.10

Test counts (with remediation):
* Base: {'success': 37, 'fail': 3, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* TD: {'success': 40, 'fail': 1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 3, 'fail': -2, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 18
* task_id: 20
* task_id: 67
* task_id: 84

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 83

---

### mbpp_sanitized_chatgpt4omini vs mbpp_sanitized_chatgpt4omini_td

Accuracy comparison (with remediation): **TD is better** - 85.71 vs 61.90

Test counts (with remediation):
* Base: {'success': 26, 'fail': 14, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* TD: {'success': 36, 'fail': 5, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 10, 'fail': -9, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 3
* task_id: 6
* task_id: 14
* task_id: 57
* task_id: 59
* task_id: 61
* task_id: 63
* task_id: 68
* task_id: 74

---

### mbpp_sanitized_claude35haiku vs mbpp_sanitized_claude35haiku_td

Accuracy comparison (with remediation): **TD is better** - 88.10 vs 78.57

Test counts (with remediation):
* Base: {'success': 33, 'fail': 5, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* TD: {'success': 37, 'fail': 3, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* Difference: {'success': 4, 'fail': -2, 'error': -2, 'generation_errors': 0, 'test_errors': -2}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 57
* task_id: 63
* task_id: 70

---

### mbpp_sanitized_claude35sonnet vs mbpp_sanitized_claude35sonnet_td

Accuracy comparison (with remediation): **TD is better** - 97.62 vs 85.71

Test counts (with remediation):
* Base: {'success': 36, 'fail': 4, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* TD: {'success': 41, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 5, 'fail': -3, 'error': -2, 'generation_errors': 0, 'test_errors': -2}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 56
* task_id: 57
* task_id: 63
* task_id: 86
* task_id: 87

---

### mbpp_sanitized_qwen25coder32b vs mbpp_sanitized_qwen25coder32b_td

Accuracy comparison (with remediation): **TD is better** - 69.05 vs 45.24

Test counts (with remediation):
* Base: {'success': 19, 'fail': 19, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* TD: {'success': 29, 'fail': 11, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* Difference: {'success': 10, 'fail': -8, 'error': -2, 'generation_errors': 0, 'test_errors': -2}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 4
* task_id: 6
* task_id: 7
* task_id: 16
* task_id: 17
* task_id: 20
* task_id: 59
* task_id: 62
* task_id: 66
* task_id: 68
* task_id: 69
* task_id: 71

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 57
* task_id: 83
* task_id: 86

---

### mbpp_sanitized_qwen25coder7b vs mbpp_sanitized_qwen25coder7b_td

Accuracy comparison (with remediation): **TD is better** - 69.05 vs 57.14

Test counts (with remediation):
* Base: {'success': 24, 'fail': 17, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 29, 'fail': 11, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* Difference: {'success': 5, 'fail': -6, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 7
* task_id: 19
* task_id: 59
* task_id: 68
* task_id: 70
* task_id: 79
* task_id: 84
* task_id: 86

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 63
* task_id: 64
* task_id: 69

---

## Incomplete Directories Analysis

**Completion Status:** 15/15 directories (100.0%)

🎉 **All directories are complete!** No re-execution needed.

## Experiment Metadata

**LLM Configuration:**
- Configuration Keys: CHATGPT_4O, CHATGPT_4O_MINI, CLAUDE_35_HAIKU, CLAUDE_35_SONNET, QWEN_2_5_CODER_32B, QWEN_7B_CODER
- Model Name: openai/gpt-4o-2024-11-20
**Dataset Configuration:**
- Research Question: rq2
- Dataset Coverage: 0.1 (10.0% of problems)
- Total Problems Across All Datasets: 995
- Total Problems Tested: 98
- Datasets:
  * code_contests: 404 problems (40 tested)
  * human_eval: 164 problems (16 tested)
  * mbpp_sanitized: 427 problems (42 tested)

