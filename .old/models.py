"""
Portfolio models - Core business logic for investments and credits
"""

from datetime import datetime
from typing import Dict, List, Optional, Union


class Investment:
    """Base class for all investment types"""
    
    def __init__(self, name: str, initial_value: float, current_value: float, quantity: float = 1.0):
        self.name = name
        self.initial_value = initial_value
        self.current_value = current_value
        self.quantity = quantity
        self.purchase_date = datetime.now()

    def update_value(self, new_value: float) -> None:
        """Update the current value of the investment"""
        self.current_value = new_value

    def get_total_value(self) -> float:
        """Calculate total value (current_value × quantity)"""
        return self.current_value * self.quantity

    def get_gain_loss(self) -> float:
        """Calculate absolute gain/loss"""
        return (self.current_value - self.initial_value) * self.quantity

    def get_gain_loss_percentage(self) -> float:
        """Calculate percentage gain/loss"""
        if self.initial_value == 0:
            return 0
        return ((self.current_value - self.initial_value) / self.initial_value) * 100


class FinancialInvestment(Investment):
    """
    Traditional financial investments
    Supports: stocks, bonds, ETFs, crypto, funds, etc.
    """
    
    def __init__(
        self, 
        name: str, 
        initial_value: float, 
        current_value: float, 
        quantity: float = 1.0,
        investment_type: str = "Stock", 
        location: str = ""
    ):
        super().__init__(name, initial_value, current_value, quantity)
        self.investment_type = investment_type  # Stock, ETF, Bond, Crypto, Fund, Other
        self.location = location  # Geographic location (USA, Europe, Global, etc.)

    def __repr__(self) -> str:
        loc_str = f" in {self.location}" if self.location else ""
        return f"<FinancialInvestment: {self.name} ({self.investment_type}){loc_str} - {self.quantity} units>"


class RealEstateInvestment(Investment):
    """
    Real estate investments
    Supports: SCPI, REIT, direct real estate, real estate companies, etc.
    """
    
    def __init__(
        self, 
        name: str, 
        initial_value: float, 
        current_value: float, 
        quantity: float = 1.0,
        property_type: str = "SCPI", 
        location: str = "", 
        rental_yield: float = 0.0
    ):
        super().__init__(name, initial_value, current_value, quantity)
        self.property_type = property_type  # SCPI, REIT, Direct real estate, etc.
        self.location = location
        self.rental_yield = rental_yield  # Annual rental yield in %

    def get_annual_rental_income(self) -> float:
        """Calculate estimated annual rental income based on yield"""
        return self.get_total_value() * (self.rental_yield / 100)

    def __repr__(self) -> str:
        return (f"<RealEstateInvestment: {self.name} ({self.property_type}) in {self.location} - "
                f"{self.quantity} units, yield {self.rental_yield}%>")


class Credit:
    """Credit/Loan with interest rate and payment tracking"""
    
    def __init__(
        self, 
        name: str, 
        initial_amount: float, 
        interest_rate: float, 
        monthly_payment: float = 0
    ):
        self.name = name
        self.initial_amount = initial_amount
        self.current_balance = initial_amount
        self.interest_rate = interest_rate  # Annual interest rate in %
        self.monthly_payment = monthly_payment
        self.creation_date = datetime.now()
    
    def make_payment(self, amount: float) -> None:
        """Make a payment on the credit"""
        self.current_balance = max(0, self.current_balance - amount)
    
    def apply_interest(self, months: int = 1) -> None:
        """Apply interest for a given number of months"""
        monthly_rate = self.interest_rate / 100 / 12
        self.current_balance *= (1 + monthly_rate) ** months
    
    def get_remaining_balance(self) -> float:
        """Get the remaining balance to pay"""
        return self.current_balance


