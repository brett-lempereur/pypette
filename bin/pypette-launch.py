#!/usr/bin/env python
"""
This module provides the command-line scripts for launching experiments, and
preparing data for analysts and techniques.
"""

import argparse
import logging

import pypette.experiment as experiment

# Logging formats.
CONSOLE_FORMAT = "<%(asctime)s> %(name)s - %(message)s"
FILE_FORMAT = "<%(asctime)s> %(name)s - %(message)s"
DATE_FORMAT = "%H:%M:%S"

# Command-line arguments for the launch script.
launch_args = argparse.ArgumentParser(
    description="launch a live digital forensic experiment"
)
launch_args.add_argument("-v", "--verbose", action="store_true",
                         help="increase output verbosity")
launch_args.add_argument("definition", type=argparse.FileType("r"),
                         help="the experiment definition")

# Main script entry point.
if __name__ == "__main__":
    args = launch_args.parse_args()
    # Configure logging.
    logging.basicConfig(
        format=CONSOLE_FORMAT,
        datefmt=DATE_FORMAT,
        level=logging.DEBUG if args.verbose else logging.INFO
    )
    ch = logging.FileHandler("./experiment.log")
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter(FILE_FORMAT, datefmt=DATE_FORMAT))
    logging.getLogger("pypette").addHandler(ch)
    # Interpret the configuration document and conduct the experiment.
    document = args.definition.read()
    definition = experiment.Definition(document)
    experiment.conduct(definition)

