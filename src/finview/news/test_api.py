"""
Script de test pour vérifier que l'API NewsAPI fonctionne
Lance ce script pour tester : python -m src.finview.news.test_api
"""

import os
from dotenv import load_dotenv
from news_fetcher import fetch_financial_news, get_news_articles, format_article

# Charger les variables d'environnement
load_dotenv()

def test_api():
    """Test de base de l'API"""
    api_key = os.getenv('NEWS_API_KEY')
    
    if not api_key:
        print("❌ Erreur: NEWS_API_KEY non trouvée dans .env")
        return
    
    print("🔑 Clé API chargée")
    print(f"   Longueur: {len(api_key)} caractères")
    print()
    
    # Test 1: Top headlines business
    print("📰 Test 1: Top headlines business (US)")
    print("-" * 50)
    
    result = get_news_articles(
        api_key=api_key,
        category="business",
        country="us",
        page_size=3
    )
    
    if result:
        print(f"✅ Succès! {result.get('totalResults', 0)} articles disponibles")
        print(f"   Articles récupérés: {len(result.get('articles', []))}")
        print()
        
        # Afficher les 3 premiers titres
        for i, article in enumerate(result.get('articles', [])[:3], 1):
            formatted = format_article(article)
            print(f"{i}. {formatted['title']}")
            print(f"   Source: {formatted['source']}")
            print(f"   Date: {formatted['published_at']}")
            print()
    else:
        print("❌ Échec de la récupération")
    
    print()
    print("=" * 50)
    print()
    
    # Test 2: Recherche avec mots-clés
    print("📰 Test 2: Recherche 'stock market'")
    print("-" * 50)
    
    result2 = fetch_financial_news(
        api_key=api_key,
        query="stock market",
        language="en",
        page_size=3
    )
    
    if result2:
        print(f"✅ Succès! {result2.get('totalResults', 0)} articles trouvés")
        print(f"   Articles récupérés: {len(result2.get('articles', []))}")
        print()
        
        for i, article in enumerate(result2.get('articles', [])[:3], 1):
            formatted = format_article(article)
            print(f"{i}. {formatted['title']}")
            print(f"   Source: {formatted['source']}")
            print()
    else:
        print("❌ Échec de la récupération")

if __name__ == "__main__":
    test_api()
