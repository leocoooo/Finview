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
├── portfolio_package/                      # Package principal contenant toute la logique métier
│   ├── __init__.py
│   ├── models.py                           # Classes : Portfolio, FinancialInvestment, RealEstateInvestment, Credit
│   ├── interface_functions.py              # Fonctions d'interface (pages, menus, actions utilisateur)
│   ├── wealth_management_functions.py      # Fonctions de gestion patrimoniale (ajout, vente, mise à jour)
│   ├── visualizations.py                   # Fonctions de visualisation avec Plotly
│   ├── patrimoine_prediction.py            # Algorithmes de prédiction d'évolution patrimoniale
│   ├── save_load_ptf_functions.py          # Sauvegarde/chargement de portfolios (JSON)
│   ├── pdf.py                              # Génération de rapports PDF personnalisés
│   ├── yahoo_search.py                     # Recherche et import de données Yahoo Finance
│   └── create_demo_portfolio.py            # Création de portfolios de démonstration
│
├── data/                                   # Données financières et historiques
│   ├── rendements_mensuels_indices.xlsx    # Rendements historiques des indices
│   ├── fond_euro.xlsx                      # Données des fonds euros
│   ├── livret a.xlsx                       # Historique du Livret A
│   ├── inflation.xlsx                      # Données d'inflation
│   ├── tab_amort_credit_immo.xlsx          # Tableaux d'amortissement crédit immobilier
│   └── Bitcoin Historical Data.csv         # Historique Bitcoin
│
├── logo/                                   # Ressources visuelles de l'application
│   └── FullLogo.png                        # Logo de l'application
│
└── .streamlit/                             # Configuration Streamlit
```

### Description des modules

- **main.py** : Point d'entrée de l'application, gère la navigation entre les différentes pages (Summary, Wealth Management, Dashboard, Predictions, Actuality, Definitions)

- **models.py** : Définit les classes de base du portefeuille
  - `Investment` : Classe de base pour tous les investissements
  - `FinancialInvestment` : Investissements financiers traditionnels (actions, ETF, obligations, crypto)
  - `RealEstateInvestment` : Investissements immobiliers avec rendements locatifs
  - `Credit` : Gestion des crédits et emprunts
  - `Portfolio` : Classe principale gérant l'ensemble du patrimoine

- **interface_functions.py** : Fonctions d'interface utilisateur Streamlit pour chaque page de l'application

- **wealth_management_functions.py** : Logique métier pour les opérations patrimoniales avec gestion des dates

- **visualizations.py** : Bibliothèque complète de graphiques Plotly (camemberts, courbes, tableaux)

- **patrimoine_prediction.py** : Modèles de prédiction et simulations Monte Carlo pour l'évolution du patrimoine

- **pdf.py** : Génération de rapports PDF avec graphiques et statistiques détaillées

- **yahoo_search.py** : Interface avec l'API Yahoo Finance pour l'import de données en temps réel

- **create_demo_portfolio.py** : Générateurs de portfolios fictifs pour démonstration et tests

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

L'application est organisée en 6 sections principales accessibles via le menu horizontal :

- **📊 Summary** : Vue d'ensemble du patrimoine (valeur nette, répartition, évolution)
- **💼 Wealth Management** : Gestion détaillée des investissements, crédits et liquidités
- **📈 Dashboard** : Tableaux de bord interactifs et analyses avancées
- **🔮 Predictions** : Simulations et prédictions d'évolution patrimoniale
- **📰 Actuality** : Actualités financières et économiques
- **📚 Definitions** : Glossaire des termes financiers

### Barre latérale (Sidebar)

La barre latérale permet de :
- Sauvegarder le portfolio actuel
- Charger un portfolio existant
- Créer un portfolio de démonstration
- Générer un rapport PDF
- Réinitialiser le portfolio

---

## Import de données financières

Le module `yahoo_search.py` permet d'importer automatiquement les données financières depuis Yahoo Finance :

```python
from portfolio_package.yahoo_search import search_ticker, get_historical_data

# Rechercher un ticker
results = search_ticker("Apple")

# Récupérer les données historiques
data = get_historical_data("AAPL", start="2020-01-01", end="2024-12-31")
```

---

## Contribution

Pour contribuer au projet, merci de respecter l'organisation suivante :

- **Classes et modèles** : Ajoutez vos classes dans `portfolio_package/models.py`
- **Fonctions métier** : Ajoutez vos fonctions dans `portfolio_package/wealth_management_functions.py`
- **Interface utilisateur** : Ajoutez vos pages dans `portfolio_package/interface_functions.py`
- **Visualisations** : Ajoutez vos graphiques dans `portfolio_package/visualizations.py`
- **Prédictions** : Ajoutez vos modèles dans `portfolio_package/patrimoine_prediction.py`
- **Interface Streamlit** : `main.py` doit rester simple et ne contenir que la navigation

Cette organisation permet de maintenir le code lisible, modulaire et facile à maintenir.

---

## Licence

Projet académique – M2 MOSEF
Développé dans le cadre du cours Base de Données & Dashboard


---

## Support et Documentation

Pour toute question ou problème :
- Ouvrir une issue sur le dépôt GitHub
- Consulter la documentation Streamlit : https://docs.streamlit.io
- Consulter la documentation Plotly : https://plotly.com/python/
