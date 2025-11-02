"""
Operations module - Opérations sur le portfolio avec gestion des dates

Ce module fournit des fonctions pour effectuer des opérations sur le portfolio
en enregistrant automatiquement l'historique des transactions.
"""

from .cash_operations import add_cash, withdraw_cash
from .investment_operations import (
    add_financial_investment,
    add_real_estate_investment,
    update_investment_value,
    sell_investment
)
from .credit_operations import add_credit, pay_credit

__all__ = [
    # Cash operations
    'add_cash',
    'withdraw_cash',
    # Investment operations
    'add_financial_investment',
    'add_real_estate_investment',
    'update_investment_value',
    'sell_investment',
    # Credit operations
    'add_credit',
    'pay_credit'
]

__version__ = "1.0.0"
