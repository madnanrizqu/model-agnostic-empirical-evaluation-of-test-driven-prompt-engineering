import sys
import os

# Add the thesis directory to Python path (same pattern as other rq2 scripts)
RQ2_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.abspath(os.path.join(RQ2_DIR, ".."))
sys.path.append(ROOT_DIR)

from rq1.test_solution_setup import TestSolutionSetup
from solution_formatter_module import SolutionFormatter
from test_runner_module.main import TestRunner

# Setup
setup = TestSolutionSetup(
    dataset_name="human_eval",
    llm_to_use="QWEN_7B_CODER",
    directory_name="human_eval_qwen25coder7b",
)

# Format Solutions
formatter = SolutionFormatter(
    language="python",
    use_multi_marker=True,
)
setup.format_solutions(formatter)

# Configure
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

# Execute Tests
runner = TestRunner(config)
runner.run()
