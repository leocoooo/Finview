"""
Predictions page - Monte Carlo simulations for portfolio forecasting
"""

import time

import pandas as pd
import streamlit as st

from src.finview.ui.formatting import format_currency
from src.finview.patrimoine_prediction import (
    simulate_portfolio_future,
    create_prediction_chart,
    create_statistics_summary,
)


def show_predictions(portfolio):
    """Page de prédictions patrimoniales"""
    st.header("🔮 Wealth Predictions")

    if not portfolio.investments:
        st.info("Add investments to see predictions")
        return

    # Configuration
    col1, col2 = st.columns(2)
    with col1:
        years = st.selectbox("Prediction horizon", options=[1, 5, 10, 20, 30], index=2)
    with col2:
        num_simulations = st.selectbox("Number of simulations", options=[100, 500, 1000, 2000], index=2)

    # Options avancées
    with st.expander("⚙️ Advanced Options"):
        include_inflation = st.checkbox("Include inflation (2% avg)", value=True,
                                        help="Adjust values for purchasing power")
        include_fees = st.checkbox("Include management fees", value=True,
                                   help="Annual fees: 0.3% ETF, 1% SCPI, etc.")
        st.info("""
        **Realistic Simulation includes:**
        - 🔻 Market crashes (~12% probability/year, -20% to -50%)
        - 📉 Market corrections (~25% probability/year, -10% to -20%)
        - 💸 Inflation (2% average)
        - 💰 Management fees (0.3% to 2% depending on asset)
        - 📊 Asset correlation during crises
        """)

    # Bouton de lancement
    run_prediction = st.button("🚀 Run Prediction", type="primary", use_container_width=True)

    if run_prediction:
        progress_text = "Running Monte Carlo simulations..."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            my_bar.progress(percent_complete + 1)
            time.sleep(0.04)

        my_bar.empty()

        with st.spinner(f"Analyzing {num_simulations} scenarios over {years} years..."):
            prediction_results = simulate_portfolio_future(
                portfolio,
                years=years,
                num_simulations=num_simulations,
                include_inflation=include_inflation,
                include_fees=include_fees
            )
            st.session_state.prediction_results = prediction_results
            st.session_state.prediction_years = years

        st.success("✅ Prediction completed successfully!")

    # Affichage des résultats
    if 'prediction_results' in st.session_state:
        results = st.session_state.prediction_results
        stats = create_statistics_summary(results)

        # Tabs
        tab1, tab2, tab3 = st.tabs(["📊 Chart", "📈 Key Metrics", "📋 Detailed Table"])

        with tab1:
            _show_prediction_chart(results, stats)

        with tab2:
            _show_key_metrics(stats, results)

        with tab3:
            _show_detailed_projections(results)


def _show_prediction_chart(results, stats):
    """Affiche le graphique de prédiction"""
    fig = create_prediction_chart(results)
    st.plotly_chart(fig, use_container_width=True)

    # Métriques clés sous le graphique
    st.markdown("---")
    st.markdown("##### Initial Wealth")
    st.metric("💼 Current Portfolio", format_currency(stats['initial']))

    st.markdown(f"##### After {stats['years']} Years")

    col1, col2, col3 = st.columns(3)

    with col1:
        gain_pct_p10 = stats['gain_percentages']['p10']
        annual_p10 = stats['returns']['p10']

        st.metric(
            label="🔴 Pessimistic (P10)",
            value=format_currency(stats['final']['p10']),
            delta=f"{gain_pct_p10:+.1f}% total | {annual_p10:+.1f}% annual"
        )

    with col2:
        gain_p50 = stats['gains']['p50']
        gain_pct_p50 = stats['gain_percentages']['p50']
        annual_p50 = stats['returns']['p50']

        st.metric(
            label="🔵 Median (P50)",
            value=format_currency(stats['final']['p50']),
            delta=f"{gain_pct_p50:+.1f}% total | {annual_p50:+.1f}% annual",
            delta_color="inverse" if gain_p50 < 0 else "normal"
        )

    with col3:
        gain_p75 = stats['gains']['p75']
        gain_pct_p75 = stats['gain_percentages']['p75']
        annual_p75 = stats['returns']['p75']

        st.metric(
            label="🟢 Optimistic (P75)",
            value=format_currency(stats['final']['p75']),
            delta=f"{gain_pct_p75:+.1f}% total | {annual_p75:+.1f}% annual",
            delta_color="inverse" if gain_p75 < 0 else "normal"
        )


