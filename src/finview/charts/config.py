"""
Configuration et constantes pour les graphiques
"""

# Thème de couleurs pour tous les graphiques
THEME = {
    'background': 'rgba(15, 23, 42, 0)',
    'card_bg': 'rgba(30, 41, 59, 0.6)',
    'text_primary': '#F1F5F9',
    'text_secondary': '#94A3B8',
    'cash': '#10B981',
    'financial': '#3B82F6',
    'real_estate': '#F59E0B',
    'credits': '#EF4444',
    'positive': '#10B981',
    'negative': '#EF4444',
    'neutral': '#64748B',
    'grid': 'rgba(148, 163, 184, 0.1)',
    'border': 'rgba(148, 163, 184, 0.2)',
    'dark_colors': [
        '#1F2937', '#374151', '#4B5563', '#6B7280', '#9CA3AF', '#D1D5DB', '#111827'
    ]
}

# Palette de couleurs professionnelles vibrantes
VIBRANT_COLORS = [
    '#FF1744',  # Rouge éclatant
    '#00E676',  # Vert néon
    '#2979FF',  # Bleu électrique
    '#FFC400',  # Jaune or vif
    '#E040FB',  # Violet néon
    '#00E5FF',  # Cyan brillant
    '#FF6E40',  # Orange corail
    '#F50057',  # Rose magenta
    '#00B8D4',  # Turquoise vif
    '#FFEA00',  # Jaune citron
    '#AA00FF',  # Violet profond
]

# Palette de couleurs avec transparence pour les graphiques
VIBRANT_COLORS_RGBA = [
    'rgba(255, 23, 68, 0.95)',   # Rouge vif
    'rgba(0, 230, 118, 0.95)',   # Vert émeraude
    'rgba(41, 121, 255, 0.95)',  # Bleu électrique
    'rgba(255, 196, 0, 0.95)',   # Jaune doré
    'rgba(224, 64, 251, 0.95)',  # Violet vif
    'rgba(0, 229, 255, 0.95)',   # Cyan lumineux
    'rgba(255, 110, 64, 0.95)',  # Orange corail
    'rgba(118, 255, 3, 0.95)',   # Vert lime
    'rgba(213, 0, 249, 0.95)',   # Magenta
    'rgba(0, 176, 255, 0.95)',   # Bleu ciel vif
    'rgba(255, 171, 0, 0.95)',   # Ambre
    'rgba(221, 44, 0, 0.95)',    # Rouge foncé vif
]

# Mapping des types de transactions vers leurs couleurs et labels
TRANSACTION_COLORS = {
    'CASH_ADD': '#10b981',           # Emerald green
    'CASH_WITHDRAW': '#ef4444',      # Red
    'INVESTMENT_BUY': '#3b82f6',     # Blue
    'INVESTMENT_SELL': '#f59e0b',    # Orange
    'INVESTMENT_UPDATE': '#8b5cf6',  # Purple
    'CREDIT_ADD': '#ec4899',         # Pink
    'CREDIT_PAYMENT': '#14b8a6',     # Teal
    'CREDIT_INTEREST': '#f97316'     # Dark orange
}

TRANSACTION_LABELS = {
    'CASH_ADD': '💰 Cash addition',
    'CASH_WITHDRAW': '💸 Cash withdrawal',
    'INVESTMENT_BUY': '📈 Investment purchase',
    'INVESTMENT_SELL': '📉 Investment sale',
    'INVESTMENT_UPDATE': '🔄 Price update',
    'CREDIT_ADD': '🏦 New credit',
    'CREDIT_PAYMENT': '💳 Credit payment',
    'CREDIT_INTEREST': '📊 Credit interest'
}

# Benchmarks disponibles pour les comparaisons
AVAILABLE_BENCHMARKS = {
    "CAC 40": "^FCHI",
    "S&P 500": "^GSPC",
    "Dow Jones": "^DJI",
    "NASDAQ": "^IXIC",
    "DAX": "^GDAXI",
    "FTSE 100": "^FTSE",
    "Nikkei 225": "^N225",
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Gold": "GC=F",
    "Crude Oil": "CL=F"
}

# Coordonnées GPS pour la carte mondiale
LOCATION_COORDS = {
    'United States': {'lat': 37.0902, 'lon': -95.7129},
    'France': {'lat': 46.2276, 'lon': 2.2137},
    'Paris': {'lat': 48.8566, 'lon': 2.3522},
    'Lyon, France': {'lat': 45.7640, 'lon': 4.8357},
    'Japan': {'lat': 36.2048, 'lon': 138.2529},
    'Tokyo, Japan': {'lat': 35.6762, 'lon': 139.6503},
    'Europe': {'lat': 50.8503, 'lon': 4.3517},
    'Global': {'lat': 20.0, 'lon': 0.0},
    'China': {'lat': 35.8617, 'lon': 104.1954},
    'Singapore': {'lat': 1.3521, 'lon': 103.8198},
    'Berlin, Germany': {'lat': 52.5200, 'lon': 13.4050},
    'Germany': {'lat': 51.1657, 'lon': 10.4515},
    'Emerging Markets': {'lat': 0.0, 'lon': 20.0},
}
