import sys
import os

# Add the thesis directory to Python path (same pattern as other rq2 scripts)
RQ2_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.abspath(os.path.join(RQ2_DIR, ".."))
sys.path.append(ROOT_DIR)

from rq1.get_solution_setup import GetSolutionSetup

# Human eval dataset: first half processed 0-81, second half starts at 82
START_INDEX = 82

setup = GetSolutionSetup(
    dataset_name="human_eval",
    language="python",
    test_driven=True,
    llm_to_use="QWEN_14B_CODER",
    directory_name="human_eval_qwen25coder14b_second_half_td",
    start_index=START_INDEX,
)
results, errors = setup.generate_solutions()
