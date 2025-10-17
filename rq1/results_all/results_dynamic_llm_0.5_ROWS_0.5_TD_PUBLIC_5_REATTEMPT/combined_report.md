# Combined Analysis Report

Generated: 2025-10-16 21:16:11

**LLMs:** Multiple (8 models) | **Research Question:** rq2

## Summary (First Attempt Only)

Total comparisons: 15

* Test-driven (TD) results were better in 15 out of 15 comparisons (100.0%)
* Test-driven (TD) results were same in 0 out of 15 comparisons (0.0%)
* Test-driven (TD) results were worse in 0 out of 15 comparisons (0.0%)

### Accuracy Statistics

* Total increase: 136.79
* Average increase: 9.12 (95% CI: [7.49, 10.74])
* Median increase: 8.53
* Standard deviation: 2.94
* Range: 3.66 to 14.55
* Interquartile range: 7.65 to 11.12
* Benchmarks improved: 15 (100.0%)
* Benchmarks worsened: 0 (0.0%)
* Benchmarks unchanged: 0 (0.0%)
* Average improvement percentage: 11.92%

#### Statistical Tests

* **Normality Test (Shapiro-Wilk)**: statistic=0.9661, p-value=0.7962, Normal=Yes
* **Paired t-test**: statistic=12.0327, p-value=0.0000
* **Effect Size (Cohen's d)**: 1.8760 (large effect)
* **Interpretation**: Results are highly significant (p < 0.001)

#### Top 5 Increases

* mbpp_sanitized_chatgpt4o: 74.65 → 89.20 (change: +14.55)
* human_eval_chatgpt4o: 78.05 → 90.24 (change: +12.19)
* mbpp_sanitized_claude35sonnet: 75.59 → 87.32 (change: +11.73)
* mbpp_sanitized_claude35haiku: 73.24 → 84.51 (change: +11.27)
* human_eval_qwen25coder14b: 79.27 → 90.24 (change: +10.97)

#### Top 5 Regressions

* human_eval_qwen25coder3b: 75.61 → 79.27 (change: +3.66)
* mbpp_sanitized_qwen25coder3b: 67.14 → 71.36 (change: +4.22)
* human_eval_claude35sonnet: 84.15 → 91.46 (change: +7.31)
* human_eval_qwen25coder7b: 76.83 → 84.15 (change: +7.32)
* mbpp_sanitized_chatgpt4omini: 75.12 → 83.10 (change: +7.98)

## Summary (With Remediation)

Total comparisons: 15

* Test-driven (TD) results were better in 15 out of 15 comparisons (100.0%)
* Test-driven (TD) results were same in 0 out of 15 comparisons (0.0%)
* Test-driven (TD) results were worse in 0 out of 15 comparisons (0.0%)

### Accuracy Statistics (With Remediation)

* Total increase: 64.37
* Average increase: 4.29 (95% CI: [2.76, 5.82])
* Median increase: 3.66
* Standard deviation: 2.76
* Range: 0.94 to 10.97
* Interquartile range: 2.44 to 4.88
* Benchmarks improved: 15 (100.0%)
* Benchmarks worsened: 0 (0.0%)
* Benchmarks unchanged: 0 (0.0%)
* Average improvement percentage: 5.30%

#### Statistical Tests

* **Normality Test (Shapiro-Wilk)**: statistic=0.8878, p-value=0.0621, Normal=Yes
* **Paired t-test**: statistic=6.0254, p-value=0.0000
* **Effect Size (Cohen's d)**: 0.5753 (medium effect)
* **Interpretation**: Results are highly significant (p < 0.001)

#### Top 5 Increases (With Remediation)

* human_eval_qwen25coder14b: 79.27 → 90.24 (change: +10.97)
* mbpp_sanitized_qwen25coder7b: 72.77 → 81.22 (change: +8.45)
* human_eval_qwen25coder7b: 76.83 → 84.15 (change: +7.32)
* human_eval_claude35haiku: 90.24 → 95.12 (change: +4.88)
* human_eval_qwen25coder32b: 89.02 → 93.90 (change: +4.88)

#### Top 5 Regressions (With Remediation)

* mbpp_sanitized_claude35haiku: 91.08 → 92.02 (change: +0.94)
* mbpp_sanitized_chatgpt4omini: 85.45 → 87.32 (change: +1.87)
* mbpp_sanitized_claude35sonnet: 93.43 → 95.31 (change: +1.88)
* human_eval_chatgpt4omini: 87.80 → 90.24 (change: +2.44)
* human_eval_chatgpt4o: 90.24 → 92.68 (change: +2.44)

## Detailed Comparisons (First Attempt Only)

### human_eval_chatgpt4o vs human_eval_chatgpt4o_td

Accuracy comparison: **TD is better** - 90.24 vs 78.05

Test counts:
* Base: {'success': 64, 'fail': 17, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 74, 'fail': 7, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 10, 'fail': -10, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 3
* task_id: 6
* task_id: 14
* task_id: 26
* task_id: 41
* task_id: 68
* task_id: 70
* task_id: 71
* task_id: 72
* task_id: 77
* task_id: 79
* task_id: 81

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 1
* task_id: 10

---

### human_eval_chatgpt4omini vs human_eval_chatgpt4omini_td

Accuracy comparison: **TD is better** - 89.02 vs 80.49

Test counts:
* Base: {'success': 66, 'fail': 12, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* TD: {'success': 73, 'fail': 8, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 7, 'fail': -4, 'error': -3, 'generation_errors': 0, 'test_errors': -3}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 41
* task_id: 68
* task_id: 70
* task_id: 71
* task_id: 76
* task_id: 77
* task_id: 79

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 10

---

### human_eval_claude35haiku vs human_eval_claude35haiku_td

Accuracy comparison: **TD is better** - 89.02 vs 79.27

Test counts:
* Base: {'success': 65, 'fail': 15, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* TD: {'success': 73, 'fail': 8, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 8, 'fail': -7, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 46
* task_id: 54
* task_id: 65
* task_id: 68
* task_id: 71
* task_id: 75
* task_id: 77
* task_id: 79

---

### human_eval_claude35sonnet vs human_eval_claude35sonnet_td

Accuracy comparison: **TD is better** - 91.46 vs 84.15

Test counts:
* Base: {'success': 69, 'fail': 11, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* TD: {'success': 75, 'fail': 6, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 6, 'fail': -5, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 3
* task_id: 68
* task_id: 70
* task_id: 71
* task_id: 77
* task_id: 79

---

### human_eval_qwen25coder14b vs human_eval_qwen25coder14b_td

Accuracy comparison: **TD is better** - 90.24 vs 79.27

Test counts:
* Base: {'success': 65, 'fail': 14, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* TD: {'success': 74, 'fail': 7, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 9, 'fail': -7, 'error': -2, 'generation_errors': 0, 'test_errors': -2}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 10
* task_id: 54
* task_id: 65
* task_id: 68
* task_id: 70
* task_id: 71
* task_id: 77
* task_id: 79

---

### human_eval_qwen25coder32b vs human_eval_qwen25coder32b_td

Accuracy comparison: **TD is better** - 90.24 vs 81.71

Test counts:
* Base: {'success': 67, 'fail': 12, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* TD: {'success': 74, 'fail': 7, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 7, 'fail': -5, 'error': -2, 'generation_errors': 0, 'test_errors': -2}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 38
* task_id: 65
* task_id: 68
* task_id: 70
* task_id: 71
* task_id: 79

---

### human_eval_qwen25coder3b vs human_eval_qwen25coder3b_td

Accuracy comparison: **TD is better** - 79.27 vs 75.61

Test counts:
* Base: {'success': 62, 'fail': 15, 'error': 5, 'generation_errors': 0, 'test_errors': 5}
* TD: {'success': 65, 'fail': 15, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* Difference: {'success': 3, 'fail': 0, 'error': -3, 'generation_errors': 0, 'test_errors': -3}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 19
* task_id: 68
* task_id: 77
* task_id: 79
* task_id: 80

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 8
* task_id: 65
* task_id: 76

---

### human_eval_qwen25coder7b vs human_eval_qwen25coder7b_td

Accuracy comparison: **TD is better** - 84.15 vs 76.83

Test counts:
* Base: {'success': 63, 'fail': 16, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* TD: {'success': 69, 'fail': 12, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 6, 'fail': -4, 'error': -2, 'generation_errors': 0, 'test_errors': -2}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 54
* task_id: 68
* task_id: 71
* task_id: 77
* task_id: 79
* task_id: 81

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 65

---

### mbpp_sanitized_chatgpt4o vs mbpp_sanitized_chatgpt4o_td

Accuracy comparison: **TD is better** - 89.20 vs 74.65

Test counts:
* Base: {'success': 159, 'fail': 46, 'error': 8, 'generation_errors': 0, 'test_errors': 8}
* TD: {'success': 190, 'fail': 15, 'error': 8, 'generation_errors': 0, 'test_errors': 8}
* Difference: {'success': 31, 'fail': -31, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 6
* task_id: 20
* task_id: 57
* task_id: 59
* task_id: 67
* task_id: 92
* task_id: 102
* task_id: 106
* task_id: 117
* task_id: 120
* task_id: 128
* task_id: 160
* task_id: 237
* task_id: 249
* task_id: 252
* task_id: 259
* task_id: 265
* task_id: 268
* task_id: 290
* task_id: 293
* task_id: 295
* task_id: 299
* task_id: 305
* task_id: 306
* task_id: 307
* task_id: 391
* task_id: 393
* task_id: 396
* task_id: 400
* task_id: 411
* task_id: 417
* task_id: 421

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 126

---

### mbpp_sanitized_chatgpt4omini vs mbpp_sanitized_chatgpt4omini_td

Accuracy comparison: **TD is better** - 83.10 vs 75.12

Test counts:
* Base: {'success': 160, 'fail': 41, 'error': 12, 'generation_errors': 0, 'test_errors': 12}
* TD: {'success': 177, 'fail': 30, 'error': 6, 'generation_errors': 0, 'test_errors': 6}
* Difference: {'success': 17, 'fail': -11, 'error': -6, 'generation_errors': 0, 'test_errors': -6}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 6
* task_id: 63
* task_id: 100
* task_id: 102
* task_id: 117
* task_id: 160
* task_id: 228
* task_id: 237
* task_id: 240
* task_id: 251
* task_id: 264
* task_id: 265
* task_id: 278
* task_id: 290
* task_id: 295
* task_id: 296
* task_id: 299
* task_id: 305
* task_id: 391
* task_id: 393
* task_id: 396
* task_id: 411
* task_id: 417
* task_id: 421

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 71
* task_id: 239
* task_id: 247
* task_id: 279
* task_id: 300
* task_id: 301
* task_id: 392

---

### mbpp_sanitized_claude35haiku vs mbpp_sanitized_claude35haiku_td

Accuracy comparison: **TD is better** - 84.51 vs 73.24

Test counts:
* Base: {'success': 156, 'fail': 44, 'error': 13, 'generation_errors': 0, 'test_errors': 13}
* TD: {'success': 180, 'fail': 27, 'error': 6, 'generation_errors': 0, 'test_errors': 6}
* Difference: {'success': 24, 'fail': -17, 'error': -7, 'generation_errors': 0, 'test_errors': -7}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 6
* task_id: 9
* task_id: 63
* task_id: 84
* task_id: 92
* task_id: 102
* task_id: 106
* task_id: 109
* task_id: 115
* task_id: 117
* task_id: 120
* task_id: 128
* task_id: 132
* task_id: 138
* task_id: 160
* task_id: 249
* task_id: 252
* task_id: 265
* task_id: 278
* task_id: 290
* task_id: 294
* task_id: 295
* task_id: 299
* task_id: 300
* task_id: 391
* task_id: 392
* task_id: 393
* task_id: 396
* task_id: 421
* task_id: 424

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 18
* task_id: 72
* task_id: 125
* task_id: 137
* task_id: 247
* task_id: 284

---

### mbpp_sanitized_claude35sonnet vs mbpp_sanitized_claude35sonnet_td

Accuracy comparison: **TD is better** - 87.32 vs 75.59

Test counts:
* Base: {'success': 161, 'fail': 41, 'error': 11, 'generation_errors': 0, 'test_errors': 11}
* TD: {'success': 186, 'fail': 20, 'error': 7, 'generation_errors': 0, 'test_errors': 7}
* Difference: {'success': 25, 'fail': -21, 'error': -4, 'generation_errors': 0, 'test_errors': -4}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 6
* task_id: 57
* task_id: 63
* task_id: 102
* task_id: 117
* task_id: 123
* task_id: 125
* task_id: 132
* task_id: 228
* task_id: 237
* task_id: 249
* task_id: 255
* task_id: 259
* task_id: 265
* task_id: 290
* task_id: 295
* task_id: 299
* task_id: 305
* task_id: 306
* task_id: 308
* task_id: 310
* task_id: 391
* task_id: 393
* task_id: 396
* task_id: 400
* task_id: 405
* task_id: 411
* task_id: 417
* task_id: 424

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 103
* task_id: 126
* task_id: 244
* task_id: 301

---

### mbpp_sanitized_qwen25coder14b vs mbpp_sanitized_qwen25coder14b_td

Accuracy comparison: **TD is better** - 84.51 vs 77.00

Test counts:
* Base: {'success': 164, 'fail': 38, 'error': 11, 'generation_errors': 0, 'test_errors': 11}
* TD: {'success': 180, 'fail': 26, 'error': 6, 'generation_errors': 1, 'test_errors': 6}
* Difference: {'success': 16, 'fail': -12, 'error': -5, 'generation_errors': 1, 'test_errors': -5}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 59
* task_id: 63
* task_id: 91
* task_id: 117
* task_id: 120
* task_id: 249
* task_id: 265
* task_id: 279
* task_id: 299
* task_id: 305
* task_id: 390
* task_id: 391
* task_id: 393
* task_id: 396
* task_id: 417
* task_id: 421

---

### mbpp_sanitized_qwen25coder32b vs mbpp_sanitized_qwen25coder32b_td

Accuracy comparison: **TD is better** - 84.51 vs 73.71

Test counts:
* Base: {'success': 157, 'fail': 43, 'error': 13, 'generation_errors': 0, 'test_errors': 13}
* TD: {'success': 180, 'fail': 25, 'error': 8, 'generation_errors': 0, 'test_errors': 8}
* Difference: {'success': 23, 'fail': -18, 'error': -5, 'generation_errors': 0, 'test_errors': -5}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 57
* task_id: 91
* task_id: 102
* task_id: 111
* task_id: 117
* task_id: 120
* task_id: 128
* task_id: 160
* task_id: 237
* task_id: 252
* task_id: 259
* task_id: 265
* task_id: 290
* task_id: 295
* task_id: 299
* task_id: 301
* task_id: 304
* task_id: 305
* task_id: 390
* task_id: 391
* task_id: 396
* task_id: 411
* task_id: 417
* task_id: 419
* task_id: 424

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 92
* task_id: 306

---

### mbpp_sanitized_qwen25coder3b vs mbpp_sanitized_qwen25coder3b_td

Accuracy comparison: **TD is better** - 71.36 vs 67.14

Test counts:
* Base: {'success': 143, 'fail': 54, 'error': 16, 'generation_errors': 0, 'test_errors': 16}
* TD: {'success': 152, 'fail': 48, 'error': 13, 'generation_errors': 0, 'test_errors': 13}
* Difference: {'success': 9, 'fail': -6, 'error': -3, 'generation_errors': 0, 'test_errors': -3}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 61
* task_id: 84
* task_id: 89
* task_id: 94
* task_id: 103
* task_id: 117
* task_id: 130
* task_id: 132
* task_id: 162
* task_id: 265
* task_id: 279
* task_id: 290
* task_id: 390
* task_id: 391
* task_id: 393
* task_id: 396
* task_id: 401
* task_id: 406
* task_id: 410
* task_id: 420
* task_id: 421

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 14
* task_id: 69
* task_id: 100
* task_id: 111
* task_id: 125
* task_id: 129
* task_id: 239
* task_id: 244
* task_id: 268
* task_id: 283
* task_id: 286
* task_id: 295

---

### mbpp_sanitized_qwen25coder7b vs mbpp_sanitized_qwen25coder7b_td

Accuracy comparison: **TD is better** - 80.75 vs 72.77

Test counts:
* Base: {'success': 155, 'fail': 43, 'error': 15, 'generation_errors': 0, 'test_errors': 15}
* TD: {'success': 172, 'fail': 31, 'error': 10, 'generation_errors': 0, 'test_errors': 10}
* Difference: {'success': 17, 'fail': -12, 'error': -5, 'generation_errors': 0, 'test_errors': -5}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 59
* task_id: 67
* task_id: 91
* task_id: 100
* task_id: 123
* task_id: 130
* task_id: 133
* task_id: 160
* task_id: 167
* task_id: 228
* task_id: 252
* task_id: 259
* task_id: 265
* task_id: 279
* task_id: 290
* task_id: 299
* task_id: 391
* task_id: 393
* task_id: 396
* task_id: 418
* task_id: 421
* task_id: 424

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 63
* task_id: 69
* task_id: 72
* task_id: 74
* task_id: 87

---

## Detailed Comparisons (With Remediation)

### human_eval_chatgpt4o vs human_eval_chatgpt4o_td

Accuracy comparison (with remediation): **TD is better** - 92.68 vs 90.24

Test counts (with remediation):
* Base: {'success': 74, 'fail': 8, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 76, 'fail': 5, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 2, 'fail': -3, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 17
* task_id: 70
* task_id: 81

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 10

---

### human_eval_chatgpt4omini vs human_eval_chatgpt4omini_td

Accuracy comparison (with remediation): **TD is better** - 90.24 vs 87.80

Test counts (with remediation):
* Base: {'success': 72, 'fail': 9, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 74, 'fail': 7, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 2, 'fail': -2, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 70
* task_id: 77
* task_id: 79

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 10

---

### human_eval_claude35haiku vs human_eval_claude35haiku_td

Accuracy comparison (with remediation): **TD is better** - 95.12 vs 90.24

Test counts (with remediation):
* Base: {'success': 74, 'fail': 8, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 78, 'fail': 3, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 4, 'fail': -5, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 50
* task_id: 65
* task_id: 75
* task_id: 76

---

### human_eval_claude35sonnet vs human_eval_claude35sonnet_td

Accuracy comparison (with remediation): **TD is better** - 93.90 vs 91.46

Test counts (with remediation):
* Base: {'success': 75, 'fail': 6, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 77, 'fail': 4, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 2, 'fail': -2, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 17
* task_id: 50

---

### human_eval_qwen25coder14b vs human_eval_qwen25coder14b_td

Accuracy comparison (with remediation): **TD is better** - 90.24 vs 79.27

Test counts (with remediation):
* Base: {'success': 65, 'fail': 16, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 74, 'fail': 8, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 9, 'fail': -8, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 10
* task_id: 54
* task_id: 65
* task_id: 68
* task_id: 70
* task_id: 71
* task_id: 77
* task_id: 79

---

### human_eval_qwen25coder32b vs human_eval_qwen25coder32b_td

Accuracy comparison (with remediation): **TD is better** - 93.90 vs 89.02

Test counts (with remediation):
* Base: {'success': 73, 'fail': 8, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 77, 'fail': 4, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 4, 'fail': -4, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 17
* task_id: 38
* task_id: 65
* task_id: 70
* task_id: 72

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 10

---

### human_eval_qwen25coder3b vs human_eval_qwen25coder3b_td

Accuracy comparison (with remediation): **TD is better** - 79.27 vs 75.61

Test counts (with remediation):
* Base: {'success': 62, 'fail': 20, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 65, 'fail': 17, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 3, 'fail': -3, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 19
* task_id: 68
* task_id: 77
* task_id: 79
* task_id: 80

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 8
* task_id: 65
* task_id: 76

---

### human_eval_qwen25coder7b vs human_eval_qwen25coder7b_td

Accuracy comparison (with remediation): **TD is better** - 84.15 vs 76.83

Test counts (with remediation):
* Base: {'success': 63, 'fail': 19, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 69, 'fail': 13, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 6, 'fail': -6, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 54
* task_id: 68
* task_id: 71
* task_id: 77
* task_id: 79
* task_id: 81

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 65

---

### mbpp_sanitized_chatgpt4o vs mbpp_sanitized_chatgpt4o_td

Accuracy comparison (with remediation): **TD is better** - 92.96 vs 89.67

Test counts (with remediation):
* Base: {'success': 191, 'fail': 18, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* TD: {'success': 198, 'fail': 9, 'error': 6, 'generation_errors': 0, 'test_errors': 6}
* Difference: {'success': 7, 'fail': -9, 'error': 2, 'generation_errors': 0, 'test_errors': 2}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 87
* task_id: 120
* task_id: 160
* task_id: 248
* task_id: 301
* task_id: 307
* task_id: 398
* task_id: 415
* task_id: 421

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 126
* task_id: 164

---

### mbpp_sanitized_chatgpt4omini vs mbpp_sanitized_chatgpt4omini_td

Accuracy comparison (with remediation): **TD is better** - 87.32 vs 85.45

Test counts (with remediation):
* Base: {'success': 182, 'fail': 27, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* TD: {'success': 186, 'fail': 23, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* Difference: {'success': 4, 'fail': -4, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 63
* task_id: 117
* task_id: 124
* task_id: 160
* task_id: 228
* task_id: 237
* task_id: 264
* task_id: 278
* task_id: 296
* task_id: 307

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 71
* task_id: 239
* task_id: 247
* task_id: 279
* task_id: 300
* task_id: 398

---

### mbpp_sanitized_claude35haiku vs mbpp_sanitized_claude35haiku_td

Accuracy comparison (with remediation): **TD is better** - 92.02 vs 91.08

Test counts (with remediation):
* Base: {'success': 194, 'fail': 14, 'error': 5, 'generation_errors': 0, 'test_errors': 5}
* TD: {'success': 196, 'fail': 14, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* Difference: {'success': 2, 'fail': 0, 'error': -2, 'generation_errors': 0, 'test_errors': -2}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 63
* task_id: 84
* task_id: 109
* task_id: 120
* task_id: 138
* task_id: 237

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 125
* task_id: 247
* task_id: 284
* task_id: 304

---

### mbpp_sanitized_claude35sonnet vs mbpp_sanitized_claude35sonnet_td

Accuracy comparison (with remediation): **TD is better** - 95.31 vs 93.43

Test counts (with remediation):
* Base: {'success': 199, 'fail': 10, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* TD: {'success': 203, 'fail': 6, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* Difference: {'success': 4, 'fail': -4, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 63
* task_id: 120
* task_id: 125
* task_id: 306
* task_id: 310
* task_id: 405

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 304
* task_id: 415

---

### mbpp_sanitized_qwen25coder14b vs mbpp_sanitized_qwen25coder14b_td

Accuracy comparison (with remediation): **TD is better** - 85.45 vs 78.40

Test counts (with remediation):
* Base: {'success': 167, 'fail': 44, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* TD: {'success': 182, 'fail': 27, 'error': 3, 'generation_errors': 1, 'test_errors': 3}
* Difference: {'success': 15, 'fail': -17, 'error': 1, 'generation_errors': 1, 'test_errors': 1}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 6
* task_id: 59
* task_id: 63
* task_id: 91
* task_id: 117
* task_id: 120
* task_id: 249
* task_id: 259
* task_id: 265
* task_id: 279
* task_id: 305
* task_id: 390
* task_id: 391
* task_id: 393
* task_id: 396

---

### mbpp_sanitized_qwen25coder32b vs mbpp_sanitized_qwen25coder32b_td

Accuracy comparison (with remediation): **TD is better** - 89.67 vs 84.98

Test counts (with remediation):
* Base: {'success': 181, 'fail': 25, 'error': 7, 'generation_errors': 0, 'test_errors': 7}
* TD: {'success': 191, 'fail': 17, 'error': 5, 'generation_errors': 0, 'test_errors': 5}
* Difference: {'success': 10, 'fail': -8, 'error': -2, 'generation_errors': 0, 'test_errors': -2}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 18
* task_id: 63
* task_id: 87
* task_id: 120
* task_id: 143
* task_id: 160
* task_id: 237
* task_id: 252
* task_id: 301
* task_id: 304
* task_id: 305
* task_id: 307
* task_id: 411
* task_id: 417

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 92
* task_id: 164
* task_id: 306
* task_id: 393

---

### mbpp_sanitized_qwen25coder3b vs mbpp_sanitized_qwen25coder3b_td

Accuracy comparison (with remediation): **TD is better** - 71.36 vs 67.14

Test counts (with remediation):
* Base: {'success': 143, 'fail': 70, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 152, 'fail': 61, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 9, 'fail': -9, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 61
* task_id: 84
* task_id: 89
* task_id: 94
* task_id: 103
* task_id: 117
* task_id: 130
* task_id: 132
* task_id: 162
* task_id: 265
* task_id: 279
* task_id: 290
* task_id: 390
* task_id: 391
* task_id: 393
* task_id: 396
* task_id: 401
* task_id: 406
* task_id: 410
* task_id: 420
* task_id: 421

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 14
* task_id: 69
* task_id: 100
* task_id: 111
* task_id: 125
* task_id: 129
* task_id: 239
* task_id: 244
* task_id: 268
* task_id: 283
* task_id: 286
* task_id: 295

---

### mbpp_sanitized_qwen25coder7b vs mbpp_sanitized_qwen25coder7b_td

Accuracy comparison (with remediation): **TD is better** - 81.22 vs 72.77

Test counts (with remediation):
* Base: {'success': 155, 'fail': 58, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 173, 'fail': 40, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 18, 'fail': -18, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 59
* task_id: 67
* task_id: 91
* task_id: 100
* task_id: 123
* task_id: 130
* task_id: 133
* task_id: 160
* task_id: 164
* task_id: 167
* task_id: 228
* task_id: 252
* task_id: 259
* task_id: 265
* task_id: 279
* task_id: 290
* task_id: 299
* task_id: 391
* task_id: 393
* task_id: 396
* task_id: 418
* task_id: 421
* task_id: 424

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 63
* task_id: 69
* task_id: 72
* task_id: 74
* task_id: 87

---

## Incomplete Directories Analysis

**Completion Status:** 15/16 directories (93.8%)

**Incomplete Directories:** 1

### 🟠 Partial Completion (1 dirs have generation errors)

- **mbpp_sanitized_qwen25coder14b**: Generation errors in td
  ```bash
  python rq1/mbpp_sanitized_qwen25coder14b/get_solution.py
  python rq1/mbpp_sanitized_qwen25coder14b_td/get_solution.py
  ```

### ✅ Successful Comparisons (15 dirs)

human_eval_chatgpt4o, human_eval_chatgpt4omini, human_eval_claude35haiku, human_eval_claude35sonnet, human_eval_qwen25coder14b, human_eval_qwen25coder32b, human_eval_qwen25coder3b, human_eval_qwen25coder7b, mbpp_sanitized_chatgpt4o, mbpp_sanitized_chatgpt4omini, and 5 more

## Experiment Metadata

**LLM Configuration:**
- Configuration Keys: CHATGPT_4O, CHATGPT_4O_MINI, CLAUDE_35_HAIKU, CLAUDE_35_SONNET, QWEN_14B_CODER, QWEN_2_5_CODER_32B, QWEN_3B_CODER, QWEN_7B_CODER
- Model Name: openai/gpt-4o-2024-11-20
**Dataset Configuration:**
- Research Question: rq2
- Dataset Coverage: 0.5 (50.0% of problems)
- Total Problems Across All Datasets: 591
- Total Problems Tested: 295
- Datasets:
  * human_eval: 164 problems (82 tested)
  * mbpp_sanitized: 427 problems (213 tested)

