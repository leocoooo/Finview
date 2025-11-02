"""
Graphiques principaux du portfolio
"""
import plotly.graph_objects as go
from src.finview.ui.formatting import format_currency
from .config import THEME, VIBRANT_COLORS
from .layouts import get_base_layout


def create_portfolio_pie_chart(portfolio):
    """
    Crée un graphique en donut montrant la distribution des actifs avec pourcentages
    
    Args:
        portfolio: Instance de Portfolio
        
    Returns:
        go.Figure: Graphique Plotly
    """
    labels, values, colors, hover_texts = [], [], [], []

    # Cash
    if getattr(portfolio, "cash", 0) > 0:
        labels.append('💰 Cash')
        values.append(portfolio.cash)
        colors.append(THEME['cash'])
        hover_texts.append(f"<b>Cash</b><br>Amount: {format_currency(portfolio.cash)}<extra></extra>")

    # Financial investments
    financial_total = getattr(portfolio, "get_financial_investments_value", lambda: 0)()
    if financial_total > 0:
        labels.append('📈 Financial')
        values.append(financial_total)
        colors.append(THEME['financial'])

        details = []
        for name, inv in list(getattr(portfolio, "financial_investments", {}).items())[:5]:
            perf = getattr(inv, "get_gain_loss_percentage", lambda: 0)()
            perf_color = '🟢' if perf >= 0 else '🔴'
            details.append(f"{perf_color} {name}: {format_currency(getattr(inv, 'get_total_value', lambda: 0)())}")
        hover_text = f"<b>Financial Investments</b><br>Total: {format_currency(financial_total)}<br><br>" + "<br>".join(details)
        if len(getattr(portfolio, "financial_investments", {})) > 5:
            hover_text += f"<br>...and {len(portfolio.financial_investments)-5} more"
        hover_text += "<extra></extra>"
        hover_texts.append(hover_text)

    # Real estate
    real_estate_total = getattr(portfolio, "get_real_estate_investments_value", lambda: 0)()
    if real_estate_total > 0:
        labels.append('🏠 Real Estate')
        values.append(real_estate_total)
        colors.append(THEME['real_estate'])

        details = []
        total_rental = 0
        for name, inv in list(getattr(portfolio, "real_estate_investments", {}).items())[:4]:
            rental_yield = getattr(inv, 'rental_yield', 0)
            annual_income = getattr(inv, 'get_annual_rental_income', lambda: 0)()
            total_rental += annual_income
            detail = f"• {name}: {format_currency(getattr(inv, 'get_total_value', lambda: 0)())}"
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
        pull=[0.02] * len(values)
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
    """
    Graphique en barres pour chaque investissement financier avec des couleurs vibrantes
    
    Args:
        portfolio: Instance de Portfolio
        
    Returns:
        go.Figure: Graphique Plotly
    """
    investments = getattr(portfolio, "financial_investments", {})
    if not investments:
        fig = go.Figure()
        fig.add_annotation(text="No financial investments", x=0.5, y=0.5,
                           font=dict(size=16, color=THEME['text_secondary']), showarrow=False)
        fig.update_layout(**get_base_layout("📊 Financial Investments", 400))
        return fig
    
    names = list(investments.keys())
    values = [getattr(inv, 'get_total_value', lambda: 0)() for inv in investments.values()]
    
    colors = VIBRANT_COLORS * ((len(values) // len(VIBRANT_COLORS)) + 1)
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
    """
    Graphique de performance avec couleurs vibrantes et effets de gradient
    
    Args:
        portfolio: Instance de Portfolio
        
    Returns:
        go.Figure: Graphique Plotly
    """
    investments = {**getattr(portfolio, "financial_investments", {}),
                   **getattr(portfolio, "real_estate_investments", {})}
    if not investments:
        fig = go.Figure()
        fig.add_annotation(text="No investments", x=0.5, y=0.5,
                           font=dict(size=16, color=THEME['text_secondary']), showarrow=False)
        fig.update_layout(**get_base_layout("📈 Investment Performance Per Asset", 400))
        return fig
    
    names = list(investments.keys())
    perfs = [getattr(inv, "get_gain_loss_percentage", lambda: 0)() for inv in investments.values()]
    values = [getattr(inv, 'get_total_value', lambda: 0)() for inv in investments.values()]
    
    colors = VIBRANT_COLORS * ((len(values) // len(VIBRANT_COLORS)) + 1)
    colors = colors[:len(values)]
    
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
    layout['xaxis'] = dict(showgrid=False, tickangle=-30 if len(names) > 6 else 0)
    layout['showlegend'] = False
    fig.update_layout(**layout)
    return fig


def create_performance_chart_filtered(portfolio):
    """
    Graphique de performance pour des actifs sélectionnés
    
    Args:
        portfolio: Instance de Portfolio
        
    Returns:
        go.Figure: Graphique Plotly
    """
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
