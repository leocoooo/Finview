"""
Pages package - Application pages
"""

from src.finview.pages.summary import show_summary
from src.finview.pages.management import show_wealth_management
from src.finview.pages.analytics import show_dashboard_tabs
from src.finview.pages.predictions import show_predictions
from src.finview.pages.content import show_news, show_definitions

__all__ = [
    'show_summary',
    'show_wealth_management',
    'show_dashboard_tabs',
    'show_predictions',
    'show_news',
    'show_definitions',
]