class Portfolio:
    """
    Main portfolio class managing cash, investments, and credits
    
    Attributes:
        cash: Available cash
        financial_investments: Dictionary of FinancialInvestment objects
        real_estate_investments: Dictionary of RealEstateInvestment objects
        credits: Dictionary of Credit objects
        transaction_history: List of all transactions
    """
    
    def __init__(self, initial_cash: float = 0):
        self.cash = initial_cash
        self.financial_investments: Dict[str, FinancialInvestment] = {}
        self.real_estate_investments: Dict[str, RealEstateInvestment] = {}
        self.credits: Dict[str, Credit] = {}
        self.transaction_history: List[Dict] = []

    @property
    def investments(self) -> Dict[str, Union[FinancialInvestment, RealEstateInvestment]]:
        """
        Compatibility property - returns all investments combined
        Useful for legacy code that doesn't distinguish between types
        """
        all_investments = {}
        all_investments.update(self.financial_investments)
        all_investments.update(self.real_estate_investments)
        return all_investments
    
    # === CASH MANAGEMENT ===
    
    def add_cash(self, amount: float, description: str = "Cash deposit") -> None:
        """Add cash to the portfolio"""
        self.cash += amount
        self._log_transaction("CASH_ADD", amount, description)

    def withdraw_cash(self, amount: float, description: str = "Cash withdrawal") -> bool:
        """
        Withdraw cash from the portfolio
        Returns True if successful, False if insufficient funds
        """
        if amount <= self.cash:
            self.cash -= amount
            self._log_transaction("CASH_WITHDRAW", amount, description)
            return True
        return False
    
    # === INVESTMENT MANAGEMENT ===
    
    def add_financial_investment(
        self, 
        name: str, 
        initial_value: float, 
        quantity: float = 1.0, 
        investment_type: str = "Stock", 
        location: str = ""
    ) -> bool:
        """
        Add a financial investment
        Returns True if successful (sufficient cash), False otherwise
        """
        total_cost = initial_value * quantity
        if total_cost <= self.cash:
            self.cash -= total_cost
            financial_inv = FinancialInvestment(name, initial_value, initial_value, quantity, investment_type, location)
            self.financial_investments[name] = financial_inv
            self._log_transaction(
                "FINANCIAL_INVESTMENT_BUY", 
                total_cost, 
                f"Purchase of {quantity} shares of {name} ({investment_type})"
            )
            return True
        return False

    def add_real_estate_investment(
        self, 
        name: str, 
        initial_value: float, 
        quantity: float = 1.0,
        property_type: str = "SCPI", 
        location: str = "", 
        rental_yield: float = 0.0
    ) -> bool:
        """
        Add a real estate investment
        Returns True if successful (sufficient cash), False otherwise
        """
        total_cost = initial_value * quantity
        if total_cost <= self.cash:
            self.cash -= total_cost
            self.real_estate_investments[name] = RealEstateInvestment(
                name, initial_value, initial_value, quantity,
                property_type, location, rental_yield
            )
            self._log_transaction(
                "REAL_ESTATE_INVESTMENT_BUY", 
                total_cost, 
                f"Purchase of {quantity} shares of {name} ({property_type})"
            )
            return True
        return False

    def add_investment(self, name: str, initial_value: float, quantity: float = 1.0) -> bool:
        """
        Compatibility method - adds a financial investment by default
        For backward compatibility with older code
        """
        return self.add_financial_investment(name, initial_value, quantity)
    
    def update_investment_value(self, name: str, new_value: float) -> bool:
        """
        Update the current value of an investment
        Returns True if investment exists, False otherwise
        """
        if name in self.investments:
            old_value = self.investments[name].current_value
            self.investments[name].update_value(new_value)
            self._log_transaction(
                "INVESTMENT_UPDATE", 
                0, 
                f"{name}: {old_value:.2f}€ → {new_value:.2f}€"
            )
            return True
        return False
    
    def sell_investment(self, name: str, quantity: Optional[float] = None) -> bool:
        """
        Sell an investment (fully or partially)
        
        Args:
            name: Investment name
            quantity: Number of shares to sell (None = sell all)
            
        Returns:
            True if successful, False if investment not found
        """
        # Find which dictionary contains the investment
        if name in self.financial_investments:
            investment = self.financial_investments[name]
            investment_dict = self.financial_investments
        elif name in self.real_estate_investments:
            investment = self.real_estate_investments[name]
            investment_dict = self.real_estate_investments
        else:
            return False

        if quantity is None or quantity >= investment.quantity:
            # Full sale
            sale_value = investment.get_total_value()
            self.cash += sale_value
            self._log_transaction("INVESTMENT_SELL", sale_value, f"Full sale of {name}")
            del investment_dict[name]
        else:
            # Partial sale
            sale_value = investment.current_value * quantity
            self.cash += sale_value
            investment.quantity -= quantity
            self._log_transaction(
                "INVESTMENT_SELL", 
                sale_value, 
                f"Sale of {quantity} shares of {name}"
            )
        
        return True
    
    # === CREDIT MANAGEMENT ===
    
    def add_credit(
        self, 
        name: str, 
        amount: float, 
        interest_rate: float, 
        monthly_payment: float = 0
    ) -> bool:
        """
        Add a credit/loan
        Returns True if successful, False if credit already exists
        """
        if name in self.credits:
            return False
        self.credits[name] = Credit(name, amount, interest_rate, monthly_payment)
        self.cash += amount
        self._log_transaction("CREDIT_ADD", amount, f"New credit: {name} at {interest_rate}%")
        return True
    
    def pay_credit(self, name: str, amount: float) -> bool:
        """
        Make a payment on a credit
        Returns True if successful, False if credit doesn't exist or insufficient cash
        """
        if name not in self.credits or amount > self.cash:
            return False

        self.cash -= amount
        self.credits[name].make_payment(amount)
        self._log_transaction("CREDIT_PAYMENT", amount, f"Payment on {name}")

        # Remove credit if fully paid
        if self.credits[name].get_remaining_balance() <= 0.01:
            del self.credits[name]
        return True
    
    # === PORTFOLIO METRICS ===
    
    def get_financial_investments_value(self) -> float:
        """Calculate total value of financial investments"""
        return sum(inv.get_total_value() for inv in self.financial_investments.values())

    def get_real_estate_investments_value(self) -> float:
        """Calculate total value of real estate investments"""
        return sum(inv.get_total_value() for inv in self.real_estate_investments.values())

    def get_total_investments_value(self) -> float:
        """Calculate total value of all investments"""
        return self.get_financial_investments_value() + self.get_real_estate_investments_value()

    def get_total_annual_rental_income(self) -> float:
        """Calculate total annual rental income from real estate"""
        return sum(inv.get_annual_rental_income() for inv in self.real_estate_investments.values())
    
    def get_total_credits_balance(self) -> float:
        """Calculate total remaining balance on all credits"""
        return sum(credit.get_remaining_balance() for credit in self.credits.values())
    
    def get_net_worth(self) -> float:
        """Calculate net worth (assets - liabilities)"""
        return self.cash + self.get_total_investments_value() - self.get_total_credits_balance()
    
    # === TRANSACTION LOGGING ===
    
    def _log_transaction(self, transaction_type: str, amount: float, description: str) -> None:
        """Internal method to log transactions"""
        self.transaction_history.append({
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': transaction_type,
            'amount': amount,
            'description': description
        })
    
    # === SERIALIZATION ===
    
    def to_dict(self) -> Dict:
        """Serialize portfolio to dictionary for saving"""
        return {
            'cash': self.cash,
            'financial_investments': {
                name: {
                    'name': inv.name,
                    'initial_value': inv.initial_value,
                    'current_value': inv.current_value,
                    'quantity': inv.quantity,
                    'purchase_date': inv.purchase_date.isoformat(),
                    'investment_type': inv.investment_type,
                    'location': inv.location
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
    def from_dict(cls, data: Dict) -> 'Portfolio':
        """Recreate portfolio from dictionary (deserialization)"""
        portfolio = cls(data['cash'])

        # Restore financial investments
        for name, inv_data in data.get('financial_investments', {}).items():
            investment = FinancialInvestment(
                inv_data['name'],
                inv_data['initial_value'],
                inv_data['current_value'],
                inv_data['quantity'],
                inv_data.get('investment_type', 'Stock'),
                inv_data.get('location', '')
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

        # Backward compatibility with old 'investments' format
        for name, inv_data in data.get('investments', {}).items():
            investment = FinancialInvestment(
                inv_data['name'],
                inv_data['initial_value'],
                inv_data['current_value'],
                inv_data['quantity'],
                inv_data.get('investment_type', 'Stock'),
                inv_data.get('location', '')
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

        # Restore transaction history
        portfolio.transaction_history = data.get('transaction_history', [])

        return portfolio