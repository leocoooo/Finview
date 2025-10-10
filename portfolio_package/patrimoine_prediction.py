"""
Module de prédiction du patrimoine basé sur des simulations Monte Carlo RÉALISTES
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================================
# DONNÉES HISTORIQUES AJUSTÉES - Plus conservatrices et réalistes
# ============================================================================

HISTORICAL_RETURNS = {
    # CRYPTOMONNAIES - Très haute volatilité, risque de pertes importantes
    'Bitcoin': {'mean': 10.0, 'std': 85.0, 'distribution': 'lognormal'},
    'Ethereum': {'mean': 8.0, 'std': 90.0, 'distribution': 'lognormal'},
    'Crypto': {'mean': 8.0, 'std': 90.0, 'distribution': 'lognormal'},
    'Altcoin': {'mean': 5.0, 'std': 110.0, 'distribution': 'lognormal'},

    # ACTIONS INDIVIDUELLES - Rendements ajustés
    'Actions Apple': {'mean': 12.0, 'std': 35.0, 'distribution': 'normal'},
    'Actions Microsoft': {'mean': 11.0, 'std': 35.0, 'distribution': 'normal'},
    'Actions Google': {'mean': 9.0, 'std': 38.0, 'distribution': 'normal'},
    'Actions Amazon': {'mean': 8.0, 'std': 42.0, 'distribution': 'normal'},
    'Actions Meta': {'mean': 6.0, 'std': 45.0, 'distribution': 'normal'},
    'Actions Tesla': {'mean': 3.0, 'std': 55.0, 'distribution': 'normal'},
    'Actions Nvidia': {'mean': 8.0, 'std': 65.0, 'distribution': 'normal'},
    'Actions Netflix': {'mean': 5.0, 'std': 42.0, 'distribution': 'normal'},
    'Actions Bancaires': {'mean': 4.0, 'std': 25.0, 'distribution': 'normal'},
    'Actions Assurance': {'mean': 4.5, 'std': 22.0, 'distribution': 'normal'},
    'Actions LVMH': {'mean': 7.5, 'std': 28.0, 'distribution': 'normal'},
    'Actions Hermès': {'mean': 8.5, 'std': 25.0, 'distribution': 'normal'},
    'Actions Énergies Renouvelables': {'mean': 6.0, 'std': 35.0, 'distribution': 'normal'},
    'Actions Pétrole': {'mean': 5.0, 'std': 32.0, 'distribution': 'normal'},
    'Action': {'mean': 7.5, 'std': 22.0, 'distribution': 'normal'},

    # ETF - Plus conservateurs
    'ETF S&P 500': {'mean': 8.0, 'std': 17.0, 'distribution': 'normal'},
    'ETF Nasdaq': {'mean': 8.5, 'std': 20.0, 'distribution': 'normal'},
    'ETF CAC 40': {'mean': 6.5, 'std': 19.0, 'distribution': 'normal'},
    'ETF Europe': {'mean': 7.0, 'std': 21.0, 'distribution': 'normal'},
    'ETF World': {'mean': 8.0, 'std': 17.0, 'distribution': 'normal'},
    'ETF MSCI World': {'mean': 8.0, 'std': 16.0, 'distribution': 'normal'},
    'ETF Émergents': {'mean': 7.0, 'std': 25.0, 'distribution': 'normal'},
    'ETF Chine': {'mean': 5.5, 'std': 28.0, 'distribution': 'normal'},
    'ETF Inde': {'mean': 8.0, 'std': 24.0, 'distribution': 'normal'},
    'ETF Tech': {'mean': 9.0, 'std': 22.0, 'distribution': 'normal'},
    'ETF Santé': {'mean': 7.5, 'std': 18.0, 'distribution': 'normal'},
    'ETF ESG': {'mean': 7.0, 'std': 17.0, 'distribution': 'normal'},
    'ETF': {'mean': 7.5, 'std': 17.0, 'distribution': 'normal'},

    # IMMOBILIER
    'SCPI Bureaux Paris': {'mean': 3.8, 'std': 9.0, 'distribution': 'normal'},
    'SCPI Résidentiel': {'mean': 4.0, 'std': 7.0, 'distribution': 'normal'},
    'SCPI Commerce': {'mean': 3.5, 'std': 11.0, 'distribution': 'normal'},
    'SCPI Diversifiée': {'mean': 4.0, 'std': 8.5, 'distribution': 'normal'},
    'SCPI Europe': {'mean': 3.8, 'std': 8.0, 'distribution': 'normal'},
    'SCPI': {'mean': 3.8, 'std': 8.5, 'distribution': 'normal'},
    'REIT Résidentiel US': {'mean': 5.0, 'std': 14.0, 'distribution': 'normal'},
    'REIT Commercial': {'mean': 5.3, 'std': 15.0, 'distribution': 'normal'},
    'REIT': {'mean': 5.0, 'std': 14.0, 'distribution': 'normal'},
    'Immobilier direct': {'mean': 4.0, 'std': 9.0, 'distribution': 'normal'},
    'Immobilier locatif': {'mean': 4.5, 'std': 10.0, 'distribution': 'normal'},

    # OBLIGATIONS
    'Obligations États AAA': {'mean': 2.3, 'std': 3.5, 'distribution': 'normal'},
    'Obligations Entreprises': {'mean': 3.2, 'std': 5.5, 'distribution': 'normal'},
    'Obligations High Yield': {'mean': 4.5, 'std': 9.0, 'distribution': 'normal'},
    'Obligations Émergentes': {'mean': 5.5, 'std': 12.0, 'distribution': 'normal'},
    'Obligations': {'mean': 2.8, 'std': 4.5, 'distribution': 'normal'},
    'Obligation': {'mean': 2.8, 'std': 4.5, 'distribution': 'normal'},

    # MATIÈRES PREMIÈRES & ALTERNATIFS
    'Or': {'mean': 3.5, 'std': 16.0, 'distribution': 'normal'},
    'Argent': {'mean': 4.0, 'std': 24.0, 'distribution': 'normal'},
    'Commodities': {'mean': 4.5, 'std': 22.0, 'distribution': 'normal'},
    'Private Equity': {'mean': 10.0, 'std': 28.0, 'distribution': 'lognormal'},

    # FONDS & LIQUIDITÉS
    'Fonds Diversifié': {'mean': 6.0, 'std': 12.0, 'distribution': 'normal'},
    'Fonds Actions': {'mean': 7.5, 'std': 18.0, 'distribution': 'normal'},
    'Fonds Obligations': {'mean': 3.0, 'std': 5.5, 'distribution': 'normal'},
    'Fonds': {'mean': 5.5, 'std': 13.0, 'distribution': 'normal'},
    'Liquidités': {'mean': 2.5, 'std': 0.3, 'distribution': 'normal'},
    'Livret A': {'mean': 3.0, 'std': 0.1, 'distribution': 'normal'},
    'Compte Épargne': {'mean': 2.0, 'std': 0.2, 'distribution': 'normal'},
}

# ============================================================================
# PARAMÈTRES DE CRISE ET RÉALISME
# ============================================================================

# Probabilité d'événements de marché
CRISIS_PARAMS = {
    'crisis_probability': 0.05,  # 12% de chance de crise par an (environ une tous les 8 ans)
    'mild_correction_probability': 0.25,  # 25% de chance de correction modérée
    'crisis_impact': {
        'Actions': (-0.35, 0.15),  # Baisse de 20% à 50% pendant une crise
        'ETF': (-0.30, 0.12),
        'Crypto': (-0.60, 0.25),  # Les cryptos peuvent perdre 40% à 85%
        'SCPI': (-0.15, 0.08),
        'Obligations': (-0.08, 0.05),
        'Liquidités': (0.0, 0.01),
        'Or': (0.05, 0.15),  # L'or peut gagner en crise
    },
    'correction_impact': {
        'Actions': (-0.15, 0.08),
        'ETF': (-0.12, 0.07),
        'Crypto': (-0.30, 0.15),
        'SCPI': (-0.05, 0.03),
        'Obligations': (-0.03, 0.02),
        'Liquidités': (0.0, 0.005),
        'Or': (0.02, 0.08),
    }
}

# Inflation moyenne et volatilité
INFLATION_PARAMS = {
    'mean': 2.0,  # 2% d'inflation moyenne
    'std': 1.0,
    'max': 8.0  # Plafond en cas de pic inflationniste
}

# Frais annuels moyens par type d'actif
ANNUAL_FEES = {
    'Actions': 0.003,  # 0.3% de frais de courtage/transaction annuels
    'ETF': 0.003,      # 0.3% TER moyen
    'Crypto': 0.010,   # 1% frais élevés (trading, gas fees)
    'SCPI': 0.010,     # 1% frais de gestion
    'Obligations': 0.002,
    'Fonds': 0.015,    # 1.5% frais de gestion actifs
    'Liquidités': 0.0,
    'Or': 0.005,
    'REIT': 0.008,
    'Private Equity': 0.020  # 2% management fees
}


def get_asset_return_params(asset_name, asset_type=None):
    """Récupère les paramètres de rendement pour un actif"""
    if asset_name in HISTORICAL_RETURNS:
        return HISTORICAL_RETURNS[asset_name]

    asset_name_lower = asset_name.lower()
    for key, params in HISTORICAL_RETURNS.items():
        if key.lower() in asset_name_lower:
            return params

    if asset_type and asset_type in HISTORICAL_RETURNS:
        return HISTORICAL_RETURNS[asset_type]

    return {'mean': 5.5, 'std': 15.0, 'distribution': 'normal'}


def get_asset_category(asset_name, asset_type):
    """Détermine la catégorie d'actif pour appliquer les impacts de crise"""
    name_lower = asset_name.lower()
    type_lower = (asset_type or '').lower()

    if any(x in name_lower or x in type_lower for x in ['crypto', 'bitcoin', 'ethereum']):
        return 'Crypto'
    elif any(x in name_lower or x in type_lower for x in ['action', 'stock', 'tesla', 'apple', 'nvda']):
        return 'Actions'
    elif 'etf' in name_lower or 'etf' in type_lower:
        return 'ETF'
    elif any(x in name_lower or x in type_lower for x in ['scpi', 'immobilier', 'reit']):
        return 'SCPI'
    elif any(x in name_lower or x in type_lower for x in ['obligation', 'bond']):
        return 'Obligations'
    elif any(x in name_lower or x in type_lower for x in ['liquidité', 'cash', 'livret', 'épargne']):
        return 'Liquidités'
    elif 'or' in name_lower or 'gold' in name_lower:
        return 'Or'
    else:
        return 'Actions'  # Défaut


