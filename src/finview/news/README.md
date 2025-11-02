# Module News - Actualités Financières

## 📰 Description

Le module `news` fournit une interface complète pour récupérer et afficher des actualités financières en temps réel via l'API NewsAPI. Il inclut également un calendrier des résultats financiers et un affichage des indices boursiers.

## 🎯 Fonctionnalités

### 1. Récupération d'actualités via NewsAPI

- **Top Headlines** : Actualités principales par catégorie et pays
- **Recherche personnalisée** : Recherche par mots-clés avec filtres
- **Cache intelligent** : Optimisation des appels API (30 minutes)
- **Formatage automatique** : Articles structurés avec métadonnées

### 2. Calendrier des résultats financiers

- **Entreprises françaises** : CAC 40, SBF 120 (40+ entreprises)
- **Entreprises internationales** : US, Europe, Asie (100+ entreprises)
- **Recherche** : Filtrage par nom d'entreprise
- **Années 2025 et 2026** : Données prévisionnelles

### 3. Indices boursiers en temps réel

- Principaux indices mondiaux (S&P 500, CAC 40, NASDAQ, etc.)
- Cryptomonnaies (Bitcoin, Ethereum)
- Variation en temps réel avec yfinance

## 📦 Structure du module

```
news/
├── __init__.py              # Exports publics
├── news_fetcher.py          # Fonctions de récupération NewsAPI
├── news_cache.py            # Système de cache Streamlit
├── test_api.py              # Tests de l'API
└── README.md                # Cette documentation
```

## 🔧 Installation et Configuration

### 1. Obtenir une clé API NewsAPI

