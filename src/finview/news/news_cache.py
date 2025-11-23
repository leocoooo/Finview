"""
Cache pour les actualités financières
Évite d'appeler l'API trop souvent
"""

import streamlit as st
from typing import Dict, Optional
from .news_fetcher import get_news_articles_from_file


@st.cache_data(ttl=1800)  # Cache de 30 minutes
def get_cached_business_news(file_path: str = "saved_json_data/news.json") -> Optional[Dict]:
    """
    Récupère les actualités business depuis le fichier JSON avec cache
    Args:
        file_path: Chemin du fichier JSON
    Returns:
        Données de l'API ou None
    """
    return get_news_articles_from_file(file_path=file_path)
