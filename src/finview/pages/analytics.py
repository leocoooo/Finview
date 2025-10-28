"""
Analytics/Dashboard page - Portfolio visualizations and performance charts
"""

import streamlit as st

from src.finview.ui.formatting import format_currency
from src.finview.visualizations import (
    display_financial_investments,
    display_performance_chart,
    display_world_map,
    render_portfolio_comparison,
    create_portfolio_pie_chart,
    create_performance_chart_filtered,
    create_kpi_metrics,
    get_cac40_data,
    get_dji_data,
    get_btc_data,
)


def show_dashboard_tabs(portfolio):
    """Dashboard avec onglets graphiques"""
    st.header("📈 Dashboard")
    tab1, tab2, tab3 = st.tabs(["📊 Portfolio", "💎 Assets", "🌍 Investments Map"])

    with tab1: 
        show_portfolio_charts(portfolio)
    with tab2: 
        show_assets_analytics(portfolio)
    with tab3: 
        show_world_map(portfolio)


def show_portfolio_charts(portfolio):
    """Fonction principale pour l'onglet Portfolio"""

    if not portfolio.investments:
        st.info("No portfolio to analyze")
        return

    # KPIs en haut
    _display_kpi_row(portfolio)

    # Graphiques
    _display_dashboard_charts(portfolio)


def _display_kpi_row(portfolio):
    """Affiche la rangée de KPIs en haut du dashboard"""
    kpis = create_kpi_metrics(portfolio)
    cac40_value, cac40_change = get_cac40_data()
    dji_value, dji_change = get_dji_data()
    btc_value, btc_change = get_btc_data()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="💰 Net Worth",
            value=format_currency(kpis['net_worth']),
            delta=None
        )

    with col2:
        st.metric(
            label="📈 Investments",
            value=format_currency(kpis['investment_value']),
            delta=f"{kpis['investment_change']:+.1f}%"
        )

    with col3:
        st.metric(
            label="📊 BTC-USD",
            value=format_currency(round(btc_value, -1)),
            delta=f"{btc_change:+.2f}%"
        )
    
    with col4:
        st.metric(
            label="📊 CAC40",
            value=format_currency(round(cac40_value, 0)),
            delta=f"{cac40_change:+.2f}%"
        )

    with col5:
        st.metric(
            label="📊 DJI",
            value=format_currency(round(dji_value, 0)),
            delta=f"{dji_change:+.2f}%"
        )


def _display_dashboard_charts(portfolio):
    """Affiche les graphiques principaux du dashboard"""
    st.markdown("<div style='margin-top:-1rem;'></div>", unsafe_allow_html=True)

    # Graphique principal en pleine largeur
    render_portfolio_comparison(portfolio)

    col1, col2 = st.columns(2)
    with col1:
        fig_pie = create_portfolio_pie_chart(portfolio)
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False, "height": 390})

    with col2:
        fig_perf = create_performance_chart_filtered(portfolio)
        st.plotly_chart(fig_perf, use_container_width=True, config={"displayModeBar": False, "height": 390})


def show_assets_analytics(portfolio):
    """Affiche l'analyse détaillée des actifs"""
    if not portfolio.investments:
        st.info("No investments to analyze")
        return
    
    display_financial_investments(portfolio)
    st.markdown("---")
    display_performance_chart(portfolio)


def show_world_map(portfolio):
    """Affiche la carte des investissements géolocalisés"""
    if len(portfolio.financial_investments) + len(portfolio.real_estate_investments) > 0:
        display_world_map(portfolio)

        # Legend for map
        st.markdown("""
            <div style='text-align: center; font-size: 14px; color: #94A3B8; margin-top: 10px;'>
                <span style='color: #3B82F6; font-weight: bold;'>●</span> <b>Blue:</b> Financial investments &nbsp;&nbsp;&nbsp;
                <span style='color: #F59E0B; font-weight: bold;'>●</span> <b>Orange:</b> Real estate investments
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("🌍 No investments to locate at the moment")