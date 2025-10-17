import sys
import os
import argparse

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from rq2.results_analyzer import RQ2ResultsAnalyzer
from rq2.code_contests_difficulty_analyzer import CodeContestsDifficultyAnalyzer
import config.rq2 as config


def main():
    """Main function to run RQ2 analysis using RQ2-specific analyzer"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run RQ2 analysis")
    parser.add_argument(
        "--combined-only",
        action="store_true",
        help="Analyze only combined (full dataset) results",
    )
    args = parser.parse_args()

    if args.combined_only:
        print("🚀 Starting RQ2 analysis for COMBINED RESULTS ONLY...")
        print(
            "   (This will only process full dataset results with '_combined' suffix)"
        )
    else:
        print("🚀 Starting RQ2 comprehensive analysis...")
        print(
            "   (This will process all matching results including partial and combined)"
        )

    # Run existing RQ2 analysis
    print("\n" + "=" * 60)
    if args.combined_only:
        print("COMBINED RESULTS ONLY ANALYSIS")
    else:
        print("STANDARD RQ2 ANALYSIS")
    print("=" * 60)
    analyzer = RQ2ResultsAnalyzer(
        "rq2", config, combined_only=args.combined_only
    )
    analyzer.run_analysis()

    # Run CodeContests difficulty analysis
    difficulty_analyzer = CodeContestsDifficultyAnalyzer(
        "rq2", config, combined_only=args.combined_only
    )
    difficulty_analyzer.run_analysis()

    print("\n🎉 All RQ2 analyses completed successfully!")
    print("   Check the results_all/ directory for generated reports and data files.")


if __name__ == "__main__":
    main()
