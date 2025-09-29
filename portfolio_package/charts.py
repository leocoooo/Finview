
import plotly.graph_objects as go


def create_professional_pie_chart(portfolio):
    """Crée un graphique en secteurs professionnel et lisible"""

    # Palette de couleurs professionnelle
    color_palette = {
        'cash': '#27AE60',           # Vert pour liquidités
        'financial': '#3498DB',      # Bleu pour investissements financiers
        'real_estate': '#E67E22',    # Orange pour immobilier
        'credits': '#E74C3C'         # Rouge pour crédits
    }

    labels = []
    values = []
    colors = []
    hover_texts = []

    # Liquidités
    if portfolio.cash > 0:
        labels.append('💰 Liquidités')
        values.append(portfolio.cash)
        colors.append(color_palette['cash'])
        hover_texts.append(f'<b>💰 Liquidités</b><br>Montant: {portfolio.cash:.2f}€')

    # Investissements financiers (regroupés)
    financial_total = portfolio.get_financial_investments_value()
    if financial_total > 0:
        labels.append('📈 Inv. Financiers')
        values.append(financial_total)
        colors.append(color_palette['financial'])

        # Détail des investissements financiers
        fin_details = []
        for name, inv in portfolio.financial_investments.items():
            inv_type = getattr(inv, 'investment_type', 'N/A')
            perf = inv.get_gain_loss_percentage()
            fin_details.append(f"• {name} ({inv_type}): {inv.get_total_value():.2f}€ ({perf:+.1f}%)")

        hover_text = f'<b>📈 Investissements Financiers</b><br>Total: {financial_total:.2f}€<br><br>' + '<br>'.join(fin_details[:5])
        if len(fin_details) > 5:
            hover_text += f'<br>... et {len(fin_details)-5} autres'
        hover_texts.append(hover_text)

    # Investissements immobiliers (regroupés)
    real_estate_total = portfolio.get_real_estate_investments_value()
    if real_estate_total > 0:
        labels.append('🏠 Inv. Immobiliers')
        values.append(real_estate_total)
        colors.append(color_palette['real_estate'])

        # Détail des investissements immobiliers
        re_details = []
        total_rental_income = 0
        for name, inv in portfolio.real_estate_investments.items():
            property_type = getattr(inv, 'property_type', 'N/A')
            location = getattr(inv, 'location', '')
            rental_yield = getattr(inv, 'rental_yield', 0)
            annual_income = inv.get_annual_rental_income() if hasattr(inv, 'get_annual_rental_income') else 0
            total_rental_income += annual_income

            detail_text = f"• {name} ({property_type}): {inv.get_total_value():.2f}€"
            if rental_yield > 0:
                detail_text += f" - {rental_yield:.1f}%"
            re_details.append(detail_text)

        hover_text = f'<b>🏠 Investissements Immobiliers</b><br>Total: {real_estate_total:.2f}€'
        if total_rental_income > 0:
            hover_text += f'<br>Revenu annuel: {total_rental_income:.2f}€'
        hover_text += '<br><br>' + '<br>'.join(re_details[:4])
        if len(re_details) > 4:
            hover_text += f'<br>... et {len(re_details)-4} autres'
        hover_texts.append(hover_text)

    if not labels:
        # Graphique vide
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune donnée à afficher<br>Ajoutez des liquidités ou des investissements",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            font=dict(size=16, color="gray"),
            showarrow=False
        )

        fig.update_layout(
            title={
                'title_font_color' : 'white',
                'text': "📊 Répartition du Portefeuille",
                'x': 0.2,
                'xanchor': 'center',
                'font': {'size': 20, 'family': 'Arial, sans-serif'}
            },
            title_font_color="white",
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        return fig

    # Création du pie chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,  # Donut chart pour un look plus moderne
        marker=dict(
            colors=colors,
            line=dict(color='#FFFFFF', width=3)
        ),
        textinfo='label+percent+value',
        texttemplate='<b>%{label}</b><br>%{value:.0f}€<br>(%{percent})',
        textposition='outside',
        textfont=dict(size=13, family='Arial, sans-serif'),
        hovertemplate='%{customdata}<extra></extra>',
        customdata=hover_texts,
        pull=[0.05 if i == values.index(max(values)) else 0 for i in range(len(values))]  # Met en avant la plus grande section
    )])

    # Mise en page professionnelle
    fig.update_layout(
        title={
            'text': "📊 Répartition du Portefeuille",
            'x': 0.45,
            'xanchor': 'center',
            'font': {'size': 22, 'family': 'Arial, sans-serif', 'color':"white"}
        },
        font=dict(family="Arial, sans-serif", size=12),
        height=600,
        margin=dict(l=50, r=50, t=100, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(size=12),
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)',
            borderwidth=0
        ),
        # Annotations au centre pour le total
        annotations=[
            dict(
                text=f"<b>Total</b><br>{sum(values):.0f}€",
                x=0.5, y=0.5,
                font_size=16,
                font_family="Arial, sans-serif",
                font_color='#2c3e50',
                showarrow=False
            )
        ]
    )

    return fig

