# Finview - Gestionnaire de Portefeuille Financier

## Description

Finview est une application complète de gestion de patrimoine développée avec Streamlit. Elle permet de gérer, analyser et visualiser un portefeuille financier comprenant des liquidités, des investissements financiers (actions, ETF, obligations, cryptomonnaies), des investissements immobiliers (SCPI, REIT, immobilier direct) et des crédits.

L'application offre des fonctionnalités avancées de visualisation, de prédiction et d'analyse patrimoniale, ainsi que la génération de rapports PDF personnalisés.

Ce projet s'inscrit dans le cadre du cours M2 MOSEF – Base de Données & Dashboard.

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
- **Actualités financières** : Intégration de flux d'actualités
- **Glossaire financier** : Définitions et explications des termes financiers
- **Portfolios de démonstration** : Génération de données fictives pour tester l'application

---

## Technologies utilisées

- **Python 3.13+**
- **[Streamlit](https://streamlit.io/)** (v1.50+) - Interface utilisateur interactive
- **[Plotly](https://plotly.com/python/)** (v6.3+) - Visualisations de données avancées
- **[yfinance](https://github.com/ranaroussi/yfinance)** (v0.2.66+) - Import de données financières en temps réel
- **[Pandas](https://pandas.pydata.org/)** (v2.3.2+) - Manipulation et analyse de données
- **[FPDF](https://pyfpdf.readthedocs.io/)** (v1.7.2) - Génération de rapports PDF
- **[Kaleido](https://github.com/plotly/Kaleido)** (v1.1+) - Export d'images statiques des graphiques Plotly
- **[Poetry](https://python-poetry.org/)** - Gestion des dépendances

---

## Organisation du projet

```
Finview/
│
├── main.py                                 # Interface principale Streamlit avec navigation horizontale
├── pyproject.toml                          # Configuration des dépendances Poetry
├── poetry.lock                             # Verrouillage des versions de dépendances
│
├── src/finview/                            # Package principal contenant toute la logique métier
│   ├── __init__.py
│   ├── models/                             # Modèles de données
│   │   ├── portfolio.py                    # Classe Portfolio
│   │   ├── investments.py                  # FinancialInvestment, RealEstateInvestment
│   │   └── credit.py                       # Classe Credit
│   ├── operations/                         # Opérations patrimoniales
│   │   ├── __init__.py
│   │   ├── cash_operations.py              # Ajout/retrait de cash
│   │   ├── investment_operations.py        # Gestion des investissements
│   │   ├── credit_operations.py            # Gestion des crédits
│   │   └── README.md                       # Documentation du module
│   ├── charts/                             # Visualisations Plotly
│   │   ├── __init__.py
│   │   ├── config.py                       # Thèmes et configuration
│   │   ├── layouts.py                      # Templates de mise en page
│   │   ├── history.py                      # Calculs d'historique
│   │   ├── market_data.py                  # Données de marché (CAC40, DJI, BTC)
│   │   ├── portfolio_charts.py             # Graphiques de portfolio
│   │   ├── analysis_charts.py              # Graphiques d'analyse
│   │   └── geo_charts.py                   # Cartes géographiques
│   ├── market/                             # Recherche et données de marché
│   │   ├── __init__.py
│   │   ├── asset_search.py                 # Recherche Yahoo Finance
│   │   ├── asset_display.py                # Visualisation actifs
│   │   ├── asset_ui.py                     # Interface Streamlit
│   │   └── README.md                       # Documentation du module
│   ├── predictions/                        # Prédictions et simulations
│   │   ├── __init__.py
│   │   ├── config.py                       # Configuration
│   │   ├── monte_carlo.py                  # Simulations Monte Carlo
│   │   ├── utils.py                        # Utilitaires
│   │   └── visualizations.py               # Graphiques de prédictions
│   ├── fixture/                            # Données de test
│   │   ├── __init__.py
│   │   └── create_demo_portfolio.py        # Génération de portfolios de démo
│   ├── pages/                              # Pages Streamlit
│   │   ├── summary.py                      # Vue d'ensemble
│   │   ├── management.py                   # Gestion patrimoniale
│   │   ├── analytics.py                    # Analyses et graphiques
│   │   └── predictions.py                  # Prédictions
│   ├── ui/                                 # Composants UI
│   │   ├── __init__.py
│   │   ├── components.py                   # Widgets réutilisables
│   │   ├── formatting.py                   # Formatage de données
│   │   ├── portfolio_persistence.py        # Sauvegarde/chargement
│   │   └── styles.py                       # Styles CSS
│   ├── pdf/                                # Génération de PDF
│   │   ├── __init__.py
│   │   ├── generator.py                    # Génération de rapports
│   │   └── sections.py                     # Sections du PDF
│   └── save_load_ptf_functions.py          # Fonctions de persistance (legacy)
│
├── logo/                                   # Ressources visuelles de l'application
│   └── FullLogo.png                        # Logo de l'application
│
└── .streamlit/                             # Configuration Streamlit
```

### Description des modules

- **main.py** : Point d'entrée de l'application, gère la navigation entre les différentes pages (Summary, Management, Analytics, Predictions)

- **models/** : Classes de base du patrimoine
  - `Portfolio` : Classe principale gérant l'ensemble du patrimoine
  - `FinancialInvestment` : Investissements financiers (actions, ETF, obligations, crypto)
  - `RealEstateInvestment` : Investissements immobiliers avec rendements locatifs
  - `Credit` : Gestion des crédits et emprunts

- **operations/** : Logique métier pour les opérations patrimoniales
  - API fonctionnelle avec validation robuste
  - Gestion d'erreurs descriptive avec exceptions
  - Type hints complets sur toutes les fonctions
  - Documentation exhaustive avec exemples d'utilisation
  - Voir [operations/README.md](src/finview/operations/README.md) pour plus de détails

- **charts/** : Bibliothèque complète de visualisations Plotly
  - Configuration centralisée (thèmes, couleurs, benchmarks)
  - Layouts réutilisables pour cohérence visuelle
  - Graphiques de portfolio (camemberts, barres, performances)
  - Graphiques d'analyse (transactions, comparaisons benchmarks)
  - Cartes géographiques des investissements mondiaux
  - Wrappers Streamlit pour affichage direct

- **market/** : Interface avec Yahoo Finance
  - Recherche d'actifs par ticker avec suggestions
  - Récupération de données en temps réel (prix, historique)
  - Validation automatique des tickers
  - Mise en cache pour optimisation des performances
  - Visualisation de prix avec graphiques interactifs
  - Interface Streamlit complète pour recherche et ajout
  - Voir [market/README.md](src/finview/market/README.md) pour plus de détails

- **predictions/** : Modèles de prédiction et simulations
  - Simulations Monte Carlo pour évolution du patrimoine
  - Visualisations interactives des scénarios
  - Configuration personnalisable des paramètres

- **pages/** : Pages Streamlit de l'application
  - Interface utilisateur moderne et intuitive
  - Navigation fluide entre les sections
  - Intégration complète de tous les modules

- **ui/** : Composants UI réutilisables
  - Widgets personnalisés pour Streamlit
  - Formatage cohérent des données financières
  - Gestion de la persistance des portfolios
  - Styles CSS pour une apparence professionnelle

- **pdf/** : Génération de rapports PDF personnalisés
  - Rapports complets avec graphiques exportés
  - Statistiques détaillées du patrimoine
  - Mise en page professionnelle

## Architecture et principes

Le projet suit une architecture modulaire basée sur les principes suivants :

### Séparation des responsabilités (SRP)
- Chaque module a une responsabilité unique et bien définie
- Séparation claire entre UI, logique métier et données
- Configuration centralisée pour faciliter la maintenance

### API fonctionnelle
- Fonctions pures qui ne mutent pas les objets directement
- Toutes les opérations retournent des résultats explicites
- Validation systématique des entrées avec exceptions descriptives

### Type hints et documentation
- Type hints complets sur toutes les fonctions publiques
- Docstrings détaillées avec exemples d'utilisation
- Documentation séparée dans des fichiers README par module

### Gestion d'erreurs robuste
- Exceptions explicites avec messages descriptifs
- Validation des entrées utilisateur
- Gestion gracieuse des cas d'erreur

---

## Exemples d'utilisation

### Opérations sur le portfolio

```python
from src.finview.operations import (
    add_cash,
    add_financial_investment,
    add_credit,
    pay_credit
)
from src.finview.models.portfolio import Portfolio

# Créer un portfolio
portfolio = Portfolio(initial_cash=10000.0)

# Ajouter du cash
add_cash(portfolio, amount=5000.0, description="Dépôt mensuel")

# Ajouter un investissement
add_financial_investment(
    portfolio,
    name="Apple Inc.",
    ticker="AAPL",
    investment_type="Action",
    unit_price=150.0,
    quantity=10
)

# Ajouter un crédit
add_credit(
    portfolio,
    name="Prêt Auto",
    amount=15000.0,
    interest_rate=2.5,
    monthly_payment=320.0
)

# Payer un crédit
pay_credit(portfolio, name="Prêt Auto", amount=320.0)
```

### Visualisations

```python
from src.finview.charts import (
    create_portfolio_pie_chart,
    display_portfolio_pie,
    create_financial_portfolio_vs_benchmark_chart
)

# Créer un graphique personnalisé
fig = create_portfolio_pie_chart(portfolio)
# Utiliser avec st.plotly_chart(fig)

# Ou utiliser le wrapper Streamlit directement
display_portfolio_pie(portfolio)  # Affiche directement dans Streamlit

# Comparer avec un benchmark
benchmark_fig = create_financial_portfolio_vs_benchmark_chart(
    portfolio,
    benchmark="CAC 40"
)
```

### Recherche d'actifs

```python
from src.finview.market import search_asset, get_asset_info, create_price_chart

# Rechercher un actif
asset = search_asset("AAPL")

if asset:
    # Obtenir les informations
    info = get_asset_info(asset)
    print(f"{info['name']}: {info['current_price']} {info['currency']}")
    
    # Créer un graphique de prix
    chart = create_price_chart(asset, period="1mo")
```

---

## Import de données financières

Le module `market` permet d'importer automatiquement les données financières depuis Yahoo Finance :

```python
from src.finview.market import search_asset, get_asset_info, get_asset_history

# Rechercher un actif
asset = search_asset("AAPL")

# Obtenir les informations complètes
if asset:
    info = get_asset_info(asset)
    print(f"{info['name']}: {info['current_price']} {info['currency']}")
    
    # Récupérer l'historique des prix
    history = get_asset_history(asset, period="1y")
    print(history.head())
```

Dans l'interface Streamlit, utilisez le widget intégré :

```python
from src.finview.market import asset_search_tab

# Affiche une interface complète de recherche et d'ajout d'actifs
asset_search_tab()
```

---

## Tests et validation

Le projet inclut plusieurs portfolios de démonstration pour tester les fonctionnalités :

```python
from src.finview.fixture.create_demo_portfolio import create_demo_portfolio_4

# Créer un portfolio de démonstration
demo_portfolio = create_demo_portfolio_4()
```

---

## Contribution

Pour contribuer au projet, merci de respecter l'organisation modulaire actuelle :

### Ajout de nouvelles fonctionnalités

- **Modèles de données** : Ajoutez vos classes dans `src/finview/models/`
- **Opérations métier** : Ajoutez vos fonctions dans `src/finview/operations/`
  - Respectez la signature fonctionnelle (portfolio en premier paramètre)
  - Ajoutez validation et type hints
  - Documentez avec des docstrings complètes
- **Visualisations** : Ajoutez vos graphiques dans `src/finview/charts/`
  - Utilisez la configuration centralisée
  - Créez des wrappers Streamlit si nécessaire
- **Pages Streamlit** : Ajoutez vos pages dans `src/finview/pages/`
- **Composants UI** : Ajoutez vos widgets dans `src/finview/ui/`

### Standards de code

- Type hints sur toutes les fonctions publiques
- Docstrings au format Google/NumPy
- Validation des entrées avec exceptions explicites
- Tests unitaires pour les nouvelles fonctionnalités
- Respect des principes SOLID

### Documentation

- Mettez à jour les README des modules concernés
- Ajoutez des exemples d'utilisation dans les docstrings
- Documentez les cas d'erreur possibles

Cette organisation permet de maintenir le code lisible, modulaire et facile à maintenir.

---

## Installation

### Prérequis
- Python 3.13 ou supérieur
- Poetry (pour la gestion des dépendances)

### Étapes d'installation

1. **Cloner le dépôt**
    ```bash
    git clone <url_du_projet>
    cd Finview
    ```

2. **Installer Poetry** (si ce n'est pas déjà fait)
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3. **Installer les dépendances avec Poetry**
    ```bash
    poetry install
    ```

4. **Activer l'environnement virtuel** (optionnel)
    ```bash
    poetry shell
    ```

---

## Utilisation

### Lancement de l'application

1. **Démarrer l'application Streamlit**
    ```bash
    poetry run streamlit run main.py
    ```

    Ou si l'environnement virtuel est activé :
    ```bash
    streamlit run main.py
    ```

2. **Accéder à l'interface**
    - Ouvrir le navigateur à l'adresse affichée dans le terminal (généralement http://localhost:8501)

### Navigation dans l'application

L'application est organisée en plusieurs sections accessibles via le menu :

- **📊 Summary** : Vue d'ensemble du patrimoine (valeur nette, répartition, évolution)
- **💼 Management** : Gestion détaillée des investissements, crédits et liquidités
- **📈 Analytics** : Tableaux de bord interactifs et analyses avancées
- **🔮 Predictions** : Simulations et prédictions d'évolution patrimoniale

### Barre latérale (Sidebar)

La barre latérale permet de :
- Sauvegarder le portfolio actuel
- Charger un portfolio existant
- Créer un portfolio de démonstration
- Générer un rapport PDF
- Réinitialiser le portfolio

---

## Licence

Projet académique – M2 MOSEF  
Développé dans le cadre du cours Base de Données & Dashboard

---

## Ressources additionnelles

### Documentation des modules
- [operations/README.md](src/finview/operations/README.md) - Guide complet du module d'opérations
- [market/README.md](src/finview/market/README.md) - Guide du module de recherche d'actifs
- [MIGRATION_COMPLETE.md](MIGRATION_COMPLETE.md) - Historique de la refactorisation
- [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) - Résumé des améliorations

### Technologies
- [Streamlit](https://docs.streamlit.io) - Documentation officielle
- [Plotly](https://plotly.com/python/) - Guide des graphiques
- [yfinance](https://github.com/ranaroussi/yfinance) - API Yahoo Finance