def get_annual_fees(asset_category):
    """Retourne les frais annuels pour une catégorie d'actif"""
    return ANNUAL_FEES.get(asset_category, 0.005)


def simulate_portfolio_future(portfolio, years=10, num_simulations=1000,
                              include_inflation=True, include_fees=True):
    """
    Simule l'évolution future du portefeuille avec Monte Carlo RÉALISTE

    Améliorations:
    - Scénarios de crise aléatoires
    - Corrélation entre actifs lors de crises
    - Inflation
    - Frais de gestion
    - Rendements plus conservateurs
    """
    # Collecter la composition
    portfolio_composition = []

    if portfolio.cash > 0:
        portfolio_composition.append({
            'name': 'Liquidités',
            'value': portfolio.cash,
            'type': 'Liquidités',
            'category': 'Liquidités',
            'params': HISTORICAL_RETURNS['Liquidités']
        })

    for name, inv in portfolio.financial_investments.items():
        inv_type = getattr(inv, 'investment_type', 'Action')
        params = get_asset_return_params(name, inv_type)
        category = get_asset_category(name, inv_type)
        portfolio_composition.append({
            'name': name,
            'value': inv.get_total_value(),
            'type': inv_type,
            'category': category,
            'params': params
        })

    for name, inv in portfolio.real_estate_investments.items():
        property_type = getattr(inv, 'property_type', 'SCPI')
        params = get_asset_return_params(name, property_type)
        category = get_asset_category(name, property_type)
        portfolio_composition.append({
            'name': name,
            'value': inv.get_total_value(),
            'type': property_type,
            'category': category,
            'params': params
        })

    initial_value = sum(asset['value'] for asset in portfolio_composition)
    total_debt = portfolio.get_total_credits_balance() if hasattr(portfolio, 'get_total_credits_balance') else 0

    # Matrices de simulation
    simulations = np.zeros((num_simulations, years + 1))
    simulations_nominal = np.zeros((num_simulations, years + 1))  # Valeur nominale (sans inflation)
    simulations[:, 0] = initial_value - total_debt
    simulations_nominal[:, 0] = initial_value - total_debt

    # Simulation Monte Carlo avec événements de crise
    for sim in range(num_simulations):
        current_values = {asset['name']: asset['value'] for asset in portfolio_composition}
        cumulative_inflation = 1.0

        for year in range(1, years + 1):
            # 1. Déterminer s'il y a une crise ou correction cette année
            market_event = np.random.random()
            is_crisis = market_event < CRISIS_PARAMS['crisis_probability']
            is_correction = (not is_crisis) and (market_event < CRISIS_PARAMS['crisis_probability'] +
                                                   CRISIS_PARAMS['mild_correction_probability'])

            # 2. Générer l'inflation pour cette année
            inflation_rate = 0
            if include_inflation:
                inflation_rate = np.random.normal(
                    INFLATION_PARAMS['mean'] / 100,
                    INFLATION_PARAMS['std'] / 100
                )
                inflation_rate = min(inflation_rate, INFLATION_PARAMS['max'] / 100)
                cumulative_inflation *= (1 + inflation_rate)

            year_total_nominal = 0

            # 3. Calculer les rendements pour chaque actif
            for asset in portfolio_composition:
                # Rendement de base
                if asset['params']['distribution'] == 'lognormal':
                    base_return = np.random.lognormal(
                        mean=np.log(1 + asset['params']['mean'] / 100) - 0.5 * (asset['params']['std'] / 100) ** 2,
                        sigma=asset['params']['std'] / 100
                    ) - 1
                else:
                    base_return = np.random.normal(
                        asset['params']['mean'] / 100,
                        asset['params']['std'] / 100
                    )

                # Impact de crise ou correction
                if is_crisis:
                    category = asset['category']
                    if category in CRISIS_PARAMS['crisis_impact']:
                        crisis_mean, crisis_std = CRISIS_PARAMS['crisis_impact'][category]
                        crisis_shock = np.random.normal(crisis_mean, crisis_std)
                        base_return += crisis_shock
                elif is_correction:
                    category = asset['category']
                    if category in CRISIS_PARAMS['correction_impact']:
                        corr_mean, corr_std = CRISIS_PARAMS['correction_impact'][category]
                        correction_shock = np.random.normal(corr_mean, corr_std)
                        base_return += correction_shock

                # Appliquer les frais
                if include_fees:
                    fees = get_annual_fees(asset['category'])
                    base_return -= fees

                # Limiter les pertes à -95% (faillite quasi-totale rare mais possible)
                base_return = max(base_return, -0.95)

                # Mise à jour de la valeur
                current_values[asset['name']] *= (1 + base_return)
                year_total_nominal += current_values[asset['name']]

            # 4. Réduction de la dette
            debt_reduction = total_debt * (1 / years) if total_debt > 0 else 0
            remaining_debt = max(0, total_debt - debt_reduction * year)

            # Valeur nominale
            simulations_nominal[sim, year] = year_total_nominal - remaining_debt

            # Valeur réelle (ajustée de l'inflation)
            simulations[sim, year] = (year_total_nominal - remaining_debt) / cumulative_inflation

    # Calculer les statistiques
    percentiles = {
        'p10': np.percentile(simulations, 10, axis=0),
        'p25': np.percentile(simulations, 25, axis=0),
        'p50': np.percentile(simulations, 50, axis=0),
        'p75': np.percentile(simulations, 75, axis=0),
        'p90': np.percentile(simulations, 90, axis=0),
        'mean': np.mean(simulations, axis=0)
    }

    percentiles_nominal = {
        'p10': np.percentile(simulations_nominal, 10, axis=0),
        'p25': np.percentile(simulations_nominal, 25, axis=0),
        'p50': np.percentile(simulations_nominal, 50, axis=0),
        'p75': np.percentile(simulations_nominal, 75, axis=0),
        'p90': np.percentile(simulations_nominal, 90, axis=0),
        'mean': np.mean(simulations_nominal, axis=0)
    }

    return {
        'simulations': simulations,
        'simulations_nominal': simulations_nominal,
        'percentiles': percentiles,
        'percentiles_nominal': percentiles_nominal,
        'initial_value': initial_value - total_debt,
        'years': years,
        'composition': portfolio_composition,
        'include_inflation': include_inflation,
        'include_fees': include_fees
    }


