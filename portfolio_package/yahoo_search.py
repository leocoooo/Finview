# yahoo_search.py
import yfinance as yf
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta


def search_and_display_asset(ticker_input):
    """
    Recherche un actif sur Yahoo Finance et affiche ses données
    """
    if not ticker_input:
        return None, None

    try:
        # Nettoyer le ticker (majuscules, espaces supprimés)
        ticker = ticker_input.upper().strip()

        # Créer l'objet yfinance
        asset = yf.Ticker(ticker)

        # Récupérer les informations de base
        info = asset.info

        # Vérifier si l'actif existe en récupérant des données récentes
        hist_data = asset.history(period="1mo")

        if hist_data.empty:
            st.error(
                f"❌ Aucune donnée trouvée pour le ticker '{ticker}'. Veuillez vérifier l'orthographe ou essayer un autre ticker.")
            st.info("💡 Exemples de tickers valides : AAPL, GOOGL, MSFT, ^GSPC, BTC-USD")
            return None, None

        # Récupérer plus de données pour le graphique (6 mois)
        hist_data_extended = asset.history(period="6mo")

        # Afficher les informations de l'actif
        col1, col2 = st.columns([2, 1])

        with col1:
            # Nom de l'actif
            asset_name = info.get('longName', info.get('shortName', ticker))
            st.subheader(f"📊 {asset_name} ({ticker})")

            # Prix actuel et variation
            current_price = hist_data['Close'].iloc[-1]
            previous_close = info.get('previousClose',
                                      hist_data['Close'].iloc[-2] if len(hist_data) > 1 else current_price)
            price_change = current_price - previous_close
            price_change_pct = (price_change / previous_close) * 100 if previous_close != 0 else 0

            # Affichage du prix avec couleur
            color = "green" if price_change >= 0 else "red"
            st.markdown(f"""
            **Prix actuel:** {current_price:.2f} {info.get('currency', 'USD')}  
            **Variation:** <span style="color:{color}">{price_change:+.2f} ({price_change_pct:+.2f}%)</span>
            """, unsafe_allow_html=True)

        with col2:
            # Informations supplémentaires
            market_cap = info.get('marketCap')
            if market_cap:
                st.metric("Cap. boursière", f"{market_cap / 1e9:.1f}B")

            volume = info.get('volume', hist_data['Volume'].iloc[-1] if 'Volume' in hist_data.columns else None)
            if volume:
                st.metric("Volume", f"{volume:,.0f}")

        # Graphique du cours
        create_price_chart(hist_data_extended, asset_name, ticker)

        return ticker, current_price

    except Exception as e:
        st.error(f"❌ Erreur lors de la recherche de '{ticker_input}': {str(e)}")
        st.info("💡 Veuillez vérifier que le ticker existe sur Yahoo Finance et réessayer.")
        return None, None


def create_price_chart(hist_data, asset_name, ticker):
    """
    Crée un graphique interactif du cours de l'actif
    """
    fig = go.Figure()

    # Ligne du cours de clôture
    fig.add_trace(go.Scatter(
        x=hist_data.index,
        y=hist_data['Close'],
        mode='lines',
        name='Prix de clôture',
        line=dict(color='#1f77b4', width=2)
    ))

    # Configuration du graphique
    fig.update_layout(
        title=f"Évolution du cours - {asset_name} ({ticker})",
        xaxis_title="Date",
        yaxis_title="Prix",
        hovermode='x unified',
        showlegend=False,
        height=400,
        margin=dict(l=0, r=0, t=50, b=0)
    )

    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True)


def save_asset_data(ticker, name, price, quantity=None):
    """
    Sauvegarde les données d'un actif (optionnel pour usage futur)
    """
    try:
        asset_data = {
            'ticker': ticker,
            'name': name,
            'price': price,
            'date_added': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        if quantity:
            asset_data['quantity'] = quantity

        # Ici tu peux ajouter la logique pour sauvegarder dans un fichier ou base de données
        return asset_data
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde : {str(e)}")
        return None


def asset_search_tab():
    """
    Interface de recherche d'actifs à intégrer dans les tabs
    """
    st.subheader("🔍 Rechercher un actif")

    # Barre de recherche
    ticker_input = st.text_input(
        "Entrez le ticker Yahoo Finance",
        placeholder="Ex: AAPL, GOOGL, ^GSPC, BTC-USD",
        help="Tapez le symbole de l'actif sur Yahoo Finance"
    )

    # Bouton de recherche ou recherche automatique
    col1, col2 = st.columns([1, 3])
    with col1:
        search_button = st.button("🔍 Rechercher")

    # Variables de session pour stocker les résultats
    if 'searched_ticker' not in st.session_state:
        st.session_state.searched_ticker = None
    if 'searched_price' not in st.session_state:
        st.session_state.searched_price = None

    # Recherche déclenchée par le bouton ou changement de ticker
    if search_button or (ticker_input and ticker_input != st.session_state.get('last_search', '')):
        if ticker_input:
            ticker, price = search_and_display_asset(ticker_input)
            st.session_state.searched_ticker = ticker
            st.session_state.searched_price = price
            st.session_state.last_search = ticker_input

    # Section d'ajout au portefeuille si un actif a été trouvé
    if st.session_state.searched_ticker and st.session_state.searched_price:
        st.markdown("---")
        st.subheader("➕ Ajouter au portefeuille")

        col1, col2 = st.columns(2)
        with col1:
            inv_quantity = st.number_input("Quantité", min_value=0.01, step=0.01, key="search_quantity")
        with col2:
            # Prix pré-rempli mais modifiable
            inv_price = st.number_input(
                "Prix unitaire",
                value=float(st.session_state.searched_price),
                min_value=0.01,
                step=0.01,
                key="search_price"
            )

        total_cost = inv_price * inv_quantity if inv_quantity > 0 else 0
        st.info(f"Coût total: {total_cost:.2f}€")

        if st.button("💰 Ajouter au portefeuille", type="primary"):
            # Ici tu peux appeler ta fonction d'ajout au portefeuille
            ticker = st.session_state.searched_ticker
            # Retourner les valeurs pour intégration avec ton système
            st.session_state.add_to_portfolio = {
                'name': ticker,
                'price': inv_price,
                'quantity': inv_quantity
            }
            st.success(f"Prêt à ajouter {ticker} au portefeuille!")

    return st.session_state.get('add_to_portfolio', None)