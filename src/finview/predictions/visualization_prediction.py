"""
Fonctions de visualisation pour les prédictions de patrimoine
"""
import plotly.graph_objects as go


def create_prediction_chart(prediction_results):
    """
    Crée un graphique des prédictions avec zones de crise visibles
    
    Args:
        prediction_results: Résultats de simulate_portfolio_future()
        
    Returns:
        go.Figure: Graphique Plotly interactif
    """
    years = prediction_results['years']
    time_points = list(range(years + 1))
    percentiles = prediction_results['percentiles']

    fig = go.Figure()

    # Zone pessimiste (risque de perte)
    fig.add_trace(go.Scatter(
        x=time_points + time_points[::-1],
        y=list(percentiles['p90']) + list(percentiles['p10'][::-1]),
        fill='toself',
        fillcolor='rgba(231, 76, 60, 0.15)',  # Rouge transparent
        line=dict(color='rgba(255,255,255,0)'),
        name='80% Confidence (P10-P90)',
        showlegend=True
    ))

    # Zone centrale
    fig.add_trace(go.Scatter(
        x=time_points + time_points[::-1],
        y=list(percentiles['p75']) + list(percentiles['p25'][::-1]),
        fill='toself',
        fillcolor='rgba(52, 152, 219, 0.25)',
        line=dict(color='rgba(255,255,255,0)'),
        name='50% Confidence (P25-P75)',
        showlegend=True
    ))

    # Scénario pessimiste P10
    fig.add_trace(go.Scatter(
        x=time_points,
        y=percentiles['p10'],
        mode='lines',
        name='Pessimistic (P10)',
        line=dict(color='#E74C3C', width=2, dash='dot')
    ))

    # Médiane
    fig.add_trace(go.Scatter(
        x=time_points,
        y=percentiles['p50'],
        mode='lines',
        name='Median (P50)',
        line=dict(color='#2E86DE', width=3)
    ))

    # Moyenne
    fig.add_trace(go.Scatter(
        x=time_points,
        y=percentiles['mean'],
        mode='lines',
        name='Average',
        line=dict(color='#10AC84', width=2, dash='dash')
    ))

    # Ligne de référence
    fig.add_hline(
        y=prediction_results['initial_value'],
        line_dash="dot",
        line_color="white",
        annotation_text="Current Value",
        annotation_position="right"
    )

    fig.update_layout(
        title={
            'text': f"Portfolio Projection - {years} Years (Real Values, Inflation-Adjusted)",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': 'white'}
        },
        xaxis_title="Years",
        yaxis_title="Portfolio Value (€, Real)",
        xaxis=dict(tickmode='linear', tick0=0, dtick=1 if years <= 10 else 2),
        yaxis=dict(tickformat='.0f', ticksuffix='€'),
        height=550,
        hovermode='x unified',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(0,0,0,0.6)',
            bordercolor='rgba(255,255,255,0.3)',
            borderwidth=1
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=12, color='white')
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')

    return fig
