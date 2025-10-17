# Combined Analysis Report

Generated: 2025-08-16 11:35:01

**LLMs:** Multiple (6 models) | **Research Question:** rq2

## Summary (First Attempt Only)

Total comparisons: 15

* Test-driven (TD) results were better in 12 out of 15 comparisons (80.0%)
* Test-driven (TD) results were same in 1 out of 15 comparisons (6.7%)
* Test-driven (TD) results were worse in 2 out of 15 comparisons (13.3%)

### Accuracy Statistics

* Total increase: 276.64
* Average increase: 18.44 (95% CI: [9.31, 27.57])
* Median increase: 15.84
* Standard deviation: 16.49
* Range: -2.44 to 46.23
* Interquartile range: 2.43 to 31.61
* Benchmarks improved: 12 (80.0%)
* Benchmarks worsened: 2 (13.3%)
* Benchmarks unchanged: 1 (6.7%)
* Average improvement percentage: 423.37%
* Average regression percentage: -2.70%

#### Statistical Tests

* **Normality Test (Shapiro-Wilk)**: statistic=0.9290, p-value=0.2633, Normal=Yes
* **Paired t-test**: statistic=4.3320, p-value=0.0007
* **Effect Size (Cohen's d)**: 0.6244 (medium effect)
* **Interpretation**: Results are highly significant (p < 0.001)

#### Top 5 Increases

* mbpp_sanitized_chatgpt4omini: 38.68 → 84.91 (change: +46.23)
* mbpp_sanitized_chatgpt4o: 47.17 → 89.62 (change: +42.45)
* code_contests_claude35sonnet: 0.99 → 36.63 (change: +35.64)
* mbpp_sanitized_qwen25coder32b: 23.58 → 58.49 (change: +34.91)
* mbpp_sanitized_claude35sonnet: 59.43 → 87.74 (change: +28.31)

#### Top 5 Regressions

* human_eval_claude35sonnet: 92.68 → 90.24 (change: -2.44)
* human_eval_claude35haiku: 87.80 → 85.37 (change: -2.43)
* human_eval_chatgpt4omini: 90.24 → 90.24 (change: +0.00)
* human_eval_qwen25coder7b: 85.37 → 87.80 (change: +2.43)
* human_eval_qwen25coder32b: 82.93 → 85.37 (change: +2.44)

## Summary (With Remediation)

Total comparisons: 15

* Test-driven (TD) results were better in 12 out of 15 comparisons (80.0%)
* Test-driven (TD) results were same in 3 out of 15 comparisons (20.0%)
* Test-driven (TD) results were worse in 0 out of 15 comparisons (0.0%)

### Accuracy Statistics (With Remediation)

* Total increase: 134.23
* Average increase: 8.95 (95% CI: [3.09, 14.80])
* Median increase: 3.77
* Standard deviation: 10.57
* Range: 0.00 to 30.18
* Interquartile range: 1.68 to 12.64
* Benchmarks improved: 12 (80.0%)
* Benchmarks worsened: 0 (0.0%)
* Benchmarks unchanged: 3 (20.0%)
* Average improvement percentage: 38.61%

#### Statistical Tests

* **Normality Test (Shapiro-Wilk)**: statistic=0.7973, p-value=0.0034, Normal=No
* **Wilcoxon signed-rank test**: statistic=0.0000, p-value=0.0022
* **Effect Size (Cohen's d)**: 0.3363 (small effect)
* **Interpretation**: Results are very significant (p < 0.01)

#### Top 5 Increases (With Remediation)

* mbpp_sanitized_qwen25coder32b: 43.40 → 73.58 (change: +30.18)
* mbpp_sanitized_chatgpt4omini: 57.55 → 86.79 (change: +29.24)
* mbpp_sanitized_qwen25coder7b: 59.43 → 82.08 (change: +22.65)
* code_contests_qwen25coder32b: 6.93 → 22.77 (change: +15.84)
* mbpp_sanitized_chatgpt4o: 83.96 → 93.40 (change: +9.44)

#### Top 5 Regressions (With Remediation)

* human_eval_chatgpt4o: 92.68 → 92.68 (change: +0.00)
* human_eval_claude35haiku: 95.12 → 95.12 (change: +0.00)
* human_eval_claude35sonnet: 95.12 → 95.12 (change: +0.00)
* mbpp_sanitized_claude35haiku: 91.51 → 92.45 (change: +0.94)
* human_eval_qwen25coder7b: 85.37 → 87.80 (change: +2.43)

## Detailed Comparisons (First Attempt Only)

### code_contests_chatgpt4o vs code_contests_chatgpt4o_td

Accuracy comparison: **TD is better** - 27.72 vs 4.95

Test counts:
* Base: {'success': 5, 'fail': 90, 'error': 6, 'generation_errors': 0, 'test_errors': 6}
* TD: {'success': 28, 'fail': 66, 'error': 7, 'generation_errors': 0, 'test_errors': 7}
* Difference: {'success': 23, 'fail': -24, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 1.0
* task_id: 4.0
* task_id: 6.0
* task_id: 10.0
* task_id: 24.0
* task_id: 30.0
* task_id: 38.0
* task_id: 40.0
* task_id: 46.0
* task_id: 47.0
* task_id: 48.0
* task_id: 53.0
* task_id: 55.0
* task_id: 64.0
* task_id: 65.0
* task_id: 70.0
* task_id: 74.0
* task_id: 79.0
* task_id: 81.0
* task_id: 83.0
* task_id: 85.0
* task_id: 86.0
* task_id: 95.0

---

### code_contests_claude35sonnet vs code_contests_claude35sonnet_td

Accuracy comparison: **TD is better** - 36.63 vs 0.99

Test counts:
* Base: {'success': 1, 'fail': 62, 'error': 38, 'generation_errors': 0, 'test_errors': 38}
* TD: {'success': 37, 'fail': 32, 'error': 32, 'generation_errors': 0, 'test_errors': 32}
* Difference: {'success': 36, 'fail': -30, 'error': -6, 'generation_errors': 0, 'test_errors': -6}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2.0
* task_id: 3.0
* task_id: 4.0
* task_id: 5.0
* task_id: 6.0
* task_id: 14.0
* task_id: 24.0
* task_id: 26.0
* task_id: 30.0
* task_id: 34.0
* task_id: 35.0
* task_id: 36.0
* task_id: 38.0
* task_id: 40.0
* task_id: 42.0
* task_id: 43.0
* task_id: 45.0
* task_id: 47.0
* task_id: 52.0
* task_id: 53.0
* task_id: 58.0
* task_id: 62.0
* task_id: 64.0
* task_id: 65.0
* task_id: 70.0
* task_id: 74.0
* task_id: 76.0
* task_id: 79.0
* task_id: 81.0
* task_id: 83.0
* task_id: 85.0
* task_id: 86.0
* task_id: 88.0
* task_id: 90.0
* task_id: 95.0
* task_id: 96.0

---

### code_contests_qwen25coder32b vs code_contests_qwen25coder32b_td

Accuracy comparison: **TD is better** - 18.81 vs 2.97

Test counts:
* Base: {'success': 3, 'fail': 86, 'error': 12, 'generation_errors': 0, 'test_errors': 12}
* TD: {'success': 19, 'fail': 64, 'error': 18, 'generation_errors': 0, 'test_errors': 18}
* Difference: {'success': 16, 'fail': -22, 'error': 6, 'generation_errors': 0, 'test_errors': 6}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 24.0
* task_id: 30.0
* task_id: 38.0
* task_id: 46.0
* task_id: 47.0
* task_id: 48.0
* task_id: 53.0
* task_id: 58.0
* task_id: 65.0
* task_id: 71.0
* task_id: 76.0
* task_id: 79.0
* task_id: 81.0
* task_id: 85.0
* task_id: 88.0
* task_id: 94.0
* task_id: 95.0
* task_id: 96.0

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 15.0
* task_id: 86.0

---

### human_eval_chatgpt4o vs human_eval_chatgpt4o_td

Accuracy comparison: **TD is better** - 92.68 vs 78.05

Test counts:
* Base: {'success': 32, 'fail': 8, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 38, 'fail': 2, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 6, 'fail': -6, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 4
* task_id: 6
* task_id: 8
* task_id: 9
* task_id: 12
* task_id: 28

---

### human_eval_chatgpt4omini vs human_eval_chatgpt4omini_td

Accuracy comparison: **TD is same** - 90.24 vs 90.24

Test counts:
* Base: {'success': 37, 'fail': 3, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 37, 'fail': 2, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* Difference: {'success': 0, 'fail': -1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 39

---

### human_eval_claude35haiku vs human_eval_claude35haiku_td

Accuracy comparison: **TD is worse** - 85.37 vs 87.80

Test counts:
* Base: {'success': 36, 'fail': 4, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 35, 'fail': 5, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': -1, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 10

---

### human_eval_claude35sonnet vs human_eval_claude35sonnet_td

Accuracy comparison: **TD is worse** - 90.24 vs 92.68

Test counts:
* Base: {'success': 38, 'fail': 2, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 37, 'fail': 3, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': -1, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 39

---

### human_eval_qwen25coder32b vs human_eval_qwen25coder32b_td

Accuracy comparison: **TD is better** - 85.37 vs 82.93

Test counts:
* Base: {'success': 34, 'fail': 6, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 35, 'fail': 5, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 1, 'fail': -1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2

---

### human_eval_qwen25coder7b vs human_eval_qwen25coder7b_td

Accuracy comparison: **TD is better** - 87.80 vs 85.37

Test counts:
* Base: {'success': 35, 'fail': 5, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 36, 'fail': 4, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 1, 'fail': -1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2

---

### mbpp_sanitized_chatgpt4o vs mbpp_sanitized_chatgpt4o_td

Accuracy comparison: **TD is better** - 89.62 vs 47.17

Test counts:
* Base: {'success': 50, 'fail': 47, 'error': 9, 'generation_errors': 0, 'test_errors': 9}
* TD: {'success': 95, 'fail': 7, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* Difference: {'success': 45, 'fail': -40, 'error': -5, 'generation_errors': 0, 'test_errors': -5}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 4
* task_id: 6
* task_id: 8
* task_id: 18
* task_id: 19
* task_id: 20
* task_id: 57
* task_id: 58
* task_id: 63
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
* task_id: 91
* task_id: 92
* task_id: 93
* task_id: 98
* task_id: 102
* task_id: 108
* task_id: 109
* task_id: 111
* task_id: 113
* task_id: 115
* task_id: 116
* task_id: 117
* task_id: 119
* task_id: 120
* task_id: 123
* task_id: 125
* task_id: 128
* task_id: 129
* task_id: 130
* task_id: 133
* task_id: 137
* task_id: 139
* task_id: 141
* task_id: 161
* task_id: 167
* task_id: 222

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 126

---

### mbpp_sanitized_chatgpt4omini vs mbpp_sanitized_chatgpt4omini_td

Accuracy comparison: **TD is better** - 84.91 vs 38.68

Test counts:
* Base: {'success': 41, 'fail': 50, 'error': 15, 'generation_errors': 0, 'test_errors': 15}
* TD: {'success': 90, 'fail': 10, 'error': 6, 'generation_errors': 0, 'test_errors': 6}
* Difference: {'success': 49, 'fail': -40, 'error': -9, 'generation_errors': 0, 'test_errors': -9}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 3
* task_id: 6
* task_id: 14
* task_id: 19
* task_id: 57
* task_id: 58
* task_id: 59
* task_id: 61
* task_id: 63
* task_id: 68
* task_id: 69
* task_id: 70
* task_id: 74
* task_id: 75
* task_id: 77
* task_id: 79
* task_id: 82
* task_id: 85
* task_id: 89
* task_id: 91
* task_id: 92
* task_id: 98
* task_id: 100
* task_id: 101
* task_id: 102
* task_id: 109
* task_id: 113
* task_id: 115
* task_id: 117
* task_id: 120
* task_id: 125
* task_id: 129
* task_id: 130
* task_id: 133
* task_id: 135
* task_id: 137
* task_id: 139
* task_id: 142
* task_id: 145
* task_id: 162
* task_id: 163
* task_id: 165
* task_id: 166
* task_id: 168
* task_id: 171
* task_id: 172
* task_id: 222
* task_id: 224

---

### mbpp_sanitized_claude35haiku vs mbpp_sanitized_claude35haiku_td

Accuracy comparison: **TD is better** - 82.08 vs 67.92

Test counts:
* Base: {'success': 72, 'fail': 23, 'error': 11, 'generation_errors': 0, 'test_errors': 11}
* TD: {'success': 87, 'fail': 13, 'error': 6, 'generation_errors': 0, 'test_errors': 6}
* Difference: {'success': 15, 'fail': -10, 'error': -5, 'generation_errors': 0, 'test_errors': -5}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 6
* task_id: 18
* task_id: 63
* task_id: 70
* task_id: 71
* task_id: 102
* task_id: 103
* task_id: 108
* task_id: 111
* task_id: 117
* task_id: 128
* task_id: 129
* task_id: 132
* task_id: 140
* task_id: 160
* task_id: 163

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 84
* task_id: 115

---

### mbpp_sanitized_claude35sonnet vs mbpp_sanitized_claude35sonnet_td

Accuracy comparison: **TD is better** - 87.74 vs 59.43

Test counts:
* Base: {'success': 63, 'fail': 33, 'error': 10, 'generation_errors': 0, 'test_errors': 10}
* TD: {'success': 93, 'fail': 7, 'error': 6, 'generation_errors': 0, 'test_errors': 6}
* Difference: {'success': 30, 'fail': -26, 'error': -4, 'generation_errors': 0, 'test_errors': -4}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 4
* task_id: 6
* task_id: 57
* task_id: 61
* task_id: 63
* task_id: 70
* task_id: 72
* task_id: 74
* task_id: 75
* task_id: 77
* task_id: 89
* task_id: 91
* task_id: 93
* task_id: 101
* task_id: 102
* task_id: 109
* task_id: 117
* task_id: 120
* task_id: 123
* task_id: 125
* task_id: 128
* task_id: 129
* task_id: 130
* task_id: 132
* task_id: 137
* task_id: 141
* task_id: 163
* task_id: 166
* task_id: 222
* task_id: 224

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 103

---

### mbpp_sanitized_qwen25coder32b vs mbpp_sanitized_qwen25coder32b_td

Accuracy comparison: **TD is better** - 58.49 vs 23.58

Test counts:
* Base: {'success': 25, 'fail': 69, 'error': 12, 'generation_errors': 0, 'test_errors': 12}
* TD: {'success': 62, 'fail': 35, 'error': 9, 'generation_errors': 0, 'test_errors': 9}
* Difference: {'success': 37, 'fail': -34, 'error': -3, 'generation_errors': 0, 'test_errors': -3}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 4
* task_id: 7
* task_id: 9
* task_id: 16
* task_id: 19
* task_id: 20
* task_id: 58
* task_id: 59
* task_id: 68
* task_id: 71
* task_id: 72
* task_id: 74
* task_id: 75
* task_id: 77
* task_id: 79
* task_id: 82
* task_id: 84
* task_id: 85
* task_id: 91
* task_id: 92
* task_id: 95
* task_id: 102
* task_id: 105
* task_id: 106
* task_id: 108
* task_id: 113
* task_id: 116
* task_id: 117
* task_id: 119
* task_id: 120
* task_id: 128
* task_id: 129
* task_id: 130
* task_id: 132
* task_id: 133
* task_id: 137
* task_id: 160
* task_id: 222

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 86
* task_id: 135

---

### mbpp_sanitized_qwen25coder7b vs mbpp_sanitized_qwen25coder7b_td

Accuracy comparison: **TD is better** - 81.13 vs 59.43

Test counts:
* Base: {'success': 63, 'fail': 35, 'error': 8, 'generation_errors': 0, 'test_errors': 8}
* TD: {'success': 86, 'fail': 14, 'error': 6, 'generation_errors': 0, 'test_errors': 6}
* Difference: {'success': 23, 'fail': -21, 'error': -2, 'generation_errors': 0, 'test_errors': -2}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 19
* task_id: 59
* task_id: 68
* task_id: 70
* task_id: 79
* task_id: 84
* task_id: 86
* task_id: 89
* task_id: 91
* task_id: 99
* task_id: 100
* task_id: 101
* task_id: 123
* task_id: 127
* task_id: 128
* task_id: 130
* task_id: 131
* task_id: 133
* task_id: 135
* task_id: 137
* task_id: 160
* task_id: 162
* task_id: 166
* task_id: 167
* task_id: 222

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 63
* task_id: 69

---

## Detailed Comparisons (With Remediation)

### code_contests_chatgpt4o vs code_contests_chatgpt4o_td

Accuracy comparison (with remediation): **TD is better** - 31.68 vs 22.77

Test counts (with remediation):
* Base: {'success': 23, 'fail': 72, 'error': 6, 'generation_errors': 0, 'test_errors': 6}
* TD: {'success': 32, 'fail': 63, 'error': 6, 'generation_errors': 0, 'test_errors': 6}
* Difference: {'success': 9, 'fail': -9, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 1.0
* task_id: 6.0
* task_id: 10.0
* task_id: 22.0
* task_id: 24.0
* task_id: 36.0
* task_id: 40.0
* task_id: 55.0
* task_id: 61.0
* task_id: 64.0
* task_id: 70.0
* task_id: 79.0
* task_id: 81.0
* task_id: 83.0

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 0.0
* task_id: 56.0
* task_id: 87.0
* task_id: 94.0
* task_id: 100.0

---

### code_contests_claude35sonnet vs code_contests_claude35sonnet_td

Accuracy comparison (with remediation): **TD is better** - 53.47 vs 47.52

Test counts (with remediation):
* Base: {'success': 48, 'fail': 20, 'error': 33, 'generation_errors': 0, 'test_errors': 33}
* TD: {'success': 54, 'fail': 24, 'error': 23, 'generation_errors': 0, 'test_errors': 23}
* Difference: {'success': 6, 'fail': 4, 'error': -10, 'generation_errors': 0, 'test_errors': -10}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2.0
* task_id: 13.0
* task_id: 26.0
* task_id: 31.0
* task_id: 35.0
* task_id: 45.0
* task_id: 70.0
* task_id: 77.0
* task_id: 83.0
* task_id: 86.0
* task_id: 95.0
* task_id: 96.0

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 0.0
* task_id: 10.0
* task_id: 51.0
* task_id: 71.0
* task_id: 87.0
* task_id: 99.0

---

### code_contests_qwen25coder32b vs code_contests_qwen25coder32b_td

Accuracy comparison (with remediation): **TD is better** - 22.77 vs 6.93

Test counts (with remediation):
* Base: {'success': 7, 'fail': 84, 'error': 10, 'generation_errors': 0, 'test_errors': 10}
* TD: {'success': 23, 'fail': 66, 'error': 12, 'generation_errors': 0, 'test_errors': 12}
* Difference: {'success': 16, 'fail': -18, 'error': 2, 'generation_errors': 0, 'test_errors': 2}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 3.0
* task_id: 4.0
* task_id: 24.0
* task_id: 30.0
* task_id: 48.0
* task_id: 53.0
* task_id: 58.0
* task_id: 65.0
* task_id: 69.0
* task_id: 71.0
* task_id: 76.0
* task_id: 79.0
* task_id: 81.0
* task_id: 82.0
* task_id: 88.0
* task_id: 94.0
* task_id: 95.0
* task_id: 96.0

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 15.0
* task_id: 86.0

---

### human_eval_chatgpt4o vs human_eval_chatgpt4o_td

Accuracy comparison (with remediation): **TD is same** - 92.68 vs 92.68

Test counts (with remediation):
* Base: {'success': 38, 'fail': 3, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 38, 'fail': 2, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 0, 'fail': -1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

---

### human_eval_chatgpt4omini vs human_eval_chatgpt4omini_td

Accuracy comparison (with remediation): **TD is better** - 97.56 vs 95.12

Test counts (with remediation):
* Base: {'success': 39, 'fail': 1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 40, 'fail': 0, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 1, 'fail': -1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 17

---

### human_eval_claude35haiku vs human_eval_claude35haiku_td

Accuracy comparison (with remediation): **TD is same** - 95.12 vs 95.12

Test counts (with remediation):
* Base: {'success': 39, 'fail': 2, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 39, 'fail': 1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 0, 'fail': -1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

---

### human_eval_claude35sonnet vs human_eval_claude35sonnet_td

Accuracy comparison (with remediation): **TD is same** - 95.12 vs 95.12

Test counts (with remediation):
* Base: {'success': 39, 'fail': 1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 39, 'fail': 1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 0, 'fail': 0, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

---

### human_eval_qwen25coder32b vs human_eval_qwen25coder32b_td

Accuracy comparison (with remediation): **TD is better** - 90.24 vs 87.80

Test counts (with remediation):
* Base: {'success': 36, 'fail': 4, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 37, 'fail': 3, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 1, 'fail': -1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 17

---

### human_eval_qwen25coder7b vs human_eval_qwen25coder7b_td

Accuracy comparison (with remediation): **TD is better** - 87.80 vs 85.37

Test counts (with remediation):
* Base: {'success': 35, 'fail': 6, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 36, 'fail': 5, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 1, 'fail': -1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2

---

### mbpp_sanitized_chatgpt4o vs mbpp_sanitized_chatgpt4o_td

Accuracy comparison (with remediation): **TD is better** - 93.40 vs 83.96

Test counts (with remediation):
* Base: {'success': 89, 'fail': 14, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* TD: {'success': 99, 'fail': 2, 'error': 5, 'generation_errors': 0, 'test_errors': 5}
* Difference: {'success': 10, 'fail': -12, 'error': 2, 'generation_errors': 0, 'test_errors': 2}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 20
* task_id: 57
* task_id: 63
* task_id: 84
* task_id: 87
* task_id: 109
* task_id: 119
* task_id: 123
* task_id: 125
* task_id: 129

---

### mbpp_sanitized_chatgpt4omini vs mbpp_sanitized_chatgpt4omini_td

Accuracy comparison (with remediation): **TD is better** - 86.79 vs 57.55

Test counts (with remediation):
* Base: {'success': 61, 'fail': 42, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* TD: {'success': 92, 'fail': 11, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* Difference: {'success': 31, 'fail': -31, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 6
* task_id: 14
* task_id: 57
* task_id: 59
* task_id: 61
* task_id: 63
* task_id: 68
* task_id: 74
* task_id: 84
* task_id: 89
* task_id: 92
* task_id: 101
* task_id: 109
* task_id: 113
* task_id: 117
* task_id: 120
* task_id: 125
* task_id: 129
* task_id: 130
* task_id: 133
* task_id: 135
* task_id: 142
* task_id: 145
* task_id: 162
* task_id: 165
* task_id: 166
* task_id: 168
* task_id: 171
* task_id: 172
* task_id: 224

---

### mbpp_sanitized_claude35haiku vs mbpp_sanitized_claude35haiku_td

Accuracy comparison (with remediation): **TD is better** - 92.45 vs 91.51

Test counts (with remediation):
* Base: {'success': 97, 'fail': 6, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* TD: {'success': 98, 'fail': 5, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* Difference: {'success': 1, 'fail': -1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 63
* task_id: 103
* task_id: 125
* task_id: 164

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 84
* task_id: 124
* task_id: 138

---

### mbpp_sanitized_claude35sonnet vs mbpp_sanitized_claude35sonnet_td

Accuracy comparison (with remediation): **TD is better** - 95.28 vs 91.51

Test counts (with remediation):
* Base: {'success': 97, 'fail': 6, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* TD: {'success': 101, 'fail': 2, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* Difference: {'success': 4, 'fail': -4, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 63
* task_id: 109
* task_id: 120
* task_id: 125

---

### mbpp_sanitized_qwen25coder32b vs mbpp_sanitized_qwen25coder32b_td

Accuracy comparison (with remediation): **TD is better** - 73.58 vs 43.40

Test counts (with remediation):
* Base: {'success': 46, 'fail': 54, 'error': 6, 'generation_errors': 0, 'test_errors': 6}
* TD: {'success': 78, 'fail': 21, 'error': 7, 'generation_errors': 0, 'test_errors': 7}
* Difference: {'success': 32, 'fail': -33, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 4
* task_id: 7
* task_id: 9
* task_id: 16
* task_id: 17
* task_id: 20
* task_id: 63
* task_id: 66
* task_id: 68
* task_id: 69
* task_id: 70
* task_id: 71
* task_id: 74
* task_id: 84
* task_id: 91
* task_id: 92
* task_id: 95
* task_id: 96
* task_id: 101
* task_id: 103
* task_id: 105
* task_id: 108
* task_id: 115
* task_id: 119
* task_id: 120
* task_id: 128
* task_id: 129
* task_id: 130
* task_id: 133
* task_id: 160
* task_id: 171
* task_id: 222

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 86

---

### mbpp_sanitized_qwen25coder7b vs mbpp_sanitized_qwen25coder7b_td

Accuracy comparison (with remediation): **TD is better** - 82.08 vs 59.43

Test counts (with remediation):
* Base: {'success': 63, 'fail': 43, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 87, 'fail': 19, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 24, 'fail': -24, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 19
* task_id: 59
* task_id: 68
* task_id: 70
* task_id: 79
* task_id: 84
* task_id: 86
* task_id: 89
* task_id: 91
* task_id: 99
* task_id: 100
* task_id: 101
* task_id: 123
* task_id: 127
* task_id: 128
* task_id: 130
* task_id: 131
* task_id: 133
* task_id: 135
* task_id: 137
* task_id: 160
* task_id: 162
* task_id: 164
* task_id: 166
* task_id: 167
* task_id: 222

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 63
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
- Dataset Coverage: 0.25 (25.0% of problems)
- Total Problems Across All Datasets: 995
- Total Problems Tested: 248
- Datasets:
  * code_contests: 404 problems (101 tested)
  * human_eval: 164 problems (41 tested)
  * mbpp_sanitized: 427 problems (106 tested)

