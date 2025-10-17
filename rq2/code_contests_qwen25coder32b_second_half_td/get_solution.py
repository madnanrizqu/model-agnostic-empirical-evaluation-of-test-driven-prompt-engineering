import sys
import os

# Add the thesis directory to Python path (same pattern as other rq2 scripts)
RQ2_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.abspath(os.path.join(RQ2_DIR, ".."))
sys.path.append(ROOT_DIR)

from rq2.get_solution_setup import GetSolutionSetup

# Code Contests dataset: first half processed 0-201, second half starts at 202
START_INDEX = 202

setup = GetSolutionSetup(
    dataset_name="code_contests",
    language="python",
    llm_to_use="QWEN_2_5_CODER_32B",
    test_driven=True,
    directory_name="code_contests_qwen25coder32b_second_half_td",
    start_index=START_INDEX,
)
results, errors = setup.generate_solutions(ratio_of_rows="ALL")