def create_portfolio_chart(portfolio):
    """Crée un graphique en barres horizontales empilées pour la répartition du portefeuille"""

    # Palette de couleurs professionnelle
    color_palette = {
        'cash': '#2E8B57',           # Vert foncé pour liquidités
        'financial': '#1E90FF',      # Bleu pour investissements financiers
        'real_estate': '#FF6B35',    # Orange pour immobilier
        'credits': '#DC143C'         # Rouge pour crédits
    }

    # Collecte des données par catégorie
    categories = []
    values = []
    colors = []
    details = []

    # Liquidités
    if portfolio.cash > 0:
        categories.append('💰 Liquidités')
        values.append(portfolio.cash)
        colors.append(color_palette['cash'])
        details.append(f'Montant disponible: {portfolio.cash:.2f}€')

    # Investissements financiers regroupés
    financial_total = portfolio.get_financial_investments_value()
    if financial_total > 0:
        categories.append('📈 Inv. Financiers')
        values.append(financial_total)
        colors.append(color_palette['financial'])

        # Détail des investissements financiers
        fin_details = []
        for name, inv in portfolio.financial_investments.items():
            inv_type = getattr(inv, 'investment_type', 'N/A')
            gain_loss = inv.get_gain_loss()
            perf = inv.get_gain_loss_percentage()
            fin_details.append(f"• {name} ({inv_type}): {inv.get_total_value():.2f}€ ({perf:+.1f}%)")
        details.append('<br>'.join(fin_details))

    # Investissements immobiliers regroupés
    real_estate_total = portfolio.get_real_estate_investments_value()
    if real_estate_total > 0:
        categories.append('🏠 Inv. Immobiliers')
        values.append(real_estate_total)
        colors.append(color_palette['real_estate'])

        # Détail des investissements immobiliers
        re_details = []
        for name, inv in portfolio.real_estate_investments.items():
            property_type = getattr(inv, 'property_type', 'N/A')
            location = getattr(inv, 'location', '')
            rental_yield = getattr(inv, 'rental_yield', 0)
            annual_income = inv.get_annual_rental_income() if hasattr(inv, 'get_annual_rental_income') else 0

            detail_text = f"• {name} ({property_type}): {inv.get_total_value():.2f}€"
            if location:
                detail_text += f" - {location}"
            if rental_yield > 0:
                detail_text += f" - Rendement: {rental_yield:.1f}%"
            if annual_income > 0:
                detail_text += f" - Revenu: {annual_income:.0f}€/an"
            re_details.append(detail_text)
        details.append('<br>'.join(re_details))

    # Crédits (valeurs négatives)
    credits_total = portfolio.get_total_credits_balance()
    if credits_total > 0:
        categories.append('💳 Crédits')
        values.append(-credits_total)  # Négatif pour l'affichage
        colors.append(color_palette['credits'])

        # Détail des crédits
        credit_details = []
        for name, credit in portfolio.credits.items():
            remaining = credit.get_remaining_balance()
            rate = credit.interest_rate
            credit_details.append(f"• {name}: -{remaining:.2f}€ (taux: {rate}%)")
        details.append('<br>'.join(credit_details))

    if not categories:
        # Graphique vide si pas de données
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune donnée à afficher",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title="📊 Répartition du Portefeuille",
            height=300,
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig

    # Création du graphique en barres horizontales empilées
    fig = go.Figure()

    total_value = sum([abs(v) for v in values])
    cumulative = 0

    for i, (cat, val, color, detail) in enumerate(zip(categories, values, colors, details)):
        percentage = (abs(val) / total_value) * 100

        # Texte à afficher sur la barre
        display_text = f"{cat}<br>{abs(val):.0f}€ ({percentage:.1f}%)"

        fig.add_trace(go.Bar(
            y=['Portfolio'],
            x=[abs(val)],
            orientation='h',
            name=cat,
            marker_color=color,
            text=display_text,
            textposition='inside',
            textfont=dict(size=11, color='white'),
            hovertemplate=f'<b>{cat}</b><br>{detail}<br>Valeur: {abs(val):.2f}€<br>Part: {percentage:.1f}%<extra></extra>',
            showlegend=True
        ))

    # Configuration de la mise en page
    fig.update_layout(
        title={
            'text': "📊 Répartition du Portefeuille",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Arial, sans-serif', 'color': '#2c3e50'}
        },
        barmode='stack',
        height=200,
        margin=dict(l=60, r=20, t=80, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(248,249,250,0.8)',
        font=dict(family="Arial, sans-serif", size=12),

        # Configuration des axes
        xaxis=dict(
            title="Valeur (€)",
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            tickformat='.0f',
            ticksuffix='€'
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False
        ),

        # Légende
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            font=dict(size=11)
        )
    )

    return fig

