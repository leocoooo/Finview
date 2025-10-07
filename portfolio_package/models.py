from datetime import datetime
from typing import Dict, List

from datetime import datetime


class Investment:
    def __init__(self, name: str, initial_value: float, current_value: float, quantity: float = 1.0):
        self.name = name
        self.initial_value = initial_value
        self.current_value = current_value
        self.quantity = quantity
        self.purchase_date = datetime.now()

    def update_value(self, new_value: float):
        self.current_value = new_value

    def get_total_value(self) -> float:
        return self.current_value * self.quantity

    def get_gain_loss(self) -> float:
        return (self.current_value - self.initial_value) * self.quantity

    def get_gain_loss_percentage(self) -> float:
        if self.initial_value == 0:
            return 0
        return ((self.current_value - self.initial_value) / self.initial_value) * 100


class FinancialInvestment(Investment):
    """Traditional financial investments (stocks, bonds, ETFs, crypto, etc.)"""
    def __init__(self, name: str, initial_value: float, current_value: float, quantity: float = 1.0,
                 investment_type: str = "Stock", location: str = ""):
        super().__init__(name, initial_value, current_value, quantity)
        self.investment_type = investment_type  # Stock, ETF, Bond, Crypto, etc.
        self.location = location  # Ex: 'USA', 'Europe', 'France', 'Global'

    def __repr__(self):
        loc_str = f" in {self.location}" if self.location else ""
        return f"<FinancialInvestment: {self.name} ({self.investment_type}){loc_str} - {self.quantity} units>"


class RealEstateInvestment(Investment):
    """Real estate investments (SCPI, REIT, direct real estate, etc.)"""
    def __init__(self, name: str, initial_value: float, current_value: float, quantity: float = 1.0,
                 property_type: str = "SCPI", location: str = "", rental_yield: float = 0.0):
        super().__init__(name, initial_value, current_value, quantity)
        self.property_type = property_type  # SCPI, REIT, Direct real estate, etc.
        self.location = location
        self.rental_yield = rental_yield  # Annual rental yield in %

    def get_annual_rental_income(self) -> float:
        """Calculates estimated annual rental income"""
        return self.get_total_value() * (self.rental_yield / 100)

    def __repr__(self):
        return (f"<RealEstateInvestment: {self.name} ({self.property_type}) in {self.location} - "
                f"{self.quantity} units, yield {self.rental_yield}%>")


class Credit:
    def __init__(self, name: str, initial_amount: float, interest_rate: float, monthly_payment: float = 0):
        self.name = name
        self.initial_amount = initial_amount
        self.current_balance = initial_amount
        self.interest_rate = interest_rate
        self.monthly_payment = monthly_payment
        self.creation_date = datetime.now()
    
    def make_payment(self, amount: float):
        self.current_balance = max(0, self.current_balance - amount)
    
    def apply_interest(self, months: int = 1):
        monthly_rate = self.interest_rate / 100 / 12
        self.current_balance *= (1 + monthly_rate) ** months
    
    def get_remaining_balance(self) -> float:
        return self.current_balance


