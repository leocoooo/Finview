import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from portfolio_package.patrimoine_prediction import create_prediction_chart

# === Theme & helpers ===
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


def format_currency(value):
    """Format currency with thousands separator"""
    try:
        if value == int(value):
            return f"{int(value):,}€".replace(',', ' ')
    except Exception:
        pass
    return f"{value:,.2f}€".replace(',', ' ')


def get_base_layout(title, height=500):
    """Base layout for all charts"""
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

# === FIGURES ===

# Dans le summary, on veut un graphique des transactions par mois et type
def create_monthly_transactions_chart(df_history):
    """
    Creates a professional chart of transactions by month and type
    
    Args:
        df_history: DataFrame containing transaction history with 'date' and 'type' columns
    
    Returns:
        fig: Plotly figure object
    """
    # Prepare data
    df_copy = df_history.copy()
    df_copy['month'] = pd.to_datetime(df_copy['date']).dt.to_period('M').astype(str)
    monthly_transactions = df_copy.groupby(['month', 'type']).size().reset_index(name='count')
    
    # Professional color palette
    color_map = {
        'CASH_ADD': '#10b981',           # Emerald green
        'CASH_WITHDRAW': '#ef4444',      # Red
        'INVESTMENT_BUY': '#3b82f6',     # Blue
        'INVESTMENT_SELL': '#f59e0b',    # Orange
        'INVESTMENT_UPDATE': '#8b5cf6',  # Purple
        'CREDIT_ADD': '#ec4899',         # Pink
        'CREDIT_PAYMENT': '#14b8a6',     # Teal
        'CREDIT_INTEREST': '#f97316'     # Dark orange
    }
    
    # Label mapping in English
    type_labels = {
        'CASH_ADD': '💰 Cash addition',
        'CASH_WITHDRAW': '💸 Cash withdrawal',
        'INVESTMENT_BUY': '📈 Investment purchase',
        'INVESTMENT_SELL': '📉 Investment sale',
        'INVESTMENT_UPDATE': '🔄 Price update',
        'CREDIT_ADD': '🏦 New credit',
        'CREDIT_PAYMENT': '💳 Credit payment',
        'CREDIT_INTEREST': '📊 Credit interest'
    }
    
    # Apply labels
    monthly_transactions['type_label'] = monthly_transactions['type'].map(type_labels)
    
    # Create chart
    fig = px.bar(
        monthly_transactions, 
        x='month', 
        y='count', 
        color='type_label',
        title="Transaction Evolution by Month",
        labels={
            'month': 'Month', 
            'count': 'Number of transactions', 
            'type_label': 'Transaction type'
        },
        color_discrete_map={type_labels[k]: v for k, v in color_map.items()},
        custom_data=['type_label']
    )
    
    # Customize chart
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color='#374151'),
        title=dict(
            font=dict(size=18, color='#1f2937', family='Arial, sans-serif'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='#e5e7eb',
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#f3f4f6',
            showline=False,
            tickfont=dict(size=11)
        ),
        legend=dict(
            title=dict(text='Transaction type', font=dict(size=12)),
            orientation='v',
            yanchor='top',
            y=1,
            xanchor='left',
            x=1.02,
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)',
            borderwidth=0
        ),
        hovermode='x unified',
        bargap=0.15,
        bargroupgap=0.1
    )
    
    # Improve tooltips
    fig.update_traces(
        hovertemplate='<b>%{customdata[0]}</b><br>Count: %{y}<extra></extra>'
    )
    
    return fig


