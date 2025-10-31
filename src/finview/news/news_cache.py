"""
Cache pour les actualités financières
Évite d'appeler l'API trop souvent
"""

import streamlit as st
from typing import Dict, Optional
from .news_fetcher import get_news_articles, fetch_financial_news


@st.cache_data(ttl=1800)  # Cache de 30 minutes
def get_cached_business_news(api_key: str, country: str = "us", page_size: int = 10) -> Optional[Dict]:
    """
    Récupère les actualités business avec cache
    
    Args:
        api_key: Clé API NewsAPI
        country: Code pays (us, fr, gb)
        page_size: Nombre d'articles
        
    Returns:
        Données de l'API ou None
    """
    return get_news_articles(
        api_key=api_key,
        category="business",
        country=country,
        page_size=page_size
    )


@st.cache_data(ttl=1800)  # Cache de 30 minutes
def get_cached_financial_news(api_key: str, query: str, language: str = "en", page_size: int = 10) -> Optional[Dict]:
    """
    Récupère les actualités par recherche avec cache
    
    Args:
        api_key: Clé API NewsAPI
        query: Mots-clés de recherche
        language: Langue
        page_size: Nombre d'articles
        
    Returns:
        Données de l'API ou None
    """
    # Remplacer les espaces par + pour éviter les erreurs curl
    query_formatted = query.replace(" ", "+")
    
    return fetch_financial_news(
        api_key=api_key,
        query=query_formatted,
        language=language,
        page_size=page_size
    )