class Portfolio:
    def __init__(self, initial_cash: float = 0):
        self.cash = initial_cash
        self.financial_investments: Dict[str, FinancialInvestment] = {}
        self.real_estate_investments: Dict[str, RealEstateInvestment] = {}
        self.credits: Dict[str, Credit] = {}
        self.transaction_history: List[Dict] = []

    @property
    def investments(self):
        """Compatibility with old interface - returns all investments"""
        all_investments = {}
        all_investments.update(self.financial_investments)
        all_investments.update(self.real_estate_investments)
        return all_investments
    
    def add_cash(self, amount: float, description: str = "Cash deposit"):
        self.cash += amount
        self._log_transaction("CASH_ADD", amount, description)

    def withdraw_cash(self, amount: float, description: str = "Cash withdrawal"):
        if amount <= self.cash:
            self.cash -= amount
            self._log_transaction("CASH_WITHDRAW", amount, description)
            return True
        return False
    
    def add_financial_investment(self, name: str, initial_value: float, quantity: float = 1.0, investment_type: str = "Stock", location: str = ""):
        """Adds a financial investment"""
        total_cost = initial_value * quantity
        if total_cost <= self.cash:
            self.cash -= total_cost
            financial_inv = FinancialInvestment(name, initial_value, initial_value, quantity, investment_type)
            if location:
                financial_inv.location = location  # Add location
            self.financial_investments[name] = financial_inv
            self._log_transaction("FINANCIAL_INVESTMENT_BUY", total_cost, f"Purchase of {quantity} shares of {name} ({investment_type})")
            return True
        return False

    def add_real_estate_investment(self, name: str, initial_value: float, quantity: float = 1.0,
                                 property_type: str = "SCPI", location: str = "", rental_yield: float = 0.0):
        """Adds a real estate investment"""
        total_cost = initial_value * quantity
        if total_cost <= self.cash:
            self.cash -= total_cost
            self.real_estate_investments[name] = RealEstateInvestment(name, initial_value, initial_value, quantity,
                                                                    property_type, location, rental_yield)
            self._log_transaction("REAL_ESTATE_INVESTMENT_BUY", total_cost, f"Purchase of {quantity} shares of {name} ({property_type})")
            return True
        return False

    def add_investment(self, name: str, initial_value: float, quantity: float = 1.0):
        """Compatibility method - adds a financial investment by default"""
        return self.add_financial_investment(name, initial_value, quantity)
    
    def update_investment_value(self, name: str, new_value: float):
        if name in self.investments:
            old_value = self.investments[name].current_value
            self.investments[name].update_value(new_value)
            self._log_transaction("INVESTMENT_UPDATE", 0, f"{name}: {old_value:.2f}€ → {new_value:.2f}€")
    
    def sell_investment(self, name: str, quantity: float = None):
        if name not in self.investments:
            return False

        investment = self.investments[name]
        if quantity is None or quantity >= investment.quantity:
            sale_value = investment.get_total_value()
            self.cash += sale_value
            self._log_transaction("INVESTMENT_SELL", sale_value, f"Full sale of {name}")
            del self.investments[name]
        else:
            sale_value = investment.current_value * quantity
            self.cash += sale_value
            investment.quantity -= quantity
            self._log_transaction("INVESTMENT_SELL", sale_value, f"Sale of {quantity} shares of {name}")
        return True
    
    def add_credit(self, name: str, amount: float, interest_rate: float, monthly_payment: float = 0):
        if name in self.credits:
            return False
        self.credits[name] = Credit(name, amount, interest_rate, monthly_payment)
        self.cash += amount
        self._log_transaction("CREDIT_ADD", amount, f"New credit: {name} at {interest_rate}%")
        return True
    
    def pay_credit(self, name: str, amount: float):
        if name not in self.credits or amount > self.cash:
            return False

        self.cash -= amount
        self.credits[name].make_payment(amount)
        self._log_transaction("CREDIT_PAYMENT", amount, f"Payment on {name}")

        if self.credits[name].get_remaining_balance() <= 0.01:
            del self.credits[name]
        return True
    
    def get_financial_investments_value(self) -> float:
        """Returns the total value of financial investments"""
        return sum(inv.get_total_value() for inv in self.financial_investments.values())

    def get_real_estate_investments_value(self) -> float:
        """Returns the total value of real estate investments"""
        return sum(inv.get_total_value() for inv in self.real_estate_investments.values())

    def get_total_investments_value(self) -> float:
        """Returns the total value of all investments"""
        return self.get_financial_investments_value() + self.get_real_estate_investments_value()

    def get_total_annual_rental_income(self) -> float:
        """Returns the total annual rental income from real estate investments"""
        return sum(inv.get_annual_rental_income() for inv in self.real_estate_investments.values())
    
    def get_total_credits_balance(self) -> float:
        return sum(credit.get_remaining_balance() for credit in self.credits.values())
    
    def get_net_worth(self) -> float:
        return self.cash + self.get_total_investments_value() - self.get_total_credits_balance()
    
    def _log_transaction(self, transaction_type: str, amount: float, description: str):
        self.transaction_history.append({
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': transaction_type,
            'amount': amount,
            'description': description
        })
    
    def to_dict(self):
        """Serializes the portfolio to a dictionary"""
        return {
            'cash': self.cash,
            'financial_investments': {
                name: {
                    'name': inv.name,
                    'initial_value': inv.initial_value,
                    'current_value': inv.current_value,
                    'quantity': inv.quantity,
                    'purchase_date': inv.purchase_date.isoformat(),
                    'investment_type': inv.investment_type
                } for name, inv in self.financial_investments.items()
            },
            'real_estate_investments': {
                name: {
                    'name': inv.name,
                    'initial_value': inv.initial_value,
                    'current_value': inv.current_value,
                    'quantity': inv.quantity,
                    'purchase_date': inv.purchase_date.isoformat(),
                    'property_type': inv.property_type,
                    'location': inv.location,
                    'rental_yield': inv.rental_yield
                } for name, inv in self.real_estate_investments.items()
            },
            'credits': {
                name: {
                    'name': credit.name,
                    'initial_amount': credit.initial_amount,
                    'current_balance': credit.current_balance,
                    'interest_rate': credit.interest_rate,
                    'monthly_payment': credit.monthly_payment,
                    'creation_date': credit.creation_date.isoformat()
                } for name, credit in self.credits.items()
            },
            'transaction_history': self.transaction_history
        }
    
    @classmethod
    def from_dict(cls, data):
        """Recreates a portfolio from a dictionary"""
        portfolio = cls(data['cash'])

        # Restore financial investments
        for name, inv_data in data.get('financial_investments', {}).items():
            investment = FinancialInvestment(
                inv_data['name'],
                inv_data['initial_value'],
                inv_data['current_value'],
                inv_data['quantity'],
                inv_data.get('investment_type', 'Stock')
            )
            investment.purchase_date = datetime.fromisoformat(inv_data['purchase_date'])
            portfolio.financial_investments[name] = investment

        # Restore real estate investments
        for name, inv_data in data.get('real_estate_investments', {}).items():
            investment = RealEstateInvestment(
                inv_data['name'],
                inv_data['initial_value'],
                inv_data['current_value'],
                inv_data['quantity'],
                inv_data.get('property_type', 'SCPI'),
                inv_data.get('location', ''),
                inv_data.get('rental_yield', 0.0)
            )
            investment.purchase_date = datetime.fromisoformat(inv_data['purchase_date'])
            portfolio.real_estate_investments[name] = investment

        # Compatibility with old investment format
        for name, inv_data in data.get('investments', {}).items():
            investment = FinancialInvestment(
                inv_data['name'],
                inv_data['initial_value'],
                inv_data['current_value'],
                inv_data['quantity']
            )
            investment.purchase_date = datetime.fromisoformat(inv_data['purchase_date'])
            portfolio.financial_investments[name] = investment

        # Restore credits
        for name, credit_data in data.get('credits', {}).items():
            credit = Credit(
                credit_data['name'],
                credit_data['initial_amount'],
                credit_data['interest_rate'],
                credit_data['monthly_payment']
            )
            credit.current_balance = credit_data['current_balance']
            credit.creation_date = datetime.fromisoformat(credit_data['creation_date'])
            portfolio.credits[name] = credit

        # Restore history
        portfolio.transaction_history = data.get('transaction_history', [])

        return portfolio
