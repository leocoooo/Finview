"""Streamlit wrapper functions for portfolio persistence.

This module provides Streamlit-specific wrappers around the core save/load functions,
handling UI feedback (success messages, error displays) for the Streamlit interface.
"""

import streamlit as st
from typing import Optional
from src.finview.models.portfolio import Portfolio
from src.finview.storage import (
    save_portfolio as _save_portfolio,
    load_portfolio as _load_portfolio,
    delete_portfolio as _delete_portfolio,
    DEFAULT_FILEPATH
)


def save_portfolio_ui(portfolio, filename: str = DEFAULT_FILEPATH, show_success: bool = True) -> bool:
    """Save portfolio with Streamlit UI feedback.
    
    Args:
        portfolio: Portfolio instance to save
        filename: Path to save file
        show_success: Whether to show success message
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    success, error = _save_portfolio(portfolio, filename)
    
    if success:
        if show_success:
            st.success("✅ Portfolio saved successfully!")
        return True
    else:
        st.error(f"❌ Error saving portfolio: {error}")
        return False


def load_portfolio_ui(filename: str = DEFAULT_FILEPATH, show_messages: bool = False) -> Optional[Portfolio]:
    """Load portfolio with optional Streamlit UI feedback.
    
    Args:
        filename: Path to load file
        show_messages: Whether to show status messages
        
    Returns:
        Portfolio instance if loaded successfully, None otherwise
    """
    portfolio, error = _load_portfolio(filename)
    
    if portfolio:
        if show_messages:
            st.success("✅ Portfolio loaded successfully!")
        return portfolio
    else:
        if show_messages and error and "File not found" not in error:
            st.error(f"❌ Error loading portfolio: {error}")
        return None


def delete_portfolio_ui(filename: str = DEFAULT_FILEPATH) -> bool:
    """Delete portfolio with Streamlit UI feedback.
    
    Args:
        filename: Path to file to delete
        
    Returns:
        bool: True if deleted successfully, False otherwise
    """
    success, error = _delete_portfolio(filename)
    
    if success:
        st.success("✅ Portfolio file deleted successfully!")
        return True
    else:
        st.error(f"❌ Error deleting portfolio: {error}")
        return False


# For backward compatibility - use the original function name
def save_portfolio(portfolio, filename: str = DEFAULT_FILEPATH) -> bool:
    """Backward compatibility wrapper for save_portfolio.
    
    Deprecated: Use save_portfolio_ui for new code.
    """
    return save_portfolio_ui(portfolio, filename, show_success=False)


def load_portfolio(filename: str = DEFAULT_FILEPATH) -> Optional[Portfolio]:
    """Backward compatibility wrapper for load_portfolio.
    
    Deprecated: Use load_portfolio_ui for new code.
    """
    return load_portfolio_ui(filename, show_messages=False)