# Dans le dashboard, on veut plusieurs graphiques :
def create_portfolio_pie_chart(portfolio):
    """Donut chart showing asset distribution with percentages"""
    labels, values, colors, hover_texts = [], [], [], []

    # Cash
    if getattr(portfolio, "cash", 0) > 0:
        labels.append('💰 Cash')
        values.append(portfolio.cash)
        colors.append(THEME['cash'])
        hover_texts.append(f"<b>Cash</b><br>Amount: {format_currency(portfolio.cash)}<extra></extra>")

    # Financial investments
    financial_total = getattr(portfolio, "get_financial_investments_value", lambda:0)()
    if financial_total > 0:
        labels.append('📈 Financial')
        values.append(financial_total)
        colors.append(THEME['financial'])

        details = []
        for name, inv in list(getattr(portfolio, "financial_investments", {}).items())[:5]:
            perf = getattr(inv, "get_gain_loss_percentage", lambda:0)()
            perf_color = '🟢' if perf >= 0 else '🔴'
            details.append(f"{perf_color} {name}: {format_currency(getattr(inv, 'get_total_value', lambda:0)())}")
        hover_text = f"<b>Financial Investments</b><br>Total: {format_currency(financial_total)}<br><br>" + "<br>".join(details)
        if len(getattr(portfolio, "financial_investments", {})) > 5:
            hover_text += f"<br>...and {len(portfolio.financial_investments)-5} more"
        hover_text += "<extra></extra>"
        hover_texts.append(hover_text)

    # Real estate
    real_estate_total = getattr(portfolio, "get_real_estate_investments_value", lambda:0)()
    if real_estate_total > 0:
        labels.append('🏠 Real Estate')
        values.append(real_estate_total)
        colors.append(THEME['real_estate'])

        details = []
        total_rental = 0
        for name, inv in list(getattr(portfolio, "real_estate_investments", {}).items())[:4]:
            rental_yield = getattr(inv, 'rental_yield', 0)
            annual_income = getattr(inv, 'get_annual_rental_income', lambda:0)()
            total_rental += annual_income
            detail = f"• {name}: {format_currency(getattr(inv, 'get_total_value', lambda:0)())}"
            if rental_yield > 0:
                detail += f" ({rental_yield:.1f}%)"
            details.append(detail)
        hover_text = f"<b>Real Estate</b><br>Total: {format_currency(real_estate_total)}<br>"
        if total_rental > 0:
            hover_text += f"Rental income: {format_currency(total_rental)}/year<br>"
        hover_text += "<br>" + "<br>".join(details)
        if len(getattr(portfolio, "real_estate_investments", {})) > 4:
            hover_text += f"<br>...and {len(portfolio.real_estate_investments)-4} more"
        hover_text += "<extra></extra>"
        hover_texts.append(hover_text)

    if not labels:
        fig = go.Figure()
        fig.add_annotation(text="No data to display", x=0.5, y=0.5,
                           font=dict(size=16, color=THEME['text_secondary']), showarrow=False)
        fig.update_layout(**get_base_layout("📊 Portfolio distribution", 500))
        return fig

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.65,
        marker=dict(colors=colors, line=dict(color='rgba(15, 23, 42, 0.3)', width=2)),
        textinfo='percent+label',
        hovertemplate='%{customdata}',
        customdata=hover_texts,
        pull=[0.02]*len(values)
    )])

    total_value = sum(values)
    fig.add_annotation(text=f"<b>{format_currency(total_value)}</b>", x=0.5, y=0.52,
                       font=dict(size=28, color=THEME['text_primary']), showarrow=False)
    fig.add_annotation(text="Total Portfolio Value", x=0.5, y=0.45,
                       font=dict(size=13, color=THEME['text_secondary']), showarrow=False)

    layout = get_base_layout("📊 Portfolio distribution", 550)
    layout['showlegend'] = True
    layout['legend'] = {
        'orientation': 'v',
        'yanchor': 'middle',
        'y': 0.5,
        'xanchor': 'left',
        'x': 1.02,
        'bgcolor': 'rgba(0,0,0,0)',
        'font': {'size': 13, 'color': THEME['text_primary']}
    }
    layout['separators'] = ' ,'
    fig.update_layout(**layout)
    return fig


