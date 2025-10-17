import sys
import os
import argparse

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from rq1.results_analyzer import RQ1ResultsAnalyzer
import config.rq1 as config


def main():
    """Main function to run RQ1 analysis using RQ1-specific analyzer"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run RQ1 analysis")
    parser.add_argument(
        "--combined-only",
        action="store_true",
        help="Analyze only combined (full dataset) results",
    )
    args = parser.parse_args()

    if args.combined_only:
        print("🚀 Starting RQ1 analysis for COMBINED RESULTS ONLY...")
        print(
            "   (This will only process full dataset results with '_combined' suffix)"
        )
    else:
        print("🚀 Starting RQ1 comprehensive analysis...")
        print(
            "   (This will process all matching results including partial and combined)"
        )

    # Run existing RQ1 analysis
    print("\n" + "=" * 60)
    if args.combined_only:
        print("COMBINED RESULTS ONLY ANALYSIS")
    else:
        print("STANDARD RQ1 ANALYSIS")
    print("=" * 60)
    analyzer = RQ1ResultsAnalyzer("rq1", config, combined_only=args.combined_only)
    analyzer.run_analysis()

    print("\n🎉 All RQ1 analyses completed successfully!")
    print("   Check the results_all/ directory for generated reports and data files.")


if __name__ == "__main__":
    main()
