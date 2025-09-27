import json 
import os 
from portfolio_package.models import Portfolio
import streamlit as st  

def save_portfolio(portfolio, filename="saved_json_data/portfolio_data.json"):
    """Sauvegarde le portefeuille dans un fichier"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(portfolio.to_dict(), f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde: {e}")
        return False

def load_portfolio(filename="saved_json_data/portfolio_data.json"):
    """Charge le portefeuille depuis un fichier"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return Portfolio.from_dict(data)
        except Exception as e:
            st.error(f"Erreur lors du chargement: {e}")
            return None
    return None
