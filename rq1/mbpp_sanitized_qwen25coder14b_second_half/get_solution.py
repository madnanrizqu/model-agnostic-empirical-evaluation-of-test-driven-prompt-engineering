import sys
import os

# Add the thesis directory to Python path (same pattern as other rq2 scripts)
RQ2_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.abspath(os.path.join(RQ2_DIR, ".."))
sys.path.append(ROOT_DIR)

from rq1.get_solution_setup import GetSolutionSetup

# MBPP Sanitized dataset: first half processed 0-212, second half starts at 213
START_INDEX = 213

setup = GetSolutionSetup(
    dataset_name="mbpp_sanitized",
    language="python",
    llm_to_use="QWEN_14B_CODER",
    directory_name="mbpp_sanitized_qwen25coder14b_second_half",
    start_index=START_INDEX,
)
results, errors = setup.generate_solutions(ratio_of_rows="ALL")