def create_prediction_chart(prediction_results):
    """Crée un graphique des prédictions avec zones de crise visibles"""
    years = prediction_results['years']
    time_points = list(range(years + 1))
    percentiles = prediction_results['percentiles']

    fig = go.Figure()

    # Zone pessimiste (risque de perte)
    fig.add_trace(go.Scatter(
        x=time_points + time_points[::-1],
        y=list(percentiles['p90']) + list(percentiles['p10'][::-1]),
        fill='toself',
        fillcolor='rgba(231, 76, 60, 0.15)',  # Rouge transparent
        line=dict(color='rgba(255,255,255,0)'),
        name='80% Confidence (P10-P90)',
        showlegend=True
    ))

    # Zone centrale
    fig.add_trace(go.Scatter(
        x=time_points + time_points[::-1],
        y=list(percentiles['p75']) + list(percentiles['p25'][::-1]),
        fill='toself',
        fillcolor='rgba(52, 152, 219, 0.25)',
        line=dict(color='rgba(255,255,255,0)'),
        name='50% Confidence (P25-P75)',
        showlegend=True
    ))

    # Scénario pessimiste P10
    fig.add_trace(go.Scatter(
        x=time_points,
        y=percentiles['p10'],
        mode='lines',
        name='Pessimistic (P10)',
        line=dict(color='#E74C3C', width=2, dash='dot')
    ))

    # Médiane
    fig.add_trace(go.Scatter(
        x=time_points,
        y=percentiles['p50'],
        mode='lines',
        name='Median (P50)',
        line=dict(color='#2E86DE', width=3)
    ))

    # Moyenne
    fig.add_trace(go.Scatter(
        x=time_points,
        y=percentiles['mean'],
        mode='lines',
        name='Average',
        line=dict(color='#10AC84', width=2, dash='dash')
    ))

    # Ligne de référence
    fig.add_hline(
        y=prediction_results['initial_value'],
        line_dash="dot",
        line_color="white",
        annotation_text="Current Value",
        annotation_position="right"
    )

    fig.update_layout(
        title={
            'text': f"Portfolio Projection - {years} Years (Real Values, Inflation-Adjusted)",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': 'white'}
        },
        xaxis_title="Years",
        yaxis_title="Portfolio Value (€, Real)",
        xaxis=dict(tickmode='linear', tick0=0, dtick=1 if years <= 10 else 2),
        yaxis=dict(tickformat='.0f', ticksuffix='€'),
        height=550,
        hovermode='x unified',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(0,0,0,0.6)',
            bordercolor='rgba(255,255,255,0.3)',
            borderwidth=1
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=12, color='white')
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')

    return fig


def create_statistics_summary(prediction_results):
    """Crée un résumé détaillé avec variations en couleur"""
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

    def annualized_return(initial_val, final_val, years):
        if initial_val <= 0 or final_val <= 0:
            return -100
        return ((final_val / initial_val) ** (1 / years) - 1) * 100

    gains = {k: v - initial for k, v in final_percentiles.items()}
    returns = {k: annualized_return(initial, v, years) for k, v in final_percentiles.items()}
    gain_pct = {k: ((v / initial - 1) * 100) if initial > 0 else 0 for k, v in final_percentiles.items()}

    return {
        'initial': initial,
        'final': final_percentiles,
        'gains': gains,
        'gain_percentages': gain_pct,
        'returns': returns,
        'years': years
    }