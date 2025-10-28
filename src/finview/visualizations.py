import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import yfinance as yf

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
        fig.update_layout(**get_base_layout(" ", 50))
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

    layout = get_base_layout("", 500)
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
    # Palette de couleurs flashy et vibrantes
    professional_colors = [
        '#FF1744',  # Rouge éclatant
        '#00E676',  # Vert néon
        '#2979FF',  # Bleu électrique
        '#FFC400',  # Jaune or vif
        '#E040FB',  # Violet néon
        '#00E5FF',  # Cyan brillant
        '#FF6E40',  # Orange corail
        # '#76FF03',  # Vert citron
        '#F50057',  # Rose magenta
        '#00B8D4',  # Turquoise vif
        '#FFEA00',  # Jaune citron
        '#AA00FF',  # Violet profond
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
        fig.update_layout(**get_base_layout("📈 Investment Performance Per Asset", 400))
        return fig
    
    names = list(investments.keys())
    perfs = [getattr(inv, "get_gain_loss_percentage", lambda:0)() for inv in investments.values()]
    values = [getattr(inv, 'get_total_value', lambda:0)() for inv in investments.values()]
    
    # Palette de couleurs vives avec transparence
    vibrant_colors = [
        'rgba(255, 23, 68, 0.95)',  # Rouge vif
        'rgba(0, 230, 118, 0.95)',  # Vert émeraude
        'rgba(41, 121, 255, 0.95)',  # Bleu électrique
        'rgba(255, 196, 0, 0.95)',  # Jaune doré
        'rgba(224, 64, 251, 0.95)',  # Violet vif
        'rgba(0, 229, 255, 0.95)',  # Cyan lumineux
        'rgba(255, 110, 64, 0.95)',  # Orange corail
        'rgba(118, 255, 3, 0.95)',  # Vert lime
        'rgba(213, 0, 249, 0.95)',  # Magenta
        'rgba(0, 176, 255, 0.95)',  # Bleu ciel vif
        'rgba(255, 171, 0, 0.95)',  # Ambre
        'rgba(221, 44, 0, 0.95)',  # Rouge foncé vif
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
            color=colors,
            line=dict(color='rgba(255,255,255,0.15)', width=1)
        ),
        text=[f"{p:+.1f}%" for p in perfs],
        textposition='outside',
        textfont=dict(size=11, color='white'),
        hovertemplate='<b>%{x}</b><br>Performance: %{y:+.1f}%<br>Value: %{customdata}<extra></extra>',
        customdata=[format_currency(v) for v in values]
    ))
    
    fig.add_hline(y=0, line=dict(color='rgba(255,255,255,0.4)', dash='dash', width=2), opacity=0.7)
    
    layout = get_base_layout("📈 Investment Performance Per Asset", 450)
    layout['yaxis'] = dict(title='Performance (%)', gridcolor=THEME['grid'], ticksuffix='%')
    layout['xaxis'] = dict(showgrid=False, tickangle=-30 if len(names)>6 else 0)
    layout['showlegend'] = False
    fig.update_layout(**layout)
    return fig


def get_financial_portfolio_value_at_date(portfolio, date):
    """Calcule la valeur totale des investissements financiers à une date donnée"""
    total = 0.0
    
    for inv in portfolio.financial_investments.values():
        if hasattr(inv, "purchase_date") and inv.purchase_date <= date:
            price_at_date = inv.initial_value
            quantity_at_date = 0.0
            
            # Parcourir l'historique des transactions pour cet investissement
            for transaction in portfolio.transaction_history:
                trans_date = pd.to_datetime(transaction["date"])
                
                if trans_date > date:
                    continue
                
                if transaction.get("name") == inv.name:
                    trans_type = transaction["type"]
                    
                    if trans_type == "FINANCIAL_INVESTMENT_BUY":
                        price_at_date = transaction.get("price", inv.initial_value)
                        quantity_at_date = transaction.get("quantity", 0)
                    
                    elif trans_type == "INVESTMENT_UPDATE":
                        price_at_date = transaction.get("price", price_at_date)
                    
                    elif trans_type == "INVESTMENT_SELL":
                        quantity_at_date -= transaction.get("quantity", 0)
            
            total += price_at_date * quantity_at_date
    
    return total


