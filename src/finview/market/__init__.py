"""
Market module - Recherche et récupération de données financières

Ce module fournit des outils pour rechercher et analyser des actifs financiers
via l'API Yahoo Finance.
"""

from .asset_search import search_asset, get_asset_info, get_asset_history
from .asset_display import create_price_chart, format_asset_info
from .asset_ui import asset_search_tab

__all__ = [
    # Core search functions
    'search_asset',
    'get_asset_info',
    'get_asset_history',
    # Display functions
    'create_price_chart',
    'format_asset_info',
    # UI components
    'asset_search_tab'
]

__version__ = "1.0.0"
