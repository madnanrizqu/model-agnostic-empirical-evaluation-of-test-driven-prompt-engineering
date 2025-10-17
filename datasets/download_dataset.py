import polars as pl
from typing import Dict, Optional, Union
from pathlib import Path
import logging
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HUGGING_FACE_TOKEN")
print("HF_TOKEN", HF_TOKEN)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_dataset_and_write_csv(
    dataset_path: Union[str, Dict[str, str]],
    dataset_name: str,
    base_hf_path: Optional[str] = None,
    output_dir: str = "./datasets",
    suffix: str = "",
) -> pl.DataFrame:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{dataset_name}{suffix}.csv"

    logger.info(f"Downloading {dataset_name}{suffix}...")

    if isinstance(dataset_path, str):
        # Handle single file case
        full_path = f"{base_hf_path}/{dataset_path}" if base_hf_path else dataset_path
        logger.info(f"Reading from: {full_path}")
        storage_options = {"token": HF_TOKEN} if HF_TOKEN else {}
        df = pl.read_parquet(full_path, storage_options=storage_options)

    elif isinstance(dataset_path, dict):
        # Handle split dataset case
        dfs = []
        for split_name, split_path in dataset_path.items():
            full_path = f"{base_hf_path}/{split_path}" if base_hf_path else split_path
            logger.info(f"Reading split {split_name} from: {full_path}")
            storage_options = {"token": HF_TOKEN} if HF_TOKEN else {}
            df_split = pl.read_parquet(full_path, storage_options=storage_options)
            df_split["split"] = split_name
            dfs.append(df_split)
        df = pl.concat(dfs, ignore_index=True)

    else:
        raise ValueError(
            "dataset_path must be either a string or a dictionary of splits"
        )

    logger.info(f"Success! DataFrame length: {len(df)}")

    # Convert nested columns to JSON strings for CSV compatibility
    for col in df.columns:
        if df[col].dtype in (pl.List, pl.Struct, pl.Array):
            df = df.with_columns(
                pl.col(col).map_elements(str, return_dtype=pl.Utf8).alias(col)
            )

    df.write_csv(output_path)
    logger.info(f"Saved to {output_path}")

    return df


def main():
    datasets_config = [
        {
            "dataset_path": "openai_humaneval/test-00000-of-00001.parquet",
            "dataset_name": "human_eval",
            "base_hf_path": "hf://datasets/openai/openai_humaneval",
        },
        {
            "dataset_path": {
                "train": "sanitized/train-00000-of-00001.parquet",
                "test": "sanitized/test-00000-of-00001.parquet",
                "validation": "sanitized/validation-00000-of-00001.parquet",
                "prompt": "sanitized/prompt-00000-of-00001.parquet",
            },
            "dataset_name": "mbpp",
            "base_hf_path": "hf://datasets/google-research-datasets/mbpp",
            "suffix": "_sanitized",
        },
    ]

    # Download all datasets
    for config in datasets_config:
        download_dataset_and_write_csv(**config)


if __name__ == "__main__":
    main()
