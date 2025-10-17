import os
import sys
import logging
import argparse
from datetime import datetime

from .core import PerformanceMonitor, ParallelExecutor


def parse_arguments(experiment_name):
    """Parse command line arguments for the experiment runner.

    Args:
        experiment_name: Name of the experiment (e.g., "rq1", "rq2")
    """
    parser = argparse.ArgumentParser(
        description=f"Run {experiment_name.upper()} scripts."
    )
    parser.add_argument(
        "--get-only",
        action="store_true",
        help="Only run get_solution.py scripts without running tests",
    )
    parser.add_argument(
        "--test-only",
        action="store_true",
        help="Only run test_solution.py scripts without generating new solutions",
    )
    parser.add_argument(
        "--folders",
        type=str,
        nargs="+",
        default=None,
        help=f"Specify one or more subfolders in {experiment_name} to run (default: all subfolders)",
    )
    parser.add_argument(
        "--exclude-folders",
        type=str,
        nargs="+",
        default=None,
        help=f"Exclude specific subfolders from running (runs all other subfolders)",
    )
    return parser.parse_args()


def parse_results_arguments():
    """Parse command line arguments for results analysis."""
    parser = argparse.ArgumentParser(description="Analyze experiment results")
    parser.add_argument(
        "--exclude-dirs",
        type=str,
        nargs="*",
        default=[],
        help="Exclude directories from incomplete tracking (e.g., --exclude-dirs human_eval mbpp_cpp)",
    )
    parser.add_argument(
        "--include-dirs",
        type=str,
        nargs="*",
        default=None,
        help="Only include specific directories in analysis (e.g., --include-dirs human_eval mbpp_cpp)",
    )
    
    args = parser.parse_args()
    
    # Validate mutual exclusivity
    if args.exclude_dirs and args.include_dirs:
        parser.error("Cannot specify both --exclude-dirs and --include-dirs")
    
    return args


def setup_logging(base_dir, experiment_name):
    """Set up logging configuration for the experiment.

    Args:
        base_dir: Base directory for the experiment
        experiment_name: Name of the experiment (e.g., "rq1", "rq2")

    Returns:
        str: Path to the created log file
    """
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(base_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    # Create a log file with timestamp in the name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(logs_dir, f"run_all_{timestamp}.log")

    # Configure logging with minimal format - just the message
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",  # Removed level name from format
        handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
    )

    logging.info(f"Log file created at: {log_file}")
    return log_file


def log_config(config):
    """Log configuration settings from the config module.

    Args:
        config: The configuration module to log
    """
    # Dynamically log all values from config.py
    logging.info("\n--- CONFIGURATION SETTINGS ---")

    # Get all non-special attributes (those not starting with __)
    config_attrs = [attr for attr in dir(config) if not attr.startswith("__")]
    for attr in config_attrs:
        value = getattr(config, attr)
        # Skip functions and modules
        if not callable(value) and not isinstance(value, type(config)):
            logging.info(f"{attr}: {value}")
    logging.info("----------------------------\n")


class ExperimentRunner:
    """Main class to run experiments with configurable parameters."""

    def __init__(self, experiment_name, base_dir, config_module):
        """Initialize the experiment runner.

        Args:
            experiment_name: Name of the experiment (e.g., "rq1", "rq2")
            base_dir: Base directory for the experiment
            config_module: Configuration module for the experiment
        """
        self.experiment_name = experiment_name
        self.base_dir = base_dir
        self.config = config_module

    def run(self):
        """Main execution method that orchestrates the entire experiment run."""
        # Create performance monitor
        perf_monitor = PerformanceMonitor()

        # Parse command-line arguments
        args = parse_arguments(self.experiment_name)

        # Validate that only one mode is selected
        if args.get_only and args.test_only:
            print("Error: Cannot specify both --get-only and --test-only")
            sys.exit(1)

        # Validate that --folders and --exclude-folders are not both specified
        if args.folders and args.exclude_folders:
            print("Error: Cannot specify both --folders and --exclude-folders")
            sys.exit(1)

        # Set up logging and get the log file path
        log_file = setup_logging(self.base_dir, self.experiment_name)

        # Log config
        log_config(self.config)

        # Create the parallel executor
        executor = ParallelExecutor(perf_monitor, self.base_dir)

        # Determine the execution mode
        mode = "default"
        if args.get_only:
            mode = "get-only"
            logging.info(f"Starting {self.experiment_name}/run_all.py in GET-ONLY mode")
        elif args.test_only:
            mode = "test-only"
            logging.info(
                f"Starting {self.experiment_name}/run_all.py in TEST-ONLY mode"
            )
        else:
            logging.info(
                f"Starting {self.experiment_name}/run_all.py in GENERATE-AND-TEST mode"
            )

        # Get all directories in the experiment, or just the specified ones
        if args.folders:
            subdirs = [
                folder
                for folder in args.folders
                if os.path.isdir(os.path.join(self.base_dir, folder))
            ]
            missing = [folder for folder in args.folders if folder not in subdirs]
            if missing:
                logging.error(
                    f"Specified folder(s) do not exist in {self.experiment_name}: {missing}"
                )
                sys.exit(1)
        elif args.exclude_folders:
            # Exclude common non-experiment directories plus blacklisted folders
            excluded_dirs = {"__pycache__", "logs", "results_all"}
            all_dirs = [
                d
                for d in os.listdir(self.base_dir)
                if os.path.isdir(os.path.join(self.base_dir, d))
                and d not in excluded_dirs
            ]

            # Validate that excluded folders exist (warn if they don't)
            missing_exclude = [
                folder for folder in args.exclude_folders if folder not in all_dirs
            ]
            if missing_exclude:
                logging.warning(
                    f"Some excluded folder(s) do not exist in {self.experiment_name}: {missing_exclude}"
                )

            # Remove blacklisted folders
            subdirs = [d for d in all_dirs if d not in args.exclude_folders]

            if not subdirs:
                logging.error("No directories left to run after exclusions")
                sys.exit(1)

            logging.info(
                f"Excluding directories: {[f for f in args.exclude_folders if f in all_dirs]}"
            )
        else:
            # Exclude common non-experiment directories
            excluded_dirs = {"__pycache__", "logs", "results_all"}
            subdirs = [
                d
                for d in os.listdir(self.base_dir)
                if os.path.isdir(os.path.join(self.base_dir, d))
                and d not in excluded_dirs
            ]

        logging.info(f"Found {len(subdirs)} subdirectories to process: {subdirs}")

        # Execute tasks based on the mode
        executor.execute(subdirs, mode)

        # Finish timing and log performance summary
        perf_monitor.finish()
        perf_monitor.log_summary()

        # Log config again at the end
        log_config(self.config)

        # Force garbage collection to prevent post-execution memory bloat
        import gc

        logging.info("Forcing garbage collection to free memory...")
        gc.collect()  # Collect unreferenced objects
        gc.collect()  # Second pass for any remaining circular references
        gc.collect()  # Third pass to be thorough
        logging.info("Garbage collection completed.")

        logging.info(f"\nAll processes completed. Log saved to: {log_file}")
