"""
Centralized logging for haunted-shell.
Outputs diagnostics to stderr only when debug mode is enabled.
"""

import logging
import os
import sys
from typing import Optional

LOGGER_NAME = "haunted_shell"
logger = logging.getLogger(LOGGER_NAME)


def setup_logger(debug: bool = False, log_file: Optional[str] = None) -> logging.Logger:
    """Configure the haunted-shell logger."""
    env_debug = os.environ.get("HAUNTED_DEBUG", "").lower() in {"1", "true", "yes"}
    is_debug = debug or env_debug

    level = logging.DEBUG if is_debug else logging.WARNING
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicates on re-init
    for handler in list(logger.handlers):
        logger.removeHandler(handler)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [haunted_shell] %(message)s", datefmt="%H:%M:%S"
    )

    # Console handler (stderr only, so stdout remains clean for CLI pipes)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Optional file handler
    if log_file:
        try:
            os.makedirs(os.path.dirname(os.path.abspath(log_file)), exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except OSError:
            pass

    return logger
