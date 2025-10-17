import os
import subprocess
import sys
import logging
import time
from collections import defaultdict
from contextlib import contextmanager
import concurrent.futures
import threading


class ThreadSafeLogger:
    """Thread-safe logging utility."""

    def __init__(self):
        self.log_lock = threading.Lock()

    def log(self, level, message):
        """Thread-safe logging wrapper."""
        with self.log_lock:
            if level == "INFO":
                logging.info(message)
            elif level == "WARNING":
                logging.warning(message)
            elif level == "ERROR":
                logging.error(message)


class PerformanceMonitor:
    """Class to track and log execution times for various operations."""

    def __init__(self):
        self.total_start_time = time.time()
        self.timing_stats = {
            "total_time": 0,
            "subdirectory_times": {},
            "get_solution_times": {},
            "test_solution_times": {},
        }

    @contextmanager
    def time_operation(self, operation_type, identifier):
        """Context manager to time an operation.

        Args:
            operation_type: Type of operation ('subdir', 'get_solution', 'test_solution')
            identifier: Name or path to identify the operation
        """
        start_time = time.time()
        elapsed_time = 0
        try:
            yield lambda: time.time() - start_time  # Yield a function to get current elapsed time
        finally:
            elapsed_time = time.time() - start_time

            if operation_type == "subdir":
                self.timing_stats["subdirectory_times"][identifier] = elapsed_time
            elif operation_type == "get_solution":
                self.timing_stats["get_solution_times"][identifier] = elapsed_time
            elif operation_type == "test_solution":
                self.timing_stats["test_solution_times"][identifier] = elapsed_time

    def finish(self):
        """Calculate the total execution time."""
        self.timing_stats["total_time"] = time.time() - self.total_start_time
        return self.timing_stats

    def log_summary(self):
        """Log a summary of all timing information."""
        logging.info("\n--- PERFORMANCE BENCHMARK ---")
        logging.info(
            f"Total execution time: {self.timing_stats['total_time']:.2f} seconds"
        )

        if self.timing_stats["subdirectory_times"]:
            logging.info("\nSubdirectory processing times:")
            for subdir, time_taken in self.timing_stats["subdirectory_times"].items():
                logging.info(f"  {subdir}: {time_taken:.2f} seconds")

        if self.timing_stats["get_solution_times"]:
            logging.info("\nget_solution.py execution times:")
            for path, time_taken in self.timing_stats["get_solution_times"].items():
                subdir = os.path.basename(path)
                logging.info(f"  {subdir}: {time_taken:.2f} seconds")

        if self.timing_stats["test_solution_times"]:
            logging.info("\ntest_solution.py execution times:")
            for path, time_taken in self.timing_stats["test_solution_times"].items():
                subdir = os.path.basename(path)
                logging.info(f"  {subdir}: {time_taken:.2f} seconds")


