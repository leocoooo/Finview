"""
Récupération d'actualités financières via l'API NewsAPI
Utilise des appels curl pour respecter les contraintes académiques
"""

import subprocess
import json
from typing import Dict, Optional
from datetime import datetime


def fetch_financial_news(
    api_key: str,
    query: str = "finance OR stock OR market OR economy",
    language: str = "en",
    page_size: int = 10,
    sort_by: str = "publishedAt"
) -> Optional[Dict]:
    """
    Récupère les actualités financières via l'API NewsAPI en utilisant curl
    
    Args:
        api_key: Clé API NewsAPI
        query: Requête de recherche (par défaut : actualités financières)
        language: Langue des articles (en, fr, etc.)
        page_size: Nombre d'articles à récupérer (max 100)
        sort_by: Tri (publishedAt, relevancy, popularity)
        
    Returns:
        Dict contenant les articles ou None en cas d'erreur
        
    Raises:
        ValueError: Si la clé API est vide
    """
    if not api_key or api_key.strip() == "":
        raise ValueError("La clé API NewsAPI est requise")
    
    # Construction de l'URL de l'API
    # Utilisation de l'endpoint 'everything' pour plus de flexibilité
    base_url = "https://newsapi.org/v2/everything"
    
    # Paramètres de la requête
    params = [
        f"q={query}",
        f"language={language}",
        f"pageSize={page_size}",
        f"sortBy={sort_by}",
        f"apiKey={api_key}"
    ]
    
    # URL complète
    url = f"{base_url}?{'&'.join(params)}"
    
    try:
        # Appel curl via subprocess
        result = subprocess.run(
            ['curl', '-s', url],  # -s pour silent (pas de barre de progression)
            capture_output=True,
            text=True,
            timeout=10  # Timeout de 10 secondes
        )
        
        # Vérifier le code de retour
        if result.returncode != 0:
            print(f"Erreur curl: code {result.returncode}")
            return None
        
        # Parser la réponse JSON
        data = json.loads(result.stdout)
        
        # Vérifier le statut de la réponse
        if data.get('status') != 'ok':
            print(f"Erreur API: {data.get('message', 'Erreur inconnue')}")
            return None
        
        return data
        
    except subprocess.TimeoutExpired:
        print("Timeout: l'API a mis trop de temps à répondre")
        return None
    except json.JSONDecodeError:
        print("Erreur: impossible de parser la réponse JSON")
        return None
    except Exception as e:
        print(f"Erreur inattendue: {str(e)}")
        return None


def get_news_articles(
    api_key: str,
    category: str = "business",
    country: str = "us",
    page_size: int = 10
) -> Optional[Dict]:
    """
    Récupère les top headlines d'une catégorie spécifique
    
    Args:
        api_key: Clé API NewsAPI
        category: Catégorie (business, technology, science, etc.)
        country: Code pays (us, fr, gb, etc.)
        page_size: Nombre d'articles à récupérer
        
    Returns:
        Dict contenant les articles ou None en cas d'erreur
    """
    if not api_key or api_key.strip() == "":
        raise ValueError("La clé API NewsAPI est requise")
    
    # URL pour les top headlines
    base_url = "https://newsapi.org/v2/top-headlines"
    
    # Paramètres
    params = [
        f"category={category}",
        f"country={country}",
        f"pageSize={page_size}",
        f"apiKey={api_key}"
    ]
    
    url = f"{base_url}?{'&'.join(params)}"
    
    try:
        result = subprocess.run(
            ['curl', '-s', url],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            print(f"Erreur curl: code {result.returncode}")
            return None
        
        data = json.loads(result.stdout)
        
        if data.get('status') != 'ok':
            print(f"Erreur API: {data.get('message', 'Erreur inconnue')}")
            return None
        
        return data
        
    except subprocess.TimeoutExpired:
        print("Timeout: l'API a mis trop de temps à répondre")
        return None
    except json.JSONDecodeError:
        print("Erreur: impossible de parser la réponse JSON")
        return None
    except Exception as e:
        print(f"Erreur inattendue: {str(e)}")
        return None


def format_article(article: Dict) -> Dict[str, str]:
    """
    Formate un article pour l'affichage
    
    Args:
        article: Article brut de l'API
        
    Returns:
        Article formaté avec les champs nécessaires
    """
    return {
        'title': article.get('title', 'No title'),
        'description': article.get('description', 'No description available'),
        'url': article.get('url', '#'),
        'source': article.get('source', {}).get('name', 'Unknown source'),
        'author': article.get('author', 'Unknown author'),
        'published_at': article.get('publishedAt', ''),
        'image_url': article.get('urlToImage', ''),
        'content': article.get('content', '')
    }


def format_published_date(date_str: str) -> str:
    """
    Formate la date de publication
    
    Args:
        date_str: Date au format ISO (2025-10-31T10:00:00Z)
        
    Returns:
        Date formatée (October 31, 2025)
    """
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        
        # Month names in English
        months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        
        return f"{months[dt.month - 1]} {dt.day}, {dt.year}"
    except Exception:
        return date_str
