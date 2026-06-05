"""BlueLog: An ultra-lightweight logging extension with ANSI colors and SUCCESS level.

This module initializes the package interface, exposing the core factory 
function and custom level constants for clean and seamless integration.
"""

from .core import get_logger, SUCCESS_LEVEL_NUM

# Alias for clean accessibility (e.g., bluelog.SUCCESS)
SUCCESS = SUCCESS_LEVEL_NUM

# Define explicit public interface for wildcard imports
__all__ = ["get_logger", "SUCCESS"]

# Package semantic versioning
__version__ = "0.1.0"