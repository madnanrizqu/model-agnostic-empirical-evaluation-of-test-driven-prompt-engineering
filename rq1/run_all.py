#!/usr/bin/env python3
"""
RQ1 Experiment Runner

Thin wrapper around the shared experiment runner infrastructure.
Configures and runs RQ1 experiments with proper paths and configuration.
"""

import os
import sys

# Get the absolute path to the rq2 directory
RQ2_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(RQ2_DIR, ".."))
sys.path.append(ROOT_DIR)

from experiment_runner import ExperimentRunner
import config.rq1 as config


def main():
    """Main entry point for RQ1 experiment execution."""
    runner = ExperimentRunner("rq1", RQ2_DIR, config)
    runner.run()


if __name__ == "__main__":
    main()