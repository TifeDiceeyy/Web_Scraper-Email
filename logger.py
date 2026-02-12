#!/usr/bin/env python3
"""
Centralized logging configuration for the outreach system
"""

import logging
import sys
from pathlib import Path


def setup_logger(name="outreach", log_file="outreach.log", level=logging.INFO):
    """
    Set up a logger with both file and console handlers

    Args:
        name: Logger name
        log_file: Path to log file
        level: Logging level (default: INFO)

    Returns:
        logging.Logger: Configured logger instance
    """

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers if logger already exists
    if logger.handlers:
        return logger

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    simple_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )

    # File handler (detailed logs)
    try:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not create log file: {e}")

    # Console handler (simple logs for user)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)

    return logger


# Global logger instance
logger = setup_logger()
