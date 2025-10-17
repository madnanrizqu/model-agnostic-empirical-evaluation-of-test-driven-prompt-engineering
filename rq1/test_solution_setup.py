import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from experiment_runner.setup import BaseTestSolutionSetup
from solution_formatter_module import SolutionFormatter
import config.rq1 as config


class TestSolutionSetup(BaseTestSolutionSetup):
    """RQ1 test solution setup with dynamic result directory naming"""

    def __init__(self, dataset_name: str, llm_to_use: str = None, directory_name: str = None,
                 test_driven: bool = False, test_driven_ratio: float = None, start_index: int = None):
        # Store LLM configuration for dynamic result directory naming
        self.llm_key = llm_to_use if llm_to_use else config.LLM_TO_USE
        
        # Store directory name for LLM-specific result directories
        self.directory_name = directory_name
        
        # Store start_index for result directory naming consistency with GetSolutionSetup
        self.start_index = start_index
        
        # Use config defaults if not explicitly provided
        if test_driven_ratio is None:
            test_driven_ratio = config.TEST_DRIVEN_RATIO
        
        super().__init__(
            research_question="rq1",
            dataset_name=dataset_name,
            config_module=config,
            llm_to_use=llm_to_use or config.LLM_TO_USE,
            test_driven=test_driven,
            test_driven_ratio=test_driven_ratio,
        )
    
    def _customize_result_dir_name(self):
        """RQ1-specific: Dynamic result directory naming based on LLM configuration"""
        base_name = f"results_{self.llm_key}_{config.RATIO_OF_ROWS_TO_RUN}_ROWS_{config.TEST_DRIVEN_RATIO}_TD_PUBLIC_{config.REATTEMPT_MAX_NUM}_REATTEMPT"
        
        # Add "_second_half" suffix if start_index is provided (matching GetSolutionSetup behavior)
        if self.start_index is not None:
            base_name += "_second_half"
            
        return base_name
    
    def format_solutions(self, formatter: SolutionFormatter):
        """Format solutions using the provided formatter"""
        return super().format_solutions(formatter)
    
    def _get_adjusted_dataset_name(self):
        """Use explicit directory name if provided, otherwise fallback"""
        if self.directory_name:
            return self.directory_name
        return self.dataset_name

    def _init_result_dir(self):
        """Initialize result directory with LLM-specific directory naming"""
        adjusted_dataset_name = self._get_adjusted_dataset_name()
        self.results_dir = os.path.join(
            self.root_dir,
            self.research_question,
            adjusted_dataset_name,
            self._customize_result_dir_name(),
        )

        # Create results directory if it doesn't exist
        os.makedirs(self.results_dir, exist_ok=True)

    def get_standard_paths(self):
        """Get standardized paths using adjusted dataset name for LLM-specific files"""
        adjusted_name = self._get_adjusted_dataset_name()
        solutions_path = os.path.join(
            self.results_dir, f"{adjusted_name}_solution.json"
        )
        formatted_path = os.path.join(
            self.results_dir, f"{adjusted_name}_solution_formatted.json"
        )
        dataset_path = os.path.join(self.results_dir, f"tmp_{adjusted_name}.csv")
        
        return solutions_path, formatted_path, dataset_path

    def _customize_base_config(self, config: dict, language: str) -> dict:
        """Override to add directory_name to config for temp directory naming"""
        config = super()._customize_base_config(config, language)

        # Add directory_name for more descriptive temp directory naming in RQ1
        if self.directory_name:
            config["directory_name"] = self.directory_name

        return config