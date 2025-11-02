"""
Interface utilisateur Streamlit pour la recherche d'actifs
"""
import streamlit as st
from datetime import datetime
from typing import Optional, Dict, Any
from .asset_search import search_asset, get_asset_info, get_asset_history, get_ticker_suggestions
from .asset_display import create_price_chart, format_asset_info


def display_asset_info(info: Dict[str, Any]):
    """
    Affiche les informations d'un actif dans Streamlit
    
    Args:
        info: Dictionnaire d'informations de l'actif
    """
    formatted = format_asset_info(info)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Nom et ticker
        st.subheader(f"📊 {info.get('name', 'N/A')} ({info.get('ticker', 'N/A')})")
        
        # Prix et variation
        if 'price' in formatted:
            st.markdown(f"**Prix actuel:** {formatted['price']}")
        
        if 'change' in formatted:
            color = formatted.get('change_color', 'gray')
            st.markdown(
                f"**Variation:** <span style='color:{color}'>{formatted['change']}</span>",
                unsafe_allow_html=True
            )
    
    with col2:
        # Métriques supplémentaires
        if 'market_cap' in formatted:
            st.metric("Cap. boursière", formatted['market_cap'])
        
        if 'volume' in formatted:
            st.metric("Volume", formatted['volume'])
    
    # Informations sectorielles
    if 'sector' in formatted or 'industry' in formatted:
        st.caption(
            f"{formatted.get('sector', 'N/A')} • {formatted.get('industry', 'N/A')}"
        )


def display_ticker_suggestions():
    """
    Affiche des suggestions de tickers valides
    """
    with st.expander("💡 Examples of Tickers"):
        suggestions = get_ticker_suggestions()
        
        cols = st.columns(2)
        items = list(suggestions.items())
        mid = len(items) // 2
        
        with cols[0]:
            for category, tickers in items[:mid]:
                st.write(f"**{category}:**")
                st.write(", ".join(tickers))
                st.write("")
        
        with cols[1]:
            for category, tickers in items[mid:]:
                st.write(f"**{category}:**")
                st.write(", ".join(tickers))
                st.write("")


def asset_search_tab() -> Optional[Dict[str, Any]]:
    """
    Interface de recherche d'actifs avec possibilité d'ajout au portfolio
    
    Returns:
        dict: Informations de l'actif à ajouter au portfolio, ou None
    """
    st.subheader("🔍 Search an asset")
    
    # Initialiser les variables de session
    if 'searched_ticker' not in st.session_state:
        st.session_state.searched_ticker = None
    if 'searched_asset_info' not in st.session_state:
        st.session_state.searched_asset_info = None
    if 'last_search' not in st.session_state:
        st.session_state.last_search = ''
    
    # Barre de recherche
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ticker_input = st.text_input(
            "Enter Yahoo Finance ticker",
            placeholder="Ex: AAPL, GOOGL, ^GSPC, BTC-USD",
            help="Type the asset symbol on Yahoo Finance",
            key="ticker_search_input"
        )
    
    with col2:
        st.write("")  # Espaceur
        st.write("")  # Espaceur
        search_button = st.button("🔍 Search", width='stretch')
    
    # Afficher les suggestions
    display_ticker_suggestions()
    
    # Déclencher la recherche
    if search_button or (ticker_input and ticker_input != st.session_state.last_search):
        if ticker_input:
            with st.spinner(f"Searching for {ticker_input}..."):
                asset = search_asset(ticker_input)
                
                if asset is None:
                    st.error(
                        f"❌ No data found for ticker '{ticker_input.upper()}'. "
                        "Please check the spelling or try another ticker."
                    )
                    st.session_state.searched_ticker = None
                    st.session_state.searched_asset_info = None
                else:
                    # Récupérer les informations
                    info = get_asset_info(asset)
                    
                    if not info:
                        st.error("❌ Unable to retrieve asset information")
                        st.session_state.searched_ticker = None
                        st.session_state.searched_asset_info = None
                    else:
                        # Sauvegarder dans la session
                        st.session_state.searched_ticker = info['ticker']
                        st.session_state.searched_asset_info = info
                        
                        # Afficher les informations
                        display_asset_info(info)
                        
                        # Récupérer et afficher le graphique
                        hist_data, error = get_asset_history(info['ticker'], period="6mo")
                        
                        if hist_data is not None and not hist_data.empty:
                            fig = create_price_chart(hist_data, info['name'], info['ticker'])
                            st.plotly_chart(fig)
                        elif error:
                            st.warning(f"⚠️ {error}")
            
            st.session_state.last_search = ticker_input
    
    # Section d'ajout au portfolio si un actif a été trouvé
    if st.session_state.searched_ticker and st.session_state.searched_asset_info:
        st.markdown("---")
        st.subheader("➕ Add to portfolio")
        
        info = st.session_state.searched_asset_info
        
        col1, col2 = st.columns(2)
        
        with col1:
            inv_quantity = st.number_input(
                "Quantity",
                min_value=0.0001,
                value=1.0,
                step=0.01,
                key="search_quantity",
                help="Number of units to buy"
            )
        
        with col2:
            inv_price = st.number_input(
                "Unit Price",
                value=float(info['current_price']),
                min_value=0.01,
                step=0.01,
                key="search_price",
                help="Price per unit (pre-filled with current price)"
            )
        
        # Type d'investissement
        investment_type = st.selectbox(
            "Investment Type",
            options=["Stock", "ETF", "Crypto", "Bond", "Index", "Commodity", "Other"],
            index=0,
            key="search_inv_type"
        )
        
        # Calcul du coût total
        total_cost = inv_price * inv_quantity if inv_quantity > 0 else 0

        st.info(f"💰 **Total Cost:** {total_cost:.2f} {info.get('currency', 'USD')}")

        # Add button
        if st.button("✅ Add to Portfolio", type="primary", width='stretch'):
            # Create return dictionary
            return {
                'name': info['name'],
                'ticker': info['ticker'],
                'price': inv_price,
                'quantity': inv_quantity,
                'investment_type': investment_type,
                'currency': info.get('currency', 'USD'),
                'added_at': datetime.now()
            }
    
    return None


def quick_search_widget(key_suffix: str = "") -> Optional[str]:
    """
    Widget de recherche rapide sans affichage complet
    
    Args:
        key_suffix: Suffixe pour les clés Streamlit (pour éviter les doublons)
        
    Returns:
        str: Ticker trouvé, ou None
    """
    ticker_input = st.text_input(
        "Ticker",
        placeholder="Ex: AAPL",
        key=f"quick_search_{key_suffix}"
    )
    
    if ticker_input:
        asset = search_asset(ticker_input)
        if asset:
            info = get_asset_info(asset)
            if info:
                st.success(f"✅ {info['name']} - {info['current_price']:.2f} {info.get('currency', 'USD')}")
                return info['ticker']
        else:
            st.error("❌ Ticker not found")
    
    return None
