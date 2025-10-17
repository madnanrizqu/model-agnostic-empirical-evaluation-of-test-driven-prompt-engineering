#!/usr/bin/env python3
"""
Download script for the CodeContests dataset from Hugging Face.
Filters for EASY, MEDIUM, HARD, HARDER, and HARDEST difficulty levels only.
Saves the filtered data as CSV files.
"""

from datasets import load_dataset
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def explore_difficulty_levels():
    """
    Explore and display all available difficulty levels in the CodeContests dataset
    before applying any filtering.
    """
    print("Exploring difficulty levels in the CodeContests dataset...")
    print("=" * 60)

    # Get Hugging Face token from environment
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise ValueError(
            "HF_TOKEN not found in environment variables.\n"
            "Please create a .env file with your Hugging Face token:\n"
            "HF_TOKEN=your_huggingface_token_here\n"
            "You can get a token from: https://huggingface.co/settings/tokens"
        )

    # Load the dataset with authentication
    print("Loading dataset from HuggingFace...")
    dataset = load_dataset("deepmind/code_contests", token=hf_token)

    print(f"Dataset loaded successfully!")
    print(f"Available splits: {list(dataset.keys())}")

    # Complete difficulty mapping based on HuggingFace documentation
    difficulty_labels = {
        0: "UNKNOWN_DIFFICULTY",
        1: "EASY",
        2: "MEDIUM",
        3: "HARD",
        4: "HARDER",
        5: "HARDEST",
        6: "EXTERNAL",
        7: "A",
        8: "B",
        9: "C",
        10: "D",
        11: "E",
        12: "F",
        13: "G",
        14: "H",
        15: "I",
        16: "J",
        17: "K",
        18: "L",
        19: "M",
        20: "N",
        21: "O",
        22: "P",
        23: "Q",
        24: "R",
        25: "S",
        26: "T",
        27: "U",
        28: "V",
    }

    all_difficulties = []
    total_examples = 0

    # Analyze each split
    for split_name, split_data in dataset.items():
        print(f"\n--- {split_name.upper()} SPLIT ---")
        print(f"Total examples: {len(split_data)}")
        total_examples += len(split_data)

        # Extract all difficulty values from this split
        split_difficulties = [
            split_data[i]["difficulty"] for i in range(len(split_data))
        ]
        all_difficulties.extend(split_difficulties)

        # Count difficulties in this split
        split_difficulty_counts = (
            pd.Series(split_difficulties).value_counts().sort_index()
        )

        print("Difficulty distribution in this split:")
        for diff_id, count in split_difficulty_counts.items():
            percentage = (count / len(split_data)) * 100
            label = difficulty_labels.get(diff_id, f"UNKNOWN_{diff_id}")
            print(
                f"  {label:20} ({diff_id:2d}): {count:4d} examples ({percentage:5.1f}%)"
            )

    # Overall analysis
    print(f"\n{'=' * 60}")
    print("OVERALL DATASET ANALYSIS")
    print(f"{'=' * 60}")
    print(f"Total examples across all splits: {total_examples}")

    overall_difficulty_counts = pd.Series(all_difficulties).value_counts().sort_index()

    print("\nOverall difficulty distribution:")
    print(f"{'Difficulty':20} {'ID':3} {'Count':8} {'Percentage':10}")
    print("-" * 45)

    for diff_id, count in overall_difficulty_counts.items():
        percentage = (count / total_examples) * 100
        label = difficulty_labels.get(diff_id, f"UNKNOWN_{diff_id}")
        print(f"{label:20} {diff_id:3d} {count:8d} {percentage:9.1f}%")

    # Highlight the requested difficulty levels
    print(f"\n{'=' * 60}")
    print("REQUESTED DIFFICULTY LEVELS FOR FILTERING:")
    print(f"{'=' * 60}")
    requested_difficulties = [1, 2, 3, 4, 5]  # EASY, MEDIUM, HARD, HARDER, HARDEST
    requested_total = 0

    for diff_id in requested_difficulties:
        if diff_id in overall_difficulty_counts:
            count = overall_difficulty_counts[diff_id]
            percentage = (count / total_examples) * 100
            label = difficulty_labels[diff_id]
            print(
                f"{label:20} ({diff_id:2d}): {count:4d} examples ({percentage:5.1f}%)"
            )
            requested_total += count
        else:
            label = difficulty_labels[diff_id]
            print(f"{label:20} ({diff_id:2d}): {0:4d} examples ({0:5.1f}%)")

    print("-" * 45)
    requested_percentage = (requested_total / total_examples) * 100
    print(
        f"{'TOTAL FILTERED':20}     {requested_total:4d} examples ({requested_percentage:5.1f}%)"
    )

    return dataset, overall_difficulty_counts


