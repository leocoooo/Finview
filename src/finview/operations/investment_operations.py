"""
Opérations sur les investissements du portfolio
"""
from datetime import datetime
from typing import Optional
from src.finview.models.investments import FinancialInvestment, RealEstateInvestment


def add_financial_investment(
    portfolio,
    name: str,
    initial_value: float,
    quantity: float,
    date: Optional[datetime] = None,
    investment_type: str = "Stock",
    location: str = ""
) -> bool:
    """
    Ajoute un investissement financier au portfolio
    
    Args:
        portfolio: Instance de Portfolio
        name: Nom de l'investissement
        initial_value: Prix unitaire
        quantity: Quantité achetée
        date: Date de l'achat (datetime.now() par défaut)
        investment_type: Type d'investissement (Stock, ETF, Crypto, etc.)
        location: Localisation géographique de l'investissement
        
    Returns:
        bool: True si l'opération a réussi
        
    Raises:
        ValueError: Si les paramètres sont invalides ou si le cash est insuffisant
    """
    if not name or not name.strip():
        raise ValueError("Le nom de l'investissement ne peut pas être vide")
    
    if initial_value <= 0:
        raise ValueError(f"Le prix unitaire doit être positif, reçu: {initial_value}")
    
    if quantity <= 0:
        raise ValueError(f"La quantité doit être positive, reçue: {quantity}")
    
    if name in portfolio.financial_investments:
        raise ValueError(f"Un investissement nommé '{name}' existe déjà")
    
    total_cost = initial_value * quantity
    
    if total_cost > portfolio.cash:
        raise ValueError(
            f"Cash insuffisant pour cet achat. "
            f"Coût: {total_cost:.2f}€, Disponible: {portfolio.cash:.2f}€"
        )
    
    if date is None:
        date = datetime.now()
    
    # Déduction du cash
    portfolio.cash -= total_cost
    
    # Création de l'investissement
    investment = FinancialInvestment(
        name=name,
        initial_value=initial_value,
        current_value=initial_value,
        quantity=quantity,
        investment_type=investment_type,
        location=location
    )
    investment.purchase_date = date
    
    # Enregistrement dans le portfolio
    portfolio.financial_investments[name] = investment
    
    # Enregistrement dans l'historique
    portfolio.transaction_history.append({
        'date': date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'FINANCIAL_INVESTMENT_BUY',
        'amount': total_cost,
        'name': name,
        'price': initial_value,
        'quantity': quantity,
        'description': (
            f'Purchase of {quantity} units of {name} ({investment_type})'
            f'{f" in {location}" if location else ""}'
        )
    })
    
    return True


def add_real_estate_investment(
    portfolio,
    name: str,
    initial_value: float,
    quantity: float,
    date: Optional[datetime] = None,
    property_type: str = "SCPI",
    location: str = "",
    rental_yield: float = 0.0
) -> bool:
    """
    Ajoute un investissement immobilier au portfolio
    
    Args:
        portfolio: Instance de Portfolio
        name: Nom de l'investissement
        initial_value: Prix unitaire
        quantity: Quantité achetée (nombre de parts)
        date: Date de l'achat (datetime.now() par défaut)
        property_type: Type de bien (SCPI, Apartment, House, etc.)
        location: Localisation du bien
        rental_yield: Rendement locatif annuel en pourcentage
        
    Returns:
        bool: True si l'opération a réussi
        
    Raises:
        ValueError: Si les paramètres sont invalides ou si le cash est insuffisant
    """
    if not name or not name.strip():
        raise ValueError("Le nom de l'investissement ne peut pas être vide")
    
    if initial_value <= 0:
        raise ValueError(f"Le prix unitaire doit être positif, reçu: {initial_value}")
    
    if quantity <= 0:
        raise ValueError(f"La quantité doit être positive, reçue: {quantity}")
    
    if name in portfolio.real_estate_investments:
        raise ValueError(f"Un investissement immobilier nommé '{name}' existe déjà")
    
    if rental_yield < 0:
        raise ValueError(f"Le rendement locatif ne peut pas être négatif, reçu: {rental_yield}")
    
    total_cost = initial_value * quantity
    
    if total_cost > portfolio.cash:
        raise ValueError(
            f"Cash insuffisant pour cet achat. "
            f"Coût: {total_cost:.2f}€, Disponible: {portfolio.cash:.2f}€"
        )
    
    if date is None:
        date = datetime.now()
    
    # Déduction du cash
    portfolio.cash -= total_cost
    
    # Création de l'investissement
    investment = RealEstateInvestment(
        name=name,
        initial_value=initial_value,
        current_value=initial_value,
        quantity=quantity,
        property_type=property_type,
        location=location,
        rental_yield=rental_yield
    )
    investment.purchase_date = date
    
    # Enregistrement dans le portfolio
    portfolio.real_estate_investments[name] = investment
    
    # Enregistrement dans l'historique
    portfolio.transaction_history.append({
        'date': date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'REAL_ESTATE_INVESTMENT_BUY',
        'amount': total_cost,
        'name': name,
        'price': initial_value,
        'quantity': quantity,
        'description': f'Purchase of {quantity} shares of {name} ({property_type})'
    })
    
    return True


