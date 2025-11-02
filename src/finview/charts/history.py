"""
Fonctions de calcul de l'historique du portfolio
"""
import pandas as pd
from datetime import datetime


def get_financial_portfolio_value_at_date(portfolio, date):
    """
    Calcule la valeur totale des investissements financiers à une date donnée
    
    Args:
        portfolio: Instance de Portfolio
        date: Date cible pour le calcul
        
    Returns:
        float: Valeur totale des investissements financiers à cette date
    """
    total = 0.0
    
    for inv in portfolio.financial_investments.values():
        if hasattr(inv, "purchase_date") and inv.purchase_date <= date:
            price_at_date = inv.initial_value
            quantity_at_date = 0.0
            
            # Parcourir l'historique des transactions pour cet investissement
            for transaction in portfolio.transaction_history:
                trans_date = pd.to_datetime(transaction["date"])
                
                if trans_date > date:
                    continue
                
                if transaction.get("name") == inv.name:
                    trans_type = transaction["type"]
                    
                    if trans_type == "FINANCIAL_INVESTMENT_BUY":
                        price_at_date = transaction.get("price", inv.initial_value)
                        quantity_at_date = transaction.get("quantity", 0)
                    
                    elif trans_type == "INVESTMENT_UPDATE":
                        price_at_date = transaction.get("price", price_at_date)
                    
                    elif trans_type == "INVESTMENT_SELL":
                        quantity_at_date -= transaction.get("quantity", 0)
            
            total += price_at_date * quantity_at_date
    
    return total


def get_total_invested_at_date(portfolio, date):
    """
    Calcule le total investi dans le portefeuille jusqu'à une certaine date
    
    Args:
        portfolio: Instance de Portfolio
        date: Date cible pour le calcul
        
    Returns:
        float: Total investi jusqu'à cette date
    """
    if not hasattr(portfolio, "transaction_history") or len(portfolio.transaction_history) == 0:
        return 0

    df = pd.DataFrame(portfolio.transaction_history)
    df["date"] = pd.to_datetime(df["date"])

    # On ne prend que les transactions avant la date donnée
    df = df[df["date"] <= pd.to_datetime(date)]

    # Somme des investissements (positifs) et des retraits (négatifs)
    total_invested = df["amount"].sum()
    return total_invested


def get_portfolio_monthly_history(portfolio):
    """
    Reconstruit l'historique mensuel du portefeuille de manière optimisée
    
    Args:
        portfolio: Instance de Portfolio
        
    Returns:
        pd.DataFrame: DataFrame avec colonnes 'date', 'value', 'invested'
    """
    if not hasattr(portfolio, "transaction_history") or len(portfolio.transaction_history) == 0:
        return pd.DataFrame(columns=["date", "value", "invested"])

    df = pd.DataFrame(portfolio.transaction_history)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    start_date = df["date"].iloc[0].replace(day=1)
    end_date = datetime.now()
    monthly_dates = pd.date_range(start=start_date, end=end_date, freq="MS")

    # OPTIMISATION : Créer un dictionnaire {nom_investissement: [(date, price, quantity)]}
    investment_states = {}
    
    for _, transaction in df.iterrows():
        trans_type = transaction["type"]
        name = transaction.get("name")
        
        if name and trans_type in ["FINANCIAL_INVESTMENT_BUY", "INVESTMENT_UPDATE", "INVESTMENT_SELL"]:
            if name not in investment_states:
                investment_states[name] = []
            
            investment_states[name].append({
                'date': transaction['date'],
                'type': trans_type,
                'price': transaction.get('price'),
                'quantity': transaction.get('quantity')
            })
    
    # Calculer les valeurs mensuelles
    values = []
    for target_date in monthly_dates:
        total = 0.0
        
        for name, states in investment_states.items():
            price = None
            quantity = 0.0
            
            for state in states:
                if state['date'] > target_date:
                    break
                
                if state['type'] == 'FINANCIAL_INVESTMENT_BUY':
                    price = state['price']
                    quantity = state['quantity']
                elif state['type'] == 'INVESTMENT_UPDATE':
                    price = state['price']
                elif state['type'] == 'INVESTMENT_SELL':
                    quantity -= state['quantity']
            
            if price is not None and quantity > 0:
                total += price * quantity
        
        values.append(total)
    
    invested = [get_total_invested_at_date(portfolio, d) for d in monthly_dates]

    history_df = pd.DataFrame({
        "date": monthly_dates,
        "value": values,
        "invested": invested
    })
    return history_df
