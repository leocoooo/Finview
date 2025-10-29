"""Storage module for portfolio persistence.

This module handles all data persistence operations for portfolios,
including saving to and loading from JSON files.
"""

from .portfolio_storage import (
    save_portfolio,
    load_portfolio,
    validate_portfolio,
    ensure_save_directory,
    portfolio_exists,
    delete_portfolio,
    DEFAULT_SAVE_DIR,
    DEFAULT_FILENAME,
    DEFAULT_FILEPATH
)

__all__ = [
    'save_portfolio',
    'load_portfolio',
    'validate_portfolio',
    'ensure_save_directory',
    'portfolio_exists',
    'delete_portfolio',
    'DEFAULT_SAVE_DIR',
    'DEFAULT_FILENAME',
    'DEFAULT_FILEPATH'
]