def update_investment_value(
    portfolio,
    name: str,
    new_value: float,
    date: Optional[datetime] = None
) -> bool:
    """
    Met à jour la valeur d'un investissement (financier ou immobilier)
    
    Args:
        portfolio: Instance de Portfolio
        name: Nom de l'investissement
        new_value: Nouvelle valeur unitaire
        date: Date de la mise à jour (datetime.now() par défaut)
        
    Returns:
        bool: True si l'opération a réussi
        
    Raises:
        ValueError: Si l'investissement n'existe pas ou si la valeur est invalide
    """
    if not name or not name.strip():
        raise ValueError("Le nom de l'investissement ne peut pas être vide")
    
    if new_value <= 0:
        raise ValueError(f"La nouvelle valeur doit être positive, reçue: {new_value}")
    
    # Chercher dans les investissements financiers
    investment = portfolio.financial_investments.get(name)
    investment_type = "financial"
    
    # Si pas trouvé, chercher dans l'immobilier
    if investment is None:
        investment = portfolio.real_estate_investments.get(name)
        investment_type = "real_estate"
    
    if investment is None:
        raise ValueError(f"Investissement '{name}' introuvable")
    
    if date is None:
        date = datetime.now()
    
    # Sauvegarde de l'ancienne valeur
    old_value = investment.current_value
    
    # Mise à jour de la valeur
    investment.update_value(new_value)
    
    # Enregistrement dans l'historique
    portfolio.transaction_history.append({
        'date': date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'INVESTMENT_UPDATE',
        'amount': new_value,
        'name': name,
        'price': new_value,
        'description': f'{name}: {old_value:.2f}€ → {new_value:.2f}€ ({investment_type})'
    })
    
    return True


def sell_investment(
    portfolio,
    name: str,
    quantity: float,
    date: Optional[datetime] = None
) -> bool:
    """
    Vend une partie ou la totalité d'un investissement
    
    Args:
        portfolio: Instance de Portfolio
        name: Nom de l'investissement
        quantity: Quantité à vendre
        date: Date de la vente (datetime.now() par défaut)
        
    Returns:
        bool: True si l'opération a réussi
        
    Raises:
        ValueError: Si l'investissement n'existe pas ou si la quantité est invalide
    """
    if not name or not name.strip():
        raise ValueError("Le nom de l'investissement ne peut pas être vide")
    
    if quantity <= 0:
        raise ValueError(f"La quantité à vendre doit être positive, reçue: {quantity}")
    
    # Chercher dans les investissements financiers
    investment = portfolio.financial_investments.get(name)
    investment_dict = portfolio.financial_investments
    investment_type = "financial"
    
    # Si pas trouvé, chercher dans l'immobilier
    if investment is None:
        investment = portfolio.real_estate_investments.get(name)
        investment_dict = portfolio.real_estate_investments
        investment_type = "real_estate"
    
    if investment is None:
        raise ValueError(f"Investissement '{name}' introuvable")
    
    if quantity > investment.quantity:
        raise ValueError(
            f"Quantité insuffisante. Disponible: {investment.quantity}, demandé: {quantity}"
        )
    
    if date is None:
        date = datetime.now()
    
    # Calcul de la valeur de vente
    sale_value = investment.current_value * quantity
    
    # Ajout du cash
    portfolio.cash += sale_value
    
    # Mise à jour de la quantité
    investment.quantity -= quantity
    
    # Si quantité = 0, supprimer l'investissement
    if investment.quantity == 0:
        del investment_dict[name]
    
    # Enregistrement dans l'historique
    portfolio.transaction_history.append({
        'date': date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'INVESTMENT_SELL',
        'amount': sale_value,
        'name': name,
        'price': investment.current_value,
        'quantity': quantity,
        'description': f'Sale of {quantity} units of {name} ({investment_type}) for {sale_value:.2f}€'
    })
    
    return True
