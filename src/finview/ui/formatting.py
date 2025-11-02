"""
Formatting utilities for currency and percentages
"""


def format_currency(value):
    """
    Formate une valeur monétaire avec séparateurs et €
    
    Args:
        value: Valeur numérique à formater
        
    Returns:
        str: Valeur formatée avec € (ex: "1 234€" ou "1 234.56€")
    """
    if value == int(value):
        return f"{int(value):,}€".replace(',', ' ')
    return f"{value:,.2f}€".replace(',', ' ')


def format_percentage(value):
    """
    Formate un pourcentage avec signe si négatif
    
    Args:
        value: Valeur numérique du pourcentage
        
    Returns:
        str: Pourcentage formaté avec % (ex: "+5%" ou "-3.2%")
    """
    if value == int(value):
        return f"{int(value):+d}%" if value < 0 else f"{int(value)}%"
    return f"{value:+.1f}%" if value < 0 else f"{value:.1f}%"