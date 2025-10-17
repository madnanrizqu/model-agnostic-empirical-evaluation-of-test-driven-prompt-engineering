# LLM Evaluation System

A sophisticated research platform that evaluates Large Language Models (LLMs) using test-driven development approaches across multiple coding benchmarks.

## Overview

This system evaluates LLMs on programming tasks using:

- **Datasets**: HumanEval, MBPP, Code Contests
- **Language**: Python
- **Research Questions**:
  - **RQ1**: Basic programming task evaluation
  - **RQ2**: Competitive programming challenges and model comparison

**Getting Started:**

- Follow this README to set up and run existing experiments
- See [EXPERIMENT_GUIDE.md](EXPERIMENT_GUIDE.md) to create new model benchmark experiments

## Prerequisites

Before setting up this project, ensure you have:

- **Python 3.11.x** (Required - Python 3.12+ is not supported)
- **pyenv** for managing Python versions (recommended)
- **Poetry** for dependency management
- **Git** for version control
- API keys for LLM providers (see Environment Setup below)

## Quick Start (Recommended)

### 1. Install pyenv and Python 3.11.x

On macOS (with Homebrew):

```zsh
brew update
brew install pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
exec zsh -l
pyenv install 3.11.14  # or latest 3.11.x
cd thesis
pyenv local 3.11.14
python --version  # Should print Python 3.11.x
```

### 2. Install Poetry (if not already installed)

```zsh
# With pip
pip install poetry
# Or with Homebrew for mac users
brew install poetry
```

### 3. Project Setup and Environment Activation (Makefile)

This project provides a Makefile to automate setup and environment activation:

```zsh
# One-shot setup (installs dependencies, configures Poetry, sets up .venv)
make setup

# If Poetry is not installed, you'll see a message with install instructions.
# After installing Poetry, re-run 'make setup'.

# To print the activation command for the Poetry environment:
make activate-cmd
# Then run the printed command, e.g.:
source $(poetry env info --path)/bin/activate

# Or run scripts directly without activating:
poetry run python path/to/script.py
```

This will:

- Configure Poetry to use a `.venv` directory in the project root
- Use your pyenv Python (if available) or system Python
- Install all required packages from `poetry.lock`

### 3. Environment Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your API keys
nano .env  # or use your preferred editor
```

## Token Requirements

To use this system, you only need to set the API tokens for the LLM providers you plan to use. The table below shows which tokens are required for each provider and which LLM configuration keys use them.

### Default Tokens (Required for Most Experiments)

| Provider      | Required Token(s)         | LLM Config Keys (examples)           |
|--------------|--------------------------|--------------------------------------|
| **HuggingFace** | `HUGGING_FACE_TOKEN`    | QWEN_2_5_CODER_32B, QWEN_14B_CODER, QWEN_7B_CODER, QWEN_3B_CODER |
| **OpenRouter**  | `OPEN_ROUTER_TOKEN`     | CHATGPT_4O, CHATGPT_4O_MINI, CLAUDE_35_SONNET, CLAUDE_35_HAIKU   |

### Optional Tokens (Only Required for Specific LLM Configs)

| Provider      | Required Token(s)         | LLM Config Keys (examples)           |
|--------------|--------------------------|--------------------------------------|
| Groq         | `GROQ_TOKEN`              | QWEN_32B_CODER_GROQ                  |
| Cloudflare   | `CLOUDFLARE_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` | QWEN_32B_CODER_CF |

**Guidance:**

- The LLM provider for each experiment is set by the `llm_to_use` argument in the `get_solution.py` script inside each experiment directory (see `rq1/*/get_solution.py` and `rq2/*/get_solution.py`).
- The config files in `config/` (e.g., `rq1.py`, `rq2.py`) provide defaults for batch runs, but **per-experiment runs use the value in each script**.
- You only need to set the tokens for the providers required by the LLM(s) you actually use in your experiments.
- For Cloudflare or Groq endpoints, set the corresponding tokens as shown above.
- You do **not** need to set tokens for unused providers.

See `.env.example` for a template and comments.

### 4. Activating the Environment & Running Code

**Recommended:**

- Use `make activate-cmd` to print the activation command, then run it in your shell:

```zsh
make activate-cmd
# Then run:
source $(poetry env info --path)/bin/activate
# Now 'python' and 'pip' use the Poetry venv
```

- Or, always use Poetry to run scripts so dependencies are available:

```zsh
poetry run python path/to/your_script.py
```

**Note:**

- Running `python ...` directly (without `poetry run` or activating the venv) will NOT see installed dependencies.
- Always use `poetry run ...` or activate the venv as above.

## Project Structure

```
thesis/
├── rq1/                          # Research Question 1 experiments
├── rq2/                          # Research Question 2 experiments
├── config/                       # Configuration files
├── datasets/                     # Benchmark datasets
├── docs/                         # Architecture documentation
├── experiment_runner/            # Core experiment orchestration
├── llm_module/                   # LLM API integration
├── prompt_module/                # Prompt generation strategies
├── solution_formatter_module/    # Code formatting strategies
├── test_runner_module/          # Multi-language test execution
├── languages/                    # Language-specific test environments
├── EXPERIMENT_GUIDE.md          # Guide for creating new experiments
├── README.md                    # This file - setup and usage
├── pyproject.toml               # Poetry dependencies
├── poetry.lock                  # Locked dependency versions
└── .env                         # API keys (create from .env.example)
```

### Understanding RQ1 and RQ2 Experiment Directories

Each folder inside `rq1/` and `rq2/` represents a **unique dataset + LLM combination**. For example:

- `rq1/human_eval_chatgpt4o/` - HumanEval dataset evaluated using ChatGPT-4o
- `rq1/human_eval_chatgpt4omini/` - HumanEval dataset evaluated using ChatGPT-4o-mini
- `rq2/code_contests_claude35sonnet/` - Code Contests dataset evaluated using Claude 3.5 Sonnet

**Each experiment directory contains:**

1. **`get_solution.py`** - Generates code solutions for the dataset using the specified LLM
   - Sets the `llm_to_use` parameter (e.g., `"CHATGPT_4O"`, `"CLAUDE_35_SONNET"`)
   - Generates solutions and saves them to the directory

2. **`test_solution.py`** - Tests the generated code solutions
   - Executes test cases against the generated solutions
   - Records pass/fail results

3. **`write_results.py`** - Analyzes and summarizes test execution results
   - Generates statistics (pass rates, error analysis, etc.)
   - Creates result summaries for analysis
   - Should be run with `--combined-only` flag by default (see Experiment Variants below)

### Experiment Variants and Directory Suffixes

Experiments can be split into halves and run with different prompting strategies:

**Directory Naming Convention:**

- **Base directory** (e.g., `human_eval_chatgpt4o`) - First half of dataset without test-driven prompts
- **`_second_half`** - Second half of dataset without test-driven prompts
- **`_td`** - First half of dataset WITH test-driven prompts (tests included in prompt)
- **`_second_half_td`** - Second half of dataset WITH test-driven prompts
- **`_combined`** - Merged results from base + `_second_half` (full dataset, no TD)
- **`_combined_td`** - Merged results from `_td` + `_second_half_td` (full dataset, with TD)

**Example structure:**

```
rq1/
├── human_eval_chatgpt4o/              # First half, no TD
├── human_eval_chatgpt4o_second_half/  # Second half, no TD
├── human_eval_chatgpt4o_td/           # First half, with TD
├── human_eval_chatgpt4o_second_half_td/ # Second half, with TD
├── human_eval_chatgpt4o_combined/     # Full dataset merged, no TD
└── human_eval_chatgpt4o_combined_td/  # Full dataset merged, with TD
```

### Merging Results with `merge_results.py`

The `scripts/merge_results.py` utility merges first half and second half results into combined datasets:

**Usage:**

```bash
# Merge base (non-TD) results
poetry run python scripts/merge_results.py --base-dir rq1/human_eval_chatgpt4o

