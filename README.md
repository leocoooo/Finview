# Finview

Gestionnaire de portefeuille financier complet, développé en Python avec Streamlit. Permet la gestion, l’analyse et la visualisation de patrimoine (liquidités, investissements, immobilier, crédits), l’accès aux actualités financières, et la génération de rapports PDF.

---

## Fonctionnalités principales

### Gestion de patrimoine
- **Gestion des liquidités** : Dépôts et retraits de trésorerie
- **Investissements financiers** : Actions, ETF, obligations, cryptomonnaies avec suivi des performances
- **Investissements immobiliers** : SCPI, REIT, immobilier direct avec calcul des rendements locatifs
- **Gestion des crédits** : Suivi des prêts, simulations de remboursement, tableaux d'amortissement

### Visualisations et analyses
- **Tableaux de bord interactifs** : Graphiques en camembert, courbes d'évolution, analyses détaillées
- **Historique des transactions** : Suivi complet de toutes les opérations
- **Analyse de performance** : Calcul automatique des gains/pertes et rendements
- **Diversification géographique** : Visualisation de la répartition par pays

### Fonctionnalités avancées
- **Prédictions patrimoniales** : Simulations d'évolution du patrimoine basées sur des données historiques
- **Import de données financières** : Récupération automatique des cours via Yahoo Finance
- **Export/Import de données** : Sauvegarde et chargement de portfolios au format JSON
- **Génération de PDF** : Création de rapports patrimoniaux complets
- **Actualités financières en temps réel** : Flux d'actualités business via NewsAPI avec mise en cache
- **Calendrier des résultats** : Suivi des publications financières des entreprises françaises et internationales
- **Indices boursiers** : Affichage en temps réel des principaux indices mondiaux
- **Glossaire financier** : Définitions et explications des termes financiers
- **Portfolios de démonstration** : Génération de données fictives pour tester l'application

---

## Technologies utilisées 
- Python 3.8+
- Streamlit
- Plotly
- yfinance
- pandas
- FPDF
- Kaleido
- NewsAPI
- uv (gestion des dépendances via pyproject.toml)
- Bash (pour les scripts)
- Docker (optionnel)

---

## Structure du projet détaillée

```
Finview/
├── main.py                  # Point d'entrée Streamlit, navigation et affichage principal
├── pyproject.toml           # Dépendances et configuration du projet (uv/Poetry)
├── .env                     # Clé API NewsAPI et autres variables d'environnement
├── install.sh               # Script bash pour préparer l'environnement et Docker
├── get_news.sh              # Script bash pour récupérer les actualités NewsAPI
├── launch.sh                # Script bash pour lancer l'application via Docker
├── saved_json_data/
│   └── news.json            # Actualités financières récupérées
├── reports/                 # Dossiers pour les rapports PDF générés
├── logo/                    # Ressources visuelles (logo, images)
├── src/
│   └── finview/
│       ├── __init__.py      # Initialise le package Python
│       ├── models/
│       │   ├── __init__.py
│       │   ├── portfolio.py         # Classe principale Portfolio (patrimoine global)
│       │   ├── investments.py       # Modèles d'investissements financiers et immobiliers
│       │   └── credit.py            # Modèle de crédit et gestion des emprunts
│       ├── operations/
│       │   ├── __init__.py
│       │   ├── cash_operations.py           # Fonctions de gestion des liquidités
│       │   ├── investment_operations.py     # Fonctions d'achat/vente d'investissements
│       │   ├── credit_operations.py         # Fonctions de gestion des crédits
│       │   └── README.md                    # Documentation du module
│       ├── charts/
│       │   ├── __init__.py
│       │   ├── config.py                    # Thèmes et configuration des graphiques
│       │   ├── layouts.py                   # Templates de mise en page graphique
│       │   ├── history.py                   # Calculs d'historique de portefeuille
│       │   ├── market_data.py               # Données de marché (indices, crypto)
│       │   ├── portfolio_charts.py          # Graphiques de répartition et performance
│       │   ├── analysis_charts.py           # Graphiques d'analyse avancée
│       │   └── geo_charts.py                # Cartes géographiques des investissements
│       ├── market/
│       │   ├── __init__.py
│       │   ├── asset_search.py              # Recherche d'actifs via Yahoo Finance
│       │   ├── asset_display.py             # Affichage des informations d'actifs
│       │   ├── asset_ui.py                  # Composants Streamlit pour le marché
│       │   └── README.md                    # Documentation du module
│       ├── news/
│       │   ├── __init__.py
│       │   ├── news_fetcher.py              # Récupération des actualités via NewsAPI
│       │   ├── news_cache.py                # Système de cache pour les news
│       │   └── test_api.py                  # Tests unitaires de l'API NewsAPI
│       ├── predictions/
│       │   ├── __init__.py
│       │   ├── config.py                    # Paramètres de simulation
│       │   ├── monte_carlo.py               # Simulations Monte Carlo du patrimoine
│       │   ├── utils.py                     # Fonctions utilitaires pour les prédictions
│       │   └── visualizations.py            # Graphiques de prédiction
│       ├── fixture/
│       │   ├── __init__.py
│       │   └── create_demo_portfolio.py     # Génération de portfolios de démonstration
│       ├── pages/
│       │   ├── __init__.py
│       │   ├── summary.py                   # Page d'accueil : vue d'ensemble
│       │   ├── management.py                # Page de gestion patrimoniale
│       │   ├── analytics.py                 # Page d'analyses et graphiques
│       │   ├── predictions.py               # Page de simulations et prédictions
│       │   └── content.py                   # Page d'actualités et glossaire
│       ├── ui/
│       │   ├── __init__.py
│       │   ├── components.py                # Widgets Streamlit réutilisables
│       │   ├── formatting.py                # Fonctions de formatage des données
│       │   ├── portfolio_persistence.py     # Sauvegarde/chargement de portfolios
│       │   └── styles.py                    # Styles CSS pour l'UI
│       ├── pdf/
│       │   ├── __init__.py
│       │   ├── generator.py                 # Génération de rapports PDF
│       │   ├── config.py                    # Configuration des rapports
│       │   └── sections.py                  # Sections du rapport PDF
│       ├── storage/
│       │   ├── __init__.py
│       │   └── portfolio_storage.py         # Persistance des données de portefeuille
```
## Modules principaux
- `models/` : Modèles de données (Portfolio, Investment, Credit)
- `operations/` : Logique métier (opérations sur le patrimoine)
- `charts/` : Visualisations Plotly
- `market/` : Recherche et import de données financières
- `news/` : Actualités financières (NewsAPI)
- `predictions/` : Simulations et prédictions
- `pages/` : Pages Streamlit
- `ui/` : Composants UI
- `pdf/` : Génération de rapports PDF
- `storage/` : Persistance des données

