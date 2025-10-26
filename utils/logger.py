import logging
import sys

LOGGER_NAME = "app_logger"

_debug_enabled = False


def setup_logger() -> logging.Logger:
    """
    Sets up the logger for the application.

    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(LOGGER_NAME)

    if getattr(sys, "frozen", False):
        logger.addHandler(logging.NullHandler())
        logging.disable(logging.CRITICAL)
        return logger

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if _debug_enabled else logging.INFO)

    return logger


def get_logger() -> logging.Logger:
    """
    Retrieves the configured logger instance.

    Returns:
        logging.Logger: The logger instance.
    """
    return logging.getLogger(LOGGER_NAME)


def enable_debug(enable: bool) -> None:
    """
    Enables or disables debug mode.

    Args:
        enable (bool): True to enable debug mode, False to disable.
    """
    global _debug_enabled
    _debug_enabled = enable
    get_logger().setLevel(logging.DEBUG if enable else logging.INFO)


def debug_enabled() -> bool:
    """
    Checks if debug mode is enabled.

    Returns:
        bool: True if debug mode is enabled, False otherwise.
    """
    return _debug_enabled
