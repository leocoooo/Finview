"""
Opérations sur le cash du portfolio
"""
from datetime import datetime
from typing import Optional


def add_cash(portfolio, amount: float, date: Optional[datetime] = None, description: str = "Cash addition") -> bool:
    """
    Ajoute du cash au portfolio
    
    Args:
        portfolio: Instance de Portfolio
        amount: Montant à ajouter (doit être positif)
        date: Date de l'opération (datetime.now() par défaut)
        description: Description de la transaction
        
    Returns:
        bool: True si l'opération a réussi, False sinon
        
    Raises:
        ValueError: Si le montant est négatif ou nul
    """
    if amount <= 0:
        raise ValueError(f"Le montant doit être positif, reçu: {amount}")
    
    if date is None:
        date = datetime.now()
    
    portfolio.cash += amount
    portfolio.transaction_history.append({
        'date': date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'CASH_ADD',
        'amount': amount,
        'description': description
    })
    
    return True


def withdraw_cash(portfolio, amount: float, date: Optional[datetime] = None, description: str = "Cash withdrawal") -> bool:
    """
    Retire du cash du portfolio
    
    Args:
        portfolio: Instance de Portfolio
        amount: Montant à retirer (doit être positif)
        date: Date de l'opération (datetime.now() par défaut)
        description: Description de la transaction
        
    Returns:
        bool: True si l'opération a réussi, False sinon
        
    Raises:
        ValueError: Si le montant est négatif, nul ou supérieur au cash disponible
    """
    if amount <= 0:
        raise ValueError(f"Le montant doit être positif, reçu: {amount}")
    
    if amount > portfolio.cash:
        raise ValueError(f"Cash insuffisant. Disponible: {portfolio.cash}€, demandé: {amount}€")
    
    if date is None:
        date = datetime.now()
    
    portfolio.cash -= amount
    portfolio.transaction_history.append({
        'date': date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'CASH_WITHDRAW',
        'amount': amount,
        'description': description
    })
    
    return True
