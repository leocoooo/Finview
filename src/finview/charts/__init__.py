"""
Charts module - Graphiques et visualisations pour le portfolio

Ce module fournit tous les graphiques et visualisations nécessaires pour l'application Finview.
"""

# Configuration
from .config import (
    THEME,
    VIBRANT_COLORS,
    VIBRANT_COLORS_RGBA,
    TRANSACTION_COLORS,
    TRANSACTION_LABELS,
    AVAILABLE_BENCHMARKS,
    LOCATION_COORDS
)

# Layouts
from .layouts import get_base_layout

# Historique du portfolio
from .history import (
    get_financial_portfolio_value_at_date,
    get_total_invested_at_date,
    get_portfolio_monthly_history
)

# Données de marché
from .market_data import (
    get_cac40_data,
    get_dji_data,
    get_btc_data,
    get_benchmark_data,
    create_benchmark_kpi_card,
    create_kpi_metrics
)

# Graphiques du portfolio
from .portfolio_charts import (
    create_portfolio_pie_chart,
    create_financial_investments_chart,
    create_performance_chart,
    create_performance_chart_filtered
)

# Graphiques d'analyse
from .analysis_charts import (
    create_monthly_transactions_chart,
    create_financial_portfolio_vs_benchmark_chart,
    render_portfolio_comparison
)

# Carte géographique
from .geo_charts import create_world_investment_map

# Wrappers Streamlit pour l'affichage
import streamlit as st


def display_predictions(results):
    """
    Wrapper minimal pour afficher le graphique de prédiction.
    
    Args:
        results: Résultats de simulation Monte Carlo
    """
    try:
        from src.finview.predictions import create_prediction_chart
    except Exception:
        st.error("Module de prédiction introuvable")
        return
    fig = create_prediction_chart(results)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def display_portfolio_pie(portfolio):
    """
    Affiche le graphique en donut du portfolio
    
    Args:
        portfolio: Instance de Portfolio
    """
    st.plotly_chart(create_portfolio_pie_chart(portfolio), use_container_width=True, config={'displayModeBar': False})


def display_financial_investments(portfolio):
    """
    Affiche le graphique des investissements financiers
    
    Args:
        portfolio: Instance de Portfolio
    """
    st.plotly_chart(create_financial_investments_chart(portfolio), use_container_width=True, config={'displayModeBar': False})


def display_performance_chart(portfolio):
    """
    Affiche le graphique de performance
    
    Args:
        portfolio: Instance de Portfolio
    """
    st.plotly_chart(create_performance_chart(portfolio), use_container_width=True, config={'displayModeBar': False})


def display_world_map(portfolio):
    """
    Affiche la carte mondiale des investissements
    
    Args:
        portfolio: Instance de Portfolio
    """
    fig = create_world_investment_map(portfolio)
    fig.update_layout(height=700)
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d']
    })


__all__ = [
    # Configuration
    'THEME',
    'VIBRANT_COLORS',
    'VIBRANT_COLORS_RGBA',
    'TRANSACTION_COLORS',
    'TRANSACTION_LABELS',
    'AVAILABLE_BENCHMARKS',
    'LOCATION_COORDS',
    # Layouts
    'get_base_layout',
    # Historique
    'get_financial_portfolio_value_at_date',
    'get_total_invested_at_date',
    'get_portfolio_monthly_history',
    # Données de marché
    'get_cac40_data',
    'get_dji_data',
    'get_btc_data',
    'get_benchmark_data',
    'create_benchmark_kpi_card',
    'create_kpi_metrics',
    # Graphiques portfolio
    'create_portfolio_pie_chart',
    'create_financial_investments_chart',
    'create_performance_chart',
    'create_performance_chart_filtered',
    # Graphiques analyse
    'create_monthly_transactions_chart',
    'create_financial_portfolio_vs_benchmark_chart',
    'render_portfolio_comparison',
    # Géographie
    'create_world_investment_map',
    # Wrappers Streamlit
    'display_predictions',
    'display_portfolio_pie',
    'display_financial_investments',
    'display_performance_chart',
    'display_world_map'
]

__version__ = "1.0.0"
