import datetime

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

