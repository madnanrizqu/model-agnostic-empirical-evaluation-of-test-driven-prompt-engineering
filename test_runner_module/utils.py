import json
import os
import pandas as pd
import threading
import subprocess  # Add this import


# Add the TimeoutExecutor class before the TestRunner class
class TimeoutExecutor:
    """A utility class that executes functions with a timeout."""

    @staticmethod
    def execute_with_timeout(function, timeout, *args, **kwargs):
        """
        Execute a function with a timeout.

        Args:
            function: The function to execute
            timeout: Maximum execution time in seconds
            *args, **kwargs: Arguments to pass to the function

        Returns:
            The result of the function if completed within timeout,
            or a subprocess.CompletedProcess-like object if execution exceeds the timeout.
        """
        result = None
        exception = None
        execution_completed = False

        def target_function():
            nonlocal result, exception, execution_completed
            try:
                result = function(*args, **kwargs)
            except Exception as e:
                exception = e
            finally:
                execution_completed = True

        thread = threading.Thread(target=target_function)
        thread.daemon = True
        thread.start()
        thread.join(timeout=timeout)

        if not execution_completed:
            # Execution timed out - create a CompletedProcess-like object
            return subprocess.CompletedProcess(
                args=[],
                returncode=1,
                stdout="",
                stderr=f"Test execution timed out after {timeout} seconds - possible infinite loop",
            )
        elif exception:
            # Execution raised an exception - create a CompletedProcess-like object
            return subprocess.CompletedProcess(
                args=[],
                returncode=1,
                stdout="",
                stderr=f"{str(exception)}",
            )
        else:
            # Execution completed successfully within timeout
            return result
