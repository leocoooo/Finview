from datetime import datetime, timedelta
from portfolio_package.models import Portfolio, Investment, Credit, FinancialInvestment, RealEstateInvestment

def create_demo_portfolio():
    """Creates a demo portfolio with simulated history"""
    portfolio = Portfolio(initial_cash=5000.0)

    # Simulation over the last 6 months
    base_date = datetime.now() - timedelta(days=180)

    # === JANUARY - Portfolio start ===
    current_date = base_date

    # Initial fund addition
    portfolio.cash = 25000.0
    portfolio.transaction_history.append({
        'date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'CASH_ADD',
        'amount': 20000.0,
        'description': 'Initial deposit'
    })

    # First financial investments
    current_date += timedelta(days=3)
    portfolio._add_financial_investment_with_date("Apple Stock", 150.0, 20, current_date, "Stock")  # 3000€

    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("S&P 500 ETF", 400.0, 10, current_date, "ETF")  # 4000€

    current_date += timedelta(days=7)
    portfolio._add_financial_investment_with_date("Bitcoin", 35000.0, 0.2, current_date, "Crypto")  # 7000€

    # === FEBRUARY - Portfolio expansion ===
    current_date += timedelta(days=15)
    portfolio.cash += 3000.0
    portfolio.transaction_history.append({
        'date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'CASH_ADD',
        'amount': 3000.0,
        'description': 'Monthly bonus'
    })

    current_date += timedelta(days=3)
    portfolio._add_financial_investment_with_date("Tesla Stock", 200.0, 15, current_date, "Stock")  # 3000€

    # First credit
    current_date += timedelta(days=10)
    portfolio._add_credit_with_date("Car Loan", 12000.0, 2.5, 280, current_date)

    # === MARCH - Price changes ===
    current_date += timedelta(days=20)
    portfolio._update_investment_with_date("Apple Stock", 165.0, current_date)  # +10%
    portfolio._update_investment_with_date("Bitcoin", 42000.0, current_date)  # +20%
    portfolio._update_investment_with_date("S&P 500 ETF", 385.0, current_date)  # -3.75%

    # Credit payment
    current_date += timedelta(days=5)
    portfolio._pay_credit_with_date("Car Loan", 500.0, current_date)

    # === APRIL - Market correction ===
    current_date += timedelta(days=25)
    portfolio._update_investment_with_date("Apple Stock", 145.0, current_date)  # Drop
    portfolio._update_investment_with_date("Bitcoin", 32000.0, current_date)  # Crypto correction
    portfolio._update_investment_with_date("Tesla Stock", 180.0, current_date)  # -10%

    # New defensive investment
    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Bonds", 95.0, 30, current_date, "Bond")  # 2850€

    # === MAY - Recovery ===
    current_date += timedelta(days=20)
    portfolio._update_investment_with_date("Apple Stock", 175.0, current_date)  # Rebound
    portfolio._update_investment_with_date("Bitcoin", 48000.0, current_date)  # Crypto rebound
    portfolio._update_investment_with_date("S&P 500 ETF", 420.0, current_date)  # New high

    # Partial sale to take profits
    current_date += timedelta(days=8)
    portfolio._sell_investment_with_date("Apple Stock", 5, current_date)  # Sale of 5 shares

    # === JUNE - Diversification ===
    current_date += timedelta(days=15)
    portfolio._add_financial_investment_with_date("Microsoft Stock", 320.0, 8, current_date, "Stock")  # 2560€
    portfolio._add_financial_investment_with_date("Europe ETF", 45.0, 50, current_date, "ETF")  # 2250€

    # First real estate investments
    current_date += timedelta(days=5)
    portfolio._add_real_estate_investment_with_date("Paris Office SCPI", 200.0, 25, current_date, "SCPI", "Paris", 4.2)  # 5000€

    current_date += timedelta(days=10)
    portfolio._add_real_estate_investment_with_date("US Residential REIT", 85.0, 35, current_date, "REIT", "United States", 3.8)  # 2975€

    # Additional payment on credit
    current_date += timedelta(days=10)
    portfolio._pay_credit_with_date("Car Loan", 1000.0, current_date)

    # === Final changes ===
    current_date = datetime.now() - timedelta(days=7)
    portfolio._update_investment_with_date("Tesla Stock", 220.0, current_date)  # +22.2%
    portfolio._update_investment_with_date("Bitcoin", 52000.0, current_date)  # Recovery
    portfolio._update_investment_with_date("Microsoft Stock", 335.0, current_date)  # +4.7%

    # Real estate investment changes
    portfolio._update_investment_with_date("Paris Office SCPI", 205.0, current_date)  # +2.5%
    portfolio._update_investment_with_date("US Residential REIT", 88.0, current_date)  # +3.5%

    return portfolio

# Helper methods for Portfolio with specific dates
def _add_financial_investment_with_date(self, name: str, initial_value: float, quantity: float, date: datetime, investment_type: str = "Stock"):
    """Adds a financial investment with a specific date"""
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
            'description': f'Purchase of {quantity} shares of {name} ({investment_type})'
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
            'amount': 0,
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
Portfolio._add_financial_investment_with_date = _add_financial_investment_with_date
Portfolio._add_real_estate_investment_with_date = _add_real_estate_investment_with_date
Portfolio._add_investment_with_date = _add_investment_with_date
Portfolio._add_credit_with_date = _add_credit_with_date
Portfolio._pay_credit_with_date = _pay_credit_with_date
Portfolio._update_investment_with_date = _update_investment_with_date
Portfolio._sell_investment_with_date = _sell_investment_with_date
