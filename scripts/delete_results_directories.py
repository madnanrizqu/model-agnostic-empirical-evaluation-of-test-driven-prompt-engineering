#!/usr/bin/env python3
"""
Script to delete all results_* directories inside rq1 or rq2 experiment directories.

This will remove all results folders to allow fresh experiment runs.
Use with caution - this is a destructive operation!
"""

import os
import sys
import shutil
import argparse


def find_and_delete_results(rq_dir, dry_run=False):
    """Find and delete all results_* directories in experiment directories"""

    if not os.path.exists(rq_dir):
        print(f"Error: {rq_dir} does not exist")
        sys.exit(1)

    # Get all experiment directories
    experiment_dirs = [
        d for d in os.listdir(rq_dir)
        if os.path.isdir(os.path.join(rq_dir, d))
        and not d.startswith('__')
        and d not in ['logs', 'results_all']
    ]

    if not experiment_dirs:
        print(f"No experiment directories found in {rq_dir}")
        return

    print(f"Scanning {len(experiment_dirs)} experiment directories...")
    print()

    total_results_dirs = 0
    deleted_count = 0
    skipped_count = 0

    for exp_dir in sorted(experiment_dirs):
        exp_path = os.path.join(rq_dir, exp_dir)

        # Find all results_* directories in this experiment
        results_dirs = [
            item for item in os.listdir(exp_path)
            if os.path.isdir(os.path.join(exp_path, item))
            and item.startswith('results_')
        ]

        if results_dirs:
            total_results_dirs += len(results_dirs)
            print(f"📁 {exp_dir}/")

            for results_dir in sorted(results_dirs):
                results_path = os.path.join(exp_path, results_dir)

                # Calculate directory size
                total_size = 0
                for dirpath, dirnames, filenames in os.walk(results_path):
                    for filename in filenames:
                        filepath = os.path.join(dirpath, filename)
                        if os.path.exists(filepath):
                            total_size += os.path.getsize(filepath)

                size_mb = total_size / (1024 * 1024)

                if dry_run:
                    print(f"  🔍 Would delete: {results_dir}/ ({size_mb:.2f} MB)")
                    skipped_count += 1
                else:
                    try:
                        shutil.rmtree(results_path)
                        print(f"  ✅ Deleted: {results_dir}/ ({size_mb:.2f} MB)")
                        deleted_count += 1
                    except Exception as e:
                        print(f"  ❌ Error deleting {results_dir}/: {e}")
                        skipped_count += 1

            print()

    print("=" * 60)
    if dry_run:
        print("🔍 DRY RUN - No files were actually deleted")
        print(f"Found {total_results_dirs} results directories that would be deleted")
    else:
        print(f"✅ Deleted: {deleted_count} directories")
        print(f"❌ Skipped/Failed: {skipped_count} directories")
        print(f"Total processed: {total_results_dirs} directories")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Delete all results_* directories from experiment folders"
    )
    parser.add_argument(
        "--rq-dir",
        required=True,
        help="Research question directory (e.g., rq1, rq2)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without actually deleting",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip confirmation prompt",
    )

    args = parser.parse_args()

    # Get the full path to the RQ directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    rq_dir_path = os.path.join(root_dir, args.rq_dir)

    print("=" * 60)
    print("Delete Results Directories Script")
    print("=" * 60)
    print(f"Target directory: {rq_dir_path}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'DELETE'}")
    print()

    if not args.dry_run and not args.yes:
        print("⚠️  WARNING: This will permanently delete all results_* directories!")
        print("   This action cannot be undone.")
        print()
        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled.")
            sys.exit(0)
        print()

    find_and_delete_results(rq_dir_path, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