def filter_dataset(dataset=None):
    """
    Download the CodeContests dataset from Hugging Face and filter for
    EASY (1), MEDIUM (2), and HARD (3) difficulty levels.

    Args:
        dataset: Pre-loaded dataset (optional). If None, will load from HuggingFace.
    """
    if dataset is None:
        print("Loading CodeContests dataset from Hugging Face...")

        # Get Hugging Face token from environment
        hf_token = os.getenv("HF_TOKEN")
        if not hf_token:
            raise ValueError(
                "HF_TOKEN not found in environment variables.\n"
                "Please create a .env file with your Hugging Face token:\n"
                "HF_TOKEN=your_huggingface_token_here\n"
                "You can get a token from: https://huggingface.co/settings/tokens"
            )

        # Load the dataset with authentication
        dataset = load_dataset("deepmind/code_contests", token=hf_token)

        print(f"Dataset loaded successfully!")
        print(f"Available splits: {list(dataset.keys())}")
    else:
        print("Using pre-loaded dataset for filtering...")
        print(f"Available splits: {list(dataset.keys())}")

    # Define the difficulty levels we want to keep
    # Based on the dataset page: EASY=1, MEDIUM=2, HARD=3
    target_difficulties = [1, 2, 3]  # EASY, MEDIUM, HARD

    filtered_dataset = {}

    # Filter each split for the target difficulties
    for split_name, split_data in dataset.items():
        print(f"\nProcessing {split_name} split...")
        print(f"Original size: {len(split_data)} examples")

        # Filter for target difficulties
        filtered_split = split_data.filter(
            lambda example: example["difficulty"] in target_difficulties
        )

        print(f"Filtered size: {len(filtered_split)} examples")

        # Count examples by difficulty
        difficulties = [
            filtered_split[i]["difficulty"] for i in range(len(filtered_split))
        ]
        difficulty_counts = pd.Series(difficulties).value_counts().sort_index()

        print("Difficulty distribution:")
        difficulty_map = {1: "EASY", 2: "MEDIUM", 3: "HARD"}
        for diff_id, count in difficulty_counts.items():
            print(f"  {difficulty_map[diff_id]} ({diff_id}): {count} examples")

        filtered_dataset[split_name] = filtered_split

    # Save the filtered dataset
    output_dir = "filtered_code_contests_csv"
    print(f"\nSaving filtered dataset to {output_dir}/...")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save each split as a separate CSV file
    for split_name, split_data in filtered_dataset.items():
        output_path = os.path.join(output_dir, f"{split_name}.csv")

        # Convert to pandas DataFrame for CSV export
        df = split_data.to_pandas()

        # Handle nested columns by converting them to string representation
        for col in df.columns:
            if df[col].dtype == "object":
                # Check if column contains lists/dicts and convert to string
                try:
                    # Convert complex nested structures to string representation
                    df[col] = df[col].apply(
                        lambda x: str(x) if isinstance(x, (list, dict)) else x
                    )
                except:
                    pass

        # Save as CSV
        df.to_csv(output_path, index=False)
        print(f"Saved {split_name} split to {output_path}")

    print("\nDownload and filtering complete!")
    return filtered_dataset


def get_dataset_info():
    """
    Display information about the dataset structure and difficulty levels.
    """
    print("CodeContests Dataset Information:")
    print("=" * 50)
    print("Source: https://huggingface.co/datasets/deepmind/code_contests")
    print("Description: Competitive programming dataset used for training AlphaCode")
    print("\nDifficulty Levels (filtered):")
    print("  1 - EASY")
    print("  2 - MEDIUM")
    print("  3 - HARD")
    print("\nDataset includes:")
    print("  - Problem descriptions")
    print("  - Public and private test cases")
    print("  - Solutions in multiple programming languages")
    print("  - Problem metadata (source, difficulty, etc.)")


if __name__ == "__main__":
    # Display dataset information
    get_dataset_info()

    try:
        # First, explore all difficulty levels in the dataset
        print("\n" + "=" * 80)
        print("STEP 1: EXPLORING DIFFICULTY LEVELS")
        print("=" * 80)
        dataset, difficulty_distribution = explore_difficulty_levels()

        # Ask user if they want to proceed with filtering
        print("\n" + "=" * 80)
        print("STEP 2: FILTERING DATASET")
        print("=" * 80)

        # Proceed with filtering using the pre-loaded dataset
        print(
            "Now applying filtering for EASY, MEDIUM, HARD, HARDER, and HARDEST difficulties..."
        )
        filtered_data = filter_dataset(dataset)
        print(
            f"\nSuccess! Filtered dataset contains {sum(len(split) for split in filtered_data.values())} total examples"
        )

    except ValueError as e:
        print(f"Authentication Error: {e}")
    except Exception as e:
        print(f"Error processing dataset: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you have the required libraries installed:")
        print("   pip install datasets pandas python-dotenv")
        print("2. Create a .env file with your Hugging Face token:")
        print("   cp .env.example .env")
        print("   # Then edit .env and add your actual token")
        print("3. Get a token from: https://huggingface.co/settings/tokens")