def create_financial_investments_chart(portfolio):
    """Bar chart for each financial investment with professional muted colors"""
    investments = getattr(portfolio, "financial_investments", {})
    if not investments:
        fig = go.Figure()
        fig.add_annotation(text="No financial investments", x=0.5, y=0.5,
                           font=dict(size=16, color=THEME['text_secondary']), showarrow=False)
        fig.update_layout(**get_base_layout("📊 Financial Investments", 400))
        return fig
    
    names = list(investments.keys())
    values = [getattr(inv, 'get_total_value', lambda:0)() for inv in investments.values()]
    
    # Palette de couleurs professionnelles légèrement plus vives
    professional_colors = [
        'rgba(90, 130, 170, 0.85)',   # Bleu acier
        'rgba(100, 160, 120, 0.85)',  # Vert sauge
        'rgba(150, 110, 150, 0.85)',  # Violet doux
        'rgba(160, 140, 90, 0.85)',   # Or mat
        'rgba(80, 150, 160, 0.85)',   # Cyan profond
        'rgba(170, 100, 110, 0.85)',  # Rose poudré
        'rgba(110, 120, 170, 0.85)',  # Indigo
        'rgba(130, 160, 100, 0.85)',  # Olive clair
        'rgba(160, 100, 150, 0.85)',  # Orchidée
        'rgba(90, 150, 150, 0.85)',   # Turquoise mat
        'rgba(170, 140, 90, 0.85)',   # Terracotta
        'rgba(140, 100, 140, 0.85)',  # Prune
    ]
    colors = professional_colors * ((len(values)//len(professional_colors))+1)
    colors = colors[:len(values)]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=names, y=values,
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.1)', width=0.5)
        ),
        text=[''] * len(values),  # Pas d'étiquettes sur les barres
        textposition='auto',
        textfont=dict(size=12, color='white'),
        hovertemplate='<b>%{x}</b><br>Value: %{y}<extra></extra>'
    ))
    
    layout = get_base_layout("📊 Financial Investments Breakdown", 400)
    layout['yaxis'] = dict(
        title='Value (€)', 
        gridcolor='rgba(255,255,255,0.08)',
        griddash='dot',
        gridwidth=0.5,
        showgrid=True,
        dtick=None  # Quadrillage automatique plus fin
    )
    layout['xaxis'] = dict(showgrid=False)
    layout['showlegend'] = False
    fig.update_layout(**layout)
    return fig


def create_performance_chart(portfolio):
    """Performance chart with vibrant colors and gradient effects"""
    investments = {**getattr(portfolio, "financial_investments", {}),
                   **getattr(portfolio, "real_estate_investments", {})}
    if not investments:
        fig = go.Figure()
        fig.add_annotation(text="No investments", x=0.5, y=0.5,
                           font=dict(size=16, color=THEME['text_secondary']), showarrow=False)
        fig.update_layout(**get_base_layout("📈 Investment Performance", 400))
        return fig
    
    names = list(investments.keys())
    perfs = [getattr(inv, "get_gain_loss_percentage", lambda:0)() for inv in investments.values()]
    values = [getattr(inv, 'get_total_value', lambda:0)() for inv in investments.values()]
    
    # Palette de couleurs vives avec transparence
    vibrant_colors = [
        'rgba(255, 23, 68, 0.7)',    # Rouge vif
        'rgba(0, 230, 118, 0.7)',    # Vert émeraude
        'rgba(41, 121, 255, 0.7)',   # Bleu électrique
        'rgba(255, 196, 0, 0.7)',    # Jaune doré
        'rgba(224, 64, 251, 0.7)',   # Violet vif
        'rgba(0, 229, 255, 0.7)',    # Cyan lumineux
        'rgba(255, 110, 64, 0.7)',   # Orange corail
        'rgba(118, 255, 3, 0.7)',    # Vert lime
        'rgba(213, 0, 249, 0.7)',    # Magenta
        'rgba(0, 176, 255, 0.7)',    # Bleu ciel vif
        'rgba(255, 171, 0, 0.7)',    # Ambre
        'rgba(221, 44, 0, 0.7)',     # Rouge foncé vif
    ]
    colors = vibrant_colors * ((len(values)//len(vibrant_colors))+1)
    colors = colors[:len(values)]
    
    # Couleurs en dégradé du rouge au vert selon la performance
    def get_performance_color(perf):
        """Retourne une couleur du rouge au vert selon la performance"""
        # Interpolation continue du rouge au vert
        
        # Limiter les valeurs extrêmes pour le calcul
        perf_clamped = max(-30, min(30, perf))
        
        # Normaliser entre -30 et +30 pour avoir une échelle de 0 à 1
        normalized = (perf_clamped + 30) / 60
        
        # Rouge foncé pour les performances négatives
        red = [180, 50, 50]
        # Jaune/orange pour le milieu (0%)
        yellow = [200, 160, 70]
        # Vert foncé pour les performances positives
        green = [60, 140, 80]
        
        if normalized < 0.5:
            # Interpolation rouge -> jaune (performances négatives)
            factor = normalized * 2
            r = int(red[0] + (yellow[0] - red[0]) * factor)
            g = int(red[1] + (yellow[1] - red[1]) * factor)
            b = int(red[2] + (yellow[2] - red[2]) * factor)
        else:
            # Interpolation jaune -> vert (performances positives)
            factor = (normalized - 0.5) * 2
            r = int(yellow[0] + (green[0] - yellow[0]) * factor)
            g = int(yellow[1] + (green[1] - yellow[1]) * factor)
            b = int(yellow[2] + (green[2] - yellow[2]) * factor)
        
        return f'rgba({r}, {g}, {b}, 0.75)'
    
    bar_colors = [get_performance_color(perf) for perf in perfs]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=names, y=perfs,
        marker=dict(
            color=bar_colors,
            line=dict(color='rgba(255,255,255,0.15)', width=1)
        ),
        text=[f"{p:+.1f}%" for p in perfs],
        textposition='outside',
        textfont=dict(size=11, color='white'),
        hovertemplate='<b>%{x}</b><br>Performance: %{y:+.1f}%<br>Value: %{customdata}<extra></extra>',
        customdata=[format_currency(v) for v in values]
    ))
    
    fig.add_hline(y=0, line=dict(color='rgba(255,255,255,0.4)', dash='dash', width=2), opacity=0.7)
    
    layout = get_base_layout("📈 Investment Performance", 450)
    layout['yaxis'] = dict(title='Performance (%)', gridcolor=THEME['grid'], ticksuffix='%')
    layout['xaxis'] = dict(showgrid=False, tickangle=-30 if len(names)>6 else 0)
    layout['showlegend'] = False
    fig.update_layout(**layout)
    return fig


