# Guide: Adding a New Model Benchmark Experiment

This guide explains how to create a new experiment directory in RQ1 or RQ2 for benchmarking a specific model on a dataset.

**Prerequisites:** Before following this guide, ensure you have completed the setup steps in [README.md](README.md), including environment configuration and API tokens.

## Table of Contents

- [Understanding Experiment Directories](#understanding-experiment-directories)
- [Quick Start: Create a New Experiment](#quick-start-create-a-new-experiment)
- [Configuration Parameters](#configuration-parameters)
- [Available Models and Datasets](#available-models-and-datasets)
- [Results Directory Structure](#results-directory-structure)
- [Advanced Scenarios](#advanced-scenarios)

## Understanding Experiment Directories

Each experiment directory represents a **single dataset + model combination** (e.g., `human_eval_claude35sonnet`). The directory structure is:

```
{dataset}_{model}[_variant]/
├── get_solution.py          # Generate solutions using LLM
├── test_solution.py         # Test generated solutions
└── results_{params}/        # Auto-generated results (one per config)
    ├── {experiment}_solution.json
    ├── {experiment}_solution_formatted.json
    ├── {experiment}_metadata.json
    ├── {experiment}_errors.json
    ├── runner_passed.json
    ├── runner_fails.json
    ├── runner_errors.json
    └── summary.json
```

**Key Points:**

- The directory name should follow the pattern `{dataset}_{model}` (e.g., `human_eval_chatgpt4o`)
- See [README.md](README.md#experiment-variants-and-directory-suffixes) for variant suffixes (`_td`, `_second_half`, `_combined`)
- Results directories are auto-generated with names encoding all experimental parameters

## Quick Start: Create a New Experiment

### Step 1: Create Directory

```bash
# For RQ1 experiments
mkdir rq1/{dataset}_{model}

# For RQ2 experiments
mkdir rq2/{dataset}_{model}

# Example
mkdir rq1/human_eval_newmodel
```

### Step 2: Create `get_solution.py`

This script generates LLM solutions for the dataset.

**For RQ1:**

```python
import sys
import os

# Standard path setup - DO NOT MODIFY
RQ1_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.abspath(os.path.join(RQ1_DIR, ".."))
sys.path.append(ROOT_DIR)

from rq1.get_solution_setup import GetSolutionSetup

setup = GetSolutionSetup(
    dataset_name="human_eval",           # Dataset to benchmark
    language="python",                   # Programming language
    llm_to_use="CHATGPT_4O",            # Model to use (see Available Models)
    directory_name="human_eval_newmodel", # MUST match directory name
)
results, errors = setup.generate_solutions()
```

**For RQ2:**

```python
import sys
import os

# Standard path setup - DO NOT MODIFY
RQ2_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.abspath(os.path.join(RQ2_DIR, ".."))
sys.path.append(ROOT_DIR)

from rq2.get_solution_setup import GetSolutionSetup

setup = GetSolutionSetup(
    dataset_name="code_contests",
    language="python",
    llm_to_use="CHATGPT_4O",
    directory_name="code_contests_newmodel",
)
results, errors = setup.generate_solutions()
```

### Step 3: Create `test_solution.py`

This script tests the generated solutions.

**For RQ1:**

```python
import sys
import os

# Standard path setup - DO NOT MODIFY
RQ1_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.abspath(os.path.join(RQ1_DIR, ".."))
sys.path.append(ROOT_DIR)

from rq1.test_solution_setup import TestSolutionSetup
from solution_formatter_module import SolutionFormatter
from test_runner_module.main import TestRunner

# Setup - parameters MUST match get_solution.py
setup = TestSolutionSetup(
    dataset_name="human_eval",
    llm_to_use="CHATGPT_4O",
    directory_name="human_eval_newmodel"
)

# Format solutions (standardize code formatting)
formatter = SolutionFormatter("python")
setup.format_solutions(formatter)

# Configure test runner for Python
config = setup.get_base_config("python")
config.update(
    {
        "needs_compilation": False,
        "test_runner_dir": os.path.join(ROOT_DIR, "languages/python"),
        "llm_output_file": "llm_output.py",
        "test_file": "llm_output_test.py",
        "test_runner_binary": "python",
    }
)

# Execute tests
runner = TestRunner(config)
runner.run()
```

**For RQ2:** Same as RQ1, but import from `rq2.test_solution_setup`.

### Step 4: Run the Experiment

```bash
cd rq1/human_eval_newmodel  # or rq2/...

# Generate solutions
python get_solution.py

# Test solutions
python test_solution.py
```

See [README.md](README.md#running-experiments) for batch execution with `run_all.py`.

## Configuration Parameters

### GetSolutionSetup Parameters

```python
GetSolutionSetup(
    dataset_name: str,           # Required: Dataset to use
    language: str,               # Required: Programming language
    llm_to_use: str,            # Required: Model key
    directory_name: str,         # Required: Experiment directory name
    test_driven: bool = False,   # Optional: Include tests in prompts
    test_driven_ratio: float = None,  # Optional: Override config TD ratio
    start_index: int = None,     # Optional: Start from index (for second half)
)
```

**Parameter Details:**

- **`dataset_name`**: Name of benchmark dataset
  - RQ1: `"human_eval"`, `"mbpp_sanitized"`
  - RQ2: `"code_contests"`

- **`language`**: Programming language (currently only `"python"` fully supported)

- **`llm_to_use`**: Model configuration key from `llm_module/config.py` (see [Available Models](#available-models-and-datasets))

- **`directory_name`**: **MUST exactly match your experiment directory name**
  - Used for organizing results and file paths
  - Wrong name = results saved to wrong location

- **`test_driven`**: Whether to include test cases in the LLM prompt
  - `False` (default): Standard code generation
  - `True`: Test-driven development (TD) approach
  - See [README.md](README.md#experiment-variants-and-directory-suffixes) for TD variants

- **`test_driven_ratio`**: Override the config file's `TEST_DRIVEN_RATIO`
  - Default: Uses value from `config/rq1.py` or `config/rq2.py`
  - Custom value: `0.0` to `1.0`

- **`start_index`**: Starting row index in dataset
  - Default: `None` (start from beginning)
  - For second half experiments: Set to `dataset_size // 2`
  - See [README.md](README.md#merging-results-with-merge_resultspy) for splitting/merging workflow

### TestSolutionSetup Parameters

```python
TestSolutionSetup(
    dataset_name: str,
    llm_to_use: str,
    directory_name: str,
    test_driven: bool = False,
    test_driven_ratio: float = None,
    start_index: int = None,
)
```

**Important:** All parameters must **exactly match** those in `get_solution.py` to ensure results are loaded from and saved to the correct location.

### Global Configuration

Global defaults are set in `config/rq1.py` or `config/rq2.py`:

```python
TEST_DRIVEN_RATIO = 0.5      # 50% of experiments use TD prompts
LLM_TO_USE = "OPEN_LLM"      # Default model for batch runs
RATIO_OF_ROWS_TO_RUN = 0.5   # Run 50% of dataset (for split experiments)
REATTEMPT_MAX_NUM = 5        # Max retry attempts for failed solutions
```

**Note:** Individual experiments override these defaults via their `get_solution.py` parameters.

## Available Models and Datasets

### Models (from `llm_module/config.py`)

The `llm_to_use` parameter accepts these keys:

**OpenRouter API (requires `OPEN_ROUTER_TOKEN`):**

- `CHATGPT_4O` - GPT-4o (openai/gpt-4o-2024-11-20)
- `CHATGPT_4O_MINI` - GPT-4o Mini (openai/gpt-4o-mini-2024-07-18)
- `CLAUDE_35_SONNET` - Claude 3.5 Sonnet
- `CLAUDE_35_HAIKU` - Claude 3.5 Haiku
- `QWEN_2_5_CODER_32B_OR` - Qwen 2.5 Coder 32B via OpenRouter

**HuggingFace Endpoints (requires `HUGGING_FACE_TOKEN`):**

- `QWEN_2_5_CODER_32B` - Qwen 2.5 Coder 32B
- `QWEN_14B_CODER` - Qwen 2.5 Coder 14B
- `QWEN_7B_CODER` - Qwen 2.5 Coder 7B
- `QWEN_3B_CODER` - Qwen 2.5 Coder 3B

**Other Providers:**

- `QWEN_32B_CODER_GROQ` - Qwen 3 32B (requires `GROQ_TOKEN`)
- `QWEN_32B_CODER_CF` - Qwen 2.5 Coder 32B (requires `CLOUDFLARE_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`)

See [README.md](README.md#token-requirements) for API token setup.

### Datasets

**RQ1 Datasets:**

- `human_eval` - HumanEval benchmark (164 problems)
- `mbpp_sanitized` - MBPP Sanitized (427 problems)

**RQ2 Datasets:**

- `code_contests` - Code Contests competitive programming

Dataset files are located in `datasets/` directory.

## Results Directory Structure

After running an experiment, results are stored in auto-generated directories:

### Directory Naming

```
results_{LLM_KEY}_{RATIO}_ROWS_{TD_RATIO}_TD_PUBLIC_{REATTEMPT}_REATTEMPT[_second_half]
```

Example:

```
results_CHATGPT_4O_0.5_ROWS_0.5_TD_PUBLIC_5_REATTEMPT
```

This naming encodes all experimental parameters for traceability.

### Generated Files

**From `get_solution.py`:**

- `{experiment}_solution.json` - Raw LLM responses
- `{experiment}_solution_formatted.json` - Code after formatting
- `{experiment}_metadata.json` - Generation metadata (timestamps, tokens, etc.)
- `{experiment}_errors.json` - Errors during generation
- `tmp_{experiment}.csv` - Dataset copy used for this run
- `tmp_{experiment}_generation_start_at_{timestamp}/` - Checkpoint directory

**From `test_solution.py`:**

- `runner_passed.json` - Solutions that passed all tests
- `runner_fails.json` - Solutions that failed tests
- `runner_errors.json` - Solutions with execution errors
- `summary.json` - Test statistics (pass rate, error counts, etc.)

### Result File Formats

**`runner_passed.json` / `runner_fails.json` / `runner_errors.json`:**

```json
{
  "problem_id_1": {
    "solution": "def example():\n    ...",
    "test_results": [...],
    "metadata": {...}
  },
  ...
}
```

**`summary.json`:**

```json
{
  "total_problems": 164,
  "passed": 142,
  "failed": 18,
  "errors": 4,
  "pass_rate": 0.8659,
  ...
}
```

## Advanced Scenarios

### Creating Test-Driven Variants

Test-driven experiments include test cases in the LLM prompt:

```python
setup = GetSolutionSetup(
    dataset_name="human_eval",
    language="python",
    llm_to_use="CHATGPT_4O",
    directory_name="human_eval_chatgpt4o_td",  # Note: _td suffix
    test_driven=True,                           # Enable TD
)
```

**Important:** Use `_td` suffix in directory name to distinguish from non-TD experiments.

### Creating Second-Half Experiments

For large datasets, split processing into two halves:

**First Half (default):**

```python
# No special parameters needed
setup = GetSolutionSetup(
    dataset_name="human_eval",
    language="python",
    llm_to_use="CHATGPT_4O",
    directory_name="human_eval_chatgpt4o",
)
```

**Second Half:**

```python
# Calculate midpoint: dataset_size // 2
# human_eval: 164 problems → start_index = 82
# mbpp_sanitized: 427 problems → start_index = 214

setup = GetSolutionSetup(
    dataset_name="human_eval",
    language="python",
    llm_to_use="CHATGPT_4O",
    directory_name="human_eval_chatgpt4o_second_half",
    start_index=82,  # Second half starts here
)
```

**Merging Halves:**

After running both halves, merge results using `scripts/merge_results.py`:

```bash
# Merge non-TD results
poetry run python scripts/merge_results.py --base-dir rq1/human_eval_chatgpt4o

# Merge TD results
poetry run python scripts/merge_results.py --base-dir rq1/human_eval_chatgpt4o --is-td
```

See [README.md](README.md#merging-results-with-merge_resultspy) for detailed merge instructions.

### Combining TD + Second Half

You can create all four variants for complete coverage:

```python
# 1. First half, no TD
directory_name="human_eval_model"

# 2. First half, with TD
directory_name="human_eval_model_td"
test_driven=True

# 3. Second half, no TD
directory_name="human_eval_model_second_half"
start_index=82

# 4. Second half, with TD
directory_name="human_eval_model_second_half_td"
test_driven=True
start_index=82
```

Then merge into `_combined` and `_combined_td` directories using `merge_results.py`.

**Next Steps:**

- Return to [README.md](README.md) for setup and general usage
- See existing experiment directories in `rq1/` and `rq2/` for examples
- Check `config/rq1.py` and `config/rq2.py` for global configuration options
