# portfolio_package/visualizations.py
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
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
        fig.update_layout(**get_base_layout("📊 Distribution of Assets", 500))
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

    layout = get_base_layout("📊 Distribution of Assets", 550)
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
    fig.update_layout(**layout)
    return fig


def create_financial_investments_chart(portfolio):
    """Bar chart for each financial investment with unique dark colors"""
    investments = getattr(portfolio, "financial_investments", {})
    if not investments:
        fig = go.Figure()
        fig.add_annotation(text="No financial investments", x=0.5, y=0.5,
                           font=dict(size=16, color=THEME['text_secondary']), showarrow=False)
        fig.update_layout(**get_base_layout("📊 Financial Investments", 400))
        return fig

    names = list(investments.keys())
    values = [getattr(inv, 'get_total_value', lambda:0)() for inv in investments.values()]
    colors = THEME['dark_colors'] * ((len(values)//len(THEME['dark_colors']))+1)
    colors = colors[:len(values)]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=names, y=values,
        marker=dict(color=colors),
        text=[format_currency(v) for v in values],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Value: %{y}<extra></extra>'
    ))

    layout = get_base_layout("📊 Financial Investments Breakdown", 400)
    layout['yaxis'] = dict(title='Value (€)', gridcolor=THEME['grid'])
    layout['xaxis'] = dict(showgrid=False)
    fig.update_layout(**layout)
    return fig


def create_performance_chart(portfolio):
    """Performance chart with colors matching financial investments chart"""
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
    colors = THEME['dark_colors'] * ((len(values)//len(THEME['dark_colors']))+1)
    colors = colors[:len(values)]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=names, y=perfs,
        marker=dict(color=colors),
        hovertemplate='<b>%{x}</b><br>Performance: %{y:+.1f}%<br>Value: %{customdata}<extra></extra>',
        customdata=[format_currency(v) for v in values]
    ))
    fig.add_hline(y=0, line=dict(color=THEME['grid'], dash='dash'), opacity=0.5)

    layout = get_base_layout("📈 Investment Performance", 450)
    layout['yaxis'] = dict(title='Performance (%)', gridcolor=THEME['grid'], ticksuffix='%')
    layout['xaxis'] = dict(showgrid=False, tickangle=-30 if len(names)>6 else 0)
    fig.update_layout(**layout)
    return fig


def create_portfolio_evolution_chart(portfolio, years=5):
    """Smoothed portfolio evolution chart"""
    current_value = getattr(portfolio, "get_net_worth", lambda:1000)()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years*365)
    dates = [start_date + timedelta(days=30*i) for i in range(years*12+1)]
    initial_value = current_value*0.6 if current_value>0 else 1000

    values = np.linspace(initial_value, current_value, len(dates))
    values += np.random.normal(0, current_value*0.02, len(dates))
    values[-1] = current_value

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=values, mode='lines',
        line=dict(color=THEME['financial'], width=3),
        fill='tozeroy', fillcolor='rgba(59,130,246,0.1)',
        hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Value: %{y:,.0f}€<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=[dates[-1]], y=[current_value], mode='markers',
        marker=dict(size=12, color=THEME['positive'], line=dict(color='white', width=2)),
        name="Current Value"
    ))

    total_gain = current_value - initial_value
    annualized = ((current_value/initial_value)**(1/years)-1)*100
    fig.add_annotation(text=f"<b>{years}-year performance</b><br>Gain: {total_gain:+,.0f}€<br>Annualized: {annualized:.1f}%",
                       x=0.02, y=0.98, xanchor='left', yanchor='top',
                       showarrow=False, bgcolor='rgba(0,0,0,0.7)',
                       bordercolor=THEME['financial'], borderwidth=1,
                       font=dict(size=11, color='white'))

    layout = get_base_layout(f"📈 Portfolio evolution over {years} years", 450)
    layout['xaxis'] = dict(showgrid=True, gridcolor=THEME['grid'])
    layout['yaxis'] = dict(showgrid=True, gridcolor=THEME['grid'], ticksuffix='€')
    fig.update_layout(**layout)
    return fig


def create_world_investment_map(portfolio):
    """World map of investments"""
    investments = []
    for name, inv in getattr(portfolio, "financial_investments", {}).items():
        investments.append({'name': name, 'type':'Financial','value':inv.get_total_value(),
                            'perf':inv.get_gain_loss_percentage(),'lat':48.8566,'lon':2.3522,'color':THEME['financial']})
    for name, inv in getattr(portfolio, "real_estate_investments", {}).items():
        investments.append({'name': name, 'type':'Real Estate','value':inv.get_total_value(),
                            'perf':inv.get_gain_loss_percentage(),'lat':46.2276,'lon':2.2137,'color':THEME['real_estate']})

    if not investments:
        fig = go.Figure()
        fig.add_annotation(text="No geo-localized investments", x=0.5, y=0.5,
                           font=dict(size=16, color=THEME['text_secondary']), showarrow=False)
        fig.update_layout(**get_base_layout("🌍 World Investment Map", 500))
        return fig

    fig = go.Figure()
    for inv in investments:
        fig.add_trace(go.Scattergeo(
            lon=[inv['lon']], lat=[inv['lat']], text=inv['name'],
            mode='markers', marker=dict(size=15, color=inv['color'], opacity=0.8),
            hovertemplate=f"<b>{inv['name']}</b><br>Value: {format_currency(inv['value'])}<br>Perf: {inv['perf']:+.1f}%<extra></extra>"
        ))

    layout = get_base_layout("🌍 World Investment Map", 600)
    layout['geo'] = dict(
        projection_type='natural earth',
        showland=True, landcolor='rgba(51, 65, 85, 0.4)',
        showocean=True, oceancolor='rgba(15, 23, 42, 0.6)',
        showcountries=True, countrycolor='rgba(148, 163, 184, 0.2)',
        bgcolor='rgba(0,0,0,0)'
    )
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


def display_portfolio_evolution(portfolio, years=5):
    st.plotly_chart(create_portfolio_evolution_chart(portfolio, years=years), use_container_width=True, config={'displayModeBar': False})


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