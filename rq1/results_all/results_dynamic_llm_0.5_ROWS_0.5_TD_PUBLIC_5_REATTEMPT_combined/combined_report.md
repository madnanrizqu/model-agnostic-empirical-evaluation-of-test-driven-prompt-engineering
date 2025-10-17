# Combined Analysis Report

Generated: 2025-10-17 22:52:20

**LLMs:** Multiple (8 models) | **Research Question:** rq1

## Summary (First Attempt Only)

Total comparisons: 16

* Test-driven (TD) results were better in 16 out of 16 comparisons (100.0%)
* Test-driven (TD) results were same in 0 out of 16 comparisons (0.0%)
* Test-driven (TD) results were worse in 0 out of 16 comparisons (0.0%)

### Accuracy Statistics

* Total increase: 97.49
* Average increase: 6.09 (95% CI: [4.01, 8.18])
* Median increase: 5.49
* Standard deviation: 3.91
* Range: 1.21 to 11.94
* Interquartile range: 2.29 to 9.54
* Benchmarks improved: 16 (100.0%)
* Benchmarks worsened: 0 (0.0%)
* Benchmarks unchanged: 0 (0.0%)
* Average improvement percentage: 8.32%

#### Statistical Tests

* **Normality Test (Shapiro-Wilk)**: statistic=0.8911, p-value=0.0580, Normal=Yes
* **Paired t-test**: statistic=6.2325, p-value=0.0000
* **Effect Size (Cohen's d)**: 1.0788 (large effect)
* **Interpretation**: Results are highly significant (p < 0.001)

#### Top 5 Increases

* mbpp_sanitized_qwen25coder7b_combined: 65.34 → 77.28 (change: +11.94)
* mbpp_sanitized_chatgpt4o_combined: 73.07 → 84.31 (change: +11.24)
* mbpp_sanitized_claude35sonnet_combined: 75.64 → 85.95 (change: +10.31)
* mbpp_sanitized_claude35haiku_combined: 73.77 → 83.84 (change: +10.07)
* mbpp_sanitized_qwen25coder14b_combined: 72.37 → 81.73 (change: +9.36)

#### Top 5 Regressions

* human_eval_claude35sonnet_combined: 87.20 → 88.41 (change: +1.21)
* human_eval_qwen25coder7b_combined: 79.27 → 80.49 (change: +1.22)
* human_eval_chatgpt4omini_combined: 79.88 → 81.71 (change: +1.83)
* human_eval_chatgpt4o_combined: 81.71 → 83.54 (change: +1.83)
* human_eval_qwen25coder3b_combined: 76.22 → 78.66 (change: +2.44)

## Summary (With Remediation)

Total comparisons: 16

* Test-driven (TD) results were better in 13 out of 16 comparisons (81.2%)
* Test-driven (TD) results were same in 3 out of 16 comparisons (18.8%)
* Test-driven (TD) results were worse in 0 out of 16 comparisons (0.0%)

### Accuracy Statistics (With Remediation)

* Total increase: 51.52
* Average increase: 3.22 (95% CI: [1.37, 5.07])
* Median increase: 2.51
* Standard deviation: 3.47
* Range: 0.00 to 12.18
* Interquartile range: 0.69 to 3.97
* Benchmarks improved: 13 (81.2%)
* Benchmarks worsened: 0 (0.0%)
* Benchmarks unchanged: 3 (18.8%)
* Average improvement percentage: 5.30%

#### Statistical Tests

* **Normality Test (Shapiro-Wilk)**: statistic=0.8353, p-value=0.0083, Normal=No
* **Wilcoxon signed-rank test**: statistic=0.0000, p-value=0.0015
* **Effect Size (Cohen's d)**: 0.3754 (small effect)
* **Interpretation**: Results are very significant (p < 0.01)

#### Top 5 Increases (With Remediation)

* mbpp_sanitized_qwen25coder7b_combined: 65.57 → 77.75 (change: +12.18)
* mbpp_sanitized_qwen25coder14b_combined: 73.77 → 83.14 (change: +9.37)
* human_eval_qwen25coder14b_combined: 80.49 → 86.59 (change: +6.10)
* mbpp_sanitized_qwen25coder3b_combined: 63.70 → 68.62 (change: +4.92)
* human_eval_qwen25coder32b_combined: 87.80 → 91.46 (change: +3.66)

#### Top 5 Regressions (With Remediation)

* human_eval_chatgpt4o_combined: 91.46 → 91.46 (change: +0.00)
* human_eval_chatgpt4omini_combined: 88.41 → 88.41 (change: +0.00)
* human_eval_claude35haiku_combined: 92.68 → 92.68 (change: +0.00)
* human_eval_claude35sonnet_combined: 95.73 → 96.34 (change: +0.61)
* mbpp_sanitized_claude35sonnet_combined: 92.97 → 93.68 (change: +0.71)

## Detailed Comparisons (First Attempt Only)

### human_eval_chatgpt4o_combined vs human_eval_chatgpt4o_combined_td

Accuracy comparison: **TD is better** - 83.54 vs 81.71

Test counts:
* Base: {'success': 134, 'fail': 27, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* TD: {'success': 137, 'fail': 24, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* Difference: {'success': 3, 'fail': -3, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 1
* task_id: 8
* task_id: 21
* task_id: 41
* task_id: 68
* task_id: 79
* task_id: 113
* task_id: 120
* task_id: 135

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 12
* task_id: 91
* task_id: 101
* task_id: 109
* task_id: 110
* task_id: 130

---

### human_eval_chatgpt4omini_combined vs human_eval_chatgpt4omini_combined_td

Accuracy comparison: **TD is better** - 81.71 vs 79.88

Test counts:
* Base: {'success': 131, 'fail': 28, 'error': 5, 'generation_errors': 0, 'test_errors': 5}
* TD: {'success': 134, 'fail': 27, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* Difference: {'success': 3, 'fail': -1, 'error': -2, 'generation_errors': 0, 'test_errors': -2}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 65
* task_id: 68
* task_id: 75
* task_id: 79
* task_id: 88
* task_id: 113

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 115
* task_id: 119
* task_id: 130
* task_id: 137

---

### human_eval_claude35haiku_combined vs human_eval_claude35haiku_combined_td

Accuracy comparison: **TD is better** - 85.37 vs 82.32

Test counts:
* Base: {'success': 135, 'fail': 27, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* TD: {'success': 140, 'fail': 21, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* Difference: {'success': 5, 'fail': -6, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 65
* task_id: 68
* task_id: 73
* task_id: 75
* task_id: 77
* task_id: 88
* task_id: 102
* task_id: 113
* task_id: 130
* task_id: 146

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 59
* task_id: 115
* task_id: 153
* task_id: 154
* task_id: 160

---

### human_eval_claude35sonnet_combined vs human_eval_claude35sonnet_combined_td

Accuracy comparison: **TD is better** - 88.41 vs 87.20

Test counts:
* Base: {'success': 143, 'fail': 20, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 145, 'fail': 14, 'error': 5, 'generation_errors': 0, 'test_errors': 5}
* Difference: {'success': 2, 'fail': -6, 'error': 4, 'generation_errors': 0, 'test_errors': 4}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 68
* task_id: 79
* task_id: 83
* task_id: 93
* task_id: 113
* task_id: 115
* task_id: 163

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 92
* task_id: 111
* task_id: 135
* task_id: 151
* task_id: 160

---

### human_eval_qwen25coder14b_combined vs human_eval_qwen25coder14b_combined_td

Accuracy comparison: **TD is better** - 85.98 vs 80.49

Test counts:
* Base: {'success': 132, 'fail': 29, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* TD: {'success': 141, 'fail': 21, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* Difference: {'success': 9, 'fail': -8, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 10
* task_id: 65
* task_id: 68
* task_id: 79
* task_id: 83
* task_id: 89
* task_id: 100
* task_id: 113
* task_id: 118
* task_id: 126

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 91
* task_id: 134

---

### human_eval_qwen25coder32b_combined vs human_eval_qwen25coder32b_combined_td

Accuracy comparison: **TD is better** - 87.20 vs 81.71

Test counts:
* Base: {'success': 134, 'fail': 27, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* TD: {'success': 143, 'fail': 19, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* Difference: {'success': 9, 'fail': -8, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 41
* task_id: 57
* task_id: 65
* task_id: 68
* task_id: 79
* task_id: 102
* task_id: 110
* task_id: 113
* task_id: 115
* task_id: 118
* task_id: 126

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 99
* task_id: 111
* task_id: 120

---

### human_eval_qwen25coder3b_combined vs human_eval_qwen25coder3b_combined_td

Accuracy comparison: **TD is better** - 78.66 vs 76.22

Test counts:
* Base: {'success': 125, 'fail': 31, 'error': 8, 'generation_errors': 0, 'test_errors': 8}
* TD: {'success': 129, 'fail': 30, 'error': 5, 'generation_errors': 0, 'test_errors': 5}
* Difference: {'success': 4, 'fail': -1, 'error': -3, 'generation_errors': 0, 'test_errors': -3}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 19
* task_id: 68
* task_id: 77
* task_id: 79
* task_id: 83
* task_id: 102
* task_id: 103
* task_id: 113
* task_id: 118
* task_id: 124
* task_id: 151

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 8
* task_id: 65
* task_id: 76
* task_id: 80
* task_id: 87
* task_id: 111
* task_id: 126
* task_id: 135

---

### human_eval_qwen25coder7b_combined vs human_eval_qwen25coder7b_combined_td

Accuracy comparison: **TD is better** - 80.49 vs 79.27

Test counts:
* Base: {'success': 130, 'fail': 29, 'error': 5, 'generation_errors': 0, 'test_errors': 5}
* TD: {'success': 132, 'fail': 29, 'error': 3, 'generation_errors': 0, 'test_errors': 3}
* Difference: {'success': 2, 'fail': 0, 'error': -2, 'generation_errors': 0, 'test_errors': -2}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 54
* task_id: 68
* task_id: 72
* task_id: 79
* task_id: 86
* task_id: 113
* task_id: 118
* task_id: 141

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 65
* task_id: 84
* task_id: 121
* task_id: 126
* task_id: 128
* task_id: 137
* task_id: 155

---

### mbpp_sanitized_chatgpt4o_combined vs mbpp_sanitized_chatgpt4o_combined_td

Accuracy comparison: **TD is better** - 84.31 vs 73.07

Test counts:
* Base: {'success': 312, 'fail': 90, 'error': 25, 'generation_errors': 0, 'test_errors': 25}
* TD: {'success': 360, 'fail': 52, 'error': 15, 'generation_errors': 0, 'test_errors': 15}
* Difference: {'success': 48, 'fail': -38, 'error': -10, 'generation_errors': 0, 'test_errors': -10}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 6
* task_id: 18
* task_id: 57
* task_id: 84
* task_id: 102
* task_id: 106
* task_id: 117
* task_id: 128
* task_id: 160
* task_id: 237
* task_id: 252
* task_id: 259
* task_id: 264
* task_id: 265
* task_id: 290
* task_id: 293
* task_id: 305
* task_id: 307
* task_id: 390
* task_id: 391
* task_id: 393
* task_id: 396
* task_id: 400
* task_id: 411
* task_id: 417
* task_id: 421
* task_id: 437
* task_id: 440
* task_id: 445
* task_id: 446
* task_id: 470
* task_id: 473
* task_id: 475
* task_id: 560
* task_id: 572
* task_id: 580
* task_id: 585
* task_id: 599
* task_id: 620
* task_id: 630
* task_id: 644
* task_id: 723
* task_id: 734
* task_id: 745
* task_id: 749
* task_id: 750
* task_id: 753
* task_id: 769
* task_id: 773
* task_id: 788
* task_id: 797
* task_id: 802

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 137
* task_id: 255
* task_id: 271
* task_id: 787

---

### mbpp_sanitized_chatgpt4omini_combined vs mbpp_sanitized_chatgpt4omini_combined_td

Accuracy comparison: **TD is better** - 79.63 vs 70.73

Test counts:
* Base: {'success': 302, 'fail': 99, 'error': 26, 'generation_errors': 0, 'test_errors': 26}
* TD: {'success': 340, 'fail': 73, 'error': 14, 'generation_errors': 0, 'test_errors': 14}
* Difference: {'success': 38, 'fail': -26, 'error': -12, 'generation_errors': 0, 'test_errors': -12}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 6
* task_id: 63
* task_id: 84
* task_id: 100
* task_id: 102
* task_id: 117
* task_id: 160
* task_id: 228
* task_id: 251
* task_id: 252
* task_id: 265
* task_id: 278
* task_id: 290
* task_id: 295
* task_id: 299
* task_id: 305
* task_id: 307
* task_id: 391
* task_id: 393
* task_id: 396
* task_id: 409
* task_id: 411
* task_id: 417
* task_id: 421
* task_id: 424
* task_id: 426
* task_id: 428
* task_id: 429
* task_id: 434
* task_id: 437
* task_id: 443
* task_id: 446
* task_id: 450
* task_id: 454
* task_id: 457
* task_id: 472
* task_id: 473
* task_id: 475
* task_id: 572
* task_id: 577
* task_id: 585
* task_id: 622
* task_id: 627
* task_id: 632
* task_id: 745
* task_id: 749
* task_id: 753
* task_id: 763
* task_id: 797

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 64
* task_id: 71
* task_id: 239
* task_id: 244
* task_id: 247
* task_id: 279
* task_id: 300
* task_id: 301
* task_id: 392
* task_id: 464
* task_id: 809

---

### mbpp_sanitized_claude35haiku_combined vs mbpp_sanitized_claude35haiku_combined_td

Accuracy comparison: **TD is better** - 83.84 vs 73.77

Test counts:
* Base: {'success': 315, 'fail': 85, 'error': 27, 'generation_errors': 0, 'test_errors': 27}
* TD: {'success': 358, 'fail': 58, 'error': 11, 'generation_errors': 0, 'test_errors': 11}
* Difference: {'success': 43, 'fail': -27, 'error': -16, 'generation_errors': 0, 'test_errors': -16}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 6
* task_id: 63
* task_id: 79
* task_id: 102
* task_id: 109
* task_id: 115
* task_id: 117
* task_id: 123
* task_id: 125
* task_id: 128
* task_id: 132
* task_id: 167
* task_id: 244
* task_id: 249
* task_id: 252
* task_id: 265
* task_id: 278
* task_id: 284
* task_id: 290
* task_id: 294
* task_id: 299
* task_id: 391
* task_id: 393
* task_id: 396
* task_id: 405
* task_id: 421
* task_id: 424
* task_id: 440
* task_id: 442
* task_id: 445
* task_id: 446
* task_id: 464
* task_id: 473
* task_id: 475
* task_id: 560
* task_id: 572
* task_id: 584
* task_id: 585
* task_id: 592
* task_id: 610
* task_id: 627
* task_id: 630
* task_id: 631
* task_id: 635
* task_id: 640
* task_id: 644
* task_id: 723
* task_id: 735
* task_id: 745
* task_id: 749
* task_id: 753
* task_id: 763
* task_id: 773
* task_id: 780

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 59
* task_id: 72
* task_id: 86
* task_id: 92
* task_id: 137
* task_id: 300
* task_id: 304
* task_id: 581
* task_id: 629
* task_id: 765
* task_id: 802

---

### mbpp_sanitized_claude35sonnet_combined vs mbpp_sanitized_claude35sonnet_combined_td

Accuracy comparison: **TD is better** - 85.95 vs 75.64

Test counts:
* Base: {'success': 323, 'fail': 81, 'error': 23, 'generation_errors': 0, 'test_errors': 23}
* TD: {'success': 367, 'fail': 46, 'error': 14, 'generation_errors': 0, 'test_errors': 14}
* Difference: {'success': 44, 'fail': -35, 'error': -9, 'generation_errors': 0, 'test_errors': -9}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 6
* task_id: 57
* task_id: 63
* task_id: 70
* task_id: 102
* task_id: 117
* task_id: 132
* task_id: 140
* task_id: 237
* task_id: 249
* task_id: 259
* task_id: 265
* task_id: 290
* task_id: 295
* task_id: 299
* task_id: 305
* task_id: 306
* task_id: 310
* task_id: 391
* task_id: 393
* task_id: 396
* task_id: 397
* task_id: 400
* task_id: 405
* task_id: 410
* task_id: 411
* task_id: 415
* task_id: 417
* task_id: 419
* task_id: 424
* task_id: 429
* task_id: 437
* task_id: 442
* task_id: 444
* task_id: 445
* task_id: 446
* task_id: 464
* task_id: 473
* task_id: 475
* task_id: 572
* task_id: 584
* task_id: 597
* task_id: 603
* task_id: 610
* task_id: 630
* task_id: 632
* task_id: 640
* task_id: 742
* task_id: 749
* task_id: 763
* task_id: 765
* task_id: 773
* task_id: 780
* task_id: 788
* task_id: 797

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 103
* task_id: 235
* task_id: 244
* task_id: 286
* task_id: 301
* task_id: 450
* task_id: 581
* task_id: 627
* task_id: 629
* task_id: 631
* task_id: 769

---

### mbpp_sanitized_qwen25coder14b_combined vs mbpp_sanitized_qwen25coder14b_combined_td

Accuracy comparison: **TD is better** - 81.73 vs 72.37

Test counts:
* Base: {'success': 309, 'fail': 94, 'error': 24, 'generation_errors': 0, 'test_errors': 24}
* TD: {'success': 349, 'fail': 63, 'error': 15, 'generation_errors': 0, 'test_errors': 15}
* Difference: {'success': 40, 'fail': -31, 'error': -9, 'generation_errors': 0, 'test_errors': -9}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 59
* task_id: 63
* task_id: 91
* task_id: 117
* task_id: 249
* task_id: 265
* task_id: 279
* task_id: 290
* task_id: 294
* task_id: 299
* task_id: 305
* task_id: 390
* task_id: 391
* task_id: 393
* task_id: 396
* task_id: 410
* task_id: 419
* task_id: 421
* task_id: 424
* task_id: 428
* task_id: 429
* task_id: 437
* task_id: 440
* task_id: 445
* task_id: 446
* task_id: 448
* task_id: 453
* task_id: 464
* task_id: 473
* task_id: 475
* task_id: 560
* task_id: 572
* task_id: 584
* task_id: 612
* task_id: 614
* task_id: 627
* task_id: 630
* task_id: 721
* task_id: 740
* task_id: 748
* task_id: 750
* task_id: 763
* task_id: 773
* task_id: 780
* task_id: 797
* task_id: 802

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 61
* task_id: 248
* task_id: 286
* task_id: 308
* task_id: 472
* task_id: 786

---

### mbpp_sanitized_qwen25coder32b_combined vs mbpp_sanitized_qwen25coder32b_combined_td

Accuracy comparison: **TD is better** - 82.20 vs 73.54

Test counts:
* Base: {'success': 314, 'fail': 88, 'error': 25, 'generation_errors': 0, 'test_errors': 25}
* TD: {'success': 351, 'fail': 57, 'error': 19, 'generation_errors': 0, 'test_errors': 19}
* Difference: {'success': 37, 'fail': -31, 'error': -6, 'generation_errors': 0, 'test_errors': -6}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 57
* task_id: 59
* task_id: 67
* task_id: 91
* task_id: 102
* task_id: 111
* task_id: 117
* task_id: 128
* task_id: 237
* task_id: 259
* task_id: 265
* task_id: 279
* task_id: 290
* task_id: 294
* task_id: 295
* task_id: 299
* task_id: 305
* task_id: 390
* task_id: 391
* task_id: 396
* task_id: 411
* task_id: 417
* task_id: 421
* task_id: 424
* task_id: 428
* task_id: 437
* task_id: 440
* task_id: 443
* task_id: 445
* task_id: 446
* task_id: 454
* task_id: 473
* task_id: 475
* task_id: 572
* task_id: 579
* task_id: 584
* task_id: 614
* task_id: 630
* task_id: 749
* task_id: 750
* task_id: 753
* task_id: 765
* task_id: 773
* task_id: 780
* task_id: 797

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 4
* task_id: 68
* task_id: 123
* task_id: 306
* task_id: 392
* task_id: 607
* task_id: 776
* task_id: 788

---

### mbpp_sanitized_qwen25coder3b_combined vs mbpp_sanitized_qwen25coder3b_combined_td

Accuracy comparison: **TD is better** - 68.15 vs 63.70

Test counts:
* Base: {'success': 272, 'fail': 122, 'error': 33, 'generation_errors': 0, 'test_errors': 33}
* TD: {'success': 291, 'fail': 109, 'error': 27, 'generation_errors': 0, 'test_errors': 27}
* Difference: {'success': 19, 'fail': -13, 'error': -6, 'generation_errors': 0, 'test_errors': -6}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 61
* task_id: 84
* task_id: 92
* task_id: 94
* task_id: 103
* task_id: 117
* task_id: 132
* task_id: 137
* task_id: 162
* task_id: 265
* task_id: 279
* task_id: 290
* task_id: 390
* task_id: 391
* task_id: 392
* task_id: 393
* task_id: 396
* task_id: 419
* task_id: 420
* task_id: 421
* task_id: 433
* task_id: 436
* task_id: 440
* task_id: 446
* task_id: 450
* task_id: 477
* task_id: 585
* task_id: 612
* task_id: 624
* task_id: 626
* task_id: 627
* task_id: 628
* task_id: 739
* task_id: 753
* task_id: 756
* task_id: 771
* task_id: 772
* task_id: 773
* task_id: 782
* task_id: 785
* task_id: 791
* task_id: 808

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 2
* task_id: 7
* task_id: 16
* task_id: 63
* task_id: 69
* task_id: 75
* task_id: 97
* task_id: 111
* task_id: 125
* task_id: 126
* task_id: 130
* task_id: 239
* task_id: 244
* task_id: 295
* task_id: 401
* task_id: 589
* task_id: 608
* task_id: 629
* task_id: 631
* task_id: 633
* task_id: 742
* task_id: 757
* task_id: 802

---

### mbpp_sanitized_qwen25coder7b_combined vs mbpp_sanitized_qwen25coder7b_combined_td

Accuracy comparison: **TD is better** - 77.28 vs 65.34

Test counts:
* Base: {'success': 279, 'fail': 107, 'error': 41, 'generation_errors': 0, 'test_errors': 41}
* TD: {'success': 330, 'fail': 77, 'error': 20, 'generation_errors': 0, 'test_errors': 20}
* Difference: {'success': 51, 'fail': -30, 'error': -21, 'generation_errors': 0, 'test_errors': -21}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 57
* task_id: 59
* task_id: 91
* task_id: 104
* task_id: 115
* task_id: 130
* task_id: 133
* task_id: 145
* task_id: 160
* task_id: 167
* task_id: 228
* task_id: 235
* task_id: 252
* task_id: 259
* task_id: 265
* task_id: 279
* task_id: 290
* task_id: 294
* task_id: 299
* task_id: 391
* task_id: 393
* task_id: 396
* task_id: 405
* task_id: 421
* task_id: 424
* task_id: 427
* task_id: 429
* task_id: 433
* task_id: 439
* task_id: 440
* task_id: 445
* task_id: 446
* task_id: 448
* task_id: 452
* task_id: 453
* task_id: 465
* task_id: 475
* task_id: 477
* task_id: 562
* task_id: 579
* task_id: 584
* task_id: 604
* task_id: 624
* task_id: 627
* task_id: 635
* task_id: 641
* task_id: 644
* task_id: 740
* task_id: 746
* task_id: 749
* task_id: 750
* task_id: 753
* task_id: 756
* task_id: 772
* task_id: 773
* task_id: 788
* task_id: 805
* task_id: 809

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 69
* task_id: 72
* task_id: 87
* task_id: 239
* task_id: 291
* task_id: 608
* task_id: 786

---

## Detailed Comparisons (With Remediation)

### human_eval_chatgpt4o_combined vs human_eval_chatgpt4o_combined_td

Accuracy comparison (with remediation): **TD is same** - 91.46 vs 91.46

Test counts (with remediation):
* Base: {'success': 150, 'fail': 14, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 150, 'fail': 13, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 0, 'fail': -1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 79

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 10

---

### human_eval_chatgpt4omini_combined vs human_eval_chatgpt4omini_combined_td

Accuracy comparison (with remediation): **TD is same** - 88.41 vs 88.41

Test counts (with remediation):
* Base: {'success': 145, 'fail': 18, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 145, 'fail': 17, 'error': 2, 'generation_errors': 0, 'test_errors': 2}
* Difference: {'success': 0, 'fail': -1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 64
* task_id: 65
* task_id: 75
* task_id: 79
* task_id: 113

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 74
* task_id: 115
* task_id: 119
* task_id: 130
* task_id: 137

---

### human_eval_claude35haiku_combined vs human_eval_claude35haiku_combined_td

Accuracy comparison (with remediation): **TD is same** - 92.68 vs 92.68

Test counts (with remediation):
* Base: {'success': 152, 'fail': 12, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 152, 'fail': 11, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 0, 'fail': -1, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 65
* task_id: 75
* task_id: 130
* task_id: 140

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 17
* task_id: 83
* task_id: 115
* task_id: 160

---

### human_eval_claude35sonnet_combined vs human_eval_claude35sonnet_combined_td

Accuracy comparison (with remediation): **TD is better** - 96.34 vs 95.73

Test counts (with remediation):
* Base: {'success': 157, 'fail': 6, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 158, 'fail': 5, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 1, 'fail': -1, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 17
* task_id: 50
* task_id: 65

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 92
* task_id: 127

---

### human_eval_qwen25coder14b_combined vs human_eval_qwen25coder14b_combined_td

Accuracy comparison (with remediation): **TD is better** - 86.59 vs 80.49

Test counts (with remediation):
* Base: {'success': 132, 'fail': 32, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 142, 'fail': 21, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 10, 'fail': -11, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 10
* task_id: 65
* task_id: 68
* task_id: 79
* task_id: 83
* task_id: 89
* task_id: 100
* task_id: 113
* task_id: 118
* task_id: 120
* task_id: 126

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 91
* task_id: 134

---

### human_eval_qwen25coder32b_combined vs human_eval_qwen25coder32b_combined_td

Accuracy comparison (with remediation): **TD is better** - 91.46 vs 87.80

Test counts (with remediation):
* Base: {'success': 144, 'fail': 19, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* TD: {'success': 150, 'fail': 13, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 6, 'fail': -6, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 17
* task_id: 65
* task_id: 68
* task_id: 102
* task_id: 110
* task_id: 115
* task_id: 118

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 10

---

### human_eval_qwen25coder3b_combined vs human_eval_qwen25coder3b_combined_td

Accuracy comparison (with remediation): **TD is better** - 78.66 vs 76.22

Test counts (with remediation):
* Base: {'success': 125, 'fail': 39, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 129, 'fail': 35, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 4, 'fail': -4, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 19
* task_id: 68
* task_id: 77
* task_id: 79
* task_id: 83
* task_id: 102
* task_id: 103
* task_id: 113
* task_id: 118
* task_id: 124
* task_id: 151

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 8
* task_id: 65
* task_id: 76
* task_id: 80
* task_id: 87
* task_id: 111
* task_id: 126
* task_id: 135

---

### human_eval_qwen25coder7b_combined vs human_eval_qwen25coder7b_combined_td

Accuracy comparison (with remediation): **TD is better** - 80.49 vs 79.27

Test counts (with remediation):
* Base: {'success': 130, 'fail': 34, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 132, 'fail': 32, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 2, 'fail': -2, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 2
* task_id: 54
* task_id: 68
* task_id: 72
* task_id: 79
* task_id: 86
* task_id: 113
* task_id: 118
* task_id: 141

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 65
* task_id: 84
* task_id: 121
* task_id: 126
* task_id: 128
* task_id: 137
* task_id: 155

---

### mbpp_sanitized_chatgpt4o_combined vs mbpp_sanitized_chatgpt4o_combined_td

Accuracy comparison (with remediation): **TD is better** - 91.10 vs 88.52

Test counts (with remediation):
* Base: {'success': 378, 'fail': 42, 'error': 7, 'generation_errors': 0, 'test_errors': 7}
* TD: {'success': 389, 'fail': 29, 'error': 9, 'generation_errors': 0, 'test_errors': 9}
* Difference: {'success': 11, 'fail': -13, 'error': 2, 'generation_errors': 0, 'test_errors': 2}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 87
* task_id: 103
* task_id: 160
* task_id: 264
* task_id: 307
* task_id: 398
* task_id: 415
* task_id: 421
* task_id: 444
* task_id: 580
* task_id: 599
* task_id: 644
* task_id: 745
* task_id: 756
* task_id: 769
* task_id: 802

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 143
* task_id: 164
* task_id: 584
* task_id: 626
* task_id: 780

---

### mbpp_sanitized_chatgpt4omini_combined vs mbpp_sanitized_chatgpt4omini_combined_td

Accuracy comparison (with remediation): **TD is better** - 85.25 vs 82.67

Test counts (with remediation):
* Base: {'success': 353, 'fail': 64, 'error': 10, 'generation_errors': 0, 'test_errors': 10}
* TD: {'success': 364, 'fail': 56, 'error': 7, 'generation_errors': 0, 'test_errors': 7}
* Difference: {'success': 11, 'fail': -8, 'error': -3, 'generation_errors': 0, 'test_errors': -3}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 63
* task_id: 138
* task_id: 160
* task_id: 164
* task_id: 228
* task_id: 252
* task_id: 278
* task_id: 307
* task_id: 409
* task_id: 434
* task_id: 440
* task_id: 472
* task_id: 473
* task_id: 622
* task_id: 627
* task_id: 749
* task_id: 773
* task_id: 777
* task_id: 801

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 71
* task_id: 103
* task_id: 247
* task_id: 264
* task_id: 279
* task_id: 300
* task_id: 584
* task_id: 630

---

### mbpp_sanitized_claude35haiku_combined vs mbpp_sanitized_claude35haiku_combined_td

Accuracy comparison (with remediation): **TD is better** - 92.74 vs 90.87

Test counts (with remediation):
* Base: {'success': 388, 'fail': 30, 'error': 9, 'generation_errors': 0, 'test_errors': 9}
* TD: {'success': 396, 'fail': 26, 'error': 5, 'generation_errors': 0, 'test_errors': 5}
* Difference: {'success': 8, 'fail': -4, 'error': -4, 'generation_errors': 0, 'test_errors': -4}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 63
* task_id: 84
* task_id: 109
* task_id: 123
* task_id: 237
* task_id: 284
* task_id: 443
* task_id: 464
* task_id: 610
* task_id: 626
* task_id: 635
* task_id: 751

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 260
* task_id: 304
* task_id: 580
* task_id: 638

---

### mbpp_sanitized_claude35sonnet_combined vs mbpp_sanitized_claude35sonnet_combined_td

Accuracy comparison (with remediation): **TD is better** - 93.68 vs 92.97

Test counts (with remediation):
* Base: {'success': 397, 'fail': 22, 'error': 8, 'generation_errors': 0, 'test_errors': 8}
* TD: {'success': 400, 'fail': 20, 'error': 7, 'generation_errors': 0, 'test_errors': 7}
* Difference: {'success': 3, 'fail': -2, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 63
* task_id: 120
* task_id: 260
* task_id: 306
* task_id: 310
* task_id: 429
* task_id: 603

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 235
* task_id: 581
* task_id: 769
* task_id: 802

---

### mbpp_sanitized_qwen25coder14b_combined vs mbpp_sanitized_qwen25coder14b_combined_td

Accuracy comparison (with remediation): **TD is better** - 83.14 vs 73.77

Test counts (with remediation):
* Base: {'success': 315, 'fail': 112, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 355, 'fail': 71, 'error': 1, 'generation_errors': 0, 'test_errors': 1}
* Difference: {'success': 40, 'fail': -41, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 59
* task_id: 63
* task_id: 91
* task_id: 117
* task_id: 249
* task_id: 259
* task_id: 265
* task_id: 279
* task_id: 290
* task_id: 294
* task_id: 299
* task_id: 305
* task_id: 390
* task_id: 391
* task_id: 393
* task_id: 396
* task_id: 410
* task_id: 417
* task_id: 419
* task_id: 424
* task_id: 428
* task_id: 429
* task_id: 437
* task_id: 440
* task_id: 445
* task_id: 446
* task_id: 448
* task_id: 453
* task_id: 464
* task_id: 475
* task_id: 560
* task_id: 572
* task_id: 612
* task_id: 627
* task_id: 630
* task_id: 640
* task_id: 721
* task_id: 740
* task_id: 750
* task_id: 752
* task_id: 763
* task_id: 773
* task_id: 776
* task_id: 780
* task_id: 797
* task_id: 802

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 61
* task_id: 123
* task_id: 248
* task_id: 286
* task_id: 308
* task_id: 472

---

### mbpp_sanitized_qwen25coder32b_combined vs mbpp_sanitized_qwen25coder32b_combined_td

Accuracy comparison (with remediation): **TD is better** - 88.06 vs 84.78

Test counts (with remediation):
* Base: {'success': 362, 'fail': 52, 'error': 13, 'generation_errors': 0, 'test_errors': 13}
* TD: {'success': 376, 'fail': 40, 'error': 11, 'generation_errors': 0, 'test_errors': 11}
* Difference: {'success': 14, 'fail': -12, 'error': -2, 'generation_errors': 0, 'test_errors': -2}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 67
* task_id: 237
* task_id: 252
* task_id: 294
* task_id: 305
* task_id: 417
* task_id: 428
* task_id: 440
* task_id: 442
* task_id: 443
* task_id: 446
* task_id: 584
* task_id: 595
* task_id: 612
* task_id: 617
* task_id: 630
* task_id: 765
* task_id: 773
* task_id: 780

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 306
* task_id: 393
* task_id: 607
* task_id: 626
* task_id: 776

---

### mbpp_sanitized_qwen25coder3b_combined vs mbpp_sanitized_qwen25coder3b_combined_td

Accuracy comparison (with remediation): **TD is better** - 68.62 vs 63.70

Test counts (with remediation):
* Base: {'success': 272, 'fail': 155, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 293, 'fail': 134, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 21, 'fail': -21, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 61
* task_id: 84
* task_id: 92
* task_id: 94
* task_id: 103
* task_id: 117
* task_id: 132
* task_id: 137
* task_id: 162
* task_id: 265
* task_id: 279
* task_id: 290
* task_id: 390
* task_id: 391
* task_id: 392
* task_id: 393
* task_id: 396
* task_id: 419
* task_id: 420
* task_id: 421
* task_id: 433
* task_id: 436
* task_id: 440
* task_id: 446
* task_id: 450
* task_id: 477
* task_id: 585
* task_id: 612
* task_id: 624
* task_id: 626
* task_id: 627
* task_id: 628
* task_id: 739
* task_id: 750
* task_id: 753
* task_id: 756
* task_id: 771
* task_id: 772
* task_id: 773
* task_id: 782
* task_id: 785
* task_id: 791
* task_id: 808

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 2
* task_id: 16
* task_id: 63
* task_id: 69
* task_id: 75
* task_id: 97
* task_id: 111
* task_id: 125
* task_id: 126
* task_id: 130
* task_id: 239
* task_id: 244
* task_id: 295
* task_id: 401
* task_id: 589
* task_id: 608
* task_id: 629
* task_id: 631
* task_id: 633
* task_id: 742
* task_id: 757
* task_id: 802

---

### mbpp_sanitized_qwen25coder7b_combined vs mbpp_sanitized_qwen25coder7b_combined_td

Accuracy comparison (with remediation): **TD is better** - 77.75 vs 65.57

Test counts (with remediation):
* Base: {'success': 280, 'fail': 147, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* TD: {'success': 332, 'fail': 95, 'error': 0, 'generation_errors': 0, 'test_errors': 0}
* Difference: {'success': 52, 'fail': -52, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 57
* task_id: 59
* task_id: 91
* task_id: 104
* task_id: 115
* task_id: 130
* task_id: 133
* task_id: 145
* task_id: 160
* task_id: 164
* task_id: 167
* task_id: 228
* task_id: 235
* task_id: 252
* task_id: 259
* task_id: 265
* task_id: 279
* task_id: 290
* task_id: 294
* task_id: 299
* task_id: 391
* task_id: 393
* task_id: 396
* task_id: 405
* task_id: 421
* task_id: 424
* task_id: 427
* task_id: 429
* task_id: 433
* task_id: 439
* task_id: 440
* task_id: 445
* task_id: 446
* task_id: 448
* task_id: 452
* task_id: 453
* task_id: 465
* task_id: 475
* task_id: 477
* task_id: 562
* task_id: 579
* task_id: 584
* task_id: 604
* task_id: 624
* task_id: 627
* task_id: 641
* task_id: 644
* task_id: 740
* task_id: 746
* task_id: 749
* task_id: 750
* task_id: 753
* task_id: 756
* task_id: 772
* task_id: 773
* task_id: 788
* task_id: 805
* task_id: 809

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 69
* task_id: 72
* task_id: 87
* task_id: 239
* task_id: 291
* task_id: 608

---

## Incomplete Directories Analysis

**Completion Status:** 16/16 directories (100.0%)

🎉 **All directories are complete!** No re-execution needed.

## Experiment Metadata

**LLM Configuration:**
- Configuration Keys: CHATGPT_4O, CHATGPT_4O_MINI, CLAUDE_35_HAIKU, CLAUDE_35_SONNET, QWEN_14B_CODER, QWEN_2_5_CODER_32B, QWEN_3B_CODER, QWEN_7B_CODER
- Model Name: openai/gpt-4o-2024-11-20
**Dataset Configuration:**
- Research Question: rq1
- Dataset Coverage: 1.0 (100.0% of problems)

