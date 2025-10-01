"""
Module de prédiction du patrimoine basé sur des simulations Monte Carlo
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Données historiques de rendements annuels moyens (en %)
HISTORICAL_RETURNS = {
    # Cryptomonnaies (haute volatilité)
    'Bitcoin': {'mean': 100.0, 'std': 80.0, 'distribution': 'lognormal'},
    'Crypto': {'mean': 80.0, 'std': 70.0, 'distribution': 'lognormal'},

    # Actions individuelles (volatilité moyenne-haute)
    'Actions Tesla': {'mean': 25.0, 'std': 50.0, 'distribution': 'normal'},
    'Actions Apple': {'mean': 20.0, 'std': 25.0, 'distribution': 'normal'},
    'Actions Microsoft': {'mean': 22.0, 'std': 28.0, 'distribution': 'normal'},
    'Action': {'mean': 18.0, 'std': 25.0, 'distribution': 'normal'},

    # ETF (volatilité moyenne)
    'ETF S&P 500': {'mean': 10.5, 'std': 18.0, 'distribution': 'normal'},
    'ETF Europe': {'mean': 8.5, 'std': 20.0, 'distribution': 'normal'},
    'ETF': {'mean': 9.0, 'std': 18.0, 'distribution': 'normal'},

    # Immobilier (faible volatilité)
    'SCPI Bureaux Paris': {'mean': 4.5, 'std': 8.0, 'distribution': 'normal'},
    'SCPI': {'mean': 4.2, 'std': 7.0, 'distribution': 'normal'},
    'REIT Résidentiel US': {'mean': 6.5, 'std': 12.0, 'distribution': 'normal'},
    'REIT': {'mean': 6.0, 'std': 12.0, 'distribution': 'normal'},
    'Immobilier direct': {'mean': 5.0, 'std': 10.0, 'distribution': 'normal'},

    # Obligations (très faible volatilité)
    'Obligations': {'mean': 3.5, 'std': 5.0, 'distribution': 'normal'},
    'Obligation': {'mean': 3.5, 'std': 5.0, 'distribution': 'normal'},

    # Autres
    'Fonds': {'mean': 7.0, 'std': 12.0, 'distribution': 'normal'},
    'Liquidités': {'mean': 2.0, 'std': 0.5, 'distribution': 'normal'},
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
    return {'mean': 7.0, 'std': 15.0, 'distribution': 'normal'}


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
        name='Intervalle 80% (P10-P90)',
        showlegend=True
    ))

    # Zone de confiance 50% (p25 à p75)
    fig.add_trace(go.Scatter(
        x=time_points + time_points[::-1],
        y=list(percentiles['p75']) + list(percentiles['p25'][::-1]),
        fill='toself',
        fillcolor='rgba(52, 152, 219, 0.3)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Intervalle 50% (P25-P75)',
        showlegend=True
    ))

    # Ligne médiane (P50)
    fig.add_trace(go.Scatter(
        x=time_points,
        y=percentiles['p50'],
        mode='lines',
        name='Médiane (P50)',
        line=dict(color='#2E86DE', width=3)
    ))

    # Ligne moyenne
    fig.add_trace(go.Scatter(
        x=time_points,
        y=percentiles['mean'],
        mode='lines',
        name='Moyenne',
        line=dict(color='#10AC84', width=2, dash='dash')
    ))

    # Ligne de référence (valeur initiale)
    fig.add_hline(
        y=prediction_results['initial_value'],
        line_dash="dot",
        line_color="gray",
        annotation_text="Valeur actuelle",
        annotation_position="right"
    )

    # Configuration
    fig.update_layout(
        title={
            'text': f"Prédiction du Patrimoine sur {years} ans",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': 'white'}
        },
        xaxis_title="Années",
        yaxis_title="Valeur du Patrimoine (€)",
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