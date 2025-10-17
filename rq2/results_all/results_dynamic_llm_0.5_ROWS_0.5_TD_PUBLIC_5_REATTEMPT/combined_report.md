# Combined Analysis Report

Generated: 2025-10-16 21:24:29

**LLMs:** Multiple (3 models) | **Research Question:** rq2

## Summary (First Attempt Only)

Total comparisons: 3

* Test-driven (TD) results were better in 3 out of 3 comparisons (100.0%)
* Test-driven (TD) results were same in 0 out of 3 comparisons (0.0%)
* Test-driven (TD) results were worse in 0 out of 3 comparisons (0.0%)

### Accuracy Statistics

* Total increase: 83.17
* Average increase: 27.72 (95% CI: [14.77, 40.67])
* Median increase: 28.22
* Standard deviation: 5.21
* Range: 22.28 to 32.67
* Interquartile range: 25.25 to 30.45
* Benchmarks improved: 3 (100.0%)
* Benchmarks worsened: 0 (0.0%)
* Benchmarks unchanged: 0 (0.0%)
* Average improvement percentage: 724.26%

#### Statistical Tests

* **Normality Test (Shapiro-Wilk)**: statistic=0.9932, p-value=0.8422, Normal=Yes
* **Paired t-test**: statistic=9.2116, p-value=0.0116
* **Effect Size (Cohen's d)**: 6.7700 (large effect)
* **Interpretation**: Results are significant (p < 0.05)

#### Top 5 Increases

* code_contests_claude35sonnet: 4.95 → 37.62 (change: +32.67)
* code_contests_qwen25coder32b: 2.97 → 31.19 (change: +28.22)
* code_contests_chatgpt4o: 3.96 → 26.24 (change: +22.28)

#### Top 5 Regressions

* code_contests_chatgpt4o: 3.96 → 26.24 (change: +22.28)
* code_contests_qwen25coder32b: 2.97 → 31.19 (change: +28.22)
* code_contests_claude35sonnet: 4.95 → 37.62 (change: +32.67)

## Summary (With Remediation)

Total comparisons: 3

* Test-driven (TD) results were better in 2 out of 3 comparisons (66.7%)
* Test-driven (TD) results were same in 0 out of 3 comparisons (0.0%)
* Test-driven (TD) results were worse in 1 out of 3 comparisons (33.3%)

### Accuracy Statistics (With Remediation)

* Total increase: 38.12
* Average increase: 12.71 (95% CI: [-26.95, 52.37])
* Median increase: 10.40
* Standard deviation: 15.97
* Range: -1.98 to 29.70
* Interquartile range: 4.21 to 20.05
* Benchmarks improved: 2 (66.7%)
* Benchmarks worsened: 1 (33.3%)
* Benchmarks unchanged: 0 (0.0%)
* Average improvement percentage: 356.83%
* Average regression percentage: -3.77%

#### Statistical Tests

* **Normality Test (Shapiro-Wilk)**: statistic=0.9843, p-value=0.7604, Normal=Yes
* **Paired t-test**: statistic=1.3785, p-value=0.3020
* **Effect Size (Cohen's d)**: 0.6829 (medium effect)
* **Interpretation**: Results are not significant (p ≥ 0.05)

#### Top 5 Increases (With Remediation)

* code_contests_qwen25coder32b: 4.46 → 34.16 (change: +29.70)
* code_contests_chatgpt4o: 21.78 → 32.18 (change: +10.40)
* code_contests_claude35sonnet: 52.48 → 50.50 (change: -1.98)

#### Top 5 Regressions (With Remediation)

* code_contests_claude35sonnet: 52.48 → 50.50 (change: -1.98)
* code_contests_chatgpt4o: 21.78 → 32.18 (change: +10.40)
* code_contests_qwen25coder32b: 4.46 → 34.16 (change: +29.70)

## Detailed Comparisons (First Attempt Only)

### code_contests_chatgpt4o vs code_contests_chatgpt4o_td

Accuracy comparison: **TD is better** - 26.24 vs 3.96

Test counts:
* Base: {'success': 8, 'fail': 186, 'error': 8, 'generation_errors': 0, 'test_errors': 8}
* TD: {'success': 53, 'fail': 142, 'error': 7, 'generation_errors': 0, 'test_errors': 7}
* Difference: {'success': 45, 'fail': -44, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

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

---

### code_contests_claude35sonnet vs code_contests_claude35sonnet_td

Accuracy comparison: **TD is better** - 37.62 vs 4.95

Test counts:
* Base: {'success': 10, 'fail': 149, 'error': 43, 'generation_errors': 0, 'test_errors': 43}
* TD: {'success': 76, 'fail': 90, 'error': 36, 'generation_errors': 0, 'test_errors': 36}
* Difference: {'success': 66, 'fail': -59, 'error': -7, 'generation_errors': 0, 'test_errors': -7}

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

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 13.0
* task_id: 15.0
* task_id: 41.0
* task_id: 82.0
* task_id: 156.0
* task_id: 168.0
* task_id: 179.0

---

### code_contests_qwen25coder32b vs code_contests_qwen25coder32b_td

Accuracy comparison: **TD is better** - 31.19 vs 2.97

Test counts:
* Base: {'success': 6, 'fail': 176, 'error': 20, 'generation_errors': 0, 'test_errors': 20}
* TD: {'success': 63, 'fail': 120, 'error': 19, 'generation_errors': 0, 'test_errors': 19}
* Difference: {'success': 57, 'fail': -56, 'error': -1, 'generation_errors': 0, 'test_errors': -1}

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

**Regressions** - Tests that passed in Base but failed/errored in TD:
* task_id: 41.0

---

## Detailed Comparisons (With Remediation)

### code_contests_chatgpt4o vs code_contests_chatgpt4o_td

Accuracy comparison (with remediation): **TD is better** - 32.18 vs 21.78

Test counts (with remediation):
* Base: {'success': 44, 'fail': 154, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* TD: {'success': 65, 'fail': 133, 'error': 4, 'generation_errors': 0, 'test_errors': 4}
* Difference: {'success': 21, 'fail': -21, 'error': 0, 'generation_errors': 0, 'test_errors': 0}

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

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 34.0
* task_id: 94.0
* task_id: 108.0
* task_id: 118.0
* task_id: 162.0
* task_id: 174.0
* task_id: 177.0

---

### code_contests_claude35sonnet vs code_contests_claude35sonnet_td

Accuracy comparison (with remediation): **TD is worse** - 50.50 vs 52.48

Test counts (with remediation):
* Base: {'success': 106, 'fail': 70, 'error': 26, 'generation_errors': 0, 'test_errors': 26}
* TD: {'success': 102, 'fail': 73, 'error': 27, 'generation_errors': 0, 'test_errors': 27}
* Difference: {'success': -4, 'fail': 3, 'error': 1, 'generation_errors': 0, 'test_errors': 1}

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

---

### code_contests_qwen25coder32b vs code_contests_qwen25coder32b_td

Accuracy comparison (with remediation): **TD is better** - 34.16 vs 4.46

Test counts (with remediation):
* Base: {'success': 9, 'fail': 182, 'error': 11, 'generation_errors': 0, 'test_errors': 11}
* TD: {'success': 69, 'fail': 120, 'error': 13, 'generation_errors': 0, 'test_errors': 13}
* Difference: {'success': 60, 'fail': -62, 'error': 2, 'generation_errors': 0, 'test_errors': 2}

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

**Regressions with Remediation** - Tests that passed in Base but failed/errored in TD:
* task_id: 41.0

---

## Incomplete Directories Analysis

**Completion Status:** 3/4 directories (75.0%)

**Incomplete Directories:** 1

### 🔴 Missing TD Directories (1 dirs need TD experiments)

- **manual_analysis**
  ```bash
  python rq2/manual_analysis_td/get_solution.py
  python rq2/manual_analysis_td/test_solution.py
  ```

### ✅ Successful Comparisons (3 dirs)

code_contests_chatgpt4o, code_contests_claude35sonnet, code_contests_qwen25coder32b

## Experiment Metadata

**LLM Configuration:**
- Configuration Keys: CHATGPT_4O, CLAUDE_35_SONNET, QWEN_2_5_CODER_32B
- Model Name: openai/gpt-4o-2024-11-20
**Dataset Configuration:**
- Research Question: rq2
- Dataset Coverage: 0.5 (50.0% of problems)
- Total Problems in Dataset: 404 (202 tested)

