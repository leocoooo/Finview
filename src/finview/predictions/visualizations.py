"""
Visualization functions for wealth predictions.

This module provides functions to create interactive charts for portfolio predictions,
including confidence intervals, scenarios, and historical comparisons.
"""
import plotly.graph_objects as go
from typing import Dict, List, Any


# Chart styling constants
CHART_COLORS = {
    'pessimistic_zone': 'rgba(231, 76, 60, 0.15)',  # Light red
    'central_zone': 'rgba(52, 152, 219, 0.25)',     # Light blue
    'pessimistic_line': '#E74C3C',                   # Red
    'median_line': '#2E86DE',                        # Blue
    'mean_line': '#10AC84',                          # Green
    'optimistic_line': '#F39C12',                    # Orange
    'reference_line': 'white',                       # White
    'grid': 'rgba(255,255,255,0.1)',                # Light gray
    'background': 'rgba(0,0,0,0)',                  # Transparent
    'legend_bg': 'rgba(0,0,0,0.6)',                 # Semi-transparent black
    'legend_border': 'rgba(255,255,255,0.3)',       # Light border
    'text': 'white'                                  # White text
}

CHART_LAYOUT = {
    'height': 550,
    'font_family': "Arial, sans-serif",
    'font_size': 12,
    'title_size': 18
}


def _add_confidence_zone(fig: go.Figure, 
                         time_points: List[int], 
                         upper_values: List[float], 
                         lower_values: List[float],
                         color: str,
                         name: str) -> None:
    """Add a confidence zone to the chart.
    
    Args:
        fig: Plotly figure to add the zone to
        time_points: List of time points (years)
        upper_values: Upper bound values
        lower_values: Lower bound values
        color: Fill color (rgba format)
        name: Legend name for this zone
    """
    fig.add_trace(go.Scatter(
        x=time_points + time_points[::-1],
        y=list(upper_values) + list(lower_values[::-1]),
        fill='toself',
        fillcolor=color,
        line=dict(color='rgba(255,255,255,0)'),
        name=name,
        showlegend=True,
        hoverinfo='skip'
    ))


def _add_scenario_line(fig: go.Figure,
                       time_points: List[int],
                       values: List[float],
                       name: str,
                       color: str,
                       width: int = 2,
                       dash: str = 'solid') -> None:
    """Add a scenario line to the chart.
    
    Args:
        fig: Plotly figure to add the line to
        time_points: List of time points (years)
        values: Values for each time point
        name: Legend name for this line
        color: Line color
        width: Line width
        dash: Line style ('solid', 'dash', 'dot')
    """
    fig.add_trace(go.Scatter(
        x=time_points,
        y=values,
        mode='lines',
        name=name,
        line=dict(color=color, width=width, dash=dash)
    ))


def _add_reference_line(fig: go.Figure, 
                        value: float, 
                        label: str) -> None:
    """Add a horizontal reference line.
    
    Args:
        fig: Plotly figure to add the line to
        value: Y-axis value for the line
        label: Label for the line
    """
    fig.add_hline(
        y=value,
        line_dash="dot",
        line_color=CHART_COLORS['reference_line'],
        annotation_text=label,
        annotation_position="right"
    )


def _configure_chart_layout(fig: go.Figure, 
                            years: int, 
                            title: str) -> None:
    """Configure the chart layout and styling.
    
    Args:
        fig: Plotly figure to configure
        years: Number of years in projection
        title: Chart title
    """
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': CHART_LAYOUT['title_size'], 'color': CHART_COLORS['text']}
        },
        xaxis_title="Years",
        yaxis_title="Portfolio Value (€, Real)",
        xaxis=dict(
            tickmode='linear', 
            tick0=0, 
            dtick=1 if years <= 10 else 2
        ),
        yaxis=dict(
            tickformat='.0f', 
            ticksuffix='€'
        ),
        height=CHART_LAYOUT['height'],
        hovermode='x unified',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor=CHART_COLORS['legend_bg'],
            bordercolor=CHART_COLORS['legend_border'],
            borderwidth=1
        ),
        paper_bgcolor=CHART_COLORS['background'],
        plot_bgcolor=CHART_COLORS['background'],
        font=dict(
            family=CHART_LAYOUT['font_family'], 
            size=CHART_LAYOUT['font_size'], 
            color=CHART_COLORS['text']
        )
    )
    
    # Add grid lines
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor=CHART_COLORS['grid']
    )
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor=CHART_COLORS['grid']
    )


