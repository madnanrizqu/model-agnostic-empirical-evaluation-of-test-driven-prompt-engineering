# Combined Analysis Report

Generated: 2025-08-15 07:18:37

**LLMs:** Multiple (6 models) | **Research Question:** rq2

## Summary (First Attempt Only)

Total comparisons: 15

* Test-driven (TD) results were better in 13 out of 15 comparisons (86.7%)
* Test-driven (TD) results were same in 0 out of 15 comparisons (0.0%)
* Test-driven (TD) results were worse in 2 out of 15 comparisons (13.3%)

### Accuracy Statistics

* Total increase: 241.66
* Average increase: 16.11 (95% CI: [7.31, 24.91])
* Median increase: 12.20
* Standard deviation: 17.39
* Range: -19.51 to 39.62
* Interquartile range: 4.72 to 33.96
* Benchmarks improved: 13 (86.7%)
* Benchmarks worsened: 2 (13.3%)
* Benchmarks unchanged: 0 (0.0%)
* Average improvement percentage: 100.95%
* Average regression percentage: -12.54%

#### Top 5 Increases

* mbpp_sanitized_chatgpt4o: 50.00 → 89.62 (change: +39.62)
* mbpp_sanitized_claude35sonnet: 40.57 → 79.25 (change: +38.68)
* mbpp_sanitized_chatgpt4omini: 29.25 → 65.09 (change: +35.84)
* mbpp_sanitized_qwen25coder32b: 24.53 → 58.49 (change: +33.96)
* code_contests_claude35sonnet: 4.95 → 38.61 (change: +33.66)

#### Top 5 Regressions

* human_eval_chatgpt4omini: 87.80 → 68.29 (change: -19.51)
* human_eval_qwen25coder7b: 85.37 → 82.93 (change: -2.44)
* code_contests_qwen25coder32b: 13.86 → 15.84 (change: +1.98)
* mbpp_sanitized_claude35haiku: 50.94 → 55.66 (change: +4.72)
* human_eval_claude35sonnet: 85.37 → 92.68 (change: +7.31)

## Summary (With Remediation)

Total comparisons: 15

* Test-driven (TD) results were better in 9 out of 15 comparisons (60.0%)
* Test-driven (TD) results were same in 2 out of 15 comparisons (13.3%)
* Test-driven (TD) results were worse in 4 out of 15 comparisons (26.7%)

### Accuracy Statistics (With Remediation)

* Total increase: 127.98
* Average increase: 8.53 (95% CI: [3.51, 13.55])
* Median increase: 8.49
* Standard deviation: 9.92
* Range: -2.44 to 27.36
* Interquartile range: -2.44 to 18.87
* Benchmarks improved: 9 (60.0%)
* Benchmarks worsened: 4 (26.7%)
* Benchmarks unchanged: 2 (13.3%)
* Average improvement percentage: 29.50%
* Average regression percentage: -2.66%

#### Top 5 Increases (With Remediation)

* mbpp_sanitized_chatgpt4omini: 58.49 → 85.85 (change: +27.36)
* code_contests_claude35sonnet: 42.57 → 62.38 (change: +19.81)
* mbpp_sanitized_qwen25coder32b: 50.94 → 69.81 (change: +18.87)
* mbpp_sanitized_qwen25coder7b: 57.55 → 76.42 (change: +18.87)
* mbpp_sanitized_claude35sonnet: 78.30 → 93.40 (change: +15.10)

#### Top 5 Regressions (With Remediation)

* human_eval_chatgpt4o: 92.68 → 90.24 (change: -2.44)
* human_eval_chatgpt4omini: 95.12 → 92.68 (change: -2.44)
* human_eval_claude35sonnet: 95.12 → 92.68 (change: -2.44)
* human_eval_qwen25coder7b: 85.37 → 82.93 (change: -2.44)
* human_eval_claude35haiku: 95.12 → 95.12 (change: +0.00)

