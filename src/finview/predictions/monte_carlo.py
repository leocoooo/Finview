"""
Moteur de simulation Monte Carlo pour les prédictions de patrimoine
"""
import numpy as np

from .config import CRISIS_PARAMS, INFLATION_PARAMS, HISTORICAL_RETURNS
from .utils import get_asset_return_params, get_asset_category, get_annual_fees


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
    
    Args:
        portfolio: Objet Portfolio à simuler
        years: Nombre d'années de projection
        num_simulations: Nombre de simulations Monte Carlo
        include_inflation: Ajuster pour l'inflation
        include_fees: Inclure les frais de gestion
        
    Returns:
        dict: Résultats de simulation avec percentiles et statistiques
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


def create_statistics_summary(prediction_results):
    """
    Crée un résumé détaillé avec variations en couleur
    
    Args:
        prediction_results: Résultats de simulate_portfolio_future()
        
    Returns:
        dict: Statistiques détaillées (valeurs finales, gains, rendements annualisés)
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
