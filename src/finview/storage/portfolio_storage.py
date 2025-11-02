"""Portfolio persistence functions for saving and loading portfolio data.

This module provides functions to save and load portfolio data to/from JSON files.
It handles file creation, validation, and error management.
"""

import json
import os
import logging
from pathlib import Path
from typing import Optional, Tuple
from src.finview.models.portfolio import Portfolio


# Configuration
DEFAULT_SAVE_DIR = "saved_json_data"
DEFAULT_FILENAME = "portfolio_data.json"
DEFAULT_FILEPATH = os.path.join(DEFAULT_SAVE_DIR, DEFAULT_FILENAME)

# Encoding settings
FILE_ENCODING = 'utf-8'
JSON_INDENT = 2

# Logger configuration
logger = logging.getLogger(__name__)


def ensure_save_directory(directory: str = DEFAULT_SAVE_DIR) -> bool:
    """Ensure the save directory exists, create it if necessary.
    
    Args:
        directory: Path to the directory to create
        
    Returns:
        bool: True if directory exists or was created successfully, False otherwise
    """
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {directory}: {e}")
        return False


def validate_portfolio(portfolio) -> Tuple[bool, Optional[str]]:
    """Validate portfolio before saving.
    
    Args:
        portfolio: Portfolio instance to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if portfolio is None:
        return False, "Portfolio is None"
    
    if not hasattr(portfolio, 'to_dict'):
        return False, "Portfolio does not have to_dict method"
    
    try:
        # Test conversion to dict
        data = portfolio.to_dict()
        if not isinstance(data, dict):
            return False, "Portfolio.to_dict() did not return a dictionary"
        return True, None
    except Exception as e:
        return False, f"Error converting portfolio to dict: {e}"


def save_portfolio(portfolio, filename: str = DEFAULT_FILEPATH) -> Tuple[bool, Optional[str]]:
    """Save portfolio to a JSON file.
    
    Args:
        portfolio: Portfolio instance to save
        filename: Path to the file where portfolio will be saved
        
    Returns:
        Tuple of (success, error_message)
        - success: True if saved successfully, False otherwise
        - error_message: None if successful, error description otherwise
        
    Example:
        >>> portfolio = Portfolio()
        >>> success, error = save_portfolio(portfolio)
        >>> if success:
        ...     print("Portfolio saved!")
        ... else:
        ...     print(f"Error: {error}")
    """
    # Validate portfolio
    is_valid, error_msg = validate_portfolio(portfolio)
    if not is_valid:
        logger.error(f"Portfolio validation failed: {error_msg}")
        return False, error_msg
    
    # Ensure directory exists
    directory = os.path.dirname(filename)
    if directory and not ensure_save_directory(directory):
        error_msg = f"Failed to create directory: {directory}"
        logger.error(error_msg)
        return False, error_msg
    
    # Save to file
    try:
        with open(filename, 'w', encoding=FILE_ENCODING) as f:
            json.dump(
                portfolio.to_dict(),
                f,
                indent=JSON_INDENT,
                ensure_ascii=False
            )
        logger.info(f"Portfolio saved successfully to {filename}")
        return True, None
        
    except PermissionError as e:
        error_msg = f"Permission denied when writing to {filename}: {e}"
        logger.error(error_msg)
        return False, error_msg
        
    except IOError as e:
        error_msg = f"I/O error when writing to {filename}: {e}"
        logger.error(error_msg)
        return False, error_msg
        
    except Exception as e:
        error_msg = f"Unexpected error during save: {e}"
        logger.error(error_msg)
        return False, error_msg


def load_portfolio(filename: str = DEFAULT_FILEPATH) -> Tuple[Optional[Portfolio], Optional[str]]:
    """Load portfolio from a JSON file.
    
    Args:
        filename: Path to the file to load
        
    Returns:
        Tuple of (portfolio, error_message)
        - portfolio: Portfolio instance if loaded successfully, None otherwise
        - error_message: None if successful, error description otherwise
        
    Example:
        >>> portfolio, error = load_portfolio()
        >>> if portfolio:
        ...     print(f"Portfolio loaded with {len(portfolio.investments)} investments")
        ... else:
        ...     print(f"Error: {error}")
    """
    # Check if file exists
    if not os.path.exists(filename):
        logger.info(f"No saved portfolio found at {filename}")
        return None, f"File not found: {filename}"
    
    # Load from file
    try:
        with open(filename, 'r', encoding=FILE_ENCODING) as f:
            data = json.load(f)
            
        # Validate loaded data
        if not isinstance(data, dict):
            error_msg = "Loaded data is not a valid dictionary"
            logger.error(error_msg)
            return None, error_msg
        
        # Convert to Portfolio
        portfolio = Portfolio.from_dict(data)
        logger.info(f"Portfolio loaded successfully from {filename}")
        return portfolio, None
        
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON format in {filename}: {e}"
        logger.error(error_msg)
        return None, error_msg
        
    except PermissionError as e:
        error_msg = f"Permission denied when reading {filename}: {e}"
        logger.error(error_msg)
        return None, error_msg
        
    except IOError as e:
        error_msg = f"I/O error when reading {filename}: {e}"
        logger.error(error_msg)
        return None, error_msg
        
    except Exception as e:
        error_msg = f"Unexpected error during load: {e}"
        logger.error(error_msg)
        return None, error_msg


def portfolio_exists(filename: str = DEFAULT_FILEPATH) -> bool:
    """Check if a portfolio file exists.
    
    Args:
        filename: Path to the file to check
        
    Returns:
        bool: True if file exists, False otherwise
    """
    return os.path.exists(filename) and os.path.isfile(filename)


def delete_portfolio(filename: str = DEFAULT_FILEPATH) -> Tuple[bool, Optional[str]]:
    """Delete a portfolio file.
    
    Args:
        filename: Path to the file to delete
        
    Returns:
        Tuple of (success, error_message)
    """
    if not os.path.exists(filename):
        return False, f"File not found: {filename}"
    
    try:
        os.remove(filename)
        logger.info(f"Portfolio file deleted: {filename}")
        return True, None
    except Exception as e:
        error_msg = f"Error deleting file {filename}: {e}"
        logger.error(error_msg)
        return False, error_msg
