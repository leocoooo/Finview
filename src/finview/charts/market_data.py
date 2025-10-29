"""
Récupération de données de marché via yfinance
"""
import yfinance as yf
import streamlit as st
from typing import Tuple, Optional


def get_cac40_data() -> Tuple[float, float]:
    """
    Récupère les données du CAC40
    
    Returns:
        tuple: (valeur_actuelle, variation_pourcentage)
    """
    ticker = yf.Ticker("^FCHI")
    hist = ticker.history(period="5d")
    current_value = hist['Close'].iloc[-1]
    previous_value = hist['Close'].iloc[-2]
    change = ((current_value - previous_value) / previous_value) * 100
    return current_value, change


def get_dji_data() -> Tuple[float, float]:
    """
    Récupère les données du Dow Jones Industrial Average
    
    Returns:
        tuple: (valeur_actuelle, variation_pourcentage)
    """
    try:
        ticker = yf.Ticker("^DJI")
        hist = ticker.history(period="5d")
        if len(hist) >= 2:
            current_value = hist['Close'].iloc[-1]
            previous_value = hist['Close'].iloc[-2]
            change = ((current_value - previous_value) / previous_value) * 100
            return current_value, change
        return 6744.0, 0.0
    except Exception:
        return 6744.0, 0.0


def get_btc_data() -> Tuple[float, float]:
    """
    Récupère les données du Bitcoin
    
    Returns:
        tuple: (valeur_actuelle, variation_pourcentage)
    """
    try:
        ticker = yf.Ticker("BTC-USD")
        hist = ticker.history(period="5d")
        if len(hist) >= 2:
            current_value = hist['Close'].iloc[-1]
            previous_value = hist['Close'].iloc[-2]
            change = ((current_value - previous_value) / previous_value) * 100
            return current_value, change
        return 125512.0, 0.0
    except Exception:
        return 125512.0, 0.0


def get_benchmark_data(ticker: str, period: str = "5d") -> Tuple[Optional[float], float]:
    """
    Récupère les données d'un benchmark
    
    Args:
        ticker: Le ticker Yahoo Finance
        period: Période de récupération (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
    
    Returns:
        tuple: (valeur_actuelle, variation_pourcentage)
    """
    try:
        ticker_obj = yf.Ticker(ticker)
        hist = ticker_obj.history(period=period)
        if len(hist) >= 2:
            current_value = hist['Close'].iloc[-1]
            previous_value = hist['Close'].iloc[-2]
            change = ((current_value - previous_value) / previous_value) * 100
            return current_value, change
        return None, 0.0
    except Exception as e:
        print(f"Erreur lors de la récupération de {ticker}: {e}")
        return None, 0.0


def create_benchmark_kpi_card(benchmark_name: str, ticker: str):
    """
    Crée une carte KPI pour un benchmark dans Streamlit
    
    Args:
        benchmark_name: Nom du benchmark à afficher
        ticker: Ticker Yahoo Finance
    """
    current_value, change = get_benchmark_data(ticker)
    
    if current_value:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.metric(
                label=benchmark_name,
                value=f"{current_value:,.2f}",
                delta=f"{change:+.2f}%"
            )


def create_kpi_metrics(portfolio):
    """
    Calcule les métriques KPI pour le dashboard
    
    Args:
        portfolio: Instance de Portfolio
        
    Returns:
        dict: Dictionnaire des KPIs calculés
    """
    net_worth = portfolio.get_net_worth()

    # Calcul de la variation des investissements
    financial_investments = getattr(portfolio, "financial_investments", {})
    total_invested = sum(inv.quantity * inv.initial_value for inv in financial_investments.values())
    current_value = sum(inv.get_total_value() for inv in financial_investments.values())
    investment_change = ((current_value - total_invested) / total_invested * 100) if total_invested > 0 else 0

    # Crédits
    total_credits = portfolio.get_total_credits_balance()

    return {
        'net_worth': net_worth,
        'investment_value': current_value,
        'investment_change': investment_change,
        'total_credits': total_credits
    }