def get_portfolio_value_at_date(portfolio, date):
    """Calcule la valeur totale du portefeuille à une date donnée."""
    total = 0.0

    # Trésorerie (approximation simple : prend la valeur actuelle)
    total += portfolio.cash

    # Valeur des investissements financiers
    for inv in portfolio.financial_investments.values():
        if hasattr(inv, "purchase_date") and inv.purchase_date <= date:
            total += inv.current_value * inv.quantity

    # Valeur des investissements immobiliers
    for inv in portfolio.real_estate_investments.values():
        if hasattr(inv, "purchase_date") and inv.purchase_date <= date:
            total += inv.current_value * inv.quantity

    # On pourrait ajouter ici la valeur nette des crédits si tu veux les inclure
    return total


def get_portfolio_monthly_history(portfolio):
    """
    Reconstruit l'historique mensuel du portefeuille à partir de transaction_history.
    Retourne un DataFrame avec les colonnes ['date', 'value'].
    """
    if not hasattr(portfolio, "transaction_history") or len(portfolio.transaction_history) == 0:
        return pd.DataFrame(columns=["date", "value"])

    df = pd.DataFrame(portfolio.transaction_history)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # Crée une série de dates mensuelles entre le début et la fin
    start_date = df["date"].iloc[0].replace(day=1)
    end_date = datetime.now()
    monthly_dates = pd.date_range(start=start_date, end=end_date, freq="MS")

    # Calcule la valeur totale à chaque début de mois
    values = [get_portfolio_value_at_date(portfolio, d) for d in monthly_dates]

    history_df = pd.DataFrame({"date": monthly_dates, "value": values})
    return history_df