def _show_key_metrics(stats, results):
    """Affiche les métriques clés avec couleurs"""
    st.subheader("📈 Portfolio Evolution - Key Scenarios")

    # Helper function pour afficher les métriques avec couleur
    def format_metric_with_color(label, value, gain, gain_pct, annual_return):
        """Affiche une métrique avec indicateurs de couleur"""
        color = "🟢" if gain >= 0 else "🔴"
        delta_text = f"{gain_pct:+.1f}% total | {annual_return:+.1f}% annual"
        st.metric(
            label=f"{color} {label}",
            value=format_currency(value),
            delta=delta_text
        )

    st.markdown("##### Initial Wealth")
    st.metric("💼 Current Portfolio", format_currency(stats['initial']))

    st.markdown(f"##### After {stats['years']} Years")

    # Grille de métriques
    col1, col2, col3 = st.columns(3)

    with col1:
        format_metric_with_color(
            "Pessimistic (P10)",
            stats['final']['p10'],
            stats['gains']['p10'],
            stats['gain_percentages']['p10'],
            stats['returns']['p10']
        )

    with col2:
        format_metric_with_color(
            "Median (P50)",
            stats['final']['p50'],
            stats['gains']['p50'],
            stats['gain_percentages']['p50'],
            stats['returns']['p50']
        )

    with col3:
        format_metric_with_color(
            "Optimistic (P75)",
            stats['final']['p75'],
            stats['gains']['p75'],
            stats['gain_percentages']['p75'],
            stats['returns']['p75']
        )

    st.markdown("---")

    # Tableau récapitulatif détaillé
    st.markdown("##### 📊 Complete Statistics")

    summary_data = []
    for scenario, label in [
        ('p10', 'Pessimistic (P10)'),
        ('p25', 'Conservative (P25)'),
        ('p50', 'Median (P50)'),
        ('mean', 'Average'),
        ('p75', 'Optimistic (P75)'),
        ('p90', 'Very Optimistic (P90)')
    ]:
        final_val = stats['final'][scenario]
        gain = stats['gains'][scenario]
        gain_pct = stats['gain_percentages'][scenario]
        annual_ret = stats['returns'][scenario]

        # Emoji selon performance
        if gain >= 0:
            emoji = "📈" if gain_pct > 20 else "➡️"
        else:
            emoji = "📉"

        summary_data.append({
            'Scenario': f"{emoji} {label}",
            'Final Value': format_currency(final_val),
            'Gain/Loss': format_currency(gain),
            'Total Return': f"{gain_pct:+.1f}%",
            'Annual Return': f"{annual_ret:+.1f}%"
        })

    df_summary = pd.DataFrame(summary_data)

    # Styling du dataframe
    def style_dataframe(df):
        def color_gain(val):
            if '€' in val:
                amount_str = val.replace('€', '').replace(' ', '').replace(',', '')
                try:
                    amount = float(amount_str)
                    return 'color: #2ecc71' if amount >= 0 else 'color: #e74c3c'
                except Exception:
                    return ''
            elif '%' in val:
                pct_str = val.replace('%', '').replace(' ', '')
                try:
                    pct = float(pct_str)
                    return 'color: #2ecc71' if pct >= 0 else 'color: #e74c3c'
                except Exception:
                    return ''
            return ''

        return df.style.applymap(color_gain, subset=['Gain/Loss', 'Total Return', 'Annual Return'])

    st.dataframe(
        style_dataframe(df_summary),
        use_container_width=True,
        hide_index=True
    )

    # Probabilité de perte
    st.markdown("---")
    st.markdown("##### ⚠️ Risk Analysis")

    # Calculer probabilité de perte
    simulations = results['simulations']
    final_values = simulations[:, -1]
    prob_loss = (final_values < stats['initial']).sum() / len(final_values) * 100
    prob_major_loss = (final_values < stats['initial'] * 0.8).sum() / len(final_values) * 100
    prob_double = (final_values > stats['initial'] * 2).sum() / len(final_values) * 100

    risk_col1, risk_col2, risk_col3 = st.columns(3)

    with risk_col1:
        st.metric(
            "📉 Probability of Loss",
            f"{prob_loss:.1f}%",
            help="Chance of having less than initial value"
        )

    with risk_col2:
        st.metric(
            "⚠️ Major Loss (>-20%)",
            f"{prob_major_loss:.1f}%",
            help="Chance of losing more than 20% of value"
        )

    with risk_col3:
        st.metric(
            "🚀 Doubling Wealth",
            f"{prob_double:.1f}%",
            help="Chance of doubling your portfolio"
        )


