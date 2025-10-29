"""
Module de prédiction de patrimoine avec simulations Monte Carlo

Ce package fournit des outils pour simuler l'évolution future d'un portefeuille
en utilisant des simulations Monte Carlo réalistes incluant :
- Scénarios de crise et corrections de marché
- Ajustement pour l'inflation
- Frais de gestion
- Rendements historiques conservateurs
"""

from .monte_carlo import simulate_portfolio_future, create_statistics_summary
from .visualizations import create_prediction_chart
from .utils import get_asset_return_params, get_asset_category

__all__ = [
    "simulate_portfolio_future",
    "create_statistics_summary",
    "create_prediction_chart",
    "get_asset_return_params",
    "get_asset_category",
]

__version__ = "1.0.0"
