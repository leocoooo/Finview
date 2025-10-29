"""
Fonctions utilitaires pour les prédictions de patrimoine
"""
from .config import HISTORICAL_RETURNS, ANNUAL_FEES


def get_asset_return_params(asset_name, asset_type=None):
    """
    Récupère les paramètres de rendement pour un actif
    
    Args:
        asset_name: Nom de l'actif
        asset_type: Type d'actif (optionnel)
        
    Returns:
        dict: Paramètres avec 'mean', 'std', 'distribution'
    """
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
    """
    Détermine la catégorie d'actif pour appliquer les impacts de crise
    
    Args:
        asset_name: Nom de l'actif
        asset_type: Type d'actif
        
    Returns:
        str: Catégorie de l'actif
    """
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
    """
    Retourne les frais annuels pour une catégorie d'actif
    
    Args:
        asset_category: Catégorie de l'actif
        
    Returns:
        float: Taux de frais annuel (ex: 0.003 = 0.3%)
    """
    return ANNUAL_FEES.get(asset_category, 0.005)
