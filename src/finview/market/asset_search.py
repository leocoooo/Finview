"""
Fonctions de recherche et récupération de données d'actifs financiers
"""
import yfinance as yf
from typing import Optional, Dict, Any, Tuple
import pandas as pd


def search_asset(ticker: str) -> Optional[yf.Ticker]:
    """
    Recherche un actif sur Yahoo Finance
    
    Args:
        ticker: Symbole du ticker (ex: AAPL, GOOGL, BTC-USD)
        
    Returns:
        yf.Ticker si l'actif est trouvé, None sinon
        
    Raises:
        ValueError: Si le ticker est vide
    """
    if not ticker or not ticker.strip():
        raise ValueError("Le ticker ne peut pas être vide")
    
    # Nettoyer le ticker (majuscules, espaces supprimés)
    clean_ticker = ticker.upper().strip()
    
    try:
        asset = yf.Ticker(clean_ticker)
        
        # Vérifier que l'actif existe en récupérant des données récentes
        hist = asset.history(period="5d")
        
        if hist.empty:
            return None
        
        return asset
    
    except Exception as e:
        print(f"Erreur lors de la recherche de {clean_ticker}: {e}")
        return None


def get_asset_info(asset: yf.Ticker) -> Dict[str, Any]:
    """
    Récupère les informations détaillées d'un actif
    
    Args:
        asset: Objet yf.Ticker
        
    Returns:
        dict: Informations de l'actif
    """
    try:
        info = asset.info
        hist = asset.history(period="1mo")
        
        if hist.empty:
            return {}
        
        current_price = hist['Close'].iloc[-1]
        previous_close = info.get('previousClose', hist['Close'].iloc[-2] if len(hist) > 1 else current_price)
        
        price_change = current_price - previous_close
        price_change_pct = (price_change / previous_close) * 100 if previous_close != 0 else 0
        
        return {
            'ticker': asset.ticker,
            'name': info.get('longName', info.get('shortName', asset.ticker)),
            'current_price': float(current_price),
            'previous_close': float(previous_close),
            'price_change': float(price_change),
            'price_change_pct': float(price_change_pct),
            'currency': info.get('currency', 'USD'),
            'market_cap': info.get('marketCap'),
            'volume': info.get('volume', hist['Volume'].iloc[-1] if 'Volume' in hist.columns else None),
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'description': info.get('longBusinessSummary', '')
        }
    
    except Exception as e:
        print(f"Erreur lors de la récupération des informations: {e}")
        return {}


def get_asset_history(ticker: str, period: str = "6mo") -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Récupère l'historique des prix d'un actif
    
    Args:
        ticker: Symbole du ticker
        period: Période d'historique (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        
    Returns:
        tuple: (DataFrame d'historique, message d'erreur si échec)
    """
    valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    
    if period not in valid_periods:
        return None, f"Période invalide. Périodes valides: {', '.join(valid_periods)}"
    
    try:
        asset = yf.Ticker(ticker)
        hist = asset.history(period=period)
        
        if hist.empty:
            return None, f"Aucune donnée historique disponible pour {ticker}"
        
        return hist, None
    
    except Exception as e:
        return None, f"Erreur lors de la récupération de l'historique: {str(e)}"


def validate_ticker(ticker: str) -> Tuple[bool, Optional[str]]:
    """
    Valide un ticker Yahoo Finance
    
    Args:
        ticker: Symbole du ticker à valider
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not ticker or not ticker.strip():
        return False, "Le ticker ne peut pas être vide"
    
    clean_ticker = ticker.upper().strip()
    
    # Vérifier le format basique
    if len(clean_ticker) > 10:
        return False, "Le ticker ne peut pas dépasser 10 caractères"
    
    # Tenter de récupérer l'actif
    asset = search_asset(clean_ticker)
    
    if asset is None:
        return False, f"Ticker '{clean_ticker}' introuvable sur Yahoo Finance"
    
    return True, None


def get_ticker_suggestions() -> Dict[str, str]:
    """
    Retourne des exemples de tickers valides par catégorie
    
    Returns:
        dict: Catégorie -> liste de tickers exemples
    """
    return {
        'US Stocks': ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'NVDA'],
        'French Stocks': ['MC.PA', 'OR.PA', 'SAN.PA', 'AIR.PA'],
        'Indices': ['^GSPC', '^DJI', '^IXIC', '^FCHI'],
        'Cryptos': ['BTC-USD', 'ETH-USD', 'BNB-USD'],
        'ETFs': ['SPY', 'QQQ', 'VOO', 'VTI'],
        'Raw Materials': ['GC=F', 'SI=F', 'CL=F']
    }
