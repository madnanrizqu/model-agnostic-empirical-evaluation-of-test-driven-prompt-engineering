import sys
import os

# Add the thesis directory to Python path (same pattern as other rq2 scripts)
RQ2_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.abspath(os.path.join(RQ2_DIR, ".."))
sys.path.append(ROOT_DIR)

from rq1.get_solution_setup import GetSolutionSetup

setup = GetSolutionSetup(
    dataset_name="mbpp_sanitized",
    language="python",
    llm_to_use="CLAUDE_35_SONNET",
    test_driven=True,
    directory_name="mbpp_sanitized_claude35sonnet_td",
)
results, errors = setup.generate_solutions()