# Merge test-driven results
poetry run python scripts/merge_results.py --base-dir rq1/human_eval_chatgpt4o --is-td
```

**What it does:**

1. Locates first half and second half experiment directories
2. Merges `runner_passed.json`, `runner_fails.json`, `runner_errors.json`
3. Combines solution files and metadata
4. Recalculates summary statistics using `SummaryCalculator`
5. Saves merged results to `_combined` or `_combined_td` directory

**When to use:**

- After completing both first half and second half experiments
- Before running `write_results.py --combined-only` for final analysis
- To generate complete dataset results from split experiments

## Running Experiments

### Option 1: Batch Execution (Recommended)

Run multiple experiments at once using `run_all.py`:

**RQ1: Basic Programming Tasks**

```bash
# Run all RQ1 experiments
poetry run python rq1/run_all.py

# Run specific experiments (solution generation only)
poetry run python rq1/run_all.py --folders human_eval_chatgpt4o human_eval_chatgpt4omini --get-only

# Run test execution only
poetry run python rq1/run_all.py --folders human_eval_chatgpt4o human_eval_chatgpt4omini --test-only
```

**RQ2: Competitive Programming**

```bash
# Run all RQ2 experiments
poetry run python rq2/run_all.py

# Run specific experiments
poetry run python rq2/run_all.py --folders code_contests_chatgpt4o code_contests_chatgpt4omini
```

### Option 2: Individual Experiment Execution

Run a single experiment step-by-step:

```bash
# 1. Generate solutions for a specific experiment
cd rq1/human_eval_chatgpt4o && poetry run python get_solution.py

# 2. Test the generated solutions
poetry run python test_solution.py

# 3. Analyze and summarize results
poetry run python write_results.py
```

## Troubleshooting

### Poetry Not Found

After installing Poetry, you may need to add it to your PATH:

```bash
# For bash/zsh
export PATH="$HOME/.local/bin:$PATH"

# Add to ~/.bashrc or ~/.zshrc to make permanent
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

### Python Version Mismatch

This project requires Python 3.11.x. If you see version errors:

```zsh
# Check your Python version
python --version

# If not 3.11.x, ensure pyenv is set up and run:
pyenv local 3.11.14
exec zsh -l

# Then re-run:
poetry env use $(pyenv which python)
poetry install
```

### Import Errors

If you get import errors after installation:

```zsh
# Ensure you're in the poetry environment
poetry run python your_script.py
# Or activate the venv:
source $(poetry env info --path)/bin/activate
python your_script.py
```

### API Key Issues

If you get authentication errors:

1. Verify `.env` file exists: `ls -la .env`
2. Check API keys are properly set (no spaces, quotes, or extra characters)

## Contributing

When contributing to this project:

1. Install development dependencies: `poetry install`
2. Make your changes
3. Test your changes: `poetry run python verify_setup.py`
4. Ensure all experiments still run: `poetry run python rq1/run_all.py --folders human_eval --get-only`
5. Commit and push your changes

## License

[Add your license information here]

## Citation

If you use this system in your research, please cite:

```bibtex
[Add your citation information here]
```

## Support

For issues or questions:

- Open an issue on GitHub
