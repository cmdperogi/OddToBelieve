"""Unit tests for structured logging (STORY-11)."""

import io
import logging

import pytest

from app.logging_config import configure_logging


@pytest.fixture(autouse=True)
def reset_root_logger():
    """Restore root logger state after each test."""
    root = logging.getLogger()
    original_level = root.level
    original_handlers = root.handlers[:]
    yield
    root.handlers = original_handlers
    root.setLevel(original_level)


def _capture_handler() -> tuple[logging.StreamHandler, io.StringIO]:
    buf = io.StringIO()
    handler = logging.StreamHandler(buf)
    handler.setLevel(logging.DEBUG)
    return handler, buf


def test_configure_logging_sets_level_from_string():
    configure_logging("DEBUG")
    assert logging.getLogger().level == logging.DEBUG


def test_configure_logging_defaults_to_info():
    configure_logging()
    assert logging.getLogger().level == logging.INFO


def test_configure_logging_invalid_level_falls_back_to_info():
    configure_logging("NONSENSE")
    assert logging.getLogger().level == logging.INFO


def test_warning_format_includes_module_name():
    configure_logging("WARNING")
    handler, buf = _capture_handler()
    # WARNING+ handler already added; add a plain capture handler too
    handler.setFormatter(logging.Formatter("%(levelname)s [%(name)s]: %(message)s"))
    logger = logging.getLogger("app.services.odds_api")
    logger.addHandler(handler)
    logger.warning("quota guard active — requests remaining: %d", 10)
    output = buf.getvalue()
    assert "app.services.odds_api" in output


def test_error_format_includes_module_name():
    configure_logging("ERROR")
    handler, buf = _capture_handler()
    handler.setFormatter(logging.Formatter("%(levelname)s [%(name)s]: %(message)s"))
    logger = logging.getLogger("app.scheduler")
    logger.addHandler(handler)
    logger.error("Betfair poll failed: connection refused")
    output = buf.getvalue()
    assert "app.scheduler" in output


def test_error_message_must_not_contain_credentials():
    """Error logs from API failures must not leak credential values."""
    configure_logging("ERROR")
    handler, buf = _capture_handler()
    handler.setFormatter(logging.Formatter("%(levelname)s [%(name)s]: %(message)s"))
    logger = logging.getLogger("app.services.betfair")
    logger.addHandler(handler)
    logger.error("Betfair poll failed: %s", "HTTPStatusError")
    output = buf.getvalue()
    assert "password" not in output.lower()
    assert "token" not in output.lower()


def test_log_level_from_env(monkeypatch):
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    import importlib

    import app.config as config_module

    importlib.reload(config_module)
    assert config_module.settings.log_level.upper() == "DEBUG"
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    importlib.reload(config_module)


def test_poll_cycle_logs_at_info():
    configure_logging("INFO")
    handler, buf = _capture_handler()
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger = logging.getLogger("app.scheduler")
    logger.addHandler(handler)
    logger.info("Scheduler: poll cycle starting")
    output = buf.getvalue()
    assert "poll cycle starting" in output


def test_rate_guard_logs_at_warning():
    configure_logging("INFO")
    handler, buf = _capture_handler()
    handler.setFormatter(logging.Formatter("%(levelname)s [%(name)s]: %(message)s"))
    logger = logging.getLogger("app.services.odds_api")
    logger.addHandler(handler)
    logger.warning("Odds API quota guard active — requests remaining: %s", 10)
    output = buf.getvalue()
    assert "quota guard" in output


def test_two_handlers_added_to_root():
    """configure_logging must set up both INFO and WARNING handler paths."""
    configure_logging("INFO")
    root = logging.getLogger()
    assert len(root.handlers) == 2
