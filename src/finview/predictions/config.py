"""
Configuration et données historiques pour les simulations de patrimoine

Ce module contient toutes les constantes et paramètres historiques
utilisés pour les simulations Monte Carlo.
"""

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
