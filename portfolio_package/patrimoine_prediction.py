"""
Module de prédiction du patrimoine basé sur des simulations Monte Carlo
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================================
# DONNÉES HISTORIQUES DE RENDEMENTS ANNUELS MOYENS
# ============================================================================
# Basées sur les moyennes historiques réelles ajustées pour plus de réalisme
# Format: {'mean': rendement annuel moyen (%), 'std': volatilité (%), 'distribution': type}
#
# Distributions utilisées:
#   - 'normal': distribution normale (Gaussienne) pour actifs traditionnels
#   - 'lognormal': distribution log-normale pour actifs à forte asymétrie
# ============================================================================

HISTORICAL_RETURNS = {
    # ========================================================================
    # CRYPTOMONNAIES - Haute volatilité / Haute croissance potentielle
    # ========================================================================
    'Bitcoin': {'mean': 30.0, 'std': 65.0, 'distribution': 'lognormal'},
    'Ethereum': {'mean': 28.0, 'std': 70.0, 'distribution': 'lognormal'},
    'Crypto': {'mean': 25.0, 'std': 70.0, 'distribution': 'lognormal'},
    'Altcoin': {'mean': 20.0, 'std': 80.0, 'distribution': 'lognormal'},

    # ========================================================================
    # ACTIONS INDIVIDUELLES - Volatilité moyenne à haute
    # ========================================================================
    # Tech Giants (GAFAM)
    'Actions Apple': {'mean': 15.0, 'std': 30.0, 'distribution': 'normal'},
    'Actions Microsoft': {'mean': 14.0, 'std': 28.0, 'distribution': 'normal'},
    'Actions Google': {'mean': 13.5, 'std': 29.0, 'distribution': 'normal'},
    'Actions Amazon': {'mean': 16.0, 'std': 35.0, 'distribution': 'normal'},
    'Actions Meta': {'mean': 12.0, 'std': 40.0, 'distribution': 'normal'},

    # Growth / Tech
    'Actions Tesla': {'mean': 12.0, 'std': 45.0, 'distribution': 'normal'},
    'Actions Nvidia': {'mean': 18.0, 'std': 42.0, 'distribution': 'normal'},
    'Actions Netflix': {'mean': 11.0, 'std': 38.0, 'distribution': 'normal'},

    # Secteur Financier
    'Actions Bancaires': {'mean': 8.0, 'std': 22.0, 'distribution': 'normal'},
    'Actions Assurance': {'mean': 7.5, 'std': 20.0, 'distribution': 'normal'},

    # Luxe & Consommation (France)
    'Actions LVMH': {'mean': 13.0, 'std': 25.0, 'distribution': 'normal'},
    'Actions Hermès': {'mean': 14.0, 'std': 22.0, 'distribution': 'normal'},

    # Énergie
    'Actions Énergies Renouvelables': {'mean': 9.0, 'std': 32.0, 'distribution': 'normal'},
    'Actions Pétrole': {'mean': 6.5, 'std': 28.0, 'distribution': 'normal'},

    # Valeur par défaut pour actions
    'Action': {'mean': 10.0, 'std': 20.0, 'distribution': 'normal'},

    # ========================================================================
    # ETF - Volatilité moyenne / Diversification
    # ========================================================================
    # Indices Majeurs
    'ETF S&P 500': {'mean': 8.0, 'std': 16.0, 'distribution': 'normal'},
    'ETF Nasdaq': {'mean': 9.0, 'std': 18.0, 'distribution': 'normal'},
    'ETF CAC 40': {'mean': 6.0, 'std': 17.0, 'distribution': 'normal'},
    'ETF Europe': {'mean': 6.5, 'std': 18.0, 'distribution': 'normal'},
    'ETF World': {'mean': 7.5, 'std': 15.0, 'distribution': 'normal'},
    'ETF MSCI World': {'mean': 7.5, 'std': 15.0, 'distribution': 'normal'},

    # Marchés Émergents
    'ETF Émergents': {'mean': 8.5, 'std': 22.0, 'distribution': 'normal'},
    'ETF Chine': {'mean': 7.0, 'std': 25.0, 'distribution': 'normal'},
    'ETF Inde': {'mean': 9.0, 'std': 23.0, 'distribution': 'normal'},

    # Sectoriels
    'ETF Tech': {'mean': 10.0, 'std': 20.0, 'distribution': 'normal'},
    'ETF Santé': {'mean': 8.5, 'std': 16.0, 'distribution': 'normal'},
    'ETF ESG': {'mean': 7.5, 'std': 16.0, 'distribution': 'normal'},

    # Valeur par défaut
    'ETF': {'mean': 7.0, 'std': 16.0, 'distribution': 'normal'},

    # ========================================================================
    # IMMOBILIER - Faible à moyenne volatilité
    # ========================================================================
    # SCPI (Sociétés Civiles de Placement Immobilier)
    'SCPI Bureaux Paris': {'mean': 4.0, 'std': 6.0, 'distribution': 'normal'},
    'SCPI Résidentiel': {'mean': 4.2, 'std': 5.5, 'distribution': 'normal'},
    'SCPI Commerce': {'mean': 4.5, 'std': 7.0, 'distribution': 'normal'},
    'SCPI Diversifiée': {'mean': 4.3, 'std': 5.8, 'distribution': 'normal'},
    'SCPI Europe': {'mean': 4.0, 'std': 6.5, 'distribution': 'normal'},
    'SCPI': {'mean': 4.0, 'std': 5.0, 'distribution': 'normal'},

    # REIT (Real Estate Investment Trusts)
    'REIT Résidentiel US': {'mean': 5.5, 'std': 12.0, 'distribution': 'normal'},
    'REIT Commercial': {'mean': 5.8, 'std': 13.0, 'distribution': 'normal'},
    'REIT': {'mean': 5.5, 'std': 12.0, 'distribution': 'normal'},

    # Immobilier Direct
    'Immobilier direct': {'mean': 4.5, 'std': 8.0, 'distribution': 'normal'},
    'Immobilier locatif': {'mean': 5.0, 'std': 9.0, 'distribution': 'normal'},

    # ========================================================================
    # OBLIGATIONS - Très faible volatilité / Revenus fixes
    # ========================================================================
    'Obligations États AAA': {'mean': 2.5, 'std': 3.0, 'distribution': 'normal'},
    'Obligations Entreprises': {'mean': 3.5, 'std': 5.0, 'distribution': 'normal'},
    'Obligations High Yield': {'mean': 5.0, 'std': 8.0, 'distribution': 'normal'},
    'Obligations Émergentes': {'mean': 6.0, 'std': 10.0, 'distribution': 'normal'},
    'Obligations': {'mean': 3.0, 'std': 4.0, 'distribution': 'normal'},
    'Obligation': {'mean': 3.0, 'std': 4.0, 'distribution': 'normal'},

    # ========================================================================
    # MATIÈRES PREMIÈRES & ALTERNATIFS
    # ========================================================================
    'Or': {'mean': 4.0, 'std': 15.0, 'distribution': 'normal'},
    'Argent': {'mean': 5.0, 'std': 22.0, 'distribution': 'normal'},
    'Commodities': {'mean': 5.5, 'std': 20.0, 'distribution': 'normal'},
    'Private Equity': {'mean': 12.0, 'std': 25.0, 'distribution': 'lognormal'},

    # ========================================================================
    # FONDS & LIQUIDITÉS - Faible risque
    # ========================================================================
    'Fonds Diversifié': {'mean': 6.5, 'std': 11.0, 'distribution': 'normal'},
    'Fonds Actions': {'mean': 8.0, 'std': 16.0, 'distribution': 'normal'},
    'Fonds Obligations': {'mean': 3.5, 'std': 5.0, 'distribution': 'normal'},
    'Fonds': {'mean': 6.0, 'std': 12.0, 'distribution': 'normal'},
    'Liquidités': {'mean': 2.5, 'std': 0.3, 'distribution': 'normal'},
    'Livret A': {'mean': 3.0, 'std': 0.1, 'distribution': 'normal'},
    'Compte Épargne': {'mean': 2.0, 'std': 0.2, 'distribution': 'normal'},
}


def get_asset_return_params(asset_name, asset_type=None):
    """
    Récupère les paramètres de rendement pour un actif

    Args:
        asset_name: Nom de l'actif
        asset_type: Type d'actif (optionnel)

    Returns:
        dict: {'mean': float, 'std': float, 'distribution': str}
    """
    # Chercher d'abord par nom exact
    if asset_name in HISTORICAL_RETURNS:
        return HISTORICAL_RETURNS[asset_name]

    # Chercher par correspondance partielle
    asset_name_lower = asset_name.lower()
    for key, params in HISTORICAL_RETURNS.items():
        if key.lower() in asset_name_lower:
            return params

    # Chercher par type
    if asset_type and asset_type in HISTORICAL_RETURNS:
        return HISTORICAL_RETURNS[asset_type]

    # Défaut conservateur
    return {'mean': 6.0, 'std': 14.0, 'distribution': 'normal'}


def simulate_portfolio_future(portfolio, years=10, num_simulations=1000):
    """
    Simule l'évolution future du portefeuille avec Monte Carlo

    Args:
        portfolio: Instance du Portfolio
        years: Nombre d'années à simuler
        num_simulations: Nombre de simulations Monte Carlo

    Returns:
        dict: Résultats des simulations
    """
    # Collecter la composition actuelle du portefeuille
    portfolio_composition = []

    # Liquidités
    if portfolio.cash > 0:
        portfolio_composition.append({
            'name': 'Liquidités',
            'value': portfolio.cash,
            'type': 'Liquidités',
            'params': HISTORICAL_RETURNS['Liquidités']
        })

    # Investissements financiers
    for name, inv in portfolio.financial_investments.items():
        inv_type = getattr(inv, 'investment_type', 'Action')
        params = get_asset_return_params(name, inv_type)
        portfolio_composition.append({
            'name': name,
            'value': inv.get_total_value(),
            'type': inv_type,
            'params': params
        })

    # Investissements immobiliers
    for name, inv in portfolio.real_estate_investments.items():
        property_type = getattr(inv, 'property_type', 'SCPI')
        params = get_asset_return_params(name, property_type)
        portfolio_composition.append({
            'name': name,
            'value': inv.get_total_value(),
            'type': property_type,
            'params': params
        })

    # Valeur initiale totale
    initial_value = sum(asset['value'] for asset in portfolio_composition)

    # Crédits (dette à déduire)
    total_debt = portfolio.get_total_credits_balance() if hasattr(portfolio, 'get_total_credits_balance') else 0

    # Matrices pour stocker les simulations
    simulations = np.zeros((num_simulations, years + 1))
    simulations[:, 0] = initial_value - total_debt  # Valeur nette initiale

    # Simulation Monte Carlo
    for sim in range(num_simulations):
        current_values = {asset['name']: asset['value'] for asset in portfolio_composition}

        for year in range(1, years + 1):
            year_total = 0

            for asset in portfolio_composition:
                # Générer le rendement annuel selon la distribution
                if asset['params']['distribution'] == 'lognormal':
                    # Pour les actifs très volatils (crypto)
                    return_rate = np.random.lognormal(
                        mean=np.log(1 + asset['params']['mean'] / 100) - 0.5 * (asset['params']['std'] / 100) ** 2,
                        sigma=asset['params']['std'] / 100
                    ) - 1
                else:
                    # Distribution normale pour les autres actifs
                    return_rate = np.random.normal(
                        asset['params']['mean'] / 100,
                        asset['params']['std'] / 100
                    )

                # Mettre à jour la valeur de l'actif
                current_values[asset['name']] *= (1 + return_rate)
                year_total += current_values[asset['name']]

            # Réduction progressive de la dette (simplification)
            debt_reduction = total_debt * (1 / years) if total_debt > 0 else 0
            simulations[sim, year] = year_total - max(0, total_debt - debt_reduction * year)

    # Calculer les statistiques
    percentiles = {
        'p10': np.percentile(simulations, 10, axis=0),
        'p25': np.percentile(simulations, 25, axis=0),
        'p50': np.percentile(simulations, 50, axis=0),  # Médiane
        'p75': np.percentile(simulations, 75, axis=0),
        'p90': np.percentile(simulations, 90, axis=0),
        'mean': np.mean(simulations, axis=0)
    }

    return {
        'simulations': simulations,
        'percentiles': percentiles,
        'initial_value': initial_value - total_debt,
        'years': years,
        'composition': portfolio_composition
    }


def create_prediction_chart(prediction_results):
    """
    Crée un graphique des prédictions du portefeuille

    Args:
        prediction_results: Résultats de simulate_portfolio_future

    Returns:
        plotly.graph_objects.Figure
    """
    years = prediction_results['years']
    time_points = list(range(years + 1))
    percentiles = prediction_results['percentiles']

    fig = go.Figure()

    # Zone de confiance 80% (p10 à p90)
    fig.add_trace(go.Scatter(
        x=time_points + time_points[::-1],
        y=list(percentiles['p90']) + list(percentiles['p10'][::-1]),
        fill='toself',
        fillcolor='rgba(52, 152, 219, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='80% Confidence Interval (P10-P90)',
        showlegend=True
    ))

    # Zone de confiance 50% (p25 à p75)
    fig.add_trace(go.Scatter(
        x=time_points + time_points[::-1],
        y=list(percentiles['p75']) + list(percentiles['p25'][::-1]),
        fill='toself',
        fillcolor='rgba(52, 152, 219, 0.3)',
        line=dict(color='rgba(255,255,255,0)'),
        name='50% Confidence Interval (P25-P75)',
        showlegend=True
    ))

    # Ligne médiane (P50)
    fig.add_trace(go.Scatter(
        x=time_points,
        y=percentiles['p50'],
        mode='lines',
        name='Median (P50)',
        line=dict(color='#2E86DE', width=3)
    ))

    # Ligne moyenne
    fig.add_trace(go.Scatter(
        x=time_points,
        y=percentiles['mean'],
        mode='lines',
        name='Average',
        line=dict(color='#10AC84', width=2, dash='dash')
    ))

    # Ligne de référence (valeur initiale)
    fig.add_hline(
        y=prediction_results['initial_value'],
        line_dash="dot",
        line_color="gray",
        annotation_text="Current value",
        annotation_position="right"
    )

    # Configuration
    fig.update_layout(
        title={
            'text': f"Portfolio Prediction over {years} years",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': 'white'}
        },
        xaxis_title="Years",
        yaxis_title="Portfolio Value (€)",
        xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=1 if years <= 10 else 2
        ),
        yaxis=dict(
            tickformat='.0f',
            ticksuffix='€'
        ),
        height=500,
        hovermode='x unified',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(0,0,0,0.5)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=12)
    )

    # Grille
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')

    return fig


def create_statistics_summary(prediction_results):
    """
    Crée un résumé des statistiques de prédiction

    Args:
        prediction_results: Résultats de simulate_portfolio_future

    Returns:
        dict: Statistiques formatées
    """
    years = prediction_results['years']
    initial = prediction_results['initial_value']
    final_percentiles = {
        'p10': prediction_results['percentiles']['p10'][-1],
        'p25': prediction_results['percentiles']['p25'][-1],
        'p50': prediction_results['percentiles']['p50'][-1],
        'p75': prediction_results['percentiles']['p75'][-1],
        'p90': prediction_results['percentiles']['p90'][-1],
        'mean': prediction_results['percentiles']['mean'][-1]
    }

    # Calcul des rendements annualisés
    def annualized_return(initial_val, final_val, years):
        if initial_val <= 0:
            return 0
        return ((final_val / initial_val) ** (1 / years) - 1) * 100

    return {
        'initial': initial,
        'final': final_percentiles,
        'gains': {k: v - initial for k, v in final_percentiles.items()},
        'returns': {k: annualized_return(initial, v, years) for k, v in final_percentiles.items()},
        'years': years
    }