# Combined Analysis Report

Generated: 2025-09-10 17:20:07

**LLMs:** Multiple (3 models) | **Research Question:** rq2

## Summary (First Attempt Only)

Total comparisons: 3

* Test-driven (TD) results were better in 3 out of 3 comparisons (100.0%)
* Test-driven (TD) results were same in 0 out of 3 comparisons (0.0%)
* Test-driven (TD) results were worse in 0 out of 3 comparisons (0.0%)

### Accuracy Statistics

* Total increase: 87.12
* Average increase: 29.04 (95% CI: [13.06, 45.02])
* Median increase: 29.20
* Standard deviation: 6.43
* Range: 22.53 to 35.39
* Interquartile range: 25.87 to 32.30
* Benchmarks improved: 3 (100.0%)
* Benchmarks worsened: 0 (0.0%)
* Benchmarks unchanged: 0 (0.0%)
* Average improvement percentage: 747.42%

#### Statistical Tests

* **Normality Test (Shapiro-Wilk)**: statistic=0.9995, p-value=0.9588, Normal=Yes
* **Paired t-test**: statistic=7.8207, p-value=0.0160
* **Effect Size (Cohen's d)**: 6.0148 (large effect)
* **Interpretation**: Results are significant (p < 0.05)

#### Top 5 Increases

* code_contests_claude35sonnet_combined: 4.46 → 39.85 (change: +35.39)
* code_contests_qwen25coder32b_combined: 3.47 → 32.67 (change: +29.20)
* code_contests_chatgpt4o_combined: 3.71 → 26.24 (change: +22.53)

#### Top 5 Regressions

* code_contests_chatgpt4o_combined: 3.71 → 26.24 (change: +22.53)
* code_contests_qwen25coder32b_combined: 3.47 → 32.67 (change: +29.20)
* code_contests_claude35sonnet_combined: 4.46 → 39.85 (change: +35.39)

## Summary (With Remediation)

Total comparisons: 3

* Test-driven (TD) results were better in 3 out of 3 comparisons (100.0%)
* Test-driven (TD) results were same in 0 out of 3 comparisons (0.0%)
* Test-driven (TD) results were worse in 0 out of 3 comparisons (0.0%)

### Accuracy Statistics (With Remediation)

* Total increase: 41.34
* Average increase: 13.78 (95% CI: [-23.46, 51.02])
* Median increase: 7.18
* Standard deviation: 14.99
* Range: 3.22 to 30.94
* Interquartile range: 5.20 to 19.06
* Benchmarks improved: 3 (100.0%)
* Benchmarks worsened: 0 (0.0%)
* Benchmarks unchanged: 0 (0.0%)
* Average improvement percentage: 210.29%

#### Statistical Tests

* **Normality Test (Shapiro-Wilk)**: statistic=0.8547, p-value=0.2530, Normal=Yes
* **Paired t-test**: statistic=1.5920, p-value=0.2524
* **Effect Size (Cohen's d)**: 0.7456 (medium effect)
* **Interpretation**: Results are not significant (p ≥ 0.05)

#### Top 5 Increases (With Remediation)

* code_contests_qwen25coder32b_combined: 5.20 → 36.14 (change: +30.94)
* code_contests_chatgpt4o_combined: 24.26 → 31.44 (change: +7.18)
* code_contests_claude35sonnet_combined: 51.24 → 54.46 (change: +3.22)

#### Top 5 Regressions (With Remediation)

* code_contests_claude35sonnet_combined: 51.24 → 54.46 (change: +3.22)
* code_contests_chatgpt4o_combined: 24.26 → 31.44 (change: +7.18)
* code_contests_qwen25coder32b_combined: 5.20 → 36.14 (change: +30.94)

## Detailed Comparisons (First Attempt Only)

### code_contests_chatgpt4o_combined vs code_contests_chatgpt4o_combined_td

Accuracy comparison: **TD is better** - 26.24 vs 3.71

Test counts:
* Base: {'success': 15, 'fail': 367, 'error': 22, 'generation_errors': 0, 'test_errors': 22}
* TD: {'success': 106, 'fail': 283, 'error': 15, 'generation_errors': 0, 'test_errors': 15}
* Difference: {'success': 91, 'fail': -84, 'error': -7, 'generation_errors': 0, 'test_errors': -7}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 1.0
* task_id: 3.0
* task_id: 4.0
* task_id: 6.0
* task_id: 10.0
* task_id: 22.0
* task_id: 30.0
* task_id: 36.0
* task_id: 38.0
* task_id: 40.0
* task_id: 46.0
* task_id: 47.0
* task_id: 48.0
* task_id: 53.0
* task_id: 55.0
* task_id: 56.0
* task_id: 62.0
* task_id: 64.0
* task_id: 70.0
* task_id: 74.0
* task_id: 79.0
* task_id: 81.0
* task_id: 83.0
* task_id: 85.0
* task_id: 86.0
* task_id: 95.0
* task_id: 105.0
* task_id: 106.0
* task_id: 115.0
* task_id: 120.0
* task_id: 122.0
* task_id: 130.0
* task_id: 139.0
* task_id: 141.0
* task_id: 144.0
* task_id: 146.0
* task_id: 163.0
* task_id: 165.0
* task_id: 169.0
* task_id: 170.0
* task_id: 173.0
* task_id: 178.0
* task_id: 179.0
* task_id: 183.0
* task_id: 196.0
* task_id: 206.0
* task_id: 211.0
* task_id: 216.0
* task_id: 221.0
* task_id: 224.0
* task_id: 225.0
* task_id: 229.0
* task_id: 230.0
* task_id: 232.0
* task_id: 234.0
* task_id: 238.0
* task_id: 251.0
* task_id: 252.0
* task_id: 254.0
* task_id: 257.0
* task_id: 263.0
* task_id: 266.0
* task_id: 273.0
* task_id: 278.0
* task_id: 279.0
* task_id: 289.0
* task_id: 293.0
* task_id: 298.0
* task_id: 303.0
* task_id: 312.0
* task_id: 313.0
* task_id: 315.0
* task_id: 323.0
* task_id: 325.0
* task_id: 327.0
* task_id: 332.0
* task_id: 333.0
* task_id: 344.0
* task_id: 347.0
* task_id: 350.0
* task_id: 351.0
* task_id: 353.0
* task_id: 356.0
* task_id: 360.0
* task_id: 368.0
* task_id: 369.0
* task_id: 387.0
* task_id: 393.0
* task_id: 396.0
* task_id: 399.0
* task_id: 402.0

---

### code_contests_claude35sonnet_combined vs code_contests_claude35sonnet_combined_td

Accuracy comparison: **TD is better** - 39.85 vs 4.46

Test counts:
* Base: {'success': 18, 'fail': 294, 'error': 92, 'generation_errors': 0, 'test_errors': 92}
* TD: {'success': 161, 'fail': 175, 'error': 68, 'generation_errors': 0, 'test_errors': 68}
* Difference: {'success': 143, 'fail': -119, 'error': -24, 'generation_errors': 0, 'test_errors': -24}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 0.0
* task_id: 2.0
* task_id: 3.0
* task_id: 4.0
* task_id: 5.0
* task_id: 10.0
* task_id: 14.0
* task_id: 24.0
* task_id: 26.0
* task_id: 30.0
* task_id: 31.0
* task_id: 33.0
* task_id: 34.0
* task_id: 35.0
* task_id: 40.0
* task_id: 42.0
* task_id: 43.0
* task_id: 45.0
* task_id: 46.0
* task_id: 47.0
* task_id: 53.0
* task_id: 55.0
* task_id: 56.0
* task_id: 58.0
* task_id: 61.0
* task_id: 62.0
* task_id: 64.0
* task_id: 65.0
* task_id: 69.0
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
* task_id: 106.0
* task_id: 108.0
* task_id: 120.0
* task_id: 122.0
* task_id: 125.0
* task_id: 130.0
* task_id: 136.0
* task_id: 138.0
* task_id: 139.0
* task_id: 146.0
* task_id: 147.0
* task_id: 149.0
* task_id: 150.0
* task_id: 151.0
* task_id: 152.0
* task_id: 154.0
* task_id: 155.0
* task_id: 158.0
* task_id: 162.0
* task_id: 163.0
* task_id: 165.0
* task_id: 167.0
* task_id: 169.0
* task_id: 170.0
* task_id: 175.0
* task_id: 177.0
* task_id: 178.0
* task_id: 183.0
* task_id: 190.0
* task_id: 192.0
* task_id: 195.0
* task_id: 196.0
* task_id: 206.0
* task_id: 216.0
* task_id: 217.0
* task_id: 220.0
* task_id: 221.0
* task_id: 223.0
* task_id: 224.0
* task_id: 225.0
* task_id: 226.0
* task_id: 229.0
* task_id: 230.0
* task_id: 233.0
* task_id: 235.0
* task_id: 237.0
* task_id: 241.0
* task_id: 246.0
* task_id: 247.0
* task_id: 251.0
* task_id: 254.0
* task_id: 255.0
* task_id: 257.0
* task_id: 258.0
* task_id: 262.0
* task_id: 263.0
* task_id: 264.0
* task_id: 267.0
* task_id: 271.0
* task_id: 272.0
* task_id: 273.0
* task_id: 278.0
* task_id: 279.0
* task_id: 280.0
* task_id: 283.0
* task_id: 288.0
* task_id: 293.0
* task_id: 298.0
* task_id: 300.0
* task_id: 303.0
* task_id: 306.0
* task_id: 307.0
* task_id: 308.0
* task_id: 310.0
* task_id: 311.0
* task_id: 313.0
* task_id: 318.0
* task_id: 320.0
* task_id: 321.0
* task_id: 325.0
* task_id: 326.0
* task_id: 327.0
* task_id: 328.0
* task_id: 332.0
* task_id: 333.0
* task_id: 338.0
* task_id: 340.0
* task_id: 344.0
* task_id: 347.0
* task_id: 348.0
* task_id: 350.0
* task_id: 352.0
* task_id: 353.0
* task_id: 354.0
* task_id: 356.0
* task_id: 360.0
* task_id: 367.0
* task_id: 368.0
* task_id: 369.0
* task_id: 373.0
* task_id: 377.0
* task_id: 379.0
* task_id: 387.0
* task_id: 389.0
* task_id: 392.0
* task_id: 395.0
* task_id: 398.0
* task_id: 399.0
* task_id: 400.0
* task_id: 402.0

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 13.0
* task_id: 15.0
* task_id: 41.0
* task_id: 82.0
* task_id: 156.0
* task_id: 168.0
* task_id: 179.0
* task_id: 361.0

---

### code_contests_qwen25coder32b_combined vs code_contests_qwen25coder32b_combined_td

Accuracy comparison: **TD is better** - 32.67 vs 3.47

Test counts:
* Base: {'success': 14, 'fail': 352, 'error': 38, 'generation_errors': 0, 'test_errors': 38}
* TD: {'success': 132, 'fail': 232, 'error': 40, 'generation_errors': 0, 'test_errors': 40}
* Difference: {'success': 118, 'fail': -120, 'error': 2, 'generation_errors': 0, 'test_errors': 2}

**Improvements** - Tests that passed in TD but failed/errored in Base:
* task_id: 0.0
* task_id: 1.0
* task_id: 5.0
* task_id: 6.0
* task_id: 10.0
* task_id: 15.0
* task_id: 22.0
* task_id: 24.0
* task_id: 26.0
* task_id: 30.0
* task_id: 38.0
* task_id: 47.0
* task_id: 51.0
* task_id: 52.0
* task_id: 53.0
* task_id: 55.0
* task_id: 58.0
* task_id: 62.0
* task_id: 65.0
* task_id: 69.0
* task_id: 71.0
* task_id: 74.0
* task_id: 81.0
* task_id: 82.0
* task_id: 83.0
* task_id: 85.0
* task_id: 86.0
* task_id: 88.0
* task_id: 92.0
* task_id: 94.0
* task_id: 95.0
* task_id: 96.0
* task_id: 100.0
* task_id: 105.0
* task_id: 108.0
* task_id: 115.0
* task_id: 120.0
* task_id: 122.0
* task_id: 125.0
* task_id: 130.0
* task_id: 136.0
* task_id: 139.0
* task_id: 144.0
* task_id: 146.0
* task_id: 147.0
* task_id: 149.0
* task_id: 151.0
* task_id: 155.0
* task_id: 158.0
* task_id: 162.0
* task_id: 170.0
* task_id: 175.0
* task_id: 177.0
* task_id: 178.0
* task_id: 183.0
* task_id: 190.0
* task_id: 195.0
* task_id: 196.0
* task_id: 206.0
* task_id: 211.0
* task_id: 214.0
* task_id: 216.0
* task_id: 217.0
* task_id: 219.0
* task_id: 221.0
* task_id: 224.0
* task_id: 227.0
* task_id: 229.0
* task_id: 235.0
* task_id: 236.0
* task_id: 237.0
* task_id: 241.0
* task_id: 244.0
* task_id: 246.0
* task_id: 249.0
* task_id: 251.0
* task_id: 253.0
* task_id: 254.0
* task_id: 255.0
* task_id: 258.0
* task_id: 263.0
* task_id: 266.0
* task_id: 267.0
* task_id: 269.0
* task_id: 272.0
* task_id: 279.0
* task_id: 280.0
* task_id: 293.0
* task_id: 298.0
* task_id: 300.0
* task_id: 303.0
* task_id: 306.0
* task_id: 311.0
* task_id: 312.0
* task_id: 313.0
* task_id: 315.0
* task_id: 318.0
* task_id: 320.0
* task_id: 323.0
* task_id: 325.0
* task_id: 326.0
* task_id: 327.0
* task_id: 333.0
* task_id: 338.0
* task_id: 347.0
* task_id: 353.0
* task_id: 354.0
* task_id: 356.0
* task_id: 360.0
* task_id: 367.0
* task_id: 369.0
* task_id: 371.0
* task_id: 373.0
* task_id: 377.0
* task_id: 379.0
* task_id: 385.0
* task_id: 387.0
* task_id: 388.0
* task_id: 395.0
* task_id: 399.0
* task_id: 402.0

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 41.0
* task_id: 234.0
* task_id: 363.0

---

## Detailed Comparisons (With Remediation)

### code_contests_chatgpt4o_combined vs code_contests_chatgpt4o_combined_td

Accuracy comparison (with remediation): **TD is better** - 31.44 vs 24.26

Test counts (with remediation):
* Base: {'success': 98, 'fail': 295, 'error': 11, 'generation_errors': 0, 'test_errors': 11}
* TD: {'success': 127, 'fail': 266, 'error': 11, 'generation_errors': 0, 'test_errors': 11}
* Difference: {'success': 29, 'fail': -29, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 1.0
* task_id: 3.0
* task_id: 6.0
* task_id: 8.0
* task_id: 10.0
* task_id: 22.0
* task_id: 36.0
* task_id: 40.0
* task_id: 42.0
* task_id: 55.0
* task_id: 56.0
* task_id: 61.0
* task_id: 62.0
* task_id: 70.0
* task_id: 81.0
* task_id: 83.0
* task_id: 86.0
* task_id: 90.0
* task_id: 106.0
* task_id: 115.0
* task_id: 122.0
* task_id: 138.0
* task_id: 141.0
* task_id: 150.0
* task_id: 163.0
* task_id: 169.0
* task_id: 178.0
* task_id: 179.0
* task_id: 221.0
* task_id: 224.0
* task_id: 225.0
* task_id: 228.0
* task_id: 230.0
* task_id: 232.0
* task_id: 235.0
* task_id: 238.0
* task_id: 252.0
* task_id: 257.0
* task_id: 266.0
* task_id: 278.0
* task_id: 306.0
* task_id: 314.0
* task_id: 315.0
* task_id: 333.0
* task_id: 344.0
* task_id: 351.0
* task_id: 356.0
* task_id: 368.0
* task_id: 372.0
* task_id: 396.0

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 34.0
* task_id: 94.0
* task_id: 108.0
* task_id: 118.0
* task_id: 162.0
* task_id: 174.0
* task_id: 177.0
* task_id: 236.0
* task_id: 237.0
* task_id: 246.0
* task_id: 253.0
* task_id: 255.0
* task_id: 269.0
* task_id: 280.0
* task_id: 300.0
* task_id: 311.0
* task_id: 326.0
* task_id: 373.0
* task_id: 377.0
* task_id: 395.0
* task_id: 401.0

---

### code_contests_claude35sonnet_combined vs code_contests_claude35sonnet_combined_td

Accuracy comparison (with remediation): **TD is better** - 54.46 vs 51.24

Test counts (with remediation):
* Base: {'success': 207, 'fail': 137, 'error': 60, 'generation_errors': 0, 'test_errors': 60}
* TD: {'success': 220, 'fail': 135, 'error': 49, 'generation_errors': 0, 'test_errors': 49}
* Difference: {'success': 13, 'fail': -2, 'error': -11, 'generation_errors': 0, 'test_errors': -11}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 22.0
* task_id: 31.0
* task_id: 52.0
* task_id: 75.0
* task_id: 114.0
* task_id: 125.0
* task_id: 134.0
* task_id: 143.0
* task_id: 158.0
* task_id: 174.0
* task_id: 178.0
* task_id: 192.0
* task_id: 209.0
* task_id: 225.0
* task_id: 247.0
* task_id: 249.0
* task_id: 257.0
* task_id: 258.0
* task_id: 262.0
* task_id: 269.0
* task_id: 271.0
* task_id: 283.0
* task_id: 287.0
* task_id: 296.0
* task_id: 307.0
* task_id: 310.0
* task_id: 321.0
* task_id: 328.0
* task_id: 354.0
* task_id: 362.0
* task_id: 368.0
* task_id: 371.0
* task_id: 374.0
* task_id: 380.0
* task_id: 383.0
* task_id: 394.0

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 1.0
* task_id: 37.0
* task_id: 38.0
* task_id: 39.0
* task_id: 48.0
* task_id: 51.0
* task_id: 71.0
* task_id: 73.0
* task_id: 92.0
* task_id: 128.0
* task_id: 141.0
* task_id: 156.0
* task_id: 164.0
* task_id: 173.0
* task_id: 181.0
* task_id: 187.0
* task_id: 222.0
* task_id: 236.0
* task_id: 244.0
* task_id: 295.0
* task_id: 312.0
* task_id: 330.0
* task_id: 351.0

---

### code_contests_qwen25coder32b_combined vs code_contests_qwen25coder32b_combined_td

Accuracy comparison (with remediation): **TD is better** - 36.14 vs 5.20

Test counts (with remediation):
* Base: {'success': 21, 'fail': 359, 'error': 24, 'generation_errors': 0, 'test_errors': 24}
* TD: {'success': 146, 'fail': 230, 'error': 28, 'generation_errors': 0, 'test_errors': 28}
* Difference: {'success': 125, 'fail': -129, 'error': 4, 'generation_errors': 0, 'test_errors': 4}

**Improvements with Remediation** - Tests that passed in TD but failed/errored in Base:
* task_id: 0.0
* task_id: 1.0
* task_id: 3.0
* task_id: 4.0
* task_id: 5.0
* task_id: 6.0
* task_id: 10.0
* task_id: 15.0
* task_id: 22.0
* task_id: 24.0
* task_id: 26.0
* task_id: 30.0
* task_id: 38.0
* task_id: 51.0
* task_id: 52.0
* task_id: 53.0
* task_id: 55.0
* task_id: 58.0
* task_id: 62.0
* task_id: 65.0
* task_id: 69.0
* task_id: 71.0
* task_id: 74.0
* task_id: 81.0
* task_id: 82.0
* task_id: 83.0
* task_id: 86.0
* task_id: 88.0
* task_id: 92.0
* task_id: 94.0
* task_id: 95.0
* task_id: 96.0
* task_id: 100.0
* task_id: 105.0
* task_id: 108.0
* task_id: 115.0
* task_id: 120.0
* task_id: 122.0
* task_id: 125.0
* task_id: 133.0
* task_id: 136.0
* task_id: 138.0
* task_id: 139.0
* task_id: 144.0
* task_id: 146.0
* task_id: 147.0
* task_id: 149.0
* task_id: 151.0
* task_id: 155.0
* task_id: 158.0
* task_id: 162.0
* task_id: 170.0
* task_id: 174.0
* task_id: 175.0
* task_id: 177.0
* task_id: 178.0
* task_id: 183.0
* task_id: 190.0
* task_id: 192.0
* task_id: 195.0
* task_id: 196.0
* task_id: 206.0
* task_id: 214.0
* task_id: 216.0
* task_id: 217.0
* task_id: 219.0
* task_id: 221.0
* task_id: 224.0
* task_id: 227.0
* task_id: 229.0
* task_id: 232.0
* task_id: 235.0
* task_id: 236.0
* task_id: 237.0
* task_id: 241.0
* task_id: 244.0
* task_id: 246.0
* task_id: 249.0
* task_id: 251.0
* task_id: 253.0
* task_id: 254.0
* task_id: 255.0
* task_id: 258.0
* task_id: 263.0
* task_id: 267.0
* task_id: 269.0
* task_id: 272.0
* task_id: 273.0
* task_id: 279.0
* task_id: 280.0
* task_id: 283.0
* task_id: 289.0
* task_id: 293.0
* task_id: 295.0
* task_id: 298.0
* task_id: 300.0
* task_id: 306.0
* task_id: 311.0
* task_id: 312.0
* task_id: 313.0
* task_id: 315.0
* task_id: 318.0
* task_id: 320.0
* task_id: 323.0
* task_id: 325.0
* task_id: 326.0
* task_id: 327.0
* task_id: 333.0
* task_id: 338.0
* task_id: 347.0
* task_id: 353.0
* task_id: 354.0
* task_id: 356.0
* task_id: 360.0
* task_id: 367.0
* task_id: 369.0
* task_id: 371.0
* task_id: 372.0
* task_id: 373.0
* task_id: 377.0
* task_id: 379.0
* task_id: 385.0
* task_id: 387.0
* task_id: 388.0
* task_id: 394.0
* task_id: 395.0
* task_id: 399.0
* task_id: 402.0

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 41.0
* task_id: 234.0
* task_id: 363.0

---

## Incomplete Directories Analysis

**Completion Status:** 3/3 directories (100.0%)

🎉 **All directories are complete!** No re-execution needed.

## Experiment Metadata

**LLM Configuration:**
- Configuration Keys: CHATGPT_4O, CLAUDE_35_SONNET, QWEN_2_5_CODER_32B
- Model Name: openai/gpt-4o-2024-11-20
**Dataset Configuration:**
- Research Question: rq2
- Dataset Coverage: 1.0 (100.0% of problems)