def create_portfolio_evolution_chart(portfolio):
    """
    Crée un graphique d'évolution basé sur l'historique mensuel réel du portefeuille.
    """

    THEME = {
        'financial': '#3B82F6',
        'positive': '#10B981',
        'grid': 'rgba(255,255,255,0.1)',
        'text_primary': '#FFFFFF',
        'text_secondary': '#9CA3AF'
    }

    df = get_portfolio_monthly_history(portfolio)
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Pas de données disponibles",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=THEME['text_secondary'])
        )
        return fig

    dates = df["date"]
    values = df["value"]

    initial_value = values.iloc[0]
    current_value = values.iloc[-1]

    total_days = (dates.iloc[-1] - dates.iloc[0]).days
    years_actual = total_days / 365 if total_days > 0 else 1

    total_gain = current_value - initial_value
    total_return = ((current_value / initial_value) - 1) * 100 if initial_value > 0 else 0
    annualized = ((current_value / initial_value) ** (1 / years_actual) - 1) * 100 if initial_value > 0 else 0

    # === Graphique
    fig = go.Figure()

    # Ligne principale
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode='lines',
        name='Portfolio Value',
        line=dict(color=THEME['financial'], width=3),
        fill='tozeroy',
        fillcolor='rgba(59,130,246,0.1)',
        hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Valeur: %{customdata}€<extra></extra>',
        customdata=[format_currency(v)[:-1] for v in values]
    ))

    # Point actuel
    fig.add_trace(go.Scatter(
        x=[dates.iloc[-1]],
        y=[current_value],
        mode='markers',
        name="Current Value",
        marker=dict(
            size=12,
            color=THEME['positive'],
            line=dict(color='white', width=2)
        ),
        hovertemplate=f'<b>Aujourd\'hui</b><br>Valeur: {format_currency(current_value)}<extra></extra>'
    ))

    # Annotation
    #annotation_text = (
        #f"<b>📈 Historique réel</b><br>"
        #f"Période: {total_days} jours<br>"
        #f"Gain: {total_gain:+,.0f}€ ({total_return:+.1f}%)<br>"
        #f"Rendement annualisé: {annualized:+.1f}%"
    #)

    #fig.add_annotation(
        #text=annotation_text,
        #x=0.02, y=0.98,
        #xanchor='left', yanchor='top',
        #xref='paper', yref='paper',
        #showarrow=False,
        #bgcolor='rgba(0,0,0,0.7)',
        #bordercolor=THEME['financial'],
        #borderwidth=2,
        #borderpad=10,
        #font=dict(size=11, color='white')
    #)

    # Layout
    fig.update_layout(**get_base_layout("📈 Portfolio Evolution", 500))
    fig.update_layout(
        # title={
        #     'text': f"📈 Portfolio Evolution",
        #     'x': 0.2,
        #     'xanchor': 'center',
        #     'font': {'size': 20, 'color': THEME['text_primary']}
        # },
        xaxis=dict(
            title="Date",
            showgrid=True,
            gridcolor=THEME['grid'],
            gridwidth=1
        ),
        yaxis=dict(
            title="Value (€)",
            showgrid=True,
            gridcolor=THEME['grid'],
            ticksuffix='€',
            gridwidth=1,
            tickformat=' '
        ),
        height=450,
        hovermode='x unified',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=12, color=THEME['text_primary']),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(0,0,0,0.5)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        ),
        margin=dict(l=60, r=30, t=80, b=60),
        separators=' ,'
    )

    return fig


def display_portfolio_evolution(portfolio):
    import streamlit as st
    from portfolio_package.visualizations import create_portfolio_evolution_chart

    fig = create_portfolio_evolution_chart(portfolio)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def create_world_investment_map(portfolio):
    """World map of investments with real locations"""
    
    # Mapping of locations to GPS coordinates
    location_coords = {
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
    
    investments = []
    
    # Financial investments
    for name, inv in getattr(portfolio, "financial_investments", {}).items():
        location = getattr(inv, 'location', None)
        if location and location in location_coords:
            coords = location_coords[location]
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
        if location and location in location_coords:
            coords = location_coords[location]
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
    import random
    from collections import defaultdict
    
    location_counts = defaultdict(int)
    for inv in investments:
        loc_key = f"{inv['lat']},{inv['lon']}"
        if location_counts[loc_key] > 0:
            # Add small random offset (±2 degrees)
            angle = random.uniform(0, 2 * 3.14159)
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


def display_predictions(results):
    """
    Wrapper minimal pour afficher le graphique de prédiction.
    On utilise ici la fonction create_prediction_chart fournie par le module
    patrimoine_prediction (déjà présent dans ton projet).
    """
    try:
        from portfolio_package.patrimoine_prediction import create_prediction_chart
    except Exception:
        st.error("Module de prédiction introuvable")
        return
    fig = create_prediction_chart(results)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# === Streamlit wrappers ===
def display_portfolio_pie(portfolio):
    st.plotly_chart(create_portfolio_pie_chart(portfolio), use_container_width=True, config={'displayModeBar': False})


def display_portfolio_evolution(portfolio, years=1):
    st.plotly_chart(create_portfolio_evolution_chart(portfolio), use_container_width=True, config={'displayModeBar': False})


def display_financial_investments(portfolio):
    st.plotly_chart(create_financial_investments_chart(portfolio), use_container_width=True, config={'displayModeBar': False})


def display_performance_chart(portfolio):
    st.plotly_chart(create_performance_chart(portfolio), use_container_width=True, config={'displayModeBar': False})


def display_world_map(portfolio):
    fig = create_world_investment_map(portfolio)
    fig.update_layout(height=700)
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d']
    })


def display_predictions(results):
    """Affiche les prédictions sous forme de graphique"""
    fig = create_prediction_chart(results)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})