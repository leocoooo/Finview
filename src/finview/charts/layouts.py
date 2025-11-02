"""
Templates de layouts Plotly pour les graphiques
"""
from .config import THEME


def get_base_layout(title: str, height: int = 500) -> dict:
    """
    Layout de base pour tous les graphiques Plotly
    
    Args:
        title: Titre du graphique
        height: Hauteur du graphique en pixels
        
    Returns:
        dict: Configuration du layout Plotly
    """
    return {
        'title': {
            'text': title,
            'x': 0.02,
            'xanchor': 'left',
            'font': {
                'size': 24,
                'family': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
                'color': THEME['text_primary'],
                'weight': 600
            }
        },
        'paper_bgcolor': THEME['background'],
        'plot_bgcolor': THEME['background'],
        'height': height,
        'margin': dict(l=20, r=20, t=80, b=60),
        'font': {
            'family': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
            'color': THEME['text_secondary'],
            'size': 13
        },
        'hoverlabel': {
            'bgcolor': 'rgba(30, 41, 59, 0.95)',
            'bordercolor': THEME['border'],
            'font': {
                'family': 'Inter, sans-serif',
                'size': 13,
                'color': THEME['text_primary']
            }
        },
        'showlegend': True,
        'legend': {
            'orientation': 'h',
            'yanchor': 'top',
            'y': -0.15,
            'xanchor': 'center',
            'x': 0.5,
            'bgcolor': 'rgba(0,0,0,0)',
            'bordercolor': 'rgba(0,0,0,0)',
            'font': {'size': 12, 'color': THEME['text_secondary']}
        }
    }
