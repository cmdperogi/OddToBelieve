"""Structured logging configuration for OddToBelieve.

Sets up two formatters:
- WARNING and above: include module name for traceability
- INFO and below: compact format without module name
"""

import logging
import logging.config


class _ModuleNameFilter(logging.Filter):
    """Pass only WARNING-and-above records to a handler."""

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno >= logging.WARNING


def configure_logging(log_level: str = "INFO") -> None:
    """Configure root logger.  Call once at application startup."""
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    root = logging.getLogger()
    root.setLevel(numeric_level)

    if root.handlers:
        root.handlers.clear()

    # INFO- handler: compact, no module name
    info_handler = logging.StreamHandler()
    info_handler.setLevel(numeric_level)
    info_handler.addFilter(_BelowWarningFilter())
    info_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

    # WARNING+ handler: includes module name for traceability
    warn_handler = logging.StreamHandler()
    warn_handler.setLevel(logging.WARNING)
    warn_handler.setFormatter(
        logging.Formatter("%(levelname)s [%(name)s]: %(message)s")
    )

    root.addHandler(info_handler)
    root.addHandler(warn_handler)


class _BelowWarningFilter(logging.Filter):
    """Pass only records below WARNING level."""

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno < logging.WARNING