def get_portfolio_monthly_history(portfolio):
    """
    Reconstruit l'historique mensuel du portefeuille de manière optimisée.
    """
    if not hasattr(portfolio, "transaction_history") or len(portfolio.transaction_history) == 0:
        return pd.DataFrame(columns=["date", "value", "invested"])

    df = pd.DataFrame(portfolio.transaction_history)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    start_date = df["date"].iloc[0].replace(day=1)
    end_date = datetime.now()
    monthly_dates = pd.date_range(start=start_date, end=end_date, freq="MS")

    # OPTIMISATION : Créer un dictionnaire {nom_investissement: [(date, price, quantity)]}
    investment_states = {}
    
    for _, transaction in df.iterrows():
        trans_type = transaction["type"]
        name = transaction.get("name")
        
        if name and trans_type in ["FINANCIAL_INVESTMENT_BUY", "INVESTMENT_UPDATE", "INVESTMENT_SELL"]:
            if name not in investment_states:
                investment_states[name] = []
            
            investment_states[name].append({
                'date': transaction['date'],
                'type': trans_type,
                'price': transaction.get('price'),
                'quantity': transaction.get('quantity')
            })
    
    # Calculer les valeurs mensuelles
    values = []
    for target_date in monthly_dates:
        total = 0.0
        
        for name, states in investment_states.items():
            price = None
            quantity = 0.0
            
            for state in states:
                if state['date'] > target_date:
                    break
                
                if state['type'] == 'FINANCIAL_INVESTMENT_BUY':
                    price = state['price']
                    quantity = state['quantity']
                elif state['type'] == 'INVESTMENT_UPDATE':
                    price = state['price']
                elif state['type'] == 'INVESTMENT_SELL':
                    quantity -= state['quantity']
            
            if price is not None and quantity > 0:
                total += price * quantity
        
        values.append(total)
    
    invested = [get_total_invested_at_date(portfolio, d) for d in monthly_dates]

    history_df = pd.DataFrame({
        "date": monthly_dates,
        "value": values,
        "invested": invested
    })
    return history_df


def create_performance_chart_filtered(portfolio):
    """Performance chart pour assets sélectionnés"""
    investments = getattr(portfolio, "financial_investments", {})

    # Filtrer uniquement les assets demandés
    selected = ['China Tech ETF', 'Tesla Stock', 'Apple Stock', 'Nvidia Stock']
    filtered_investments = {k: v for k, v in investments.items() if k in selected}

    if not filtered_investments:
        fig = go.Figure()
        fig.add_annotation(text="No data", x=0.5, y=0.5, showarrow=False)
        layout = get_base_layout(" ", 300)
        layout.update({
            'margin': dict(l=40, r=20, t=30, b=30)
        })
        return fig

    names = list(filtered_investments.keys())
    perfs = [inv.get_gain_loss_percentage() for inv in filtered_investments.values()]

    colors = ['#FF1744', '#00E676', '#2979FF', '#FFC400'][:len(names)]

    fig = go.Figure(data=[go.Bar(
        x=names,
        y=perfs,
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.2)', width=1)
        ),
        text=[f"{p:+.1f}%" for p in perfs],
        textposition='outside'
    )])

    layout = get_base_layout(" ", 400)
    layout.update({
        'yaxis_title': "Performance (%)",
        'xaxis_title': "",
        'showlegend': False,
        'margin': dict(l=40, r=20, t=30, b=30)
    })

    return fig


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


def get_total_invested_at_date(portfolio, date):
    """
    Calcule le total investi dans le portefeuille jusqu'à une certaine date.
    On suppose que transaction_history contient les entrées de type:
    {'date': ..., 'amount': ..., 'type': 'investment' ou 'withdrawal'}
    """
    if not hasattr(portfolio, "transaction_history") or len(portfolio.transaction_history) == 0:
        return 0

    df = pd.DataFrame(portfolio.transaction_history)
    df["date"] = pd.to_datetime(df["date"])

    # On ne prend que les transactions avant la date donnée
    df = df[df["date"] <= pd.to_datetime(date)]

    # Somme des investissements (positifs) et des retraits (négatifs)
    total_invested = df["amount"].sum()
    return total_invested


