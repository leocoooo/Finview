from datetime import datetime, timedelta
from portfolio_package.models import Portfolio, Investment, Credit, FinancialInvestment, RealEstateInvestment

def create_demo_portfolio():
    """Crée un portefeuille de démonstration avec un historique simulé"""
    portfolio = Portfolio(initial_cash=5000.0)
    
    # Simulation sur les 6 derniers mois
    base_date = datetime.now() - timedelta(days=180)
    
    # === JANVIER - Début du portefeuille ===
    current_date = base_date
    
    # Ajout initial de fonds
    portfolio.cash = 25000.0
    portfolio.transaction_history.append({
        'date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'CASH_ADD',
        'amount': 20000.0,
        'description': 'Apport initial'
    })
    
    # Premiers investissements financiers
    current_date += timedelta(days=3)
    portfolio._add_financial_investment_with_date("Actions Apple", 150.0, 20, current_date, "Action")  # 3000€

    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("ETF S&P 500", 400.0, 10, current_date, "ETF")  # 4000€

    current_date += timedelta(days=7)
    portfolio._add_financial_investment_with_date("Bitcoin", 35000.0, 0.2, current_date, "Crypto")  # 7000€
    
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
    portfolio._add_financial_investment_with_date("Actions Tesla", 200.0, 15, current_date, "Action")  # 3000€
    
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
    portfolio._add_financial_investment_with_date("Obligations", 95.0, 30, current_date, "Obligation")  # 2850€
    
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
    portfolio._add_financial_investment_with_date("Actions Microsoft", 320.0, 8, current_date, "Action")  # 2560€
    portfolio._add_financial_investment_with_date("ETF Europe", 45.0, 50, current_date, "ETF")  # 2250€

    # Premiers investissements immobiliers
    current_date += timedelta(days=5)
    portfolio._add_real_estate_investment_with_date("SCPI Bureaux Paris", 200.0, 25, current_date, "SCPI", "Paris", 4.2)  # 5000€

    current_date += timedelta(days=10)
    portfolio._add_real_estate_investment_with_date("REIT Résidentiel US", 85.0, 35, current_date, "REIT", "États-Unis", 3.8)  # 2975€

    # Paiement supplémentaire sur le crédit
    current_date += timedelta(days=10)
    portfolio._pay_credit_with_date("Prêt Auto", 1000.0, current_date)
    
    # === Évolutions finales ===
    current_date = datetime.now() - timedelta(days=7)
    portfolio._update_investment_with_date("Actions Tesla", 220.0, current_date)  # +22.2%
    portfolio._update_investment_with_date("Bitcoin", 52000.0, current_date)  # Reprise
    portfolio._update_investment_with_date("Actions Microsoft", 335.0, current_date)  # +4.7%

    # Évolution des investissements immobiliers
    portfolio._update_investment_with_date("SCPI Bureaux Paris", 205.0, current_date)  # +2.5%
    portfolio._update_investment_with_date("REIT Résidentiel US", 88.0, current_date)  # +3.5%
    
    return portfolio

# Méthodes helper pour Portfolio avec dates spécifiques
def _add_financial_investment_with_date(self, name: str, initial_value: float, quantity: float, date: datetime, investment_type: str = "Action"):
    """Ajoute un investissement financier avec une date spécifique"""
    total_cost = initial_value * quantity
    if total_cost <= self.cash:
        self.cash -= total_cost
        investment = FinancialInvestment(name, initial_value, initial_value, quantity, investment_type)
        investment.purchase_date = date
        self.financial_investments[name] = investment
        self.transaction_history.append({
            'date': date.strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'FINANCIAL_INVESTMENT_BUY',
            'amount': total_cost,
            'description': f'Achat de {quantity} parts de {name} ({investment_type})'
        })

def _add_real_estate_investment_with_date(self, name: str, initial_value: float, quantity: float, date: datetime,
                                        property_type: str = "SCPI", location: str = "", rental_yield: float = 0.0):
    """Ajoute un investissement immobilier avec une date spécifique"""
    total_cost = initial_value * quantity
    if total_cost <= self.cash:
        self.cash -= total_cost
        investment = RealEstateInvestment(name, initial_value, initial_value, quantity, property_type, location, rental_yield)
        investment.purchase_date = date
        self.real_estate_investments[name] = investment
        self.transaction_history.append({
            'date': date.strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'REAL_ESTATE_INVESTMENT_BUY',
            'amount': total_cost,
            'description': f'Achat de {quantity} parts de {name} ({property_type})'
        })

def _add_investment_with_date(self, name: str, initial_value: float, quantity: float, date: datetime):
    """Ajoute un investissement avec une date spécifique - méthode de compatibilité"""
    return self._add_financial_investment_with_date(name, initial_value, quantity, date)


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

# Patch toutes les méthodes helper sur la classe Portfolio
Portfolio._add_financial_investment_with_date = _add_financial_investment_with_date
Portfolio._add_real_estate_investment_with_date = _add_real_estate_investment_with_date
Portfolio._add_investment_with_date = _add_investment_with_date
Portfolio._add_credit_with_date = _add_credit_with_date
Portfolio._pay_credit_with_date = _pay_credit_with_date
Portfolio._update_investment_with_date = _update_investment_with_date
Portfolio._sell_investment_with_date = _sell_investment_with_date