def create_performance_chart(portfolio):
    """Crée un graphique de performance des investissements"""

    # Collecte des performances
    financial_data = []
    real_estate_data = []

    # Investissements financiers
    for name, inv in portfolio.financial_investments.items():
        performance = inv.get_gain_loss_percentage()
        value = inv.get_total_value()
        inv_type = getattr(inv, 'investment_type', 'N/A')
        financial_data.append({
            'name': name,
            'performance': performance,
            'value': value,
            'type': inv_type
        })

    # Investissements immobiliers
    for name, inv in portfolio.real_estate_investments.items():
        performance = inv.get_gain_loss_percentage()
        value = inv.get_total_value()
        property_type = getattr(inv, 'property_type', 'N/A')
        real_estate_data.append({
            'name': name,
            'performance': performance,
            'value': value,
            'type': property_type
        })

    if not financial_data and not real_estate_data:
        fig = go.Figure()
        fig.add_annotation(
            text="Aucun investissement à analyser",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title="📈 Performance des Investissements",
            height=300,
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig

    fig = go.Figure()

    # Ajout des investissements financiers
    if financial_data:
        names_fin = [d['name'] for d in financial_data]
        perfs_fin = [d['performance'] for d in financial_data]
        values_fin = [d['value'] for d in financial_data]
        types_fin = [d['type'] for d in financial_data]

        fig.add_trace(go.Bar(
            x=names_fin,
            y=perfs_fin,
            name='📈 Financiers',
            marker_color='#1E90FF',
            hovertemplate='<b>%{x}</b><br>Type: %{customdata}<br>Performance: %{y:+.1f}%<br>Valeur: %{text:.2f}€<extra></extra>',
            customdata=types_fin,
            text=values_fin
        ))

    # Ajout des investissements immobiliers
    if real_estate_data:
        names_re = [d['name'] for d in real_estate_data]
        perfs_re = [d['performance'] for d in real_estate_data]
        values_re = [d['value'] for d in real_estate_data]
        types_re = [d['type'] for d in real_estate_data]

        fig.add_trace(go.Bar(
            x=names_re,
            y=perfs_re,
            name='🏠 Immobiliers',
            marker_color='#FF6B35',
            hovertemplate='<b>%{x}</b><br>Type: %{customdata}<br>Performance: %{y:+.1f}%<br>Valeur: %{text:.2f}€<extra></extra>',
            customdata=types_re,
            text=values_re
        ))

    # Ligne de référence à 0%
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

    # Configuration
    fig.update_layout(
        title={
            'text': "📈 Performance des Investissements",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'family': 'Arial, sans-serif', 'color': '#2c3e50'}
        },
        xaxis_title="Investissements",
        yaxis_title="Performance (%)",
        yaxis=dict(ticksuffix='%'),
        height=400,
        margin=dict(l=50, r=20, t=80, b=100),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(248,249,250,0.8)',
        font=dict(family="Arial, sans-serif", size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )

    # Rotation des labels sur l'axe X si nécessaire
    if len(financial_data) + len(real_estate_data) > 6:
        fig.update_xaxes(tickangle=45)

    return fig

def create_world_investment_map(portfolio):
    """Crée une carte du monde interactive des investissements"""

    # Dictionnaire de géolocalisation pour les investissements
    location_coordinates = {
        # Pays
        'france': {'lat': 46.2276, 'lon': 2.2137, 'country': 'France'},
        'paris': {'lat': 48.8566, 'lon': 2.3522, 'country': 'France'},
        'états-unis': {'lat': 39.8283, 'lon': -98.5795, 'country': 'États-Unis'},
        'usa': {'lat': 39.8283, 'lon': -98.5795, 'country': 'États-Unis'},
        'états unis': {'lat': 39.8283, 'lon': -98.5795, 'country': 'États-Unis'},
        'etats-unis': {'lat': 39.8283, 'lon': -98.5795, 'country': 'États-Unis'},
        'allemagne': {'lat': 51.1657, 'lon': 10.4515, 'country': 'Allemagne'},
        'royaume-uni': {'lat': 55.3781, 'lon': -3.4360, 'country': 'Royaume-Uni'},
        'japon': {'lat': 36.2048, 'lon': 138.2529, 'country': 'Japon'},
        'chine': {'lat': 35.8617, 'lon': 104.1954, 'country': 'Chine'},
        'canada': {'lat': 56.1304, 'lon': -106.3468, 'country': 'Canada'},
        'australie': {'lat': -25.2744, 'lon': 133.7751, 'country': 'Australie'},
        'brésil': {'lat': -14.2350, 'lon': -51.9253, 'country': 'Brésil'},
        'inde': {'lat': 20.5937, 'lon': 78.9629, 'country': 'Inde'},
        'suisse': {'lat': 46.8182, 'lon': 8.2275, 'country': 'Suisse'},
        'espagne': {'lat': 40.4637, 'lon': -3.7492, 'country': 'Espagne'},
        'italie': {'lat': 41.8719, 'lon': 12.5674, 'country': 'Italie'},
        'pays-bas': {'lat': 52.1326, 'lon': 5.2913, 'country': 'Pays-Bas'},
        'belgique': {'lat': 50.5039, 'lon': 4.4699, 'country': 'Belgique'},

        # Villes principales
        'new york': {'lat': 40.7128, 'lon': -74.0060, 'country': 'États-Unis'},
        'londres': {'lat': 51.5074, 'lon': -0.1278, 'country': 'Royaume-Uni'},
        'tokyo': {'lat': 35.6762, 'lon': 139.6503, 'country': 'Japon'},
        'hong kong': {'lat': 22.3193, 'lon': 114.1694, 'country': 'Hong Kong'},
        'singapour': {'lat': 1.3521, 'lon': 103.8198, 'country': 'Singapour'},
        'sydney': {'lat': -33.8688, 'lon': 151.2093, 'country': 'Australie'},
        'toronto': {'lat': 43.6532, 'lon': -79.3832, 'country': 'Canada'},
        'zurich': {'lat': 47.3769, 'lon': 8.5417, 'country': 'Suisse'},
        'amsterdam': {'lat': 52.3676, 'lon': 4.9041, 'country': 'Pays-Bas'},
        'francfort': {'lat': 50.1109, 'lon': 8.6821, 'country': 'Allemagne'},

        # Régions
        'europe': {'lat': 54.5260, 'lon': 15.2551, 'country': 'Europe'},
        'asie': {'lat': 34.0479, 'lon': 100.6197, 'country': 'Asie'},
        'amérique du nord': {'lat': 54.5260, 'lon': -105.2551, 'country': 'Amérique du Nord'},
        'amérique latine': {'lat': -8.7832, 'lon': -55.4915, 'country': 'Amérique Latine'},
    }

    # Collecter les données des investissements avec localisation
    investment_data = []

    # Investissements financiers
    for name, inv in portfolio.financial_investments.items():
        inv_type = getattr(inv, 'investment_type', 'Financier')
        location = getattr(inv, 'location', '')

        # Tentative de géolocalisation basée sur le nom ou autres indices
        coords = None
        if location:
            location_lower = location.lower().strip()
            coords = location_coordinates.get(location_lower)

        # Si pas de localisation explicite, essayer de deviner à partir du nom
        if not coords:
            name_lower = name.lower()
            for loc_key, loc_data in location_coordinates.items():
                if loc_key in name_lower:
                    coords = loc_data
                    break

        # Localisation par défaut pour les investissements financiers globaux
        if not coords:
            if 'sp' in name_lower or 's&p' in name_lower or 'nasdaq' in name_lower:
                coords = location_coordinates['états-unis']
            elif 'europe' in name_lower or 'eur' in name_lower:
                coords = location_coordinates['europe']
            elif 'world' in name_lower or 'global' in name_lower or 'msci' in name_lower:
                coords = location_coordinates['états-unis']  # Par défaut
            else:
                coords = location_coordinates['france']  # Défaut local

        if coords:
            investment_data.append({
                'name': name,
                'type': 'Financial',
                'category': inv_type,
                'value': inv.get_total_value(),
                'performance': inv.get_gain_loss_percentage(),
                'lat': coords['lat'],
                'lon': coords['lon'],
                'country': coords['country'],
                'color': '#3498DB',
                'size': max(10, min(50, inv.get_total_value() / 100))  # Taille proportionnelle
            })

    # Investissements immobiliers
    for name, inv in portfolio.real_estate_investments.items():
        property_type = getattr(inv, 'property_type', 'Immobilier')
        location = getattr(inv, 'location', 'France')
        rental_yield = getattr(inv, 'rental_yield', 0)

        # Géolocalisation pour l'immobilier
        coords = None
        if location:
            location_lower = location.lower().strip()
            coords = location_coordinates.get(location_lower)

        # Localisation par défaut
        if not coords:
            coords = location_coordinates['france']

        investment_data.append({
            'name': name,
            'type': 'Real Estate',
            'category': property_type,
            'value': inv.get_total_value(),
            'performance': inv.get_gain_loss_percentage(),
            'rental_yield': rental_yield,
            'lat': coords['lat'],
            'lon': coords['lon'],
            'country': coords['country'],
            'location_name': location,
            'color': '#E67E22',
            'size': max(15, min(60, inv.get_total_value() / 80))  # Taille légèrement plus grande
        })

    if not investment_data:
        # Carte vide
        fig = go.Figure()
        fig.add_annotation(
            text="Aucun investissement localisé à afficher<br>Ajoutez des investissements avec des localisations",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            font=dict(size=16, color="gray"),
            showarrow=False
        )
        fig.update_layout(
            title="🌍 Carte Mondiale des Investissements",
            height=400,
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig

    # Création de la carte
    fig = go.Figure()

    # Ajouter les investissements financiers
    financial_data = [inv for inv in investment_data if inv['type'] == 'Financial']
    if financial_data:
        fig.add_trace(go.Scattergeo(
            lon=[inv['lon'] for inv in financial_data],
            lat=[inv['lat'] for inv in financial_data],
            text=[f"<b>{inv['name']}</b><br>{inv['category']}<br>{inv['value']:.0f}€<br>{inv['performance']:+.1f}%"
                  for inv in financial_data],
            mode='markers',
            name='📈 Investissements Financiers',
            marker=dict(
                size=[inv['size'] for inv in financial_data],
                color='#3498DB',
                sizemode='diameter',
                line=dict(width=2, color='white'),
                opacity=0.8
            ),
            hovertemplate='<b>%{text}</b><br>Pays: %{customdata}<extra></extra>',
            customdata=[inv['country'] for inv in financial_data]
        ))

    # Ajouter les investissements immobiliers
    real_estate_data = [inv for inv in investment_data if inv['type'] == 'Real Estate']
    if real_estate_data:
        fig.add_trace(go.Scattergeo(
            lon=[inv['lon'] for inv in real_estate_data],
            lat=[inv['lat'] for inv in real_estate_data],
            text=[f"<b>{inv['name']}</b><br>{inv['category']}<br>{inv['value']:.0f}€<br>Rendement: {inv.get('rental_yield', 0):.1f}%<br>{inv['performance']:+.1f}%"
                  for inv in real_estate_data],
            mode='markers',
            name='🏠 Investissements Immobiliers',
            marker=dict(
                size=[inv['size'] for inv in real_estate_data],
                color='#E67E22',
                sizemode='diameter',
                line=dict(width=2, color='white'),
                opacity=0.8,
                symbol='square'  # Carré pour différencier de l'immobilier
            ),
            hovertemplate='<b>%{text}</b><br>Localisation: %{customdata}<extra></extra>',
            customdata=[inv['location_name'] for inv in real_estate_data]
        ))

    # Configuration de la carte
    fig.update_layout(
        title={
            'text': "🌍 Carte Mondiale des Investissements",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Arial, sans-serif', 'color': 'white'}
        },
        geo=dict(
            projection_type='equirectangular',
            showland=True,
            landcolor='rgb(217, 217, 217)',
            showocean=True,
            oceancolor='rgb(230, 245, 255)',
            showlakes=True,
            lakecolor='rgb(230, 245, 255)',
            showrivers=True,
            rivercolor='rgb(230, 245, 255)',
            showcoastlines=True,
            coastlinecolor='rgb(204, 204, 204)',
            showframe=False,
            showsubunits=True,
            subunitcolor='rgb(204, 204, 204)'
        ),
        height=500,
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=11),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)',
            borderwidth=0
        )
    )

    return fig

# Alias pour compatibilité - utilise maintenant le nouveau pie chart professionnel
def create_portfolio_pie_chart(portfolio):
    """Alias pour compatibilité avec l'ancien nom de fonction"""
    return create_professional_pie_chart(portfolio)
