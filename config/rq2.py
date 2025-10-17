"""
RQ2 Configuration

Configuration Variables:
------------------------

LLM_TO_USE (str):
  - Default LLM for batch runs (e.g., run_all.py)
  - Individual experiments OVERRIDE this in their get_solution.py
  - Options: "OPEN_LLM", "CLOSED_LLM", "BOTH_LLM", or specific keys from llm_module/config.py
  - See README.md 'Token Requirements' for token mappings

TEST_DRIVEN_RATIO (float):
  - Proportion of experiments to run with test-driven prompts (tests included in prompt)
  - 0.5 = 50% of experiments will include tests in prompts (_td directories)
  - 0.0 = no test-driven prompts, 1.0 = all test-driven prompts
  - Used by run_all.py to determine which experiments get TD variants

RATIO_OF_ROWS_TO_RUN (float):
  - Proportion of dataset rows to process in each run
  - Default: 0.5 for first/second half split experiment approach
    • Base experiments run on first 50% of dataset
    • _second_half experiments run on remaining 50%
    • Results merged into _combined using scripts/merge_results.py
  - Set to 1.0 to run full dataset at once (no splitting)
  - Examples: 0.1 = 10%, 0.5 = 50%, 1.0 = 100%

REATTEMPT_MAX_NUM (int):
  - Maximum number of retry attempts when LLM solution fails tests
  - Default: 5 attempts
  - Used during remediation/self-healing process
  - Higher values = more chances to fix failing code, but slower execution

RESULT_DIR_NAME (str):
  - Auto-generated directory name for storing experiment results
  - Format includes all config parameters for traceability
  - Example: "results_OPEN_LLM_0.5_ROWS_0.5_TD_PUBLIC_5_REATTEMPT"
"""

TEST_DRIVEN_RATIO = 0.5
LLM_TO_USE = "OPEN_LLM"
RATIO_OF_ROWS_TO_RUN = 0.5  # 0.5 for first/second half split, 1.0 for full dataset
REATTEMPT_MAX_NUM = 5
RESULT_DIR_NAME = f"results_{LLM_TO_USE}_{RATIO_OF_ROWS_TO_RUN}_ROWS_{TEST_DRIVEN_RATIO}_TD_PUBLIC_{REATTEMPT_MAX_NUM}_REATTEMPT"
