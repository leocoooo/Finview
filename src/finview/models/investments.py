import datetime 

class Investment:
    """Base class for all investment types"""
    
    def __init__(self, name: str, initial_value: float, current_value: float, quantity: float = 1.0):
        self.name = name
        self.initial_value = initial_value
        self.current_value = current_value
        self.quantity = quantity
        self.purchase_date = datetime.datetime.now()

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

