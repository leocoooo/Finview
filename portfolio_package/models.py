from datetime import datetime
from typing import Dict, List

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
        self.investments: Dict[str, Investment] = {}
        self.credits: Dict[str, Credit] = {}
        self.transaction_history: List[Dict] = []
    
    def add_cash(self, amount: float, description: str = "Ajout de liquidités"):
        self.cash += amount
        self._log_transaction("CASH_ADD", amount, description)
    
    def withdraw_cash(self, amount: float, description: str = "Retrait de liquidités"):
        if amount <= self.cash:
            self.cash -= amount
            self._log_transaction("CASH_WITHDRAW", amount, description)
            return True
        return False
    
    def add_investment(self, name: str, initial_value: float, quantity: float = 1.0):
        total_cost = initial_value * quantity
        if total_cost <= self.cash:
            self.cash -= total_cost
            self.investments[name] = Investment(name, initial_value, initial_value, quantity)
            self._log_transaction("INVESTMENT_BUY", total_cost, f"Achat de {quantity} parts de {name}")
            return True
        return False
    
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
            self._log_transaction("INVESTMENT_SELL", sale_value, f"Vente totale de {name}")
            del self.investments[name]
        else:
            sale_value = investment.current_value * quantity
            self.cash += sale_value
            investment.quantity -= quantity
            self._log_transaction("INVESTMENT_SELL", sale_value, f"Vente de {quantity} parts de {name}")
        return True
    
    def add_credit(self, name: str, amount: float, interest_rate: float, monthly_payment: float = 0):
        if name in self.credits:
            return False
        self.credits[name] = Credit(name, amount, interest_rate, monthly_payment)
        self.cash += amount
        self._log_transaction("CREDIT_ADD", amount, f"Nouveau crédit: {name} à {interest_rate}%")
        return True
    
    def pay_credit(self, name: str, amount: float):
        if name not in self.credits or amount > self.cash:
            return False
        
        self.cash -= amount
        self.credits[name].make_payment(amount)
        self._log_transaction("CREDIT_PAYMENT", amount, f"Paiement sur {name}")
        
        if self.credits[name].get_remaining_balance() <= 0.01:
            del self.credits[name]
        return True
    
    def get_total_investments_value(self) -> float:
        return sum(inv.get_total_value() for inv in self.investments.values())
    
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
        """Sérialise le portefeuille en dictionnaire"""
        return {
            'cash': self.cash,
            'investments': {
                name: {
                    'name': inv.name,
                    'initial_value': inv.initial_value,
                    'current_value': inv.current_value,
                    'quantity': inv.quantity,
                    'purchase_date': inv.purchase_date.isoformat()
                } for name, inv in self.investments.items()
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
        """Recrée un portefeuille à partir d'un dictionnaire"""
        portfolio = cls(data['cash'])
        
        # Restaurer les investissements
        for name, inv_data in data.get('investments', {}).items():
            investment = Investment(
                inv_data['name'],
                inv_data['initial_value'],
                inv_data['current_value'],
                inv_data['quantity']
            )
            investment.purchase_date = datetime.fromisoformat(inv_data['purchase_date'])
            portfolio.investments[name] = investment
        
        # Restaurer les crédits
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
        
        # Restaurer l'historique
        portfolio.transaction_history = data.get('transaction_history', [])
        
        return portfolio
