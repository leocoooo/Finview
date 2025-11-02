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
    'create_world_investment_map'
]

__version__ = "1.0.0"
