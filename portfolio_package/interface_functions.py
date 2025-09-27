from datetime import datetime, timedelta
from portfolio_package.models import Portfolio, Investment, Credit

def create_demo_portfolio():
    """Crée un portefeuille de démonstration avec un historique simulé"""
    portfolio = Portfolio(initial_cash=5000.0)
    
    # Simulation sur les 6 derniers mois
    base_date = datetime.now() - timedelta(days=180)
    
    # === JANVIER - Début du portefeuille ===
    current_date = base_date
    
    # Ajout initial de fonds
    portfolio.cash = 15000.0
    portfolio.transaction_history.append({
        'date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'CASH_ADD',
        'amount': 10000.0,
        'description': 'Apport initial'
    })
    
    # Premiers investissements
    current_date += timedelta(days=3)
    portfolio._add_investment_with_date("Actions Apple", 150.0, 20, current_date)  # 3000€
    
    current_date += timedelta(days=5)
    portfolio._add_investment_with_date("ETF S&P 500", 400.0, 10, current_date)  # 4000€
    
    current_date += timedelta(days=7)
    portfolio._add_investment_with_date("Bitcoin", 35000.0, 0.2, current_date)  # 7000€
    
    # === FÉVRIER - Expansion du portefeuille ===
    current_date += timedelta(days=15)
    portfolio.cash += 3000.0
    portfolio.transaction_history.append({
        'date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'CASH_ADD',
        'amount': 3000.0,
        'description': 'Bonus mensuel'
    })
    
    current_date += timedelta(days=3)
    portfolio._add_investment_with_date("Actions Tesla", 200.0, 15, current_date)  # 3000€
    
    # Premier crédit
    current_date += timedelta(days=10)
    portfolio._add_credit_with_date("Prêt Auto", 12000.0, 2.5, 280, current_date)
    
    # === MARS - Évolutions des prix ===
    current_date += timedelta(days=20)
    portfolio._update_investment_with_date("Actions Apple", 165.0, current_date)  # +10%
    portfolio._update_investment_with_date("Bitcoin", 42000.0, current_date)  # +20%
    portfolio._update_investment_with_date("ETF S&P 500", 385.0, current_date)  # -3.75%
    
    # Paiement crédit
    current_date += timedelta(days=5)
    portfolio._pay_credit_with_date("Prêt Auto", 500.0, current_date)
    
    # === AVRIL - Correction du marché ===
    current_date += timedelta(days=25)
    portfolio._update_investment_with_date("Actions Apple", 145.0, current_date)  # Baisse
    portfolio._update_investment_with_date("Bitcoin", 32000.0, current_date)  # Correction crypto
    portfolio._update_investment_with_date("Actions Tesla", 180.0, current_date)  # -10%
    
    # Nouvel investissement défensif
    current_date += timedelta(days=10)
    portfolio._add_investment_with_date("Obligations", 95.0, 30, current_date)  # 2850€
    
    # === MAI - Récupération ===
    current_date += timedelta(days=20)
    portfolio._update_investment_with_date("Actions Apple", 175.0, current_date)  # Rebond
    portfolio._update_investment_with_date("Bitcoin", 48000.0, current_date)  # Rebond crypto
    portfolio._update_investment_with_date("ETF S&P 500", 420.0, current_date)  # Nouveau record
    
    # Vente partielle pour prendre des bénéfices
    current_date += timedelta(days=8)
    portfolio._sell_investment_with_date("Actions Apple", 5, current_date)  # Vente de 5 actions
    
    # === JUIN - Diversification ===
    current_date += timedelta(days=15)
    portfolio._add_investment_with_date("Actions Microsoft", 320.0, 8, current_date)  # 2560€
    portfolio._add_investment_with_date("ETF Europe", 45.0, 50, current_date)  # 2250€
    
    # Paiement supplémentaire sur le crédit
    current_date += timedelta(days=10)
    portfolio._pay_credit_with_date("Prêt Auto", 1000.0, current_date)
    
    # === Évolutions finales ===
    current_date = datetime.now() - timedelta(days=7)
    portfolio._update_investment_with_date("Actions Tesla", 220.0, current_date)  # +22.2%
    portfolio._update_investment_with_date("Bitcoin", 52000.0, current_date)  # Reprise
    portfolio._update_investment_with_date("Actions Microsoft", 335.0, current_date)  # +4.7%
    
    return portfolio

def _add_investment_with_date(self, name: str, initial_value: float, quantity: float, date: datetime):
    """Ajoute un investissement avec une date spécifique"""
    total_cost = initial_value * quantity
    if total_cost <= self.cash:
        self.cash -= total_cost
        investment = Investment(name, initial_value, initial_value, quantity)
        investment.purchase_date = date
        self.investments[name] = investment
        self.transaction_history.append({
            'date': date.strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'INVESTMENT_BUY',
            'amount': total_cost,
            'description': f'Achat de {quantity} parts de {name}'
        })

def _update_investment_with_date(self, name: str, new_value: float, date: datetime):
    """Met à jour la valeur d'un investissement avec une date spécifique"""
    if name in self.investments:
        old_value = self.investments[name].current_value
        self.investments[name].update_value(new_value)
        self.transaction_history.append({
            'date': date.strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'INVESTMENT_UPDATE',
            'amount': 0,
            'description': f'{name}: {old_value:.2f}€ → {new_value:.2f}€'
        })

def _sell_investment_with_date(self, name: str, quantity: float, date: datetime):
    """Vend un investissement avec une date spécifique"""
    if name in self.investments:
        investment = self.investments[name]
        sale_value = investment.current_value * quantity
        self.cash += sale_value
        investment.quantity -= quantity
        self.transaction_history.append({
            'date': date.strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'INVESTMENT_SELL',
            'amount': sale_value,
            'description': f'Vente de {quantity} parts de {name}'
        })

def _add_credit_with_date(self, name: str, amount: float, interest_rate: float, monthly_payment: float, date: datetime):
    """Ajoute un crédit avec une date spécifique"""
    credit = Credit(name, amount, interest_rate, monthly_payment)
    credit.creation_date = date
    self.credits[name] = credit
    self.cash += amount
    self.transaction_history.append({
        'date': date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'CREDIT_ADD',
        'amount': amount,
        'description': f'Nouveau crédit: {name} à {interest_rate}%'
    })

def _pay_credit_with_date(self, name: str, amount: float, date: datetime):
    """Effectue un paiement sur un crédit avec une date spécifique"""
    if name in self.credits:
        self.cash -= amount
        self.credits[name].make_payment(amount)
        self.transaction_history.append({
            'date': date.strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'CREDIT_PAYMENT',
            'amount': amount,
            'description': f'Paiement sur {name}'
        })
