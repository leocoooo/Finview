"""
Opérations sur les crédits du portfolio
"""
from datetime import datetime
from typing import Optional
from src.finview.models.credit import Credit


def add_credit(
    portfolio,
    name: str,
    amount: float,
    interest_rate: float,
    monthly_payment: float,
    date: Optional[datetime] = None
) -> bool:
    """
    Ajoute un crédit au portfolio
    
    Args:
        portfolio: Instance de Portfolio
        name: Nom du crédit
        amount: Montant emprunté
        interest_rate: Taux d'intérêt annuel (en pourcentage)
        monthly_payment: Mensualité
        date: Date de création du crédit (datetime.now() par défaut)
        
    Returns:
        bool: True si l'opération a réussi
        
    Raises:
        ValueError: Si les paramètres sont invalides
    """
    if not name or not name.strip():
        raise ValueError("Le nom du crédit ne peut pas être vide")
    
    if amount <= 0:
        raise ValueError(f"Le montant du crédit doit être positif, reçu: {amount}")
    
    if interest_rate < 0:
        raise ValueError(f"Le taux d'intérêt ne peut pas être négatif, reçu: {interest_rate}")
    
    if monthly_payment <= 0:
        raise ValueError(f"La mensualité doit être positive, reçue: {monthly_payment}")
    
    if name in portfolio.credits:
        raise ValueError(f"Un crédit nommé '{name}' existe déjà")
    
    if date is None:
        date = datetime.now()
    
    # Création du crédit
    credit = Credit(
        name=name,
        initial_amount=amount,
        interest_rate=interest_rate,
        monthly_payment=monthly_payment
    )
    credit.creation_date = date
    
    # Enregistrement dans le portfolio
    portfolio.credits[name] = credit
    
    # Ajout du cash emprunté
    portfolio.cash += amount
    
    # Enregistrement dans l'historique
    portfolio.transaction_history.append({
        'date': date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'CREDIT_ADD',
        'amount': amount,
        'name': name,
        'description': f'New credit: {name} at {interest_rate}% (monthly: {monthly_payment}€)'
    })
    
    return True


def pay_credit(
    portfolio,
    name: str,
    amount: float,
    date: Optional[datetime] = None
) -> bool:
    """
    Effectue un paiement sur un crédit
    
    Args:
        portfolio: Instance de Portfolio
        name: Nom du crédit
        amount: Montant du paiement
        date: Date du paiement (datetime.now() par défaut)
        
    Returns:
        bool: True si l'opération a réussi
        
    Raises:
        ValueError: Si le crédit n'existe pas ou si les paramètres sont invalides
    """
    if not name or not name.strip():
        raise ValueError("Le nom du crédit ne peut pas être vide")
    
    if amount <= 0:
        raise ValueError(f"Le montant du paiement doit être positif, reçu: {amount}")
    
    if name not in portfolio.credits:
        raise ValueError(f"Crédit '{name}' introuvable")
    
    credit = portfolio.credits[name]
    
    if amount > portfolio.cash:
        raise ValueError(
            f"Cash insuffisant pour ce paiement. "
            f"Montant: {amount:.2f}€, Disponible: {portfolio.cash:.2f}€"
        )
    
    if amount > credit.current_balance:
        raise ValueError(
            f"Le montant du paiement ({amount:.2f}€) dépasse le solde restant ({credit.current_balance:.2f}€)"
        )
    
    if date is None:
        date = datetime.now()
    
    # Déduction du cash
    portfolio.cash -= amount
    
    # Enregistrement du paiement
    credit.make_payment(amount)
    
    # Si le crédit est soldé, le supprimer
    if credit.current_balance <= 0:
        del portfolio.credits[name]
    
    # Enregistrement dans l'historique
    portfolio.transaction_history.append({
        'date': date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'CREDIT_PAYMENT',
        'amount': amount,
        'name': name,
        'description': f'Payment of {amount:.2f}€ on {name} (remaining: {max(0, credit.current_balance):.2f}€)'
    })
    
    return True
