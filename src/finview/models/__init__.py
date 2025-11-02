"""
Models module - Classes de données pour le portfolio

Ce module contient les classes de base pour représenter les différents
éléments d'un portefeuille financier :
- Portfolio : Conteneur principal du patrimoine
- Investment : Classe de base pour les investissements
- FinancialInvestment : Investissements financiers (actions, ETF, obligations, crypto)
- RealEstateInvestment : Investissements immobiliers (SCPI, REIT, immobilier direct)
- Credit : Gestion des crédits et emprunts
"""

from .portfolio import Portfolio
from .investments import Investment, FinancialInvestment, RealEstateInvestment
from .credit import Credit

__all__ = [
    # Portfolio principal
    'Portfolio',
    # Investissements
    'Investment',
    'FinancialInvestment',
    'RealEstateInvestment',
    # Crédits
    'Credit'
]

__version__ = "1.0.0"