def _show_detailed_projections(results):
    """Affiche les projections détaillées année par année"""
    st.subheader("📋 Year-by-Year Projections")

    # Choix d'affichage
    show_nominal = st.checkbox(
        "Show nominal values (without inflation adjustment)",
        value=False,
        help="Nominal values don't account for purchasing power erosion"
    )

    # Sélectionner les bonnes percentiles
    if show_nominal and 'percentiles_nominal' in results:
        percentiles_to_use = results['percentiles_nominal']
        value_type = " (Nominal)"
    else:
        percentiles_to_use = results['percentiles']
        value_type = " (Real)" if results.get('include_inflation') else ""

    # Créer le tableau
    projection_data = []
    percentiles = percentiles_to_use
    initial_value = results['initial_value']

    # Helper function to calculate annualized return
    def calc_annualized_return(initial, final, years):
        if years == 0 or initial <= 0:
            return 0
        return ((final / initial) ** (1 / years) - 1) * 100

    for year in range(results['years'] + 1):
        row = {
            'Year': year,
            'P10 (Pessimistic)': format_currency(percentiles['p10'][year]),
            'P25 (Conservative)': format_currency(percentiles['p25'][year]),
            'P50 (Median)': format_currency(percentiles['p50'][year]),
            'P75 (Optimistic)': format_currency(percentiles['p75'][year]),
            'P90 (Very Optimistic)': format_currency(percentiles['p90'][year]),
            'Average': format_currency(percentiles['mean'][year])
        }

        # Add annualized returns for each percentile
        if year > 0:
            row['Annualized Return P10 (%)'] = f"{calc_annualized_return(initial_value, percentiles['p10'][year], year):+.1f}%"
            row['Annualized Return P25 (%)'] = f"{calc_annualized_return(initial_value, percentiles['p25'][year], year):+.1f}%"
            row['Annualized Return P50 (%)'] = f"{calc_annualized_return(initial_value, percentiles['p50'][year], year):+.1f}%"
            row['Annualized Return P75 (%)'] = f"{calc_annualized_return(initial_value, percentiles['p75'][year], year):+.1f}%"
            row['Annualized Return P90 (%)'] = f"{calc_annualized_return(initial_value, percentiles['p90'][year], year):+.1f}%"
            row['Annualized Return Avg (%)'] = f"{calc_annualized_return(initial_value, percentiles['mean'][year], year):+.1f}%"
        else:
            row['Annualized Return P10 (%)'] = "—"
            row['Annualized Return P25 (%)'] = "—"
            row['Annualized Return P50 (%)'] = "—"
            row['Annualized Return P75 (%)'] = "—"
            row['Annualized Return P90 (%)'] = "—"
            row['Annualized Return Avg (%)'] = "—"

        projection_data.append(row)

    df_projections = pd.DataFrame(projection_data)

    # Affichage avec style
    st.markdown(f"**Values shown{value_type}**")

    st.dataframe(
        df_projections,
        use_container_width=True,
        height=min(600, (results['years'] + 2) * 35),
        hide_index=True
    )

    # Téléchargement CSV
    csv = df_projections.to_csv(index=False)
    st.download_button(
        label="📥 Download projections (CSV)",
        data=csv,
        file_name=f"portfolio_predictions_{results['years']}years.csv",
        mime="text/csv"
    )

    # Légende
    st.markdown("---")
    st.info("""
    **Interpretation Guide:**
    - **P10 (Pessimistic)**: Only 10% of scenarios are worse. Includes major market crashes.
    - **P25 (Conservative)**: 25% of scenarios are worse. Includes moderate crises.
    - **P50 (Median)**: Half of scenarios above, half below. Most realistic central scenario.
    - **P75 (Optimistic)**: 75% of scenarios are worse. Favorable market conditions.
    - **P90 (Very Optimistic)**: 90% of scenarios are worse. Exceptional growth.

    **Real vs Nominal Values:**
    - **Real values**: Adjusted for inflation (purchasing power)
    - **Nominal values**: Raw numbers without inflation adjustment

    **This simulation includes:**
    ✅ Market crashes (~12% probability per year)
    ✅ Market corrections (~25% probability per year)  
    ✅ Inflation (2% average)
    ✅ Management fees (0.3% to 2% depending on assets)
    ✅ Asset correlation during crises
    """)

    # Warning sur les limites
    st.warning("""
    ⚠️ **Important Limitations:**
    - Past performance does not guarantee future results
    - Black swan events (COVID, 2008 crisis) can exceed simulation parameters
    - Individual stock risk is higher than diversified portfolios
    - Tax implications are not included
    - This is a statistical tool, not financial advice
    """)