## Detailed Comparisons (First Attempt Only)

### code_contests_chatgpt4o vs code_contests_chatgpt4o_td

Accuracy comparison: **TD is better** - 24.75 vs 13.86

Test counts:
* Base: {'success': 14, 'fail': 79, 'error': 8, 'generation_errors': 0, 'test_errors': 8}
* TD: {'success': 25, 'fail': 70, 'error': 6, 'generation_errors': 0, 'test_errors': 6}
* Difference: {'success': 11, 'fail': -9, 'error': -2, 'generation_errors': 0, 'test_errors': -2}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 1.0
* task_id: 2.0
* task_id: 3.0
* task_id: 6.0
* task_id: 10.0
* task_id: 26.0
* task_id: 30.0
* task_id: 32.0
* task_id: 34.0
* task_id: 40.0
* task_id: 46.0
* task_id: 47.0
* task_id: 48.0
* task_id: 50.0
* task_id: 54.0
* task_id: 55.0
* task_id: 62.0
* task_id: 64.0
* task_id: 65.0
* task_id: 71.0
* task_id: 73.0
* task_id: 79.0
* task_id: 80.0

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 13.0
* task_id: 36.0
* task_id: 37.0
* task_id: 38.0
* task_id: 41.0
* task_id: 42.0
* task_id: 63.0
* task_id: 74.0
* task_id: 77.0
* task_id: 78.0
* task_id: 82.0
* task_id: 99.0

---

### code_contests_claude35sonnet vs code_contests_claude35sonnet_td

Accuracy comparison: **TD is better** - 38.61 vs 4.95

