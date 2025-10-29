"""
Finview - Gestionnaire de Portefeuille Financier

Application complète de gestion de patrimoine développée avec Streamlit.
Permet de gérer, analyser et visualiser un portefeuille financier comprenant
des liquidités, investissements financiers, investissements immobiliers et crédits.

Modules principaux:
- models: Classes de données (Portfolio, Investment, Credit)
- operations: Opérations sur le portfolio (ajout, vente, paiements)
- charts: Visualisations Plotly interactives
- market: Recherche et données de marché (Yahoo Finance)
- predictions: Simulations et prédictions patrimoniales
- pages: Pages Streamlit de l'application
- ui: Composants UI réutilisables
- pdf: Génération de rapports PDF
"""

# Classes principales
from .models import (
    Portfolio,
    Investment,
    FinancialInvestment,
    RealEstateInvestment,
    Credit
)

# Opérations sur le portfolio
from .operations import (
    add_cash,
    withdraw_cash,
    add_financial_investment,
    add_real_estate_investment,
    update_investment_value,
    sell_investment,
    add_credit,
    pay_credit
)

# Visualisations
from .charts import (
    create_portfolio_pie_chart,
    create_financial_investments_chart,
    create_monthly_transactions_chart
)

# Recherche de marché
from .market import (
    search_asset,
    get_asset_info,
    asset_search_tab
)

# Fixtures
from .fixture import create_demo_portfolio_4

# PDF
from .pdf import generate_portfolio_pdf

__all__ = [
    # Models
    'Portfolio',
    'Investment',
    'FinancialInvestment',
    'RealEstateInvestment',
    'Credit',
    # Operations
    'add_cash',
    'withdraw_cash',
    'add_financial_investment',
    'add_real_estate_investment',
    'update_investment_value',
    'sell_investment',
    'add_credit',
    'pay_credit',
    # Charts
    'create_portfolio_pie_chart',
    'create_financial_investments_chart',
    'create_monthly_transactions_chart',
    # Market
    'search_asset',
    'get_asset_info',
    'asset_search_tab',
    # Fixtures
    'create_demo_portfolio_4',
    # PDF
    'generate_portfolio_pdf'
]

__version__ = "1.0.0"
__author__ = "M2 MOSEF - Base de Données & Dashboard"
