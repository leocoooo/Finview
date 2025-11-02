"""
News module - Récupération d'actualités financières via API

Ce module fournit des fonctions pour récupérer des actualités financières
depuis l'API NewsAPI en utilisant des appels curl.
"""

from .news_fetcher import fetch_financial_news, get_news_articles, format_article, format_published_date
from .news_cache import get_cached_business_news, get_cached_financial_news

__all__ = [
    'fetch_financial_news',
    'get_news_articles',
    'format_article',
    'format_published_date',
    'get_cached_business_news',
    'get_cached_financial_news'
]

__version__ = "1.0.0"
