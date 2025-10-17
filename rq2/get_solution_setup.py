import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from experiment_runner.setup import BaseGetSolutionSetup
import config.rq2 as config


class GetSolutionSetup(BaseGetSolutionSetup):
    """RQ2 solution generation setup with dynamic LLM configuration and result directory naming"""

    def __init__(
        self,
        dataset_name,
        language,
        llm_to_use=None,
        test_driven=False,
        test_driven_ratio=None,
        directory_name=None,
        start_index=None,
    ):
        # Store LLM key for dynamic result directory naming
        self.llm_key = llm_to_use if llm_to_use else config.LLM_TO_USE
        
        # Store directory name for LLM-specific result directories
        self.directory_name = directory_name
        
        # Store start_index for second half processing
        self.start_index = start_index

        # Use config defaults if not explicitly provided
        if llm_to_use is None:
            llm_to_use = config.LLM_TO_USE
        if test_driven_ratio is None:
            test_driven_ratio = config.TEST_DRIVEN_RATIO

        super().__init__(
            research_question="rq2",
            dataset_name=dataset_name,
            language=language,
            config_module=config,
            llm_to_use=llm_to_use,
            test_driven=test_driven,
            test_driven_ratio=test_driven_ratio,
        )

    def _customize_result_dir_name(self):
        """RQ2-specific: Dynamic result directory naming based on LLM configuration"""
        base_name = f"results_{self.llm_key}_{config.RATIO_OF_ROWS_TO_RUN}_ROWS_{config.TEST_DRIVEN_RATIO}_TD_PUBLIC_{config.REATTEMPT_MAX_NUM}_REATTEMPT"
        
        # Add "_second_half" suffix if start_index is provided
        if self.start_index is not None:
            base_name += "_second_half"
            
        return base_name

    def _get_llm_key(self):
        """Get the LLM key used for this configuration"""
        return self.llm_key

    def _get_adjusted_dataset_name(self):
        """Use explicit directory name if provided, otherwise fallback to original logic"""
        if self.directory_name:
            return self.directory_name
        
        # Fallback to original behavior
        if self.test_driven:
            return f"{self.dataset_name}_td"
        return self.dataset_name

    def generate_solutions(self, ratio_of_rows=None):
        """Generate solutions using inherited base functionality with RQ2 defaults"""
        if ratio_of_rows is None:
            ratio_of_rows = config.RATIO_OF_ROWS_TO_RUN
        return super().generate_solutions(ratio_of_rows, start_index=self.start_index)