1. Créer un compte gratuit sur [newsapi.org](https://newsapi.org/)
2. Copier votre clé API (format : `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)

### 2. Configurer la variable d'environnement

Créer un fichier `.env` à la racine du projet :

```bash
NEWS_API_KEY=votre_cle_api_ici
```

### 3. Installer les dépendances

Les dépendances sont gérées par Poetry :

```bash
poetry install
```

Packages requis :
- `python-dotenv` : Gestion des variables d'environnement
- `streamlit` : Cache et interface utilisateur

## 💻 Utilisation

### API de base

```python
from src.finview.news import fetch_financial_news, get_news_articles

# Top headlines business (US)
news = get_news_articles(
    api_key="YOUR_API_KEY",
    category="business",
    country="us",
    page_size=10
)

# Recherche personnalisée
finance_news = fetch_financial_news(
    api_key="YOUR_API_KEY",
    query="stock market OR finance",
    language="en",
    page_size=10,
    sort_by="publishedAt"  # ou "relevancy", "popularity"
)

# Vérifier le statut
if news and news.get('status') == 'ok':
    articles = news['articles']
    print(f"Récupéré {len(articles)} articles")
```

### Avec cache Streamlit (recommandé)

```python
from src.finview.news import get_cached_business_news

# Cache automatique de 30 minutes
news_data = get_cached_business_news(
    api_key="YOUR_API_KEY",
    country="us",
    page_size=10
)
```

### Formatage des articles

```python
from src.finview.news import format_article, format_published_date

if news_data:
    for article_raw in news_data['articles']:
        article = format_article(article_raw)
        
        # Accès aux champs formatés
        print(f"Titre: {article['title']}")
        print(f"Source: {article['source']}")
        print(f"Auteur: {article['author']}")
        print(f"URL: {article['url']}")
        print(f"Image: {article['image_url']}")
        
        # Date formatée
        date = format_published_date(article['published_at'])
        print(f"Publié le: {date}")
```

## 🔍 Référence des fonctions

### `fetch_financial_news()`

Récupère des actualités via l'endpoint `everything` de NewsAPI.

**Paramètres :**
- `api_key` (str) : Clé API NewsAPI *(requis)*
- `query` (str) : Requête de recherche (défaut : "finance OR stock OR market OR economy")
- `language` (str) : Code langue ISO (défaut : "en")
- `page_size` (int) : Nombre d'articles (1-100, défaut : 10)
- `sort_by` (str) : Tri ("publishedAt", "relevancy", "popularity")

**Retour :** `Dict | None`

```json
{
  "status": "ok",
  "totalResults": 42,
  "articles": [...]
}
```

### `get_news_articles()`

Récupère les top headlines par catégorie et pays.

**Paramètres :**
- `api_key` (str) : Clé API NewsAPI *(requis)*
- `category` (str) : Catégorie ("business", "technology", "science", etc.)
- `country` (str) : Code pays ISO (défaut : "us")
- `page_size` (int) : Nombre d'articles (1-100, défaut : 10)

**Retour :** `Dict | None`

### `get_cached_business_news()`

Version avec cache de `get_news_articles()` optimisée pour Streamlit.

**Cache :** 30 minutes (`ttl=1800`)

### `format_article()`

Formate un article brut en structure standardisée.

**Paramètres :**
- `article` (Dict) : Article brut de l'API

**Retour :** `Dict[str, str]`

```python
{
    'title': str,
    'description': str,
    'url': str,
    'source': str,
    'author': str,
    'published_at': str,  # Format ISO
    'image_url': str,
    'content': str
}
```

### `format_published_date()`

Convertit une date ISO en format lisible.

**Entrée :** `"2025-10-31T10:00:00Z"`  
**Sortie :** `"October 31, 2025"`

## 🚀 Exemples avancés

### Recherche multi-critères

```python
# Actualités sur Tesla et Apple
news = fetch_financial_news(
    api_key=api_key,
    query="(Tesla OR Apple) AND earnings",
    language="en",
    page_size=20,
    sort_by="relevancy"
)
```

### Gestion d'erreurs

```python
from src.finview.news import get_news_articles

try:
    news = get_news_articles(api_key="", category="business")
except ValueError as e:
    print(f"Erreur de validation: {e}")

if news is None:
    print("Erreur API : timeout ou quota dépassé")
elif news.get('status') != 'ok':
    print(f"Erreur API: {news.get('message')}")
```

### Test rapide de l'API

Utilisez le script de test inclus :

```bash
cd src/finview/news
python test_api.py
```

Ce script :
- Charge la clé API depuis `.env`
- Teste les deux endpoints
- Affiche les 3 premiers articles
- Vérifie le formatage

## 📊 Interface Streamlit

Le module est intégré dans la page `Content` de l'application.

### Onglet "Latest News"

```python
from src.finview.pages.content import show_news
import streamlit as st

# Afficher la page complète
show_news()
```

Affiche :
- Top 10 des actualités business
- Images et métadonnées
- Liens vers articles complets
- Tableau de bord des indices mondiaux

### Onglet "Upcoming Results"

Calendrier des résultats avec :
- Recherche par entreprise
- Filtrage France/International
- Tri chronologique

## ⚙️ Architecture technique

### Appels API via curl

Le module utilise `subprocess` et `curl` pour les appels API :

```python
import subprocess
import json

result = subprocess.run(
    ['curl', '-s', url],
    capture_output=True,
    text=True,
    timeout=10
)

data = json.loads(result.stdout)
```

**Avantages :**
- Respect des contraintes académiques (pas de bibliothèque requests)
- Contrôle précis des timeouts
- Compatibilité multi-plateforme

### Système de cache

Utilise `@st.cache_data` de Streamlit :

```python
@st.cache_data(ttl=1800)  # 30 minutes
def get_cached_business_news(...):
    return get_news_articles(...)
```

**Bénéfices :**
- Réduction des appels API (quota 100/jour)
- Amélioration des performances
- Réactivité de l'interface

### Gestion d'erreurs robuste

- **Validation** : Clé API requise
- **Timeouts** : 10 secondes max
- **Parsing JSON** : Gestion des erreurs
- **Status API** : Vérification du code retour
- **Messages clairs** : Erreurs explicites pour l'utilisateur

## 🔒 Limites et quotas

### API gratuite NewsAPI

| Limite | Valeur |
|--------|--------|
| Requêtes/jour | 100 |
| Articles/requête | Max 100 |
| Historique | 24h (plan gratuit) |
| Sources premium | ❌ Non accessibles |

### Optimisations

1. **Cache de 30 minutes** : Réduit drastiquement les appels
2. **Page size raisonnable** : 10 articles par défaut
3. **Requêtes ciblées** : Catégorie business uniquement
4. **Fallback** : Affichage d'indices boursiers sans NewsAPI

## 🐛 Dépannage

### Erreur "NewsAPI key not configured"

**Cause :** Fichier `.env` absent ou clé manquante

**Solution :**
```bash
# Créer .env à la racine du projet
echo "NEWS_API_KEY=votre_cle_ici" > .env
```

### Erreur "Unable to fetch news"

**Causes possibles :**
1. Quota API dépassé (100 requêtes/jour)
2. Timeout réseau
3. Clé API invalide

**Solutions :**
- Vérifier le quota sur newsapi.org
- Vérifier la connexion internet
- Régénérer la clé API

### Erreur "curl command not found"

**Cause :** curl non installé

**Solution :**
- Windows : Déjà inclus dans Windows 10+
- Linux : `sudo apt-get install curl`
- macOS : `brew install curl`

## 📚 Ressources

- [Documentation NewsAPI](https://newsapi.org/docs)
- [Explorer les sources](https://newsapi.org/sources)
- [Streamlit Caching](https://docs.streamlit.io/library/advanced-features/caching)
- [yfinance pour indices](https://github.com/ranaroussi/yfinance)

## 🎓 Notes académiques

Ce module a été développé dans le cadre du cours **M2 MOSEF - Base de Données & Dashboard**.

**Choix techniques :**
- Utilisation de `curl` plutôt que `requests` (contrainte académique)
- Architecture modulaire et réutilisable
- Documentation exhaustive
- Type hints et validation
- Gestion d'erreurs professionnelle

## 📝 Licence

Projet académique – M2 MOSEF  
Développé dans le cadre du cours Base de Données & Dashboard