def create_kpi_metrics(portfolio):
    """Calcule les métriques KPI pour le dashboard"""
    net_worth = portfolio.get_net_worth()

    # Calcul de la variation des investissements
    financial_investments = getattr(portfolio, "financial_investments", {})
    total_invested = sum(inv.quantity * inv.initial_value for inv in financial_investments.values())
    current_value = sum(inv.get_total_value() for inv in financial_investments.values())
    investment_change = ((current_value - total_invested) / total_invested * 100) if total_invested > 0 else 0

    # Crédits
    total_credits = portfolio.get_total_credits_balance()

    return {
        'net_worth': net_worth,
        'investment_value': current_value,
        'investment_change': investment_change,
        'total_credits': total_credits
    }


def get_cac40_data():
    """Récupère les données du CAC40"""
    
    ticker = yf.Ticker("^FCHI")
    hist = ticker.history(period="5d")
    current_value = hist['Close'].iloc[-1]
    previous_value = hist['Close'].iloc[-2]
    change = ((current_value - previous_value) / previous_value) * 100
    return current_value, change


def get_dji_data():
    """Récupère les données du CAC40"""
    try:
        
        ticker = yf.Ticker("^DJI")
        hist = ticker.history(period="5d")
        if len(hist) >= 2:
            current_value = hist['Close'].iloc[-1]
            previous_value = hist['Close'].iloc[-2]
            change = ((current_value - previous_value) / previous_value) * 100
            return current_value, change
        return 6744.0, 0.0
    except:
        return 6744.0, 0.0


def get_btc_data():
    """Récupère les données du CAC40"""
    try:
        
        ticker = yf.Ticker("BTC-USD")
        hist = ticker.history(period="5d")
        if len(hist) >= 2:
            current_value = hist['Close'].iloc[-1]
            previous_value = hist['Close'].iloc[-2]
            change = ((current_value - previous_value) / previous_value) * 100
            return current_value, change
        return 125512.0, 0.0
    except:
        return 125512.0, 0.0


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


def display_portfolio_pie(portfolio):
    st.plotly_chart(create_portfolio_pie_chart(portfolio), use_container_width=True, config={'displayModeBar': False})


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