---

## Installation et lancement

### 1. Préparer la clé API NewsAPI
Créez un fichier `.env` à la racine du projet :
```
NEWSAPI_KEY=your_api_key_here
```

### 2. Avec Docker
1. Ouvrez un terminal bash dans le dossier du projet.
2. Installez Docker et Docker Compose.
3. Lancez :
   ```bash
   bash install.sh
   bash get_news.sh
   bash launch.sh
   ```
4. Accédez à l’application sur http://localhost:8501

### 3. Sans Docker
1. Installez Python 3.8+ et l’outil [uv](https://github.com/astral-sh/uv) :
   ```bash
   pip install uv
   ```
2. Installez les dépendances :
   ```bash
   uv pip install -r pyproject.toml
   ```
3. Créez le fichier `.env` avec votre clé API.
4. Récupérez les actualités :
   ```bash
   bash get_news.sh
   ```
5. Lancez l’application :
   ```bash
   streamlit run main.py
   ```
6. Accédez à l’application sur http://localhost:8501

---

## Utilisation des scripts
- `install.sh` : Prépare l’environnement et construit l’image Docker
- `get_news.sh` : Récupère les actualités via NewsAPI et les stocke dans `saved_json_data/news.json`.
  
   Utilisation :
   ```bash
   bash get_news.sh [CATEGORY] [COUNTRY] [PAGE_SIZE]
   ```
   - `CATEGORY` (défaut : business)
   - `COUNTRY` (défaut : us)
   - `PAGE_SIZE` (défaut : 10)

   Si aucun argument n'est fourni, les valeurs par défaut sont utilisées.

      Valeurs compatibles avec NewsAPI :
      - CATEGORY : business, entertainment, general, health, science, sports, technology
      - COUNTRY (quelques exemples) :
         - fr : France
         - us : United States
         - gb : United Kingdom
         - de : Germany
         - it : Italy
         - jp : Japan
         - br : Brazil
- `launch.sh` : Démarre l’application (via Docker)

---

### Navigation dans l'application

L'application est organisée en plusieurs sections accessibles via le menu :

- **📊 Summary** : Vue d'ensemble du patrimoine (valeur nette, répartition, évolution)
- **💼 Management** : Gestion détaillée des investissements, crédits et liquidités
- **📈 Analytics** : Tableaux de bord interactifs et analyses avancées
- **🔮 Predictions** : Simulations et prédictions d'évolution patrimoniale
- **📰 Content** : Actualités financières en temps réel et glossaire de termes financiers

---

## Ressources
- [Streamlit](https://docs.streamlit.io)
- [Plotly](https://plotly.com/python/)
- [yfinance](https://github.com/ranaroussi/yfinance)
- [NewsAPI](https://newsapi.org/)
- [uv](https://github.com/astral-sh/uv)
