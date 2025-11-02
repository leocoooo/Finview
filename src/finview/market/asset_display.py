"""
Fonctions d'affichage et de visualisation des données d'actifs
"""
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any


def create_price_chart(
    hist_data: pd.DataFrame,
    asset_name: str,
    ticker: str,
    height: int = 400
) -> go.Figure:
    """
    Crée un graphique interactif du cours d'un actif
    
    Args:
        hist_data: DataFrame avec l'historique des prix
        asset_name: Nom de l'actif
        ticker: Symbole du ticker
        height: Hauteur du graphique en pixels
        
    Returns:
        go.Figure: Graphique Plotly
    """
    fig = go.Figure()

    # Ligne du cours de clôture
    fig.add_trace(go.Scatter(
        x=hist_data.index,
        y=hist_data['Close'],
        mode='lines',
        name='Prix de clôture',
        line=dict(color='#1f77b4', width=2),
        hovertemplate='<b>Date:</b> %{x}<br><b>Prix:</b> %{y:.2f}<extra></extra>'
    ))

    # Configuration du graphique
    fig.update_layout(
        title=dict(
            text=f"Évolution du cours - {asset_name} ({ticker})",
            x=0.5,
            xanchor='center',
            font=dict(size=16)
        ),
        xaxis=dict(
            title="Date",
            showgrid=True,
            gridcolor='rgba(128, 128, 128, 0.2)'
        ),
        yaxis=dict(
            title="Prix",
            showgrid=True,
            gridcolor='rgba(128, 128, 128, 0.2)'
        ),
        hovermode='x unified',
        showlegend=False,
        height=height,
        margin=dict(l=50, r=50, t=80, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig


def create_volume_chart(
    hist_data: pd.DataFrame,
    asset_name: str,
    ticker: str,
    height: int = 300
) -> go.Figure:
    """
    Crée un graphique du volume de transactions
    
    Args:
        hist_data: DataFrame avec l'historique
        asset_name: Nom de l'actif
        ticker: Symbole du ticker
        height: Hauteur du graphique
        
    Returns:
        go.Figure: Graphique Plotly
    """
    if 'Volume' not in hist_data.columns:
        return None
    
    fig = go.Figure()
    
    # Barres de volume
    fig.add_trace(go.Bar(
        x=hist_data.index,
        y=hist_data['Volume'],
        name='Volume',
        marker=dict(color='#3B82F6'),
        hovertemplate='<b>Date:</b> %{x}<br><b>Volume:</b> %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=f"Volume de transactions - {asset_name} ({ticker})",
            x=0.5,
            xanchor='center'
        ),
        xaxis_title="Date",
        yaxis_title="Volume",
        height=height,
        margin=dict(l=50, r=50, t=80, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def format_asset_info(info: Dict[str, Any]) -> Dict[str, str]:
    """
    Formate les informations d'un actif pour l'affichage
    
    Args:
        info: Dictionnaire d'informations de l'actif
        
    Returns:
        dict: Informations formatées
    """
    formatted = {}
    
    # Prix actuel
    if 'current_price' in info:
        formatted['price'] = f"{info['current_price']:.2f} {info.get('currency', 'USD')}"
    
    # Variation
    if 'price_change' in info and 'price_change_pct' in info:
        change = info['price_change']
        pct = info['price_change_pct']
        sign = '+' if change >= 0 else ''
        color = 'green' if change >= 0 else 'red'
        formatted['change'] = f"{sign}{change:.2f} ({sign}{pct:.2f}%)"
        formatted['change_color'] = color
    
    # Capitalisation boursière
    if info.get('market_cap'):
        cap = info['market_cap']
        if cap >= 1e12:
            formatted['market_cap'] = f"{cap/1e12:.2f}T"
        elif cap >= 1e9:
            formatted['market_cap'] = f"{cap/1e9:.2f}B"
        elif cap >= 1e6:
            formatted['market_cap'] = f"{cap/1e6:.2f}M"
        else:
            formatted['market_cap'] = f"{cap:,.0f}"
    
    # Volume
    if info.get('volume'):
        vol = info['volume']
        if vol >= 1e9:
            formatted['volume'] = f"{vol/1e9:.2f}B"
        elif vol >= 1e6:
            formatted['volume'] = f"{vol/1e6:.2f}M"
        elif vol >= 1e3:
            formatted['volume'] = f"{vol/1e3:.2f}K"
        else:
            formatted['volume'] = f"{vol:,.0f}"
    
    # Secteur et industrie
    if info.get('sector'):
        formatted['sector'] = info['sector']
    
    if info.get('industry'):
        formatted['industry'] = info['industry']
    
    return formatted


def get_price_trend(hist_data: pd.DataFrame, days: int = 30) -> str:
    """
    Détermine la tendance du prix sur une période
    
    Args:
        hist_data: DataFrame historique
        days: Nombre de jours à analyser
        
    Returns:
        str: 'bullish', 'bearish', ou 'neutral'
    """
    if hist_data.empty or len(hist_data) < 2:
        return 'neutral'
    
    # Prendre les derniers jours disponibles
    recent_data = hist_data.tail(min(days, len(hist_data)))
    
    if len(recent_data) < 2:
        return 'neutral'
    
    # Calculer la variation
    start_price = recent_data['Close'].iloc[0]
    end_price = recent_data['Close'].iloc[-1]
    change_pct = ((end_price - start_price) / start_price) * 100
    
    if change_pct > 5:
        return 'bullish'
    elif change_pct < -5:
        return 'bearish'
    else:
        return 'neutral'