def create_financial_portfolio_vs_benchmark_chart(portfolio, benchmark_ticker="^FCHI", benchmark_name="CAC40"):
    """
    Graphique comparant le portfolio (sans immobilier) à un benchmark choisi
    
    Args:
        portfolio: Le portfolio à analyser
        benchmark_ticker: Le ticker Yahoo Finance (ex: "^FCHI", "^DJI", "^GSPC", "BTC-USD")
        benchmark_name: Le nom à afficher (ex: "CAC40", "Dow Jones", "S&P 500", "Bitcoin")
    """
    

    df = get_portfolio_monthly_history(portfolio)
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data", x=0.5, y=0.5, showarrow=False)
        return fig

    # Filtrer pour exclure l'immobilier
    dates = df["date"]
    values_no_real_estate = df["value"] - df.get("real_estate_value", 0)

    # Récupérer les données du benchmark
    benchmark_series = None
    try:
        
        ticker = yf.Ticker(benchmark_ticker)

        # Convertir explicitement en datetime
        start_date = pd.to_datetime(dates.iloc[0])
        end_date = pd.to_datetime(dates.iloc[-1])

        # Ajouter des marges
        start_date = start_date - pd.Timedelta(days=30)
        end_date = end_date + pd.Timedelta(days=1)

        # Récupérer les données
        benchmark_hist = ticker.history(start=start_date, end=end_date)

        # Supprimer la timezone pour éviter les erreurs de comparaison
        if benchmark_hist.index.tz is not None:
            benchmark_hist.index = benchmark_hist.index.tz_localize(None)

        print(f"📥 Lignes reçues: {len(benchmark_hist)}")

        if len(benchmark_hist) > 0:

            # Aligner avec les dates du portfolio
            benchmark_values = []
            for date in dates:
                date_pd = pd.to_datetime(date)
                # Trouver la date la plus proche (avant ou le jour même)
                mask = benchmark_hist.index <= date_pd
                if mask.any():
                    closest_idx = benchmark_hist.index[mask][-1]
                    benchmark_values.append(benchmark_hist.loc[closest_idx, 'Close'])
                else:
                    benchmark_values.append(None)

            benchmark_series = pd.Series(benchmark_values, index=dates)
            # Remplir les valeurs manquantes
            benchmark_series = benchmark_series.fillna(method='ffill').fillna(method='bfill')

        else:
            print("⚠️ Aucune ligne reçue de yfinance")

    except Exception as e:
        print(f"❌ ERREUR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

    # Créer le graphique
    fig = go.Figure()

    # Benchmark (axe gauche)
    if benchmark_series is not None and not benchmark_series.empty:
        fig.add_trace(go.Scatter(
            x=dates,
            y=benchmark_series,
            name=benchmark_name,
            line=dict(color='#F59E0B', width=2),
            yaxis='y'
        ))
    else:
        print(f"❌ Pas de trace {benchmark_name}")

    # Portfolio (axe droit)
    fig.add_trace(go.Scatter(
        x=dates,
        y=values_no_real_estate,
        name='Portfolio',
        line=dict(color='#3B82F6', width=3),
        fill='tozeroy',
        fillcolor='rgba(59,130,246,0.1)',
        yaxis='y2'
    ))

    layout = get_base_layout(" ", 400)
    layout.update({
        'xaxis_title': "Date",
        'hovermode': 'x unified',
        'yaxis': dict(
            title=dict(text=f'{benchmark_name}', font=dict(color='#F59E0B')),
            tickfont=dict(color='#F59E0B'),
            side='left'
        ),
        'yaxis2': dict(
            title=dict(text='Financial Portfolio value (€)', font=dict(color='#3B82F6')),
            tickfont=dict(color='#3B82F6'),
            overlaying='y',
            side='right'
        ),
        'legend': dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(0,0,0,0.5)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        ),
        'margin': dict(l=60, r=60, t=50, b=40)
    })
    fig.update_layout(**layout)

    return fig


# Dictionnaire des benchmarks disponibles
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


# Exemple d'utilisation dans Streamlit
def render_portfolio_comparison(portfolio):
    """
    Interface Streamlit pour afficher la comparaison avec sélection du benchmark
    """
    
    # Selectbox pour choisir le benchmark
    selected_benchmark = st.selectbox(
        "Choosing a comparison benchmark",
        options=list(AVAILABLE_BENCHMARKS.keys()),
        index=0  # CAC 40 par défaut
    )
    
    # Récupérer le ticker correspondant
    ticker = AVAILABLE_BENCHMARKS[selected_benchmark]
    
    # Créer et afficher le graphique
    fig = create_financial_portfolio_vs_benchmark_chart(
        portfolio, 
        benchmark_ticker=ticker,
        benchmark_name=selected_benchmark
    )
    
    st.plotly_chart(fig, use_container_width=True)


# Alternative: Fonction pour obtenir les données d'un benchmark spécifique
def get_benchmark_data(ticker, period="5d"):
    """
    Récupère les données d'un benchmark
    
    Args:
        ticker: Le ticker Yahoo Finance
        period: Période de récupération (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
    
    Returns:
        tuple: (current_value, change_percentage)
    """
    try:
        
        ticker_obj = yf.Ticker(ticker)
        hist = ticker_obj.history(period=period)
        if len(hist) >= 2:
            current_value = hist['Close'].iloc[-1]
            previous_value = hist['Close'].iloc[-2]
            change = ((current_value - previous_value) / previous_value) * 100
            return current_value, change
        return None, 0.0
    except Exception as e:
        print(f"Erreur lors de la récupération de {ticker}: {e}")
        return None, 0.0


# Exemple d'utilisation pour les KPIs
def create_benchmark_kpi_card(benchmark_name, ticker):
    """Crée une carte KPI pour un benchmark"""
    import streamlit as st
    
    current_value, change = get_benchmark_data(ticker)
    
    if current_value:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.metric(
                label=benchmark_name,
                value=f"{current_value:,.2f}",
                delta=f"{change:+.2f}%"
            )