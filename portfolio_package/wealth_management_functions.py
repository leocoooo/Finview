from datetime import datetime
from portfolio_package.models import Portfolio, Credit, FinancialInvestment, RealEstateInvestment

# Helper methods for Portfolio with specific dates
def _add_cash_with_date(self, amount: float, date: datetime, description: str = "Cash addition"):
    self.cash += amount
    self.transaction_history.append({
        'date': date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'CASH_ADD',
        'amount': amount,
        'description': description
    })


def _add_financial_investment_with_date(self, name: str, initial_value: float, quantity: float, date: datetime,
                                       investment_type: str = "Stock", location: str = ""):
    """Adds a financial investment with a specific date and location"""
    total_cost = initial_value * quantity
    if total_cost <= self.cash:
        self.cash -= total_cost
       
        # Création de l'investissement financier avec localisation
        investment = FinancialInvestment(name, initial_value, initial_value, quantity, investment_type, location)
        investment.purchase_date = date
       
        # Enregistrement de l'investissement
        self.financial_investments[name] = investment
       
        # Historique de la transaction (AVEC name, price, quantity)
        self.transaction_history.append({
            'date': date.strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'FINANCIAL_INVESTMENT_BUY',
            'amount': total_cost,
            'name': name,  # AJOUT
            'price': initial_value,  # AJOUT
            'quantity': quantity,  # AJOUT
            'description': f'Purchase of {quantity} units of {name} ({investment_type}) in {location if location else "unspecified location"}'
        })


def _add_real_estate_investment_with_date(self, name: str, initial_value: float, quantity: float, date: datetime,
                                        property_type: str = "SCPI", location: str = "", rental_yield: float = 0.0):
    """Adds a real estate investment with a specific date"""
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
            'description': f'Purchase of {quantity} shares of {name} ({property_type})'
        })


# def _add_investment_with_date(self, name: str, initial_value: float, quantity: float, date: datetime):
    """Adds an investment with a specific date - compatibility method"""
    return self._add_financial_investment_with_date(name, initial_value, quantity, date)


def _add_investment_with_date(self, name: str, initial_value: float, quantity: float, date: datetime):
    """Adds an investment with a specific date - compatibility method"""
    return self._add_financial_investment_with_date(name, initial_value, quantity, date)


def _update_investment_with_date(self, name: str, new_value: float, date: datetime):
    """Updates an investment value with a specific date"""
    if name in self.investments:
        old_value = self.investments[name].current_value
        self.investments[name].update_value(new_value)
        self.transaction_history.append({
            'date': date.strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'INVESTMENT_UPDATE',
            'amount': new_value,  # CHANGEMENT: mettre le nouveau prix au lieu de 0
            'name': name,  # AJOUT
            'price': new_value,  # AJOUT
            'description': f'{name}: {old_value:.2f}€ → {new_value:.2f}€'
        })


def _sell_investment_with_date(self, name: str, quantity: float, date: datetime):
    """Sells an investment with a specific date"""
    if name in self.investments:
        investment = self.investments[name]
        sale_value = investment.current_value * quantity
        self.cash += sale_value
        investment.quantity -= quantity
        self.transaction_history.append({
            'date': date.strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'INVESTMENT_SELL',
            'amount': sale_value,
            'description': f'Sale of {quantity} shares of {name}'
        })


def _add_credit_with_date(self, name: str, amount: float, interest_rate: float, monthly_payment: float, date: datetime):
    """Adds a credit with a specific date"""
    credit = Credit(name, amount, interest_rate, monthly_payment)
    credit.creation_date = date
    self.credits[name] = credit
    self.cash += amount
    self.transaction_history.append({
        'date': date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'CREDIT_ADD',
        'amount': amount,
        'description': f'New credit: {name} at {interest_rate}%'
    })


def _pay_credit_with_date(self, name: str, amount: float, date: datetime):
    """Makes a payment on a credit with a specific date"""
    if name in self.credits:
        self.cash -= amount
        self.credits[name].make_payment(amount)
        self.transaction_history.append({
            'date': date.strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'CREDIT_PAYMENT',
            'amount': amount,
            'description': f'Payment on {name}'
        })

# Patch all helper methods on the Portfolio class
Portfolio._add_cash_with_date = _add_cash_with_date
Portfolio._add_financial_investment_with_date = _add_financial_investment_with_date
Portfolio._add_real_estate_investment_with_date = _add_real_estate_investment_with_date
Portfolio._add_investment_with_date = _add_investment_with_date
Portfolio._add_credit_with_date = _add_credit_with_date
Portfolio._pay_credit_with_date = _pay_credit_with_date
Portfolio._update_investment_with_date = _update_investment_with_date
Portfolio._sell_investment_with_date = _sell_investment_with_date
