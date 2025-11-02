# Module Market

Module de recherche et d'analyse des actifs financiers via l'API Yahoo Finance.

## Structure

```
market/
├── __init__.py           # Exports publics
├── asset_search.py       # Recherche et récupération de données
├── asset_display.py      # Visualisation et formatage
├── asset_ui.py          # Composants Streamlit
└── legacy.py            # Compatibilité avec yahoo_search.py
```

## Architecture

### Séparation des responsabilités

1. **asset_search.py** : Logique métier
   - Recherche de tickers
   - Récupération d'informations
   - Validation des données
   - Gestion du cache

2. **asset_display.py** : Logique d'affichage
   - Création de graphiques
   - Formatage des informations
   - Calcul de tendances

3. **asset_ui.py** : Interface utilisateur
   - Composants Streamlit
   - Gestion des interactions
   - Intégration avec le portfolio

## Utilisation

### Recherche d'actifs

```python
from src.finview.market import search_asset, get_asset_info

# Rechercher un actif
asset = search_asset("AAPL")

# Obtenir les informations
if asset:
    info = get_asset_info(asset)
    print(f"Ticker: {info['ticker']}")
    print(f"Nom: {info['name']}")
    print(f"Prix: {info['current_price']} {info['currency']}")
```

### Affichage des données

```python
from src.finview.market import create_price_chart, format_asset_info

# Créer un graphique de prix
chart = create_price_chart(asset, period="1mo")

# Formater les informations
formatted_info = format_asset_info(asset)
for key, value in formatted_info.items():
    print(f"{key}: {value}")
```

### Interface Streamlit

```python
from src.finview.market import asset_search_tab

# Dans votre page Streamlit
def my_page():
    # Onglet complet de recherche d'actifs
    asset_search_tab()
```

## Fonctions principales

### asset_search.py

- `search_asset(ticker: str) -> Optional[yf.Ticker]`
  - Recherche un actif par son ticker
  - Retourne l'objet Ticker ou None si introuvable

- `get_asset_info(asset: yf.Ticker) -> Dict[str, Any]`
  - Récupère les informations complètes d'un actif
  - Retourne un dictionnaire avec ticker, nom, prix, secteur, etc.

- `get_asset_history(asset: yf.Ticker, period: str = "1mo") -> pd.DataFrame`
  - Récupère l'historique de prix
  - Périodes supportées: "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max"

- `validate_ticker(ticker: str) -> bool`
  - Vérifie si un ticker est valide
  - Utile pour la validation des entrées utilisateur

- `get_ticker_suggestions(query: str) -> List[str]`
  - Obtient des suggestions de tickers
  - Basé sur des mots-clés ou noms d'entreprises

### asset_display.py

- `create_price_chart(asset: yf.Ticker, period: str = "1mo") -> go.Figure`
  - Crée un graphique de prix avec chandelier
  - Options de période personnalisables

- `create_volume_chart(asset: yf.Ticker, period: str = "1mo") -> go.Figure`
  - Crée un graphique de volume
  - Synchronisé avec le graphique de prix

- `format_asset_info(asset: yf.Ticker) -> Dict[str, str]`
  - Formate les informations pour l'affichage
  - Valeurs formatées avec unités et symboles

- `get_price_trend(asset: yf.Ticker, period: str = "1mo") -> str`
  - Calcule la tendance du prix
  - Retourne "Hausse", "Baisse", ou "Stable"

### asset_ui.py

- `asset_search_tab()`
  - Onglet complet de recherche d'actifs
  - Inclut recherche, affichage, et ajout au portfolio

- `display_asset_info(asset: yf.Ticker)`
  - Affiche les informations d'un actif
  - Format structuré avec métriques et graphiques

- `quick_search_widget() -> Optional[yf.Ticker]`
  - Widget de recherche rapide
  - Retourne l'actif sélectionné

## Gestion du cache

Le module utilise `@st.cache_data` pour optimiser les performances :

- Les recherches de tickers sont mises en cache (5 min)
- Les historiques de prix sont mis en cache (30 min)
- Les informations d'actifs sont mises en cache (5 min)

Pour forcer le rafraîchissement, utilisez le bouton "Clear Cache" dans Streamlit.

## Gestion des erreurs

Toutes les fonctions gèrent les erreurs de manière robuste :

```python
# Recherche avec validation
asset = search_asset("TICKER_INVALIDE")
if asset is None:
    print("Ticker non trouvé")
    
# Récupération d'historique
history = get_asset_history(asset, period="1mo")
if history.empty:
    print("Aucune donnée historique disponible")
```

## Migration depuis yahoo_search.py

Pour migrer l'ancien code, utilisez le module `legacy` :

```python
# Ancien code
from src.finview.yahoo_search import search_and_display_asset

# Nouveau code (avec avertissement de dépréciation)
from src.finview.market.legacy import search_and_display_asset

# Recommandé
from src.finview.market import search_asset, get_asset_info
```

## Exemples avancés

### Analyse comparative

```python
from src.finview.market import search_asset, get_asset_history
import pandas as pd

# Comparer deux actifs
asset1 = search_asset("AAPL")
asset2 = search_asset("MSFT")

hist1 = get_asset_history(asset1, period="1y")
hist2 = get_asset_history(asset2, period="1y")

# Normaliser et comparer
normalized = pd.DataFrame({
    'AAPL': hist1['Close'] / hist1['Close'].iloc[0],
    'MSFT': hist2['Close'] / hist2['Close'].iloc[0]
})
```

### Widget personnalisé

```python
import streamlit as st
from src.finview.market import search_asset, format_asset_info

def custom_asset_widget():
    ticker = st.text_input("Ticker")
    if ticker:
        asset = search_asset(ticker)
        if asset:
            info = format_asset_info(asset)
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Prix", info['Prix actuel'])
            with col2:
                st.metric("Variation", info['Variation (1j)'])
```

## Dépendances

- `yfinance` : API Yahoo Finance
- `pandas` : Manipulation de données
- `plotly` : Visualisations interactives
- `streamlit` : Interface utilisateur

## Notes techniques

- Les données proviennent de Yahoo Finance (gratuit, pas d'API key requise)
- Les prix sont en temps quasi-réel (délai de ~15 minutes)
- Certains marchés peuvent ne pas être disponibles
- La validation des tickers est optimiste (assume valide si données disponibles)

## Tests

Pour tester le module :

```python
# Test de recherche
from src.finview.market import search_asset, validate_ticker

assert validate_ticker("AAPL") == True
assert validate_ticker("INVALID_TICKER_123") == False

asset = search_asset("AAPL")
assert asset is not None

# Test de données
from src.finview.market import get_asset_info, get_asset_history

info = get_asset_info(asset)
assert 'ticker' in info
assert 'current_price' in info

history = get_asset_history(asset, period="1mo")
assert not history.empty
assert 'Close' in history.columns
```
