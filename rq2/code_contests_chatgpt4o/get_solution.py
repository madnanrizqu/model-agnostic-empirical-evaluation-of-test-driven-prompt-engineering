import sys
import os

# Add the thesis directory to Python path (same pattern as other rq2 scripts)
RQ2_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.abspath(os.path.join(RQ2_DIR, ".."))
sys.path.append(ROOT_DIR)

from rq2.get_solution_setup import GetSolutionSetup

setup = GetSolutionSetup(
    dataset_name="code_contests",
    language="python",
    llm_to_use="CHATGPT_4O",
    directory_name="code_contests_chatgpt4o",
)
results, errors = setup.generate_solutions()
