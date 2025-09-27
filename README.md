# Gestionnaire de Portefeuille Financier

## Description

Ce projet propose une application Streamlit pour la gestion, l’analyse et la visualisation d’un portefeuille financier (liquidités, investissements, crédits).  
Il s’inscrit dans le cadre du cours M2 MOSEF – Base de Données & Dashboard.

---

## Fonctionnalités principales

- Gestion des investissements, crédits et liquidités
- Visualisation interactive (camemberts, historiques, analyses)
- Import/export de données (Excel, JSON)
- Génération de données de démonstration
- Filtres et recherches avancées

---

## Technologies utilisées

- Python 3.10+
- [Streamlit](https://streamlit.io/) pour l’interface
- [Plotly](https://plotly.com/python/) pour les graphiques
- [yfinance](https://github.com/ranaroussi/yfinance) pour l’import de données financières
- [Poetry](https://python-poetry.org/) pour la gestion des dépendances

---

## Organisation du projet

```
projet/
│
├── main.py                        # Interface principale Streamlit
├── pyproject.toml                 # Dépendances Poetry
│
├── portfolio_package/             # Logique métier et outils du portefeuille
│   ├── __init__.py
│   ├── models.py                  # Classes : Portfolio, Investment, Credit
│   ├── interface_functions.py     # Fonctions métiers (ajout, vente, paiement, etc.)
│   ├── save_load_ptf_functions.py # Fonctions de sauvegarde/chargement
│   └── charts.py                  # Fonctions de visualisation (Plotly)
│
├── data/                          # Données sauvegardées
│   └── rendements_mensuels_indices.xlsx
│
└── import_yahoo_data.py           # Script d’import des données financières
```

- **main.py** : Interface utilisateur Streamlit (navigation, sidebar, appels aux fonctions du package).
- **portfolio_package/** : Toute la logique métier, la gestion des données et les visualisations.
- **import_yahoo_data.py** : Script indépendant pour télécharger et préparer les données financières.
- **data/** : Dossier pour stocker les fichiers de données générés ou importés.

---

## Installation

1. **Cloner le dépôt**
    ```bash
    git clone <url_du_projet>
    cd <nom_du_dossier>
    ```

2. **Installer les dépendances avec Poetry**
    ```bash
    poetry install
    ```
---

## Utilisation

1. **Lancer l’application Streamlit**
    ```bash
    streamlit run main.py
    ```

2. **Accéder à l’interface**
    - Ouvrir le lien affiché dans le terminal (généralement http://localhost:8501)

---

## Contribution

- Ajoutez vos fonctions métier dans `portfolio_package/interface_functions.py`
- Ajoutez vos classes dans `portfolio_package/models.py`
- Ajoutez vos graphiques dans `portfolio_package/charts.py`
- Gardez `main.py` réservé à l’interface Streamlit

Merci de respecter cette organisation pour garder le projet lisible et maintenable.

---

## Licence

Projet académique – M2 MOSEF