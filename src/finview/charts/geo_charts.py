"""
Carte mondiale des investissements géolocalisés
"""
import plotly.graph_objects as go
import random
from collections import defaultdict
from src.finview.ui.formatting import format_currency
from .config import THEME, LOCATION_COORDS
from .layouts import get_base_layout


def create_world_investment_map(portfolio):
    """
    Carte mondiale des investissements avec positions réelles
    
    Args:
        portfolio: Instance de Portfolio
        
    Returns:
        go.Figure: Graphique Plotly avec carte géographique
    """
    investments = []
    
    # Financial investments
    for name, inv in getattr(portfolio, "financial_investments", {}).items():
        location = getattr(inv, 'location', None)
        if location and location in LOCATION_COORDS:
            coords = LOCATION_COORDS[location]
            investments.append({
                'name': name,
                'type': 'Financial',
                'value': inv.get_total_value(),
                'perf': inv.get_gain_loss_percentage(),
                'lat': coords['lat'],
                'lon': coords['lon'],
                'color': THEME['financial'],
                'location': location
            })
    
    # Real estate investments
    for name, inv in getattr(portfolio, "real_estate_investments", {}).items():
        location = getattr(inv, 'location', None)
        if location and location in LOCATION_COORDS:
            coords = LOCATION_COORDS[location]
            investments.append({
                'name': name,
                'type': 'Real Estate',
                'value': inv.get_total_value(),
                'perf': inv.get_gain_loss_percentage(),
                'lat': coords['lat'],
                'lon': coords['lon'],
                'color': THEME['real_estate'],
                'location': location
            })
    
    # Apply slight offset to investments at the same location to avoid overlap
    location_counts = defaultdict(int)
    for inv in investments:
        loc_key = f"{inv['lat']},{inv['lon']}"
        if location_counts[loc_key] > 0:
            # Add small random offset (±2 degrees)
            radius = 2 + location_counts[loc_key] * 1.5
            inv['lat'] += radius * random.uniform(-1, 1)
            inv['lon'] += radius * random.uniform(-1, 1)
        location_counts[loc_key] += 1
    
    if not investments:
        fig = go.Figure()
        fig.add_annotation(
            text="No geo-localized investments", 
            x=0.5, y=0.5,
            font=dict(size=16, color=THEME['text_secondary']), 
            showarrow=False
        )
        fig.update_layout(**get_base_layout("🌍 World Investment Map", 500))
        return fig
    
    fig = go.Figure()
    
    for inv in investments:
        fig.add_trace(go.Scattergeo(
            lon=[inv['lon']], 
            lat=[inv['lat']], 
            text=inv['name'],
            mode='markers',
            marker=dict(
                size=max(12, min(25, inv['value'] / 1000)),  # Taille proportionnelle à la valeur
                color=inv['color'], 
                opacity=0.7,
                line=dict(width=1.5, color='white')
            ),
            hovertemplate=f"<b>{inv['name']}</b><br>" +
                         f"Location: {inv['location']}<br>" +
                         f"Type: {inv['type']}<br>" +
                         f"Value: {format_currency(inv['value'])}<br>" +
                         f"Performance: {inv['perf']:+.1f}%<extra></extra>",
            name=inv['name'],
            showlegend=False
        ))
    
    layout = get_base_layout("🌍 World Investment Map", 600)
    layout['geo'] = dict(
        projection_type='natural earth',
        showland=True,
        landcolor='rgba(51, 65, 85, 0.4)',
        showocean=True,
        oceancolor='rgba(15, 23, 42, 0.6)',
        showcountries=True,
        countrycolor='rgba(148, 163, 184, 0.2)',
        bgcolor='rgba(0,0,0,0)',
        coastlinecolor='rgba(148, 163, 184, 0.3)',
        showlakes=True,
        lakecolor='rgba(15, 23, 42, 0.6)'
    )
    layout['separators'] = ' ,'

    fig.update_layout(**layout)
    
    return fig
