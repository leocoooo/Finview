
import plotly.graph_objects as go


def create_professional_pie_chart(portfolio):
    """Creates a professional and readable pie chart"""

    # Professional color palette
    color_palette = {
        'cash': '#27AE60',           # Green for cash
        'financial': '#3498DB',      # Blue for financial investments
        'real_estate': '#E67E22',    # Orange for real estate
        'credits': '#E74C3C'         # Red for credits
    }

    labels = []
    values = []
    colors = []
    hover_texts = []

    # Cash
    if portfolio.cash > 0:
        labels.append('💰 Cash')
        values.append(portfolio.cash)
        colors.append(color_palette['cash'])
        hover_texts.append(f'<b>💰 Cash</b><br>Amount: {portfolio.cash:.2f}€')

    # Financial investments (grouped)
    financial_total = portfolio.get_financial_investments_value()
    if financial_total > 0:
        labels.append('📈 Financial Inv.')
        values.append(financial_total)
        colors.append(color_palette['financial'])

        # Financial investments details
        fin_details = []
        for name, inv in portfolio.financial_investments.items():
            inv_type = getattr(inv, 'investment_type', 'N/A')
            perf = inv.get_gain_loss_percentage()
            fin_details.append(f"• {name} ({inv_type}): {inv.get_total_value():.2f}€ ({perf:+.1f}%)")

        hover_text = f'<b>📈 Financial Investments</b><br>Total: {financial_total:.2f}€<br><br>' + '<br>'.join(fin_details[:5])
        if len(fin_details) > 5:
            hover_text += f'<br>... and {len(fin_details)-5} more'
        hover_texts.append(hover_text)

    # Real estate investments (grouped)
    real_estate_total = portfolio.get_real_estate_investments_value()
    if real_estate_total > 0:
        labels.append('🏠 Real Estate Inv.')
        values.append(real_estate_total)
        colors.append(color_palette['real_estate'])

        # Real estate investments details
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

        hover_text = f'<b>🏠 Real Estate Investments</b><br>Total: {real_estate_total:.2f}€'
        if total_rental_income > 0:
            hover_text += f'<br>Annual income: {total_rental_income:.2f}€'
        hover_text += '<br><br>' + '<br>'.join(re_details[:4])
        if len(re_details) > 4:
            hover_text += f'<br>... and {len(re_details)-4} more'
        hover_texts.append(hover_text)

    if not labels:
        # Empty chart
        fig = go.Figure()
        fig.add_annotation(
            text="No data to display<br>Add cash or investments",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            font=dict(size=16, color="gray"),
            showarrow=False
        )

        fig.update_layout(
            title={
                'title_font_color' : 'white',
                'text': "📊 Portfolio Distribution",
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

    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,  # Donut chart for a more modern look
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
        pull=[0.05 if i == values.index(max(values)) else 0 for i in range(len(values))]  # Highlight the largest section
    )])

    # Professional layout
    fig.update_layout(
        title={
            'text': "📊 Portfolio Distribution",
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
        # Center annotations for total
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
    """Creates a horizontal stacked bar chart for portfolio distribution"""

    # Professional color palette
    color_palette = {
        'cash': '#2E8B57',           # Dark green for cash
        'financial': '#1E90FF',      # Blue for financial investments
        'real_estate': '#FF6B35',    # Orange for real estate
        'credits': '#DC143C'         # Red for credits
    }

    # Collect data by category
    categories = []
    values = []
    colors = []
    details = []

    # Cash
    if portfolio.cash > 0:
        categories.append('💰 Cash')
        values.append(portfolio.cash)
        colors.append(color_palette['cash'])
        details.append(f'Available amount: {portfolio.cash:.2f}€')

    # Grouped financial investments
    financial_total = portfolio.get_financial_investments_value()
    if financial_total > 0:
        categories.append('📈 Financial Inv.')
        values.append(financial_total)
        colors.append(color_palette['financial'])

        # Financial investments details
        fin_details = []
        for name, inv in portfolio.financial_investments.items():
            inv_type = getattr(inv, 'investment_type', 'N/A')
            gain_loss = inv.get_gain_loss()
            perf = inv.get_gain_loss_percentage()
            fin_details.append(f"• {name} ({inv_type}): {inv.get_total_value():.2f}€ ({perf:+.1f}%)")
        details.append('<br>'.join(fin_details))

    # Grouped real estate investments
    real_estate_total = portfolio.get_real_estate_investments_value()
    if real_estate_total > 0:
        categories.append('🏠 Real Estate Inv.')
        values.append(real_estate_total)
        colors.append(color_palette['real_estate'])

        # Real estate investments details
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
                detail_text += f" - Yield: {rental_yield:.1f}%"
            if annual_income > 0:
                detail_text += f" - Income: {annual_income:.0f}€/yr"
            re_details.append(detail_text)
        details.append('<br>'.join(re_details))

    # Credits (negative values)
    credits_total = portfolio.get_total_credits_balance()
    if credits_total > 0:
        categories.append('💳 Credits')
        values.append(-credits_total)  # Negative for display
        colors.append(color_palette['credits'])

        # Credits details
        credit_details = []
        for name, credit in portfolio.credits.items():
            remaining = credit.get_remaining_balance()
            rate = credit.interest_rate
            credit_details.append(f"• {name}: -{remaining:.2f}€ (rate: {rate}%)")
        details.append('<br>'.join(credit_details))

    if not categories:
        # Empty chart if no data
        fig = go.Figure()
        fig.add_annotation(
            text="No data to display",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title="📊 Portfolio Distribution",
            height=300,
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig

    # Create horizontal stacked bar chart
    fig = go.Figure()

    total_value = sum([abs(v) for v in values])
    cumulative = 0

    for i, (cat, val, color, detail) in enumerate(zip(categories, values, colors, details)):
        percentage = (abs(val) / total_value) * 100

        # Text to display on bar
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
            hovertemplate=f'<b>{cat}</b><br>{detail}<br>Value: {abs(val):.2f}€<br>Share: {percentage:.1f}%<extra></extra>',
            showlegend=True
        ))

    # Layout configuration
    fig.update_layout(
        title={
            'text': "📊 Portfolio Distribution",
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

        # Axes configuration
        xaxis=dict(
            title="Value (€)",
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            tickformat='.0f',
            ticksuffix='€'
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False
        ),

        # Legend
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
    """Creates an investment performance chart"""

    # Collect performance data
    financial_data = []
    real_estate_data = []

    # Financial investments
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

    # Real estate investments
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
            text="No investments to analyze",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title="📈 Investment Performance",
            height=300,
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig

    fig = go.Figure()

    # Add financial investments
    if financial_data:
        names_fin = [d['name'] for d in financial_data]
        perfs_fin = [d['performance'] for d in financial_data]
        values_fin = [d['value'] for d in financial_data]
        types_fin = [d['type'] for d in financial_data]

        fig.add_trace(go.Bar(
            x=names_fin,
            y=perfs_fin,
            name='📈 Financial',
            marker_color='#1E90FF',
            hovertemplate='<b>%{x}</b><br>Type: %{customdata}<br>Performance: %{y:+.1f}%<br>Value: %{text:.2f}€<extra></extra>',
            customdata=types_fin,
            text=values_fin
        ))

    # Add real estate investments
    if real_estate_data:
        names_re = [d['name'] for d in real_estate_data]
        perfs_re = [d['performance'] for d in real_estate_data]
        values_re = [d['value'] for d in real_estate_data]
        types_re = [d['type'] for d in real_estate_data]

        fig.add_trace(go.Bar(
            x=names_re,
            y=perfs_re,
            name='🏠 Real Estate',
            marker_color='#FF6B35',
            hovertemplate='<b>%{x}</b><br>Type: %{customdata}<br>Performance: %{y:+.1f}%<br>Value: %{text:.2f}€<extra></extra>',
            customdata=types_re,
            text=values_re
        ))

    # Reference line at 0%
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

    # Configuration
    fig.update_layout(
        title={
            'text': "📈 Investment Performance",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'family': 'Arial, sans-serif', 'color': '#2c3e50'}
        },
        xaxis_title="Investments",
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

    # Rotate X-axis labels if necessary
    if len(financial_data) + len(real_estate_data) > 6:
        fig.update_xaxes(tickangle=45)

    return fig

def create_world_investment_map(portfolio):
    """Creates an interactive world map of investments"""

    # Geolocation dictionary for investments
    location_coordinates = {
        # Countries
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

        # Major cities
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

        # Regions
        'europe': {'lat': 54.5260, 'lon': 15.2551, 'country': 'Europe'},
        'asie': {'lat': 34.0479, 'lon': 100.6197, 'country': 'Asie'},
        'amérique du nord': {'lat': 54.5260, 'lon': -105.2551, 'country': 'Amérique du Nord'},
        'amérique latine': {'lat': -8.7832, 'lon': -55.4915, 'country': 'Amérique Latine'},
    }

    # Collect investment data with location
    investment_data = []

    # Financial investments
    for name, inv in portfolio.financial_investments.items():
        inv_type = getattr(inv, 'investment_type', 'Financial')
        location = getattr(inv, 'location', '')

        # Attempt geolocation based on name or other clues
        coords = None
        if location:
            location_lower = location.lower().strip()
            coords = location_coordinates.get(location_lower)

        # If no explicit location, try to guess from name
        if not coords:
            name_lower = name.lower()
            for loc_key, loc_data in location_coordinates.items():
                if loc_key in name_lower:
                    coords = loc_data
                    break

        # Default location for global financial investments
        if not coords:
            if 'sp' in name_lower or 's&p' in name_lower or 'nasdaq' in name_lower:
                coords = location_coordinates['états-unis']
            elif 'europe' in name_lower or 'eur' in name_lower:
                coords = location_coordinates['europe']
            elif 'world' in name_lower or 'global' in name_lower or 'msci' in name_lower:
                coords = location_coordinates['états-unis']  # Default
            else:
                coords = location_coordinates['france']  # Local default

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
                'size': max(10, min(50, inv.get_total_value() / 100))  # Proportional size
            })

    # Real estate investments
    for name, inv in portfolio.real_estate_investments.items():
        property_type = getattr(inv, 'property_type', 'Real Estate')
        location = getattr(inv, 'location', 'France')
        rental_yield = getattr(inv, 'rental_yield', 0)

        # Geolocation for real estate
        coords = None
        if location:
            location_lower = location.lower().strip()
            coords = location_coordinates.get(location_lower)

        # Default location
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
            'size': max(15, min(60, inv.get_total_value() / 80))  # Slightly larger size
        })

    if not investment_data:
        # Empty map
        fig = go.Figure()
        fig.add_annotation(
            text="No located investments to display<br>Add investments with locations",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            font=dict(size=16, color="gray"),
            showarrow=False
        )
        fig.update_layout(
            title="🌍 World Investment Map",
            height=400,
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig

    # Create the map
    fig = go.Figure()

    # Add financial investments
    financial_data = [inv for inv in investment_data if inv['type'] == 'Financial']
    if financial_data:
        fig.add_trace(go.Scattergeo(
            lon=[inv['lon'] for inv in financial_data],
            lat=[inv['lat'] for inv in financial_data],
            text=[f"<b>{inv['name']}</b><br>{inv['category']}<br>{inv['value']:.0f}€<br>{inv['performance']:+.1f}%"
                  for inv in financial_data],
            mode='markers',
            name='📈 Financial Investments',
            marker=dict(
                size=[inv['size'] for inv in financial_data],
                color='#3498DB',
                sizemode='diameter',
                line=dict(width=2, color='white'),
                opacity=0.8
            ),
            hovertemplate='<b>%{text}</b><br>Country: %{customdata}<extra></extra>',
            customdata=[inv['country'] for inv in financial_data]
        ))

    # Add real estate investments
    real_estate_data = [inv for inv in investment_data if inv['type'] == 'Real Estate']
    if real_estate_data:
        fig.add_trace(go.Scattergeo(
            lon=[inv['lon'] for inv in real_estate_data],
            lat=[inv['lat'] for inv in real_estate_data],
            text=[f"<b>{inv['name']}</b><br>{inv['category']}<br>{inv['value']:.0f}€<br>Yield: {inv.get('rental_yield', 0):.1f}%<br>{inv['performance']:+.1f}%"
                  for inv in real_estate_data],
            mode='markers',
            name='🏠 Real Estate Investments',
            marker=dict(
                size=[inv['size'] for inv in real_estate_data],
                color='#E67E22',
                sizemode='diameter',
                line=dict(width=2, color='white'),
                opacity=0.8,
                symbol='square'  # Square to differentiate from financial
            ),
            hovertemplate='<b>%{text}</b><br>Location: %{customdata}<extra></extra>',
            customdata=[inv['location_name'] for inv in real_estate_data]
        ))

    # Map configuration
    fig.update_layout(
        title={
            'text': "🌍 World Investment Map",
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

# Alias for compatibility - now uses the new professional pie chart
def create_portfolio_pie_chart(portfolio):
    """Alias for compatibility with old function name"""
    return create_professional_pie_chart(portfolio)
