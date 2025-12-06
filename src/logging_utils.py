"""Centralized logging configuration for the NEL demo application.

The functions here provide a single entry point for creating loggers with a
consistent format. Downstream modules should call :func:`get_logger` instead of
configuring logging themselves to avoid duplicate handlers and mismatched
formats.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

DEFAULT_LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def setup_logging(level: Optional[int] = None) -> None:
    """Configure the root logger with a sensible default format.

    Args:
        level: Optional log level; if omitted, respects the ``LOG_LEVEL``
            environment variable and falls back to :data:`DEFAULT_LOG_LEVEL`.
    """

    resolved_level = level
    if resolved_level is None:
        env_value = os.getenv("LOG_LEVEL", "").upper()
        resolved_level = getattr(logging, env_value, DEFAULT_LOG_LEVEL)

    logging.basicConfig(level=resolved_level, format=LOG_FORMAT)


def get_logger(name: str) -> logging.Logger:
    """Return a module-scoped logger configured via :func:`setup_logging`.

    Args:
        name: Logger name, typically ``__name__`` from the caller.

    Returns:
        A :class:`logging.Logger` instance.
    """

    return logging.getLogger(name)
