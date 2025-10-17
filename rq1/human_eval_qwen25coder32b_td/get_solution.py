import sys
import os

# Add the thesis directory to Python path (same pattern as other rq2 scripts)
RQ2_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.abspath(os.path.join(RQ2_DIR, ".."))
sys.path.append(ROOT_DIR)

from rq1.get_solution_setup import GetSolutionSetup

setup = GetSolutionSetup(
    dataset_name="human_eval",
    language="python",
    llm_to_use="QWEN_2_5_CODER_32B",
    test_driven=True,
    directory_name="human_eval_qwen25coder32b_td",
)
results, errors = setup.generate_solutions()
