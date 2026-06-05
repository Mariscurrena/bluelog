import logging
import sys
import re
from typing import Optional

# Numeric priority for the new SUCCESS level (positioned between INFO: 20 and WARNING: 30)
SUCCESS_LEVEL_NUM = 25
logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")


def success(self, message: str, *args, **kws) -> None:
    """Dynamically injected method into logging.Logger to support the SUCCESS level.

    This method allows developers to call `logger.success("msg")` natively,
    ensuring compliance with standard logging severity checks and parameter handling.

    Args:
        message (str): The log message or a format string.
        *args: Variable length argument list to format the message string.
        **kws: Arbitrary keyword arguments passed down to the underlying logger
            (e.g., exc_info, stack_info, extra).
    """
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kws)


# Bind the success method to the native Logger class
logging.Logger.success = success

# ANSI Format Escape Codes
RESET = "\x1b[0m"
BOLD = "\x1b[1m"

# Map logging levels to their respective high-visibility ANSI colors
COLORS = {
    logging.DEBUG: "\x1b[36m",        # Cyan
    logging.INFO: "\x1b[32m",         # Green
    SUCCESS_LEVEL_NUM: "\x1b[1;32m",  # Bold Bright Green (Cybersecurity Success)
    logging.WARNING: "\x1b[33m",      # Yellow
    logging.ERROR: "\x1b[31m",        # Red
    logging.CRITICAL: "\x1b[1;41m"    # White Bold Text on Red Background (Incident/Panic)
}


class ColoredFormatter(logging.Formatter):
    """Custom logging formatter that dynamically applies ANSI colors to log levels.

    Inherits from the native logging.Formatter. It intercepts the format pipeline
    to wrap the `%(levelname)s` placeholder with terminal color codes based on
    the record's severity level.
    """

    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None):
        """Initializes the formatter with custom log format and date structures.

        Args:
            fmt (str, optional): A standard logging format string. Defaults to None.
            datefmt (str, optional): A strftime format string for timestamps. Defaults to None.
        """
        super().__init__(fmt, datefmt)

    def format(self, record: logging.LogRecord) -> str:
        """Formats the specified record as text, colorizing the level name prefix.

        This approach isolates color escape codes within the `levelname` field,
        leaving the raw message clean and easily pipeable into SIEM or external tools.

        Args:
            record (logging.LogRecord): The log record instance containing log metadata.

        Returns:
            str: The color-coded and fully formatted log string ready for terminal stdout.
        """
        log_fmt = self._style._fmt
        level_color = COLORS.get(record.levelno, RESET)

        # Safely wrap only the level name tag with ANSI colors and reset them afterwards
        custom_fmt = re.sub(r"(%\(levelname\).*?s)", f"{level_color}\\1{RESET}", log_fmt)

        # Create a transient formatter to securely parse the current log record
        formatter = logging.Formatter(custom_fmt, self.datefmt)
        return formatter.format(record)


def get_logger(name: str = "app", level: int = logging.INFO) -> logging.Logger:
    """Factory function that retrieves or initializes a customized BlueLog instance.

    Guarantees the setup of a high-visibility terminal StreamHandler with proper
    color formatting. Includes safety checks to prevent stream duplication and log
    bubbling in multi-module setups.

    Args:
        name (str, optional): The name of the logger (typically used for tracking
            sub-systems). Defaults to "app".
        level (int, optional): The initial logging severity threshold. Defaults to logging.INFO.

    Returns:
        logging.Logger: A fully configured Logger instance equipped with BlueLog formatting
            and the custom success method.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Idempotency guard: Prevent adding handlers if the logger has already been configured
    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # Standard clean blueprint for production environments
        log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"

        formatter = ColoredFormatter(log_format, date_format)
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

        # Stop log propagation to root to eliminate double log entries across frameworks
        logger.propagate = False

    return logger