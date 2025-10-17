import pandas as pd
from ..strategies_interface import DatasetFormatterInterface


class DefaultFormatter(DatasetFormatterInterface):
    """Default formatter that returns the dataset unchanged"""

    def _transform_dataset(self, original_df: pd.DataFrame) -> pd.DataFrame:
        """Return dataset unchanged"""
        return original_df.copy()
