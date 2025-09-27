
import plotly.graph_objects as go

def create_portfolio_pie_chart(portfolio):
    labels = []
    values = []
    colors = []
    
    if portfolio.cash > 0:
        labels.append('Liquidités')
        values.append(portfolio.cash)
        colors.append('#1f77b4')
    
    for name, inv in portfolio.investments.items():
        labels.append(name)
        values.append(inv.get_total_value())
        colors.append('#2ca02c')
    
    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values,
        marker_colors=colors,
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Valeur: %{value:.2f}€<br>Pourcentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title="Répartition du portefeuille",
        showlegend=True,
        height=400
    )
    
    return fig