def create_prediction_chart(prediction_results: Dict[str, Any]) -> go.Figure:
    """Create an interactive chart for portfolio predictions.
    
    This function creates a comprehensive visualization showing:
    - Confidence zones (80% and 50%)
    - Multiple scenario lines (pessimistic, median, average, optimistic)
    - Reference line for current value
    
    Args:
        prediction_results: Results from simulate_portfolio_future() containing:
            - years: Number of years projected
            - percentiles: Dict with p10, p25, p50, p75, p90, mean
            - initial_value: Starting portfolio value
        
    Returns:
        go.Figure: Interactive Plotly chart
        
    Example:
        >>> results = simulate_portfolio_future(portfolio, years=10)
        >>> fig = create_prediction_chart(results)
        >>> fig.show()
    """
    years = prediction_results['years']
    time_points = list(range(years + 1))
    percentiles = prediction_results['percentiles']
    
    fig = go.Figure()
    
    # Add confidence zones (from widest to narrowest)
    _add_confidence_zone(
        fig, 
        time_points,
        percentiles['p90'],
        percentiles['p10'],
        CHART_COLORS['pessimistic_zone'],
        '80% Confidence (P10-P90)'
    )
    
    _add_confidence_zone(
        fig,
        time_points,
        percentiles['p75'],
        percentiles['p25'],
        CHART_COLORS['central_zone'],
        '50% Confidence (P25-P75)'
    )
    
    # Add scenario lines
    _add_scenario_line(
        fig,
        time_points,
        percentiles['p10'],
        'Pessimistic (P10)',
        CHART_COLORS['pessimistic_line'],
        width=2,
        dash='dot'
    )
    
    _add_scenario_line(
        fig,
        time_points,
        percentiles['p50'],
        'Median (P50)',
        CHART_COLORS['median_line'],
        width=3,
        dash='solid'
    )
    
    _add_scenario_line(
        fig,
        time_points,
        percentiles['mean'],
        'Average',
        CHART_COLORS['mean_line'],
        width=2,
        dash='dash'
    )
    
    # Optional: Add optimistic scenario (P90)
    _add_scenario_line(
        fig,
        time_points,
        percentiles['p90'],
        'Optimistic (P90)',
        CHART_COLORS['optimistic_line'],
        width=2,
        dash='dot'
    )
    
    # Add reference line for current value
    _add_reference_line(
        fig,
        prediction_results['initial_value'],
        "Current Value"
    )
    
    # Configure chart layout
    title = f"Portfolio Projection - {years} Years (Real Values, Inflation-Adjusted)"
    _configure_chart_layout(fig, years, title)
    
    return fig


def create_comparison_chart(multiple_predictions: Dict[str, Dict[str, Any]]) -> go.Figure:
    """Create a comparison chart for multiple prediction scenarios.
    
    Args:
        multiple_predictions: Dict of scenario_name -> prediction_results
        
    Returns:
        go.Figure: Comparison chart
        
    Example:
        >>> conservative = simulate_portfolio_future(portfolio, years=10, num_simulations=500)
        >>> aggressive = simulate_portfolio_future(portfolio, years=10, num_simulations=500)
        >>> fig = create_comparison_chart({
        ...     'Conservative': conservative,
        ...     'Aggressive': aggressive
        ... })
    """
    fig = go.Figure()
    
    colors = ['#2E86DE', '#10AC84', '#F39C12', '#E74C3C', '#9B59B6']
    
    for idx, (scenario_name, results) in enumerate(multiple_predictions.items()):
        time_points = list(range(results['years'] + 1))
        color = colors[idx % len(colors)]
        
        # Add median line for each scenario
        _add_scenario_line(
            fig,
            time_points,
            results['percentiles']['p50'],
            f"{scenario_name} (Median)",
            color,
            width=3
        )
    
    # Configure layout
    _configure_chart_layout(
        fig, 
        max(r['years'] for r in multiple_predictions.values()),
        "Portfolio Projections - Scenario Comparison"
    )
    
    return fig

