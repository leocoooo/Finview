"""
Fonction pour créer un graphique d'évolution historique du portefeuille
"""
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np


def create_portfolio_evolution_chart(portfolio, years=5):
    """
    Crée un graphique d'évolution du portefeuille sur X années
    avec des données simulées convergeant vers la valeur actuelle

    Args:
        portfolio: Instance du Portfolio
        years: Nombre d'années d'historique à afficher (défaut: 5)

    Returns:
        plotly.graph_objects.Figure
    """
    # Valeur actuelle du portefeuille
    current_value = portfolio.get_net_worth()

    # Générer les dates (du passé à aujourd'hui)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)

    # Nombre de points mensuels
    num_months = years * 12
    dates = [start_date + timedelta(days=30 * i) for i in range(num_months + 1)]

    # Générer une évolution réaliste
    # On part d'une valeur initiale (par exemple 60-80% de la valeur actuelle)
    initial_value = current_value * np.random.uniform(0.4, 0.7)

    # Créer une tendance générale de croissance avec volatilité
    # Taux de croissance mensuel moyen pour atteindre la valeur actuelle
    monthly_growth_rate = (current_value / initial_value) ** (1 / num_months) - 1

    # Générer les valeurs avec volatilité
    values = [initial_value]

    for i in range(1, num_months + 1):
        # Tendance de croissance + bruit aléatoire
        volatility = np.random.normal(0, 0.03)  # Volatilité de 3%
        growth = monthly_growth_rate + volatility

        # Nouvelle valeur
        new_value = values[-1] * (1 + growth)

        # S'assurer que les valeurs restent positives
        new_value = max(new_value, initial_value * 0.5)

        values.append(new_value)

    # Forcer la dernière valeur à être exactement la valeur actuelle
    values[-1] = current_value

    # Lisser légèrement les derniers points pour converger naturellement
    for i in range(-5, 0):
        weight = (5 + i) / 5
        values[i] = values[i] * (1 - weight) + current_value * weight

    # Créer le graphique
    fig = go.Figure()

    # Ligne principale
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode='lines',
        name='Valeur du Portefeuille',
        line=dict(color='#3498DB', width=3),
        fill='tozeroy',
        fillcolor='rgba(52, 152, 219, 0.1)',
        hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Valeur: %{y:,.0f}€<extra></extra>'
    ))

    # Point actuel mis en évidence
    fig.add_trace(go.Scatter(
        x=[dates[-1]],
        y=[current_value],
        mode='markers',
        name='Valeur Actuelle',
        marker=dict(
            size=12,
            color='#2ECC71',
            symbol='circle',
            line=dict(color='white', width=2)
        ),
        hovertemplate=f'<b>Aujourd\'hui</b><br>Valeur: {current_value:,.0f}€<extra></extra>'
    ))

    # Calculer les statistiques
    total_gain = current_value - initial_value
    total_return = ((current_value / initial_value) - 1) * 100
    annualized_return = ((current_value / initial_value) ** (1 / years) - 1) * 100

    # Ligne de référence valeur initiale
    fig.add_hline(
        y=initial_value,
        line_dash="dash",
        line_color="gray",
        opacity=0.5,
        annotation_text=f"Départ: {initial_value:,.0f}€",
        annotation_position="left"
    )

    # Configuration du layout
    fig.update_layout(
        title={
            'text': f"📈 Évolution du Portefeuille sur {years} ans",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': 'white'}
        },
        xaxis=dict(
            title="Date",
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            gridwidth=1
        ),
        yaxis=dict(
            title="Valeur (€)",
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            gridwidth=1,
            tickformat=',.0f',
            ticksuffix='€'
        ),
        height=400,
        hovermode='x unified',
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
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=12),
        margin=dict(l=60, r=30, t=80, b=60)
    )

    # Ajouter des annotations pour les statistiques
    annotation_text = (
        f"<b>Performance sur {years} ans</b><br>"
        f"Gain total: {total_gain:+,.0f}€ ({total_return:+.1f}%)<br>"
        f"Rendement annualisé: {annualized_return:.1f}%/an"
    )

    fig.add_annotation(
        text=annotation_text,
        xref="paper", yref="paper",
        x=0.02, y=0.98,
        xanchor='left', yanchor='top',
        showarrow=False,
        bgcolor='rgba(0,0,0,0.7)',
        bordercolor='rgba(52, 152, 219, 0.5)',
        borderwidth=2,
        borderpad=10,
        font=dict(size=11, color='white')
    )

    return fig


def add_evolution_chart_to_dashboard(portfolio):
    """
    Ajoute le graphique d'évolution au tableau de bord
    À insérer dans la fonction show_dashboard() après le pie chart
    """
    st.markdown("---")
    st.subheader("📈 Évolution Historique")

    # Sélecteur de période
    col1, col2 = st.columns([3, 1])

    with col1:
        years_option = st.selectbox(
            "Période d'affichage",
            options=[1, 2, 5, 10],
            index=2,  # Par défaut 5 ans
            help="Sélectionnez la période d'historique à afficher"
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        refresh = st.button("🔄 Actualiser", help="Régénérer l'historique simulé")

    # Générer et afficher le graphique
    fig = create_portfolio_evolution_chart(portfolio, years=years_option)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Note explicative
    st.info("""
    💡 **Note**: Cet historique est une simulation rétrospective basée sur votre valeur actuelle. 
    Pour un historique réel, vos transactions futures seront automatiquement enregistrées.
    """)