Test counts:
* Base: {'success': 5, 'fail': 53, 'error': 31, 'generation_errors': 0, 'test_errors': 31}
* TD: {'success': 39, 'fail': 26, 'error': 30, 'generation_errors': 0, 'test_errors': 30}
* Difference: {'success': 34, 'fail': -27, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 1.0
* task_id: 2.0
* task_id: 5.0
* task_id: 6.0
* task_id: 7.0
* task_id: 8.0
* task_id: 9.0
* task_id: 15.0
* task_id: 16.0
* task_id: 19.0
* task_id: 27.0
* task_id: 30.0
* task_id: 33.0
* task_id: 34.0
* task_id: 35.0
* task_id: 38.0
* task_id: 40.0
* task_id: 42.0
* task_id: 43.0
* task_id: 47.0
* task_id: 52.0
* task_id: 53.0
* task_id: 58.0
* task_id: 62.0
* task_id: 64.0
* task_id: 65.0
* task_id: 70.0
* task_id: 74.0
* task_id: 75.0
* task_id: 76.0
* task_id: 79.0
* task_id: 81.0
* task_id: 83.0
* task_id: 85.0
* task_id: 86.0
* task_id: 88.0
* task_id: 90.0
* task_id: 95.0

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 21.0
* task_id: 56.0
* task_id: 72.0
* task_id: 98.0

---

### code_contests_qwen25coder32b vs code_contests_qwen25coder32b_td

Accuracy comparison: **TD is better** - 15.84 vs 13.86

Test counts:
* Base: {'success': 14, 'fail': 58, 'error': 11, 'generation_errors': 0, 'test_errors': 11}
* TD: {'success': 16, 'fail': 56, 'error': 18, 'generation_errors': 0, 'test_errors': 18}
* Difference: {'success': 2, 'fail': -2, 'error': 7, 'generation_errors': 0, 'test_errors': 7}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 22.0
* task_id: 30.0
* task_id: 38.0
* task_id: 41.0
* task_id: 46.0
* task_id: 53.0
* task_id: 66.0
* task_id: 72.0
* task_id: 75.0
* task_id: 85.0
* task_id: 88.0
* task_id: 98.0

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 10.0
* task_id: 13.0
* task_id: 23.0
* task_id: 24.0
* task_id: 25.0
* task_id: 32.0
* task_id: 60.0
* task_id: 79.0
* task_id: 86.0
* task_id: 100.0

---

### human_eval_chatgpt4o vs human_eval_chatgpt4o_td

Accuracy comparison: **TD is better** - 87.80 vs 68.29

Test counts:
* Base: {'success': 28, 'fail': 12, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 36, 'fail': 4, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 8, 'fail': -8, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 0
* task_id: 1
* task_id: 3
* task_id: 4
* task_id: 6
* task_id: 9
* task_id: 12
* task_id: 20
* task_id: 26

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 14

---

### human_eval_chatgpt4omini vs human_eval_chatgpt4omini_td

Accuracy comparison: **TD is worse** - 68.29 vs 87.80

Test counts:
* Base: {'success': 36, 'fail': 3, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* TD: {'success': 28, 'fail': 7, 'error': 6, 'generation_errors': 0, 'test_errors': 6}
* Difference: {'success': -8, 'fail': 4, 'error': 4, 'generation_errors': 0, 'test_errors': 4}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 17
* task_id: 35

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 0
* task_id: 7
* task_id: 9
* task_id: 10
* task_id: 13
* task_id: 18
* task_id: 19
* task_id: 28
* task_id: 31
* task_id: 34
* task_id: 38

---

### human_eval_claude35haiku vs human_eval_claude35haiku_td

Accuracy comparison: **TD is better** - 82.93 vs 75.61

Test counts:
* Base: {'success': 31, 'fail': 8, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* TD: {'success': 34, 'fail': 5, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* Difference: {'success': 3, 'fail': -3, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 4
* task_id: 5
* task_id: 12
* task_id: 19
* task_id: 31

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 10
* task_id: 39

---

### human_eval_claude35sonnet vs human_eval_claude35sonnet_td

Accuracy comparison: **TD is better** - 92.68 vs 85.37

Test counts:
* Base: {'success': 35, 'fail': 4, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* TD: {'success': 38, 'fail': 2, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 3, 'fail': -2, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 12
* task_id: 28
* task_id: 39

---

### human_eval_qwen25coder32b vs human_eval_qwen25coder32b_td

Accuracy comparison: **TD is better** - 85.37 vs 73.17

Test counts:
* Base: {'success': 30, 'fail': 8, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* TD: {'success': 35, 'fail': 5, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 5, 'fail': -3, 'error': -2, 'generation_errors': 0, 'test_errors': -2}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 10
* task_id: 24
* task_id: 28
* task_id: 29
* task_id: 31
* task_id: 40

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 1
* task_id: 19

---

### human_eval_qwen25coder7b vs human_eval_qwen25coder7b_td

Accuracy comparison: **TD is worse** - 82.93 vs 85.37

Test counts:
* Base: {'success': 35, 'fail': 5, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 34, 'fail': 6, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': -1, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 27

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 6
* task_id: 8
* task_id: 26

---

### mbpp_sanitized_chatgpt4o vs mbpp_sanitized_chatgpt4o_td

Accuracy comparison: **TD is better** - 89.62 vs 50.00

Test counts:
* Base: {'success': 53, 'fail': 44, 'error': 9, 'generation_errors': 0, 'test_errors': 9}
* TD: {'success': 95, 'fail': 7, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* Difference: {'success': 42, 'fail': -37, 'error': -5, 'generation_errors': 0, 'test_errors': -5}

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
* task_id: 58
* task_id: 59
* task_id: 64
* task_id: 66
* task_id: 68
* task_id: 70
* task_id: 71
* task_id: 75
* task_id: 77
* task_id: 79
* task_id: 84
* task_id: 86
* task_id: 91
* task_id: 92
* task_id: 93
* task_id: 98
* task_id: 101
* task_id: 102
* task_id: 104
* task_id: 105
* task_id: 108
* task_id: 111
* task_id: 113
* task_id: 115
* task_id: 116
* task_id: 117
* task_id: 125
* task_id: 128
* task_id: 130
* task_id: 135
* task_id: 137
* task_id: 141
* task_id: 160
* task_id: 167
* task_id: 222

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 9
* task_id: 126

---

### mbpp_sanitized_chatgpt4omini vs mbpp_sanitized_chatgpt4omini_td

Accuracy comparison: **TD is better** - 65.09 vs 29.25

Test counts:
* Base: {'success': 31, 'fail': 53, 'error': 22, 'generation_errors': 0, 'test_errors': 22}
* TD: {'success': 69, 'fail': 27, 'error': 10, 'generation_errors': 0, 'test_errors': 10}
* Difference: {'success': 38, 'fail': -26, 'error': -12, 'generation_errors': 0, 'test_errors': -12}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 3
* task_id: 4
* task_id: 7
* task_id: 9
* task_id: 14
* task_id: 19
* task_id: 57
* task_id: 58
* task_id: 59
* task_id: 61
* task_id: 62
* task_id: 63
* task_id: 69
* task_id: 70
* task_id: 74
* task_id: 75
* task_id: 79
* task_id: 80
* task_id: 82
* task_id: 85
* task_id: 86
* task_id: 88
* task_id: 96
* task_id: 97
* task_id: 101
* task_id: 102
* task_id: 103
* task_id: 108
* task_id: 111
* task_id: 113
* task_id: 115
* task_id: 117
* task_id: 120
* task_id: 125
* task_id: 129
* task_id: 130
* task_id: 133
* task_id: 135
* task_id: 142
* task_id: 145
* task_id: 160
* task_id: 165
* task_id: 167
* task_id: 171
* task_id: 222

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 8
* task_id: 20
* task_id: 65
* task_id: 93
* task_id: 106
* task_id: 116
* task_id: 131
* task_id: 170

---

### mbpp_sanitized_claude35haiku vs mbpp_sanitized_claude35haiku_td

Accuracy comparison: **TD is better** - 55.66 vs 50.94

Test counts:
* Base: {'success': 54, 'fail': 32, 'error': 20, 'generation_errors': 0, 'test_errors': 20}
* TD: {'success': 59, 'fail': 39, 'error': 8, 'generation_errors': 0, 'test_errors': 8}
* Difference: {'success': 5, 'fail': 7, 'error': -12, 'generation_errors': 0, 'test_errors': -12}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 3
* task_id: 8
* task_id: 12
* task_id: 14
* task_id: 18
* task_id: 59
* task_id: 63
* task_id: 67
* task_id: 68
* task_id: 69
* task_id: 71
* task_id: 79
* task_id: 95
* task_id: 98
* task_id: 105
* task_id: 109
* task_id: 116
* task_id: 119
* task_id: 128
* task_id: 129
* task_id: 133
* task_id: 140
* task_id: 163
* task_id: 172

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 9
* task_id: 61
* task_id: 65
* task_id: 66
* task_id: 74
* task_id: 75
* task_id: 80
* task_id: 84
* task_id: 87
* task_id: 100
* task_id: 101
* task_id: 102
* task_id: 103
* task_id: 104
* task_id: 106
* task_id: 118
* task_id: 125
* task_id: 132
* task_id: 142
* task_id: 224

---

### mbpp_sanitized_claude35sonnet vs mbpp_sanitized_claude35sonnet_td

Accuracy comparison: **TD is better** - 79.25 vs 40.57

Test counts:
* Base: {'success': 43, 'fail': 45, 'error': 18, 'generation_errors': 0, 'test_errors': 18}
* TD: {'success': 84, 'fail': 14, 'error': 8, 'generation_errors': 0, 'test_errors': 8}
* Difference: {'success': 41, 'fail': -31, 'error': -10, 'generation_errors': 0, 'test_errors': -10}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 4
* task_id: 6
* task_id: 7
* task_id: 8
* task_id: 9
* task_id: 11
* task_id: 14
* task_id: 17
* task_id: 62
* task_id: 63
* task_id: 64
* task_id: 68
* task_id: 70
* task_id: 71
* task_id: 72
* task_id: 74
* task_id: 75
* task_id: 77
* task_id: 86
* task_id: 88
* task_id: 89
* task_id: 94
* task_id: 95
* task_id: 96
* task_id: 99
* task_id: 102
* task_id: 106
* task_id: 108
* task_id: 117
* task_id: 120
* task_id: 123
* task_id: 129
* task_id: 131
* task_id: 132
* task_id: 133
* task_id: 135
* task_id: 137
* task_id: 140
* task_id: 141
* task_id: 163
* task_id: 168
* task_id: 171
* task_id: 222
* task_id: 224

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 87
* task_id: 98
* task_id: 115
* task_id: 145

---

### mbpp_sanitized_qwen25coder32b vs mbpp_sanitized_qwen25coder32b_td

Accuracy comparison: **TD is better** - 58.49 vs 24.53

Test counts:
* Base: {'success': 26, 'fail': 66, 'error': 14, 'generation_errors': 0, 'test_errors': 14}
* TD: {'success': 62, 'fail': 34, 'error': 10, 'generation_errors': 0, 'test_errors': 10}
* Difference: {'success': 36, 'fail': -32, 'error': -4, 'generation_errors': 0, 'test_errors': -4}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 3
* task_id: 4
* task_id: 7
* task_id: 11
* task_id: 12
* task_id: 16
* task_id: 19
* task_id: 20
* task_id: 57
* task_id: 58
* task_id: 59
* task_id: 67
* task_id: 68
* task_id: 69
* task_id: 71
* task_id: 72
* task_id: 75
* task_id: 77
* task_id: 79
* task_id: 84
* task_id: 85
* task_id: 89
* task_id: 91
* task_id: 92
* task_id: 102
* task_id: 105
* task_id: 106
* task_id: 108
* task_id: 111
* task_id: 113
* task_id: 115
* task_id: 116
* task_id: 117
* task_id: 120
* task_id: 128
* task_id: 130
* task_id: 131
* task_id: 132
* task_id: 133
* task_id: 137
* task_id: 139
* task_id: 141
* task_id: 160
* task_id: 224

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 82
* task_id: 83
* task_id: 87
* task_id: 95
* task_id: 96
* task_id: 98
* task_id: 125
* task_id: 135

---

### mbpp_sanitized_qwen25coder7b vs mbpp_sanitized_qwen25coder7b_td

Accuracy comparison: **TD is better** - 75.47 vs 57.55

Test counts:
* Base: {'success': 61, 'fail': 36, 'error': 9, 'generation_errors': 0, 'test_errors': 9}
* TD: {'success': 80, 'fail': 18, 'error': 8, 'generation_errors': 0, 'test_errors': 8}
* Difference: {'success': 19, 'fail': -18, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 4
* task_id: 7
* task_id: 19
* task_id: 59
* task_id: 68
* task_id: 70
* task_id: 75
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
* task_id: 167
* task_id: 222

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 63
* task_id: 69
* task_id: 74
* task_id: 93
* task_id: 96
* task_id: 98
* task_id: 120
* task_id: 129

---

## Detailed Comparisons (With Remediation)

### code_contests_chatgpt4o vs code_contests_chatgpt4o_td

Accuracy comparison (with remediation): **TD is better** - 49.50 vs 37.62

Test counts (with remediation):
* Base: {'success': 38, 'fail': 59, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* TD: {'success': 50, 'fail': 47, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* Difference: {'success': 12, 'fail': -12, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 1.0
* task_id: 2.0
* task_id: 3.0
* task_id: 4.0
* task_id: 6.0
* task_id: 10.0
* task_id: 21.0
* task_id: 26.0
* task_id: 30.0
* task_id: 32.0
* task_id: 39.0
* task_id: 40.0
* task_id: 50.0
* task_id: 52.0
* task_id: 54.0
* task_id: 55.0
* task_id: 61.0
* task_id: 62.0
* task_id: 64.0
* task_id: 65.0
* task_id: 66.0
* task_id: 79.0
* task_id: 80.0
* task_id: 81.0
* task_id: 83.0
* task_id: 86.0
* task_id: 95.0
* task_id: 96.0

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 8.0
* task_id: 16.0
* task_id: 20.0
* task_id: 22.0
* task_id: 31.0
* task_id: 35.0
* task_id: 36.0
* task_id: 41.0
* task_id: 51.0
* task_id: 67.0
* task_id: 74.0
* task_id: 77.0
* task_id: 78.0
* task_id: 90.0
* task_id: 97.0
* task_id: 98.0

---

### code_contests_claude35sonnet vs code_contests_claude35sonnet_td

Accuracy comparison (with remediation): **TD is better** - 62.38 vs 42.57

Test counts (with remediation):
* Base: {'success': 43, 'fail': 33, 'error': 25, 'generation_errors': 0, 'test_errors': 25}
* TD: {'success': 63, 'fail': 22, 'error': 16, 'generation_errors': 0, 'test_errors': 16}
* Difference: {'success': 20, 'fail': -11, 'error': -9, 'generation_errors': 0, 'test_errors': -9}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 0.0
* task_id: 2.0
* task_id: 7.0
* task_id: 9.0
* task_id: 12.0
* task_id: 13.0
* task_id: 16.0
* task_id: 17.0
* task_id: 24.0
* task_id: 25.0
* task_id: 27.0
* task_id: 33.0
* task_id: 34.0
* task_id: 39.0
* task_id: 40.0
* task_id: 41.0
* task_id: 42.0
* task_id: 45.0
* task_id: 46.0
* task_id: 47.0
* task_id: 54.0
* task_id: 55.0
* task_id: 61.0
* task_id: 62.0
* task_id: 69.0
* task_id: 74.0
* task_id: 75.0
* task_id: 79.0
* task_id: 82.0
* task_id: 86.0
* task_id: 95.0

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 21.0
* task_id: 23.0
* task_id: 26.0
* task_id: 49.0
* task_id: 71.0
* task_id: 72.0
* task_id: 77.0
* task_id: 80.0
* task_id: 87.0
* task_id: 97.0
* task_id: 98.0

---

### code_contests_qwen25coder32b vs code_contests_qwen25coder32b_td

Accuracy comparison (with remediation): **TD is better** - 34.65 vs 26.73

Test counts (with remediation):
* Base: {'success': 27, 'fail': 52, 'error': 6, 'generation_errors': 0, 'test_errors': 6}
* TD: {'success': 35, 'fail': 47, 'error': 9, 'generation_errors': 0, 'test_errors': 9}
* Difference: {'success': 8, 'fail': -5, 'error': 3, 'generation_errors': 0, 'test_errors': 3}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 9.0
* task_id: 15.0
* task_id: 19.0
* task_id: 21.0
* task_id: 22.0
* task_id: 27.0
* task_id: 30.0
* task_id: 38.0
* task_id: 40.0
* task_id: 41.0
* task_id: 42.0
* task_id: 46.0
* task_id: 47.0
* task_id: 51.0
* task_id: 53.0
* task_id: 65.0
* task_id: 66.0
* task_id: 69.0
* task_id: 75.0
* task_id: 82.0
* task_id: 83.0
* task_id: 88.0
* task_id: 90.0
* task_id: 92.0
* task_id: 94.0
* task_id: 97.0
* task_id: 98.0

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 2.0
* task_id: 3.0
* task_id: 4.0
* task_id: 13.0
* task_id: 23.0
* task_id: 24.0
* task_id: 25.0
* task_id: 32.0
* task_id: 44.0
* task_id: 49.0
* task_id: 52.0
* task_id: 54.0
* task_id: 55.0
* task_id: 57.0
* task_id: 60.0
* task_id: 79.0
* task_id: 86.0
* task_id: 89.0
* task_id: 100.0

---

### human_eval_chatgpt4o vs human_eval_chatgpt4o_td

Accuracy comparison (with remediation): **TD is worse** - 90.24 vs 92.68

Test counts (with remediation):
* Base: {'success': 38, 'fail': 2, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 37, 'fail': 3, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': -1, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 38

---

### human_eval_chatgpt4omini vs human_eval_chatgpt4omini_td

Accuracy comparison (with remediation): **TD is worse** - 92.68 vs 95.12

Test counts (with remediation):
* Base: {'success': 39, 'fail': 1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 38, 'fail': 2, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': -1, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 17

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 9
* task_id: 10

---

### human_eval_claude35haiku vs human_eval_claude35haiku_td

Accuracy comparison (with remediation): **TD is same** - 95.12 vs 95.12

Test counts (with remediation):
* Base: {'success': 39, 'fail': 2, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 39, 'fail': 1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 0, 'fail': -1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

---

### human_eval_claude35sonnet vs human_eval_claude35sonnet_td

Accuracy comparison (with remediation): **TD is worse** - 92.68 vs 95.12

Test counts (with remediation):
* Base: {'success': 39, 'fail': 1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 38, 'fail': 2, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': -1, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 38

---

### human_eval_qwen25coder32b vs human_eval_qwen25coder32b_td

Accuracy comparison (with remediation): **TD is same** - 90.24 vs 90.24

Test counts (with remediation):
* Base: {'success': 37, 'fail': 3, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 37, 'fail': 4, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 0, 'fail': 1, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

---

### human_eval_qwen25coder7b vs human_eval_qwen25coder7b_td

Accuracy comparison (with remediation): **TD is worse** - 82.93 vs 85.37

Test counts (with remediation):
* Base: {'success': 35, 'fail': 6, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 34, 'fail': 7, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': -1, 'fail': 1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 27

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 6
* task_id: 8
* task_id: 26

---

### mbpp_sanitized_chatgpt4o vs mbpp_sanitized_chatgpt4o_td

Accuracy comparison (with remediation): **TD is better** - 93.40 vs 83.96

Test counts (with remediation):
* Base: {'success': 89, 'fail': 13, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* TD: {'success': 99, 'fail': 4, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* Difference: {'success': 10, 'fail': -9, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 20
* task_id: 68
* task_id: 87
* task_id: 92
* task_id: 105
* task_id: 124
* task_id: 125
* task_id: 130
* task_id: 137
* task_id: 160

---

### mbpp_sanitized_chatgpt4omini vs mbpp_sanitized_chatgpt4omini_td

Accuracy comparison (with remediation): **TD is better** - 85.85 vs 58.49

Test counts (with remediation):
* Base: {'success': 62, 'fail': 37, 'error': 7, 'generation_errors': 0, 'test_errors': 7}
* TD: {'success': 91, 'fail': 11, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* Difference: {'success': 29, 'fail': -26, 'error': -3, 'generation_errors': 0, 'test_errors': -3}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 3
* task_id: 7
* task_id: 9
* task_id: 14
* task_id: 18
* task_id: 19
* task_id: 57
* task_id: 58
* task_id: 59
* task_id: 61
* task_id: 69
* task_id: 70
* task_id: 72
* task_id: 74
* task_id: 79
* task_id: 82
* task_id: 85
* task_id: 89
* task_id: 103
* task_id: 108
* task_id: 109
* task_id: 113
* task_id: 117
* task_id: 120
* task_id: 130
* task_id: 133
* task_id: 135
* task_id: 142
* task_id: 160
* task_id: 165
* task_id: 166
* task_id: 168
* task_id: 171
* task_id: 172
* task_id: 224

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 8
* task_id: 20
* task_id: 83
* task_id: 131
* task_id: 137
* task_id: 138
* task_id: 170

---

### mbpp_sanitized_claude35haiku vs mbpp_sanitized_claude35haiku_td

Accuracy comparison (with remediation): **TD is better** - 88.68 vs 80.19

Test counts (with remediation):
* Base: {'success': 85, 'fail': 12, 'error': 9, 'generation_errors': 0, 'test_errors': 9}
* TD: {'success': 94, 'fail': 8, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* Difference: {'success': 9, 'fail': -4, 'error': -5, 'generation_errors': 0, 'test_errors': -5}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 3
* task_id: 12
* task_id: 18
* task_id: 57
* task_id: 62
* task_id: 70
* task_id: 98
* task_id: 99
* task_id: 108
* task_id: 109
* task_id: 111
* task_id: 124
* task_id: 128
* task_id: 163
* task_id: 164
* task_id: 223

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 84
* task_id: 85
* task_id: 100
* task_id: 101
* task_id: 103
* task_id: 125
* task_id: 126
* task_id: 143

---

### mbpp_sanitized_claude35sonnet vs mbpp_sanitized_claude35sonnet_td

Accuracy comparison (with remediation): **TD is better** - 93.40 vs 78.30

Test counts (with remediation):
* Base: {'success': 83, 'fail': 14, 'error': 9, 'generation_errors': 0, 'test_errors': 9}
* TD: {'success': 99, 'fail': 5, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* Difference: {'success': 16, 'fail': -9, 'error': -7, 'generation_errors': 0, 'test_errors': -7}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 7
* task_id: 17
* task_id: 56
* task_id: 63
* task_id: 71
* task_id: 75
* task_id: 86
* task_id: 106
* task_id: 124
* task_id: 131
* task_id: 133
* task_id: 135
* task_id: 137
* task_id: 141
* task_id: 143
* task_id: 222

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 172

---

### mbpp_sanitized_qwen25coder32b vs mbpp_sanitized_qwen25coder32b_td

Accuracy comparison (with remediation): **TD is better** - 69.81 vs 50.94

Test counts (with remediation):
* Base: {'success': 54, 'fail': 41, 'error': 11, 'generation_errors': 0, 'test_errors': 11}
* TD: {'success': 74, 'fail': 25, 'error': 7, 'generation_errors': 0, 'test_errors': 7}
* Difference: {'success': 20, 'fail': -16, 'error': -4, 'generation_errors': 0, 'test_errors': -4}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 7
* task_id: 16
* task_id: 19
* task_id: 57
* task_id: 67
* task_id: 69
* task_id: 71
* task_id: 72
* task_id: 75
* task_id: 79
* task_id: 84
* task_id: 91
* task_id: 92
* task_id: 101
* task_id: 102
* task_id: 103
* task_id: 105
* task_id: 108
* task_id: 109
* task_id: 113
* task_id: 117
* task_id: 120
* task_id: 128
* task_id: 130
* task_id: 133
* task_id: 139
* task_id: 141
* task_id: 160
* task_id: 168
* task_id: 224

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 9
* task_id: 14
* task_id: 18
* task_id: 83
* task_id: 87
* task_id: 95
* task_id: 98
* task_id: 125
* task_id: 135
* task_id: 138

---

### mbpp_sanitized_qwen25coder7b vs mbpp_sanitized_qwen25coder7b_td

Accuracy comparison (with remediation): **TD is better** - 76.42 vs 57.55

Test counts (with remediation):
* Base: {'success': 61, 'fail': 44, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 81, 'fail': 22, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* Difference: {'success': 20, 'fail': -22, 'error': 2, 'generation_errors': 0, 'test_errors': 2}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 4
* task_id: 7
* task_id: 19
* task_id: 59
* task_id: 68
* task_id: 70
* task_id: 75
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
* task_id: 167
* task_id: 222

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 63
* task_id: 69
* task_id: 74
* task_id: 93
* task_id: 96
* task_id: 98
* task_id: 120
* task_id: 129

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