class ScriptRunner:
    """Class responsible for running Python scripts."""

    def __init__(self, perf_monitor, logger):
        """Initialize the script runner.

        Args:
            perf_monitor: PerformanceMonitor instance for timing operations
            logger: ThreadSafeLogger instance for logging
        """
        self.perf_monitor = perf_monitor
        self.logger = logger

    def run_script(self, script_path):
        """Run a Python script and log its output."""
        script_name = os.path.basename(script_path)
        operation_type = (
            "get_solution" if script_name == "get_solution.py" else "test_solution"
        )

        with self.perf_monitor.time_operation(
            operation_type, os.path.dirname(script_path)
        ) as get_elapsed_time:
            try:
                # Log the start of script execution
                self.logger.log("INFO", f"Starting: {script_name}")

                # Run the script but don't log detailed output
                result = subprocess.run(
                    [sys.executable, script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True,
                )

                # Log successful completion with timing
                elapsed_time = get_elapsed_time()
                self.logger.log("INFO", f"Completed: {script_name} ({elapsed_time:.1f}s)")
                return True

            except subprocess.CalledProcessError as e:
                self.logger.log("ERROR", f"Error running {script_name}: {e}")
                if e.stdout:
                    self.logger.log("ERROR", f"\n--- STDOUT before failure ---")
                    self.logger.log("ERROR", e.stdout)
                if e.stderr:
                    self.logger.log("ERROR", f"\n--- STDERR from failure ---")
                    self.logger.log("ERROR", e.stderr)

                elapsed_time = get_elapsed_time()  # Get the elapsed time
                self.logger.log(
                    "INFO", f"Failed {script_name} after {elapsed_time:.2f} seconds"
                )
                return False


class SubdirectoryProcessor:
    """Class responsible for processing subdirectories."""

    def __init__(self, perf_monitor, logger, script_runner, base_dir):
        """Initialize the subdirectory processor.

        Args:
            perf_monitor: PerformanceMonitor instance for timing operations
            logger: ThreadSafeLogger instance for logging
            script_runner: ScriptRunner instance for running scripts
            base_dir: Base directory for all operations
        """
        self.perf_monitor = perf_monitor
        self.logger = logger
        self.script_runner = script_runner
        self.base_dir = base_dir

    def process_subdir(self, subdir):
        """Process a single subdirectory by running get_solution.py and test_solution.py."""
        with self.perf_monitor.time_operation("subdir", subdir):
            subdir_path = os.path.join(self.base_dir, subdir)
            get_solution_path = os.path.join(subdir_path, "get_solution.py")
            test_solution_path = os.path.join(subdir_path, "test_solution.py")

            # Check if test script exists
            if not os.path.isfile(test_solution_path):
                self.logger.log("WARNING", f"Missing test_solution.py in {subdir}")
                return False

            # Check and run get_solution.py
            if not os.path.isfile(get_solution_path):
                self.logger.log("WARNING", f"Missing get_solution.py in {subdir}")
                return False

            # Log just the start of processing
            self.logger.log("INFO", f"Processing: {subdir}")

            # Run get_solution.py first
            self.logger.log("INFO", f"Running get_solution.py for {subdir}")
            run_test = self.script_runner.run_script(get_solution_path)
            if not run_test:
                self.logger.log(
                    "WARNING", f"Failed to run get_solution.py for {subdir}"
                )
                return False

            # Run test_solution.py if get_solution.py succeeded
            self.logger.log("INFO", f"Running test_solution.py for {subdir}")
            test_result = self.script_runner.run_script(test_solution_path)

            # No need for completion log since progress is tracked in the executor
            return True


class ParallelExecutor:
    """Class to handle parallel execution of scripts across subdirectories."""

    def __init__(self, perf_monitor, base_dir):
        """Initialize the executor with a performance monitor.

        Args:
            perf_monitor: PerformanceMonitor instance
            base_dir: Base directory for all operations
        """
        self.perf_monitor = perf_monitor
        self.base_dir = base_dir

        # Create composed objects
        self.logger = ThreadSafeLogger()
        self.script_runner = ScriptRunner(perf_monitor, self.logger)
        self.subdir_processor = SubdirectoryProcessor(
            perf_monitor, self.logger, self.script_runner, self.base_dir
        )

    def execute(self, subdirs, mode="default", max_workers=None):
        """Execute tasks across subdirectories based on the specified mode.

        Args:
            subdirs (list): List of subdirectory names to process
            mode (str): Execution mode - "default", "get-only", or "test-only"
            max_workers (int, optional): Maximum number of parallel workers
        """
        if not subdirs:
            self.logger.log("WARNING", "No subdirectories to process")
            return

        # Calculate max_workers for parallel modes
        if not max_workers:
            max_workers = min(os.cpu_count() or 4, len(subdirs))

        if mode == "get-only":
            self.logger.log("INFO", f"Using {max_workers} parallel workers")
            self._run_get_only(subdirs, max_workers)
        elif mode == "test-only":
            self.logger.log("INFO", f"Using {max_workers} parallel workers")
            self._run_test_only(subdirs, max_workers)
        else:  # default mode
            self.logger.log("INFO", f"Using {max_workers} parallel workers")
            self._run_default(subdirs, max_workers)

    def _run_get_only(self, subdirs, max_workers):
        """Run get_solution.py scripts in parallel."""
        total_subdirs = len(subdirs)
        completed_subdirs = 0
        progress_lock = threading.Lock()

        def process_get_only(subdir):
            nonlocal completed_subdirs
            with self.perf_monitor.time_operation("subdir", subdir):
                subdir_path = os.path.join(self.base_dir, subdir)
                get_solution_path = os.path.join(subdir_path, "get_solution.py")

                if not os.path.isfile(get_solution_path):
                    self.logger.log("WARNING", f"Missing get_solution.py in {subdir}")
                    with progress_lock:
                        completed_subdirs += 1
                        self.logger.log(
                            "INFO",
                            f"Skipped {subdir}. Progress: {completed_subdirs}/{total_subdirs} subdirectories processed ({(completed_subdirs/total_subdirs*100):.1f}%)",
                        )
                    return False

                self.logger.log("INFO", f"[{completed_subdirs + 1}/{total_subdirs}] Running get_solution.py for {subdir}")
                result = self.script_runner.run_script(get_solution_path)
                
                with progress_lock:
                    completed_subdirs += 1
                    self.logger.log(
                        "INFO",
                        f"Completed {subdir}. Progress: {completed_subdirs}/{total_subdirs} subdirectories processed ({(completed_subdirs/total_subdirs*100):.1f}%)",
                    )
                return result

        self.logger.log(
            "INFO", f"Starting parallel processing of {total_subdirs} subdirectories"
        )

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all directories for parallel processing
            futures = [
                executor.submit(process_get_only, subdir) for subdir in subdirs
            ]

            # Wait for all tasks to complete
            concurrent.futures.wait(futures)

        self.logger.log("INFO", f"Completed processing all {total_subdirs} subdirectories")

    def _run_test_only(self, subdirs, max_workers):
        """Run test_solution.py scripts in parallel."""
        total_subdirs = len(subdirs)
        completed_subdirs = 0
        progress_lock = threading.Lock()

        def process_test_only(subdir):
            nonlocal completed_subdirs
            with self.perf_monitor.time_operation("subdir", subdir):
                subdir_path = os.path.join(self.base_dir, subdir)
                test_solution_path = os.path.join(subdir_path, "test_solution.py")

                if not os.path.isfile(test_solution_path):
                    self.logger.log("WARNING", f"Missing test_solution.py in {subdir}")
                    with progress_lock:
                        completed_subdirs += 1
                        self.logger.log(
                            "INFO",
                            f"Skipped {subdir}. Progress: {completed_subdirs}/{total_subdirs} subdirectories processed ({(completed_subdirs/total_subdirs*100):.1f}%)",
                        )
                    return False

                self.logger.log("INFO", f"[{completed_subdirs + 1}/{total_subdirs}] Running test_solution.py for {subdir}")
                result = self.script_runner.run_script(test_solution_path)
                
                with progress_lock:
                    completed_subdirs += 1
                    self.logger.log(
                        "INFO",
                        f"Completed {subdir}. Progress: {completed_subdirs}/{total_subdirs} subdirectories processed ({(completed_subdirs/total_subdirs*100):.1f}%)",
                    )
                return result

        self.logger.log(
            "INFO", f"Starting parallel testing of {total_subdirs} subdirectories"
        )

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all directories for parallel processing
            futures = [
                executor.submit(process_test_only, subdir) for subdir in subdirs
            ]

            # Wait for all tasks to complete
            concurrent.futures.wait(futures)

        self.logger.log("INFO", f"Completed testing all {total_subdirs} subdirectories")

    def _run_default(self, subdirs, max_workers):
        """Run both get_solution.py and test_solution.py in parallel with progress tracking."""
        total_subdirs = len(subdirs)
        completed_subdirs = 0
        progress_lock = threading.Lock()

        def process_with_progress(subdir):
            nonlocal completed_subdirs
            result = self.subdir_processor.process_subdir(subdir)
            with progress_lock:
                completed_subdirs += 1
                self.logger.log(
                    "INFO",
                    f"Completed {subdir}. Progress: {completed_subdirs}/{total_subdirs} subdirectories completed ({(completed_subdirs/total_subdirs*100):.1f}%)",
                )
            return result

        self.logger.log(
            "INFO", f"Starting parallel processing of {total_subdirs} subdirectories"
        )

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all directories for parallel processing
            futures = [
                executor.submit(process_with_progress, subdir) for subdir in subdirs
            ]

            # Wait for all tasks to complete
            concurrent.futures.wait(futures)

        self.logger.log("INFO", f"Completed all {total_subdirs} subdirectories")