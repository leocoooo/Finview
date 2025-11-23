"""
Récupération d'actualités financières via l'API NewsAPI
Utilise des appels curl via subprocess plutot que request (contrainte ?)
"""

import json
from typing import Dict, Optional
from datetime import datetime


def get_news_articles_from_file(file_path: str = "saved_json_data/news.json") -> Optional[Dict]:
    """
    Lit les actualités depuis un fichier JSON généré par le script bash
    Args:
        file_path: Chemin du fichier JSON
    Returns:
        Dict contenant les articles ou None en cas d'erreur
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if data.get('status') != 'ok':
            print(f"Erreur API: {data.get('message', 'Erreur inconnue')}")
            return None
        return data
    except FileNotFoundError:
        print(f"Fichier non trouvé: {file_path}")
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
