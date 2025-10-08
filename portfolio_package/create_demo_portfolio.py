from datetime import datetime, timedelta
from portfolio_package.models import Portfolio


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


def create_demo_portfolio_bis():
    """Creates a demo portfolio with simulated 5-year history"""
    portfolio = Portfolio(initial_cash=5000.0)

    # Simulation over the last 5 years
    base_date = datetime.now() - timedelta(days=1825)  # 5 years

    # === YEAR 1 - JANUARY - Portfolio start ===
    current_date = base_date

    # Initial fund addition
    portfolio._add_cash_with_date(20000.0, current_date, "Initial deposit")

    # First financial investments
    current_date += timedelta(days=3)
    portfolio._add_financial_investment_with_date("Apple Stock", 120.0, 25, current_date, "Stock", "United States")  # 3000€

    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("S&P 500 ETF", 350.0, 12, current_date, "ETF", "United States")  # 4200€

    current_date += timedelta(days=7)
    portfolio._add_financial_investment_with_date("Bitcoin", 28000.0, 0.25, current_date, "Crypto", "Global")  # 7000€

    # === YEAR 1 - MARCH ===
    current_date += timedelta(days=30)
    portfolio._add_cash_with_date(3000.0, current_date, "Quarterly bonus")

    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("Tesla Stock", 180.0, 15, current_date, "Stock", "United States")  # 2700€

    # First credit - Car loan
    current_date += timedelta(days=15)
    portfolio._add_credit_with_date("Car Loan", 15000.0, 2.8, 320, current_date)

    # === YEAR 1 - JUNE ===
    current_date += timedelta(days=60)
    portfolio._add_financial_investment_with_date("LVMH Stock", 650.0, 5, current_date, "Stock", "France")  # 3250€
    
    current_date += timedelta(days=10)
    portfolio._update_investment_with_date("Apple Stock", 135.0, current_date)  # +12.5%
    portfolio._update_investment_with_date("Bitcoin", 35000.0, current_date)  # +25%

    # === YEAR 1 - SEPTEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("Europe ETF", 42.0, 50, current_date, "ETF", "Europe")  # 2100€
    
    current_date += timedelta(days=15)
    portfolio._pay_credit_with_date("Car Loan", 500.0, current_date)

    # === YEAR 1 - DECEMBER ===
    current_date += timedelta(days=80)
    portfolio._add_cash_with_date(2500.0, current_date, "End of year bonus")
    
    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("Tokyo TOPIX ETF", 180.0, 12, current_date, "ETF", "Japan")  # 2160€
    
    current_date += timedelta(days=10)
    portfolio._update_investment_with_date("Tesla Stock", 210.0, current_date)  # +16.7%

    # === YEAR 2 - MARCH ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(5000.0, current_date, "Annual bonus")

    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("Amazon Stock", 2800.0, 2, current_date, "Stock", "United States")  # 5600€

    # === YEAR 2 - JUNE ===
    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("Bonds", 98.0, 35, current_date, "Bond", "France")  # 3430€
    
    current_date += timedelta(days=20)
    portfolio._update_investment_with_date("Bitcoin", 42000.0, current_date)  # +20%
    portfolio._update_investment_with_date("S&P 500 ETF", 380.0, current_date)  # +8.6%

    # === YEAR 2 - SEPTEMBER - MAJOR EVENT: Real Estate Purchase in Japan ===
    current_date += timedelta(days=90)
    
    # Mortgage for primary residence in Japan
    portfolio._add_credit_with_date("Japanese Mortgage", 200000.0, 1.5, 950, current_date)
    
    # Add the property to real estate investments
    current_date += timedelta(days=3)
    portfolio._add_real_estate_investment_with_date("Tokyo Apartment", 200000.0, 1, current_date, "Apartment", "Tokyo, Japan", 0.0)  # Primary residence, no rental yield

    # === YEAR 2 - DECEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(3000.0, current_date, "Year-end bonus")
    
    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("Sony Stock", 85.0, 25, current_date, "Stock", "Japan")  # 2125€
    
    current_date += timedelta(days=10)
    portfolio._pay_credit_with_date("Japanese Mortgage", 2000.0, current_date)

    # === YEAR 3 - MARCH ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(4500.0, current_date, "Quarterly bonus")

    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Paris Office SCPI", 210.0, 20, current_date, "SCPI", "France")  # 4200€

    # Market correction
    current_date += timedelta(days=20)
    portfolio._update_investment_with_date("Apple Stock", 125.0, current_date)  # -7.4%
    portfolio._update_investment_with_date("Tesla Stock", 190.0, current_date)  # -9.5%
    portfolio._update_investment_with_date("Bitcoin", 30000.0, current_date)  # -28.6%

    # === YEAR 3 - JUNE ===
    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("US Residential REIT", 75.0, 35, current_date, "REIT", "United States")  # 2625€
    
    current_date += timedelta(days=15)
    portfolio._sell_investment_with_date("Tesla Stock", 6, current_date)  # Partial sale for profit-taking

    # === YEAR 3 - SEPTEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(3500.0, current_date, "Freelance income")
    
    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Gold ETF", 160.0, 18, current_date, "ETF", "Global")  # 2880€
    
    current_date += timedelta(days=20)
    portfolio._pay_credit_with_date("Car Loan", 1500.0, current_date)

    # === YEAR 3 - DECEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(4000.0, current_date, "Year-end bonus")
    
    current_date += timedelta(days=10)
    portfolio._update_investment_with_date("Tokyo Apartment", 215000.0, current_date)  # +7.5% property value
    portfolio._update_investment_with_date("Tokyo TOPIX ETF", 195.0, current_date)  # +8.3%

    # === YEAR 4 - MARCH ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(6000.0, current_date, "Annual bonus")

    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Microsoft Stock", 300.0, 9, current_date, "Stock", "United States")  # 2700€
    
    current_date += timedelta(days=15)
    portfolio._add_financial_investment_with_date("China Tech ETF", 55.0, 45, current_date, "ETF", "China")  # 2475€

    # === YEAR 4 - JUNE - Recovery ===
    current_date += timedelta(days=90)
    portfolio._update_investment_with_date("Apple Stock", 165.0, current_date)  # +32%
    portfolio._update_investment_with_date("Bitcoin", 50000.0, current_date)  # +66.7%
    portfolio._update_investment_with_date("Amazon Stock", 3200.0, current_date)  # +14.3%

    current_date += timedelta(days=20)
    portfolio._add_cash_with_date(5000.0, current_date, "Investment gains distribution")
    
    current_date += timedelta(days=5)
    portfolio._add_real_estate_investment_with_date("Lyon Residential SCPI", 180.0, 25, current_date, "SCPI", "Lyon, France", 4.5)  # 4500€

    # === YEAR 4 - SEPTEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("Nvidia Stock", 420.0, 7, current_date, "Stock", "United States")  # 2940€
    
    current_date += timedelta(days=15)
    portfolio._pay_credit_with_date("Japanese Mortgage", 3000.0, current_date)

    # === YEAR 4 - DECEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(5500.0, current_date, "Year-end bonus + profit sharing")
    
    current_date += timedelta(days=10)
    portfolio._update_investment_with_date("Microsoft Stock", 350.0, current_date)  # +16.7%
    portfolio._update_investment_with_date("Sony Stock", 95.0, current_date)  # +11.8%
    portfolio._update_investment_with_date("LVMH Stock", 720.0, current_date)  # +10.8%

    # === YEAR 5 - MARCH ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(7500.0, current_date, "Promotion bonus")

    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Singapore REIT", 2.5, 800, current_date, "REIT", "Singapore")  # 2000€

    # === YEAR 5 - JUNE ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(4000.0, current_date, "Quarterly bonus")
    
    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Emerging Markets ETF", 38.0, 60, current_date, "ETF", "Emerging Markets")  # 2280€
    
    current_date += timedelta(days=20)
    portfolio._update_investment_with_date("Nvidia Stock", 580.0, current_date)  # +38.1%
    portfolio._update_investment_with_date("Bitcoin", 62000.0, current_date)  # +24%

    # === YEAR 5 - SEPTEMBER ===
    current_date += timedelta(days=90)
    portfolio._sell_investment_with_date("Apple Stock", 10, current_date)  # Taking profits
    
    current_date += timedelta(days=15)
    portfolio._add_cash_with_date(3500.0, current_date, "Consulting income")
    
    current_date += timedelta(days=5)
    portfolio._add_real_estate_investment_with_date("Berlin Residential REIT", 92.0, 30, current_date, "REIT", "Berlin, Germany", 3.9)  # 2760€

    # === YEAR 5 - NOVEMBER ===
    current_date += timedelta(days=60)
    portfolio._add_cash_with_date(6000.0, current_date, "Year-end bonus")

    # === YEAR 5 - RECENT UPDATES ===
    current_date = datetime.now() - timedelta(days=30)
    portfolio._update_investment_with_date("Tokyo Apartment", 228000.0, current_date)  # +14% over 5 years
    portfolio._update_investment_with_date("Paris Office SCPI", 225.0, current_date)  # +7.1%
    portfolio._update_investment_with_date("Lyon Residential SCPI", 192.0, current_date)  # +6.7%

    current_date = datetime.now() - timedelta(days=14)
    portfolio._update_investment_with_date("Tesla Stock", 240.0, current_date)  # Recovery
    portfolio._update_investment_with_date("S&P 500 ETF", 430.0, current_date)  # +22.9% over 5 years
    portfolio._update_investment_with_date("Europe ETF", 48.0, current_date)  # +14.3%

    current_date = datetime.now() - timedelta(days=7)
    portfolio._pay_credit_with_date("Japanese Mortgage", 2500.0, current_date)
    
    current_date = datetime.now() - timedelta(days=3)
    portfolio._update_investment_with_date("Bitcoin", 58000.0, current_date)
    portfolio._update_investment_with_date("Microsoft Stock", 370.0, current_date)
    portfolio._update_investment_with_date("Tokyo TOPIX ETF", 205.0, current_date)

    return portfolio
    """Creates a demo portfolio with simulated 5-year history"""
    portfolio = Portfolio(initial_cash=5000.0)

    # Simulation over the last 5 years
    base_date = datetime.now() - timedelta(days=1825)  # 5 years

    # === YEAR 1 - JANUARY - Portfolio start ===
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
    portfolio._add_financial_investment_with_date("Apple Stock", 120.0, 25, current_date, "Stock", "United States")  # 3000€

    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("S&P 500 ETF", 350.0, 12, current_date, "ETF", "United States")  # 4200€

    current_date += timedelta(days=7)
    portfolio._add_financial_investment_with_date("Bitcoin", 28000.0, 0.25, current_date, "Crypto", "Global")  # 7000€

    # === YEAR 1 - MARCH ===
    current_date += timedelta(days=30)
    portfolio.cash += 3000.0
    portfolio.transaction_history.append({
        'date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'CASH_ADD',
        'amount': 3000.0,
        'description': 'Quarterly bonus'
    })

    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("Tesla Stock", 180.0, 17, current_date, "Stock", "United States")  # 3060€

    # First credit - Car loan
    current_date += timedelta(days=15)
    portfolio._add_credit_with_date("Car Loan", 15000.0, 2.8, 320, current_date)

    # === YEAR 1 - JUNE ===
    current_date += timedelta(days=60)
    portfolio._add_financial_investment_with_date("LVMH Stock", 650.0, 5, current_date, "Stock", "France")  # 3250€
    
    current_date += timedelta(days=10)
    portfolio._update_investment_with_date("Apple Stock", 135.0, current_date)  # +12.5%
    portfolio._update_investment_with_date("Bitcoin", 35000.0, current_date)  # +25%

    # === YEAR 1 - SEPTEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("Europe ETF", 42.0, 60, current_date, "ETF", "Europe")  # 2520€
    
    current_date += timedelta(days=15)
    portfolio._pay_credit_with_date("Car Loan", 500.0, current_date)

    # === YEAR 1 - DECEMBER ===
    current_date += timedelta(days=80)
    portfolio._add_financial_investment_with_date("Tokyo TOPIX ETF", 180.0, 15, current_date, "ETF", "Japan")  # 2700€
    
    current_date += timedelta(days=10)
    portfolio._update_investment_with_date("Tesla Stock", 210.0, current_date)  # +16.7%

    # === YEAR 2 - MARCH ===
    current_date += timedelta(days=90)
    portfolio.cash += 5000.0
    portfolio.transaction_history.append({
        'date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'CASH_ADD',
        'amount': 5000.0,
        'description': 'Annual bonus'
    })

    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("Amazon Stock", 2800.0, 2, current_date, "Stock", "United States")  # 5600€

    # === YEAR 2 - JUNE ===
    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("Bonds", 98.0, 40, current_date, "Bond", "France")  # 3920€
    
    current_date += timedelta(days=20)
    portfolio._update_investment_with_date("Bitcoin", 42000.0, current_date)  # +20%
    portfolio._update_investment_with_date("S&P 500 ETF", 380.0, current_date)  # +8.6%

    # === YEAR 2 - SEPTEMBER - MAJOR EVENT: Real Estate Purchase in Japan ===
    current_date += timedelta(days=90)
    
    # Mortgage for primary residence in Japan
    portfolio._add_credit_with_date("Japanese Mortgage", 200000.0, 1.5, 950, current_date)
    
    # Add the property to real estate investments
    current_date += timedelta(days=3)
    portfolio._add_real_estate_investment_with_date("Tokyo Apartment", 200000.0, 1, current_date, "Apartment", "Tokyo, Japan", 0.0)  # Primary residence, no rental yield

    # === YEAR 2 - DECEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("Sony Stock", 85.0, 30, current_date, "Stock", "Japan")  # 2550€
    
    current_date += timedelta(days=10)
    portfolio._pay_credit_with_date("Japanese Mortgage", 2000.0, current_date)

    # === YEAR 3 - MARCH ===
    current_date += timedelta(days=90)
    portfolio.cash += 4000.0
    portfolio.transaction_history.append({
        'date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'CASH_ADD',
        'amount': 4000.0,
        'description': 'Quarterly bonus'
    })

    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Paris Office SCPI", 210.0, 25, current_date, "SCPI", "France")  # 5250€

    # Market correction
    current_date += timedelta(days=20)
    portfolio._update_investment_with_date("Apple Stock", 125.0, current_date)  # -7.4%
    portfolio._update_investment_with_date("Tesla Stock", 190.0, current_date)  # -9.5%
    portfolio._update_investment_with_date("Bitcoin", 30000.0, current_date)  # -28.6%

    # === YEAR 3 - JUNE ===
    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("US Residential REIT", 75.0, 40, current_date, "REIT", "United States")  # 3000€
    
    current_date += timedelta(days=15)
    portfolio._sell_investment_with_date("Tesla Stock", 7, current_date)  # Partial sale for profit-taking

    # === YEAR 3 - SEPTEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("Gold ETF", 160.0, 20, current_date, "ETF", "Global")  # 3200€
    
    current_date += timedelta(days=20)
    portfolio._pay_credit_with_date("Car Loan", 1500.0, current_date)

    # === YEAR 3 - DECEMBER ===
    current_date += timedelta(days=90)
    portfolio._update_investment_with_date("Tokyo Apartment", 215000.0, current_date)  # +7.5% property value
    portfolio._update_investment_with_date("Tokyo TOPIX ETF", 195.0, current_date)  # +8.3%

    # === YEAR 4 - MARCH ===
    current_date += timedelta(days=90)
    portfolio.cash += 6000.0
    portfolio.transaction_history.append({
        'date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'CASH_ADD',
        'amount': 6000.0,
        'description': 'Annual bonus'
    })

    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Microsoft Stock", 300.0, 10, current_date, "Stock", "United States")  # 3000€
    
    current_date += timedelta(days=15)
    portfolio._add_financial_investment_with_date("China Tech ETF", 55.0, 50, current_date, "ETF", "China")  # 2750€

    # === YEAR 4 - JUNE - Recovery ===
    current_date += timedelta(days=90)
    portfolio._update_investment_with_date("Apple Stock", 165.0, current_date)  # +32%
    portfolio._update_investment_with_date("Bitcoin", 50000.0, current_date)  # +66.7%
    portfolio._update_investment_with_date("Amazon Stock", 3200.0, current_date)  # +14.3%

    current_date += timedelta(days=20)
    portfolio._add_real_estate_investment_with_date("Lyon Residential SCPI", 180.0, 30, current_date, "SCPI", "Lyon, France", 4.5)  # 5400€

    # === YEAR 4 - SEPTEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("Nvidia Stock", 420.0, 8, current_date, "Stock", "United States")  # 3360€
    
    current_date += timedelta(days=15)
    portfolio._pay_credit_with_date("Japanese Mortgage", 3000.0, current_date)

    # === YEAR 4 - DECEMBER ===
    current_date += timedelta(days=90)
    portfolio._update_investment_with_date("Microsoft Stock", 350.0, current_date)  # +16.7%
    portfolio._update_investment_with_date("Sony Stock", 95.0, current_date)  # +11.8%
    portfolio._update_investment_with_date("LVMH Stock", 720.0, current_date)  # +10.8%

    # === YEAR 5 - MARCH ===
    current_date += timedelta(days=90)
    portfolio.cash += 7000.0
    portfolio.transaction_history.append({
        'date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'CASH_ADD',
        'amount': 7000.0,
        'description': 'Promotion bonus'
    })

    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Singapore REIT", 2.5, 1000, current_date, "REIT", "Singapore")  # 2500€

    # === YEAR 5 - JUNE ===
    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("Emerging Markets ETF", 38.0, 70, current_date, "ETF", "Emerging Markets")  # 2660€
    
    current_date += timedelta(days=20)
    portfolio._update_investment_with_date("Nvidia Stock", 580.0, current_date)  # +38.1%
    portfolio._update_investment_with_date("Bitcoin", 62000.0, current_date)  # +24%

    # === YEAR 5 - SEPTEMBER ===
    current_date += timedelta(days=90)
    portfolio._sell_investment_with_date("Apple Stock", 10, current_date)  # Taking profits
    
    current_date += timedelta(days=15)
    portfolio._add_real_estate_investment_with_date("Berlin Residential REIT", 92.0, 35, current_date, "REIT", "Berlin, Germany", 3.9)  # 3220€

    # === YEAR 5 - RECENT UPDATES ===
    current_date = datetime.now() - timedelta(days=30)
    portfolio._update_investment_with_date("Tokyo Apartment", 228000.0, current_date)  # +14% over 5 years
    portfolio._update_investment_with_date("Paris Office SCPI", 225.0, current_date)  # +7.1%
    portfolio._update_investment_with_date("Lyon Residential SCPI", 192.0, current_date)  # +6.7%

    current_date = datetime.now() - timedelta(days=14)
    portfolio._update_investment_with_date("Tesla Stock", 240.0, current_date)  # Recovery
    portfolio._update_investment_with_date("S&P 500 ETF", 430.0, current_date)  # +22.9% over 5 years
    portfolio._update_investment_with_date("Europe ETF", 48.0, current_date)  # +14.3%

    current_date = datetime.now() - timedelta(days=7)
    portfolio._pay_credit_with_date("Japanese Mortgage", 2500.0, current_date)
    
    current_date = datetime.now() - timedelta(days=3)
    portfolio._update_investment_with_date("Bitcoin", 58000.0, current_date)
    portfolio._update_investment_with_date("Microsoft Stock", 370.0, current_date)
    portfolio._update_investment_with_date("Tokyo TOPIX ETF", 205.0, current_date)

    portfolio.cash = 5000
    portfolio.transaction_history.append({
        'date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'CASH_ADD',
        'amount': 5000.,
        'description': 'Initial deposit'
    })

    return portfolio


def create_demo_portfolio_3():
    """Creates a demo portfolio with simulated 5-year history (includes some negative average returns)"""
    portfolio = Portfolio(initial_cash=5000.0)

    # Simulation over the last 5 years
    base_date = datetime.now() - timedelta(days=1825)  # 5 years

    # === YEAR 1 - JANUARY - Portfolio start ===
    current_date = base_date

    portfolio._add_cash_with_date(20000.0, current_date, "Initial deposit")

    # Initial investments
    current_date += timedelta(days=3)
    portfolio._add_financial_investment_with_date("Apple Stock", 120.0, 25, current_date, "Stock", "United States")
    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("S&P 500 ETF", 350.0, 12, current_date, "ETF", "United States")
    current_date += timedelta(days=7)
    portfolio._add_financial_investment_with_date("Bitcoin", 28000.0, 0.25, current_date, "Crypto", "Global")

    # === YEAR 1 - MARCH ===
    current_date += timedelta(days=30)
    portfolio._add_cash_with_date(3000.0, current_date, "Quarterly bonus")

    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("Tesla Stock", 180.0, 15, current_date, "Stock", "United States")

    # Car loan
    current_date += timedelta(days=15)
    portfolio._add_credit_with_date("Car Loan", 15000.0, 2.8, 320, current_date)

    # === YEAR 1 - JUNE ===
    current_date += timedelta(days=60)
    portfolio._add_financial_investment_with_date("LVMH Stock", 650.0, 5, current_date, "Stock", "France")

    current_date += timedelta(days=10)
    portfolio._update_investment_with_date("Apple Stock", 135.0, current_date)
    portfolio._update_investment_with_date("Bitcoin", 35000.0, current_date)

    # === YEAR 1 - SEPTEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("Europe ETF", 42.0, 50, current_date, "ETF", "Europe")

    current_date += timedelta(days=15)
    portfolio._pay_credit_with_date("Car Loan", 500.0, current_date)

    # === YEAR 1 - DECEMBER ===
    current_date += timedelta(days=80)
    portfolio._add_cash_with_date(2500.0, current_date, "End of year bonus")

    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("Tokyo TOPIX ETF", 180.0, 12, current_date, "ETF", "Japan")

    current_date += timedelta(days=10)
    portfolio._update_investment_with_date("Tesla Stock", 210.0, current_date)

    # === YEAR 2 ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(5000.0, current_date, "Annual bonus")

    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("Amazon Stock", 2800.0, 2, current_date, "Stock", "United States")

    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("Bonds", 98.0, 35, current_date, "Bond", "France")

    current_date += timedelta(days=20)
    portfolio._update_investment_with_date("Bitcoin", 42000.0, current_date)
    portfolio._update_investment_with_date("S&P 500 ETF", 380.0, current_date)

    # Real Estate + mortgage
    current_date += timedelta(days=90)
    portfolio._add_credit_with_date("Japanese Mortgage", 200000.0, 1.5, 950, current_date)

    current_date += timedelta(days=3)
    portfolio._add_real_estate_investment_with_date("Tokyo Apartment", 200000.0, 1, current_date, "Apartment", "Tokyo, Japan", 0.0)

    # === YEAR 2 - DECEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(3000.0, current_date, "Year-end bonus")
    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("Sony Stock", 85.0, 25, current_date, "Stock", "Japan")
    current_date += timedelta(days=10)
    portfolio._pay_credit_with_date("Japanese Mortgage", 2000.0, current_date)

    # === YEAR 3 ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(4500.0, current_date, "Quarterly bonus")

    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Paris Office SCPI", 210.0, 20, current_date, "SCPI", "France")

    # Market correction
    current_date += timedelta(days=20)
    portfolio._update_investment_with_date("Apple Stock", 125.0, current_date)
    portfolio._update_investment_with_date("Tesla Stock", 190.0, current_date)
    portfolio._update_investment_with_date("Bitcoin", 30000.0, current_date)
    portfolio._update_investment_with_date("Bonds", 90.0, current_date)  # -8.2%
    portfolio._update_investment_with_date("Europe ETF", 39.0, current_date)  # -7.1%

    # === YEAR 3 - JUNE ===
    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("US Residential REIT", 75.0, 35, current_date, "REIT", "United States")
    current_date += timedelta(days=15)
    portfolio._sell_investment_with_date("Tesla Stock", 6, current_date)

    # === YEAR 3 - SEPTEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(3500.0, current_date, "Freelance income")
    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Gold ETF", 160.0, 18, current_date, "ETF", "Global")
    current_date += timedelta(days=20)
    portfolio._pay_credit_with_date("Car Loan", 1500.0, current_date)

    # === YEAR 3 - DECEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(4000.0, current_date, "Year-end bonus")
    current_date += timedelta(days=10)
    portfolio._update_investment_with_date("Tokyo Apartment", 215000.0, current_date)
    portfolio._update_investment_with_date("Tokyo TOPIX ETF", 195.0, current_date)

    # === YEAR 4 ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(6000.0, current_date, "Annual bonus")

    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Microsoft Stock", 300.0, 9, current_date, "Stock", "United States")
    current_date += timedelta(days=15)
    portfolio._add_financial_investment_with_date("China Tech ETF", 55.0, 45, current_date, "ETF", "China")

    # === YEAR 4 - JUNE ===
    current_date += timedelta(days=90)
    portfolio._update_investment_with_date("Apple Stock", 165.0, current_date)
    portfolio._update_investment_with_date("Bitcoin", 50000.0, current_date)
    portfolio._update_investment_with_date("Amazon Stock", 3200.0, current_date)
    portfolio._update_investment_with_date("China Tech ETF", 48.0, current_date)  # -12.7%

    current_date += timedelta(days=20)
    portfolio._add_cash_with_date(5000.0, current_date, "Investment gains distribution")
    current_date += timedelta(days=5)
    portfolio._add_real_estate_investment_with_date("Lyon Residential SCPI", 180.0, 25, current_date, "SCPI", "Lyon, France", 4.5)

    # === YEAR 4 - SEPTEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("Nvidia Stock", 420.0, 7, current_date, "Stock", "United States")
    current_date += timedelta(days=15)
    portfolio._pay_credit_with_date("Japanese Mortgage", 3000.0, current_date)

    # === YEAR 4 - DECEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(5500.0, current_date, "Year-end bonus + profit sharing")
    current_date += timedelta(days=10)
    portfolio._update_investment_with_date("Microsoft Stock", 350.0, current_date)
    portfolio._update_investment_with_date("Sony Stock", 95.0, current_date)
    portfolio._update_investment_with_date("LVMH Stock", 720.0, current_date)

    # === YEAR 5 ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(7500.0, current_date, "Promotion bonus")
    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Singapore REIT", 2.5, 800, current_date, "REIT", "Singapore")

    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(4000.0, current_date, "Quarterly bonus")
    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Emerging Markets ETF", 38.0, 60, current_date, "ETF", "Emerging Markets")

    current_date += timedelta(days=20)
    portfolio._update_investment_with_date("Nvidia Stock", 580.0, current_date)
    portfolio._update_investment_with_date("Bitcoin", 62000.0, current_date)
    portfolio._update_investment_with_date("Bonds", 80.0, current_date)  # Final negative update
    portfolio._update_investment_with_date("China Tech ETF", 41.0, current_date)  # -25% total

    # === YEAR 5 - SEPTEMBER ===
    current_date += timedelta(days=90)
    portfolio._sell_investment_with_date("Apple Stock", 10, current_date)
    current_date += timedelta(days=15)
    portfolio._add_cash_with_date(3500.0, current_date, "Consulting income")
    current_date += timedelta(days=5)
    portfolio._add_real_estate_investment_with_date("Berlin Residential REIT", 92.0, 30, current_date, "REIT", "Berlin, Germany", 3.9)

    # === YEAR 5 - NOVEMBER ===
    current_date += timedelta(days=60)
    portfolio._add_cash_with_date(6000.0, current_date, "Year-end bonus")

    # === YEAR 5 - RECENT UPDATES ===
    current_date = datetime.now() - timedelta(days=30)
    portfolio._update_investment_with_date("Tokyo Apartment", 228000.0, current_date)
    portfolio._update_investment_with_date("Paris Office SCPI", 225.0, current_date)
    portfolio._update_investment_with_date("Lyon Residential SCPI", 192.0, current_date)

    current_date = datetime.now() - timedelta(days=14)
    portfolio._update_investment_with_date("Tesla Stock", 240.0, current_date)
    portfolio._update_investment_with_date("S&P 500 ETF", 430.0, current_date)
    portfolio._update_investment_with_date("Europe ETF", 40.0, current_date)  # Slight decline (-5%)

    current_date = datetime.now() - timedelta(days=7)
    portfolio._pay_credit_with_date("Japanese Mortgage", 2500.0, current_date)

    current_date = datetime.now() - timedelta(days=3)
    portfolio._update_investment_with_date("Bitcoin", 58000.0, current_date)
    portfolio._update_investment_with_date("Microsoft Stock", 370.0, current_date)
    portfolio._update_investment_with_date("Tokyo TOPIX ETF", 205.0, current_date)

    return portfolio


def create_demo_portfolio_4():
    """Creates a demo portfolio with simulated 5-year history (includes volatile market conditions)"""
    portfolio = Portfolio(initial_cash=5000.0)

    # Simulation over the last 5 years
    base_date = datetime.now() - timedelta(days=1825)  # 5 years

    # === YEAR 1 - JANUARY - Portfolio start ===
    current_date = base_date

    portfolio._add_cash_with_date(20000.0, current_date, "Initial deposit")

    # Initial investments
    current_date += timedelta(days=3)
    portfolio._add_financial_investment_with_date("Apple Stock", 120.0, 25, current_date, "Stock", "United States")
    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("S&P 500 ETF", 350.0, 12, current_date, "ETF", "United States")
    current_date += timedelta(days=7)
    portfolio._add_financial_investment_with_date("Bitcoin", 28000.0, 0.25, current_date, "Crypto", "Global")

    # === YEAR 1 - MARCH ===
    current_date += timedelta(days=30)
    portfolio._add_cash_with_date(3000.0, current_date, "Quarterly bonus")

    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("Tesla Stock", 180.0, 15, current_date, "Stock", "United States")

    # Car loan
    current_date += timedelta(days=15)
    portfolio._add_credit_with_date("Car Loan", 15000.0, 2.8, 320, current_date)

    # === YEAR 1 - APRIL - First market correction ===
    current_date += timedelta(days=25)
    portfolio._update_investment_with_date("Apple Stock", 105.0, current_date)  # -12.5%
    portfolio._update_investment_with_date("Tesla Stock", 155.0, current_date)  # -13.9%
    portfolio._update_investment_with_date("S&P 500 ETF", 325.0, current_date)  # -7.1%
    portfolio._update_investment_with_date("Bitcoin", 22000.0, current_date)  # -21.4%

    # === YEAR 1 - JUNE - Recovery ===
    current_date += timedelta(days=35)
    portfolio._add_financial_investment_with_date("LVMH Stock", 650.0, 5, current_date, "Stock", "France")

    current_date += timedelta(days=10)
    portfolio._update_investment_with_date("Apple Stock", 135.0, current_date)  # Recovery
    portfolio._update_investment_with_date("Bitcoin", 35000.0, current_date)  # Strong recovery

    # === YEAR 1 - SEPTEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("Europe ETF", 42.0, 50, current_date, "ETF", "Europe")

    current_date += timedelta(days=15)
    portfolio._pay_credit_with_date("Car Loan", 500.0, current_date)

    # === YEAR 1 - OCTOBER - Market volatility ===
    current_date += timedelta(days=20)
    portfolio._update_investment_with_date("Tesla Stock", 165.0, current_date)  # -8.3%
    portfolio._update_investment_with_date("S&P 500 ETF", 340.0, current_date)

    # === YEAR 1 - DECEMBER ===
    current_date += timedelta(days=60)
    portfolio._add_cash_with_date(2500.0, current_date, "End of year bonus")

    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("Tokyo TOPIX ETF", 180.0, 12, current_date, "ETF", "Japan")

    current_date += timedelta(days=10)
    portfolio._update_investment_with_date("Tesla Stock", 210.0, current_date)

    # === YEAR 2 - JANUARY ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(5000.0, current_date, "Annual bonus")

    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("Amazon Stock", 2800.0, 2, current_date, "Stock", "United States")

    # === YEAR 2 - MARCH - Major correction (bear market begins) ===
    current_date += timedelta(days=60)
    portfolio._update_investment_with_date("Apple Stock", 115.0, current_date)  # -14.8%
    portfolio._update_investment_with_date("Tesla Stock", 175.0, current_date)  # -16.7%
    portfolio._update_investment_with_date("Amazon Stock", 2500.0, current_date)  # -10.7%
    portfolio._update_investment_with_date("S&P 500 ETF", 310.0, current_date)  # -11.4%
    portfolio._update_investment_with_date("Bitcoin", 28000.0, current_date)  # -20%
    portfolio._update_investment_with_date("LVMH Stock", 580.0, current_date)  # -10.8%

    current_date += timedelta(days=30)
    portfolio._add_financial_investment_with_date("Bonds", 98.0, 35, current_date, "Bond", "France")

    # === YEAR 2 - MAY - Continued decline ===
    current_date += timedelta(days=30)
    portfolio._update_investment_with_date("Bitcoin", 19000.0, current_date)  # -32.1%
    portfolio._update_investment_with_date("Tesla Stock", 145.0, current_date)  # -17.1%
    portfolio._update_investment_with_date("Europe ETF", 37.0, current_date)  # -11.9%

    # === YEAR 2 - JULY - Bottom reached ===
    current_date += timedelta(days=60)
    portfolio._update_investment_with_date("S&P 500 ETF", 295.0, current_date)  # -15.7% from initial

    # Real Estate + mortgage
    current_date += timedelta(days=30)
    portfolio._add_credit_with_date("Japanese Mortgage", 200000.0, 1.5, 950, current_date)

    current_date += timedelta(days=3)
    portfolio._add_real_estate_investment_with_date("Tokyo Apartment", 200000.0, 1, current_date, "Apartment", "Tokyo, Japan", 0.0)

    # === YEAR 2 - OCTOBER - Slow recovery begins ===
    current_date += timedelta(days=60)
    portfolio._update_investment_with_date("Bitcoin", 25000.0, current_date)  # Recovery
    portfolio._update_investment_with_date("Apple Stock", 125.0, current_date)

    # === YEAR 2 - DECEMBER ===
    current_date += timedelta(days=60)
    portfolio._add_cash_with_date(3000.0, current_date, "Year-end bonus")
    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("Sony Stock", 85.0, 25, current_date, "Stock", "Japan")
    current_date += timedelta(days=10)
    portfolio._pay_credit_with_date("Japanese Mortgage", 2000.0, current_date)

    # === YEAR 3 - JANUARY ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(4500.0, current_date, "Quarterly bonus")

    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Paris Office SCPI", 210.0, 20, current_date, "SCPI", "France")

    # === YEAR 3 - MARCH - Strong recovery ===
    current_date += timedelta(days=60)
    portfolio._update_investment_with_date("Bitcoin", 42000.0, current_date)  # Strong recovery
    portfolio._update_investment_with_date("Tesla Stock", 220.0, current_date)
    portfolio._update_investment_with_date("S&P 500 ETF", 380.0, current_date)
    portfolio._update_investment_with_date("Amazon Stock", 3100.0, current_date)

    # === YEAR 3 - JUNE ===
    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("US Residential REIT", 75.0, 35, current_date, "REIT", "United States")
    current_date += timedelta(days=15)
    portfolio._sell_investment_with_date("Tesla Stock", 6, current_date)

    # === YEAR 3 - AUGUST - Mid-year correction ===
    current_date += timedelta(days=60)
    portfolio._update_investment_with_date("Apple Stock", 118.0, current_date)  # -5.6%
    portfolio._update_investment_with_date("Bonds", 90.0, current_date)  # -8.2%
    portfolio._update_investment_with_date("Europe ETF", 39.0, current_date)  # -7.1%

    # === YEAR 3 - SEPTEMBER ===
    current_date += timedelta(days=30)
    portfolio._add_cash_with_date(3500.0, current_date, "Freelance income")
    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Gold ETF", 160.0, 18, current_date, "ETF", "Global")
    current_date += timedelta(days=20)
    portfolio._pay_credit_with_date("Car Loan", 1500.0, current_date)

    # === YEAR 3 - DECEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(4000.0, current_date, "Year-end bonus")
    current_date += timedelta(days=10)
    portfolio._update_investment_with_date("Tokyo Apartment", 215000.0, current_date)
    portfolio._update_investment_with_date("Tokyo TOPIX ETF", 195.0, current_date)
    portfolio._update_investment_with_date("Bitcoin", 38000.0, current_date)  # Pullback

    # === YEAR 4 - JANUARY ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(6000.0, current_date, "Annual bonus")

    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Microsoft Stock", 300.0, 9, current_date, "Stock", "United States")
    current_date += timedelta(days=15)
    portfolio._add_financial_investment_with_date("China Tech ETF", 55.0, 45, current_date, "ETF", "China")

    # === YEAR 4 - MARCH - MAJOR MARKET CRASH (Black Swan Event) ===
    current_date += timedelta(days=60)
    # Massive simultaneous crash across ALL financial assets
    portfolio._update_investment_with_date("Apple Stock", 85.0, current_date)  # -29.2%
    portfolio._update_investment_with_date("Microsoft Stock", 210.0, current_date)  # -30%
    portfolio._update_investment_with_date("Amazon Stock", 2200.0, current_date)  # -31.3%
    portfolio._update_investment_with_date("Tesla Stock", 125.0, current_date)  # -40.5%
    portfolio._update_investment_with_date("China Tech ETF", 33.0, current_date)  # -40%
    portfolio._update_investment_with_date("Bitcoin", 18000.0, current_date)  # -52.6%
    portfolio._update_investment_with_date("S&P 500 ETF", 265.0, current_date)  # -30.3%
    portfolio._update_investment_with_date("Europe ETF", 28.0, current_date)  # -28.2%
    portfolio._update_investment_with_date("Tokyo TOPIX ETF", 140.0, current_date)  # -28.2%
    portfolio._update_investment_with_date("LVMH Stock", 505.0, current_date)  # -29.9%
    portfolio._update_investment_with_date("Sony Stock", 65.0, current_date)  # -31.6%
    portfolio._update_investment_with_date("Bonds", 75.0, current_date)  # -23.5%
    portfolio._update_investment_with_date("Gold ETF", 135.0, current_date)  # -15.6%
    portfolio._update_investment_with_date("US Residential REIT", 55.0, current_date)  # -26.7%
    portfolio._update_investment_with_date("Paris Office SCPI", 175.0, current_date)  # -16.7%

    # === YEAR 4 - APRIL - Gradual recovery begins ===
    current_date += timedelta(days=30)
    portfolio._update_investment_with_date("Apple Stock", 130.0, current_date)  # Partial recovery
    portfolio._update_investment_with_date("Bitcoin", 35000.0, current_date)  # Still below pre-crash
    portfolio._update_investment_with_date("Amazon Stock", 2800.0, current_date)
    portfolio._update_investment_with_date("Microsoft Stock", 290.0, current_date)
    portfolio._update_investment_with_date("S&P 500 ETF", 340.0, current_date)

    current_date += timedelta(days=20)
    portfolio._add_cash_with_date(5000.0, current_date, "Investment gains distribution")
    current_date += timedelta(days=5)
    portfolio._add_real_estate_investment_with_date("Lyon Residential SCPI", 180.0, 25, current_date, "SCPI", "Lyon, France", 4.5)

    # === YEAR 4 - SEPTEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("Nvidia Stock", 420.0, 7, current_date, "Stock", "United States")
    current_date += timedelta(days=15)
    portfolio._pay_credit_with_date("Japanese Mortgage", 3000.0, current_date)

    # === YEAR 4 - NOVEMBER - Emerging markets crisis ===
    current_date += timedelta(days=60)
    portfolio._update_investment_with_date("China Tech ETF", 38.0, current_date)  # -30.9% total
    portfolio._update_investment_with_date("Bonds", 82.0, current_date)  # -16.3% total

    # === YEAR 4 - DECEMBER ===
    current_date += timedelta(days=30)
    portfolio._add_cash_with_date(5500.0, current_date, "Year-end bonus + profit sharing")
    current_date += timedelta(days=10)
    portfolio._update_investment_with_date("Microsoft Stock", 350.0, current_date)
    portfolio._update_investment_with_date("Sony Stock", 95.0, current_date)
    portfolio._update_investment_with_date("LVMH Stock", 720.0, current_date)

    # === YEAR 5 - JANUARY ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(7500.0, current_date, "Promotion bonus")
    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Singapore REIT", 2.5, 800, current_date, "REIT", "Singapore")

    # === YEAR 5 - MARCH - Tech sector correction ===
    current_date += timedelta(days=60)
    portfolio._update_investment_with_date("Nvidia Stock", 380.0, current_date)  # -9.5%
    portfolio._update_investment_with_date("Microsoft Stock", 320.0, current_date)  # -8.6%
    portfolio._update_investment_with_date("Apple Stock", 152.0, current_date)  # -7.9%

    current_date += timedelta(days=30)
    portfolio._add_cash_with_date(4000.0, current_date, "Quarterly bonus")
    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Emerging Markets ETF", 38.0, 60, current_date, "ETF", "Emerging Markets")

    # === YEAR 5 - JUNE - Recovery begins ===
    current_date += timedelta(days=60)
    portfolio._update_investment_with_date("Nvidia Stock", 580.0, current_date)
    portfolio._update_investment_with_date("Bitcoin", 62000.0, current_date)
    portfolio._update_investment_with_date("Apple Stock", 170.0, current_date)

    # === YEAR 5 - AUGUST - Another pullback ===
    current_date += timedelta(days=60)
    portfolio._update_investment_with_date("Bitcoin", 54000.0, current_date)  # -12.9%
    portfolio._update_investment_with_date("S&P 500 ETF", 365.0, current_date)  # -4.0%
    portfolio._update_investment_with_date("Europe ETF", 36.5, current_date)  # -8.8%

    # === YEAR 5 - SEPTEMBER ===
    current_date += timedelta(days=30)
    portfolio._sell_investment_with_date("Apple Stock", 10, current_date)
    current_date += timedelta(days=15)
    portfolio._add_cash_with_date(3500.0, current_date, "Consulting income")
    current_date += timedelta(days=5)
    portfolio._add_real_estate_investment_with_date("Berlin Residential REIT", 92.0, 30, current_date, "REIT", "Berlin, Germany", 3.9)

    # === YEAR 5 - NOVEMBER ===
    current_date += timedelta(days=60)
    portfolio._add_cash_with_date(6000.0, current_date, "Year-end bonus")

    # === YEAR 5 - RECENT UPDATES ===
    current_date = datetime.now() - timedelta(days=30)
    portfolio._update_investment_with_date("Tokyo Apartment", 228000.0, current_date)
    portfolio._update_investment_with_date("Paris Office SCPI", 225.0, current_date)
    portfolio._update_investment_with_date("Lyon Residential SCPI", 192.0, current_date)
    portfolio._update_investment_with_date("Bonds", 78.0, current_date)  # Further decline -20.4% total

    current_date = datetime.now() - timedelta(days=14)
    portfolio._update_investment_with_date("Tesla Stock", 240.0, current_date)
    portfolio._update_investment_with_date("S&P 500 ETF", 430.0, current_date)  # Recovery
    portfolio._update_investment_with_date("Europe ETF", 40.0, current_date)
    portfolio._update_investment_with_date("China Tech ETF", 35.0, current_date)  # -36.4% total

    current_date = datetime.now() - timedelta(days=7)
    portfolio._pay_credit_with_date("Japanese Mortgage", 2500.0, current_date)

    current_date = datetime.now() - timedelta(days=3)
    portfolio._update_investment_with_date("Bitcoin", 58000.0, current_date)
    portfolio._update_investment_with_date("Microsoft Stock", 370.0, current_date)
    portfolio._update_investment_with_date("Tokyo TOPIX ETF", 205.0, current_date)
    portfolio._update_investment_with_date("Nvidia Stock", 560.0, current_date)  # Slight pullback

    return portfolio
    """Creates a demo portfolio with simulated 5-year history (includes volatile market conditions)"""
    portfolio = Portfolio(initial_cash=5000.0)

    # Simulation over the last 5 years
    base_date = datetime.now() - timedelta(days=1825)  # 5 years

    # === YEAR 1 - JANUARY - Portfolio start ===
    current_date = base_date

    portfolio._add_cash_with_date(20000.0, current_date, "Initial deposit")

    # Initial investments
    current_date += timedelta(days=3)
    portfolio._add_financial_investment_with_date("Apple Stock", 120.0, 25, current_date, "Stock", "United States")
    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("S&P 500 ETF", 350.0, 12, current_date, "ETF", "United States")
    current_date += timedelta(days=7)
    portfolio._add_financial_investment_with_date("Bitcoin", 28000.0, 0.25, current_date, "Crypto", "Global")

    # === YEAR 1 - MARCH ===
    current_date += timedelta(days=30)
    portfolio._add_cash_with_date(3000.0, current_date, "Quarterly bonus")

    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("Tesla Stock", 180.0, 15, current_date, "Stock", "United States")

    # Car loan
    current_date += timedelta(days=15)
    portfolio._add_credit_with_date("Car Loan", 15000.0, 2.8, 320, current_date)

    # === YEAR 1 - APRIL - First market correction ===
    current_date += timedelta(days=25)
    portfolio._update_investment_with_date("Apple Stock", 105.0, current_date)  # -12.5%
    portfolio._update_investment_with_date("Tesla Stock", 155.0, current_date)  # -13.9%
    portfolio._update_investment_with_date("S&P 500 ETF", 325.0, current_date)  # -7.1%
    portfolio._update_investment_with_date("Bitcoin", 22000.0, current_date)  # -21.4%

    # === YEAR 1 - JUNE - Recovery ===
    current_date += timedelta(days=35)
    portfolio._add_financial_investment_with_date("LVMH Stock", 650.0, 5, current_date, "Stock", "France")

    current_date += timedelta(days=10)
    portfolio._update_investment_with_date("Apple Stock", 135.0, current_date)  # Recovery
    portfolio._update_investment_with_date("Bitcoin", 35000.0, current_date)  # Strong recovery

    # === YEAR 1 - SEPTEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("Europe ETF", 42.0, 50, current_date, "ETF", "Europe")

    current_date += timedelta(days=15)
    portfolio._pay_credit_with_date("Car Loan", 500.0, current_date)

    # === YEAR 1 - OCTOBER - Market volatility ===
    current_date += timedelta(days=20)
    portfolio._update_investment_with_date("Tesla Stock", 165.0, current_date)  # -8.3%
    portfolio._update_investment_with_date("S&P 500 ETF", 340.0, current_date)

    # === YEAR 1 - DECEMBER ===
    current_date += timedelta(days=60)
    portfolio._add_cash_with_date(2500.0, current_date, "End of year bonus")

    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("Tokyo TOPIX ETF", 180.0, 12, current_date, "ETF", "Japan")

    current_date += timedelta(days=10)
    portfolio._update_investment_with_date("Tesla Stock", 210.0, current_date)

    # === YEAR 2 - JANUARY ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(5000.0, current_date, "Annual bonus")

    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("Amazon Stock", 2800.0, 2, current_date, "Stock", "United States")

    # === YEAR 2 - MARCH - Major correction (bear market begins) ===
    current_date += timedelta(days=60)
    portfolio._update_investment_with_date("Apple Stock", 115.0, current_date)  # -14.8%
    portfolio._update_investment_with_date("Tesla Stock", 175.0, current_date)  # -16.7%
    portfolio._update_investment_with_date("Amazon Stock", 2500.0, current_date)  # -10.7%
    portfolio._update_investment_with_date("S&P 500 ETF", 310.0, current_date)  # -11.4%
    portfolio._update_investment_with_date("Bitcoin", 28000.0, current_date)  # -20%
    portfolio._update_investment_with_date("LVMH Stock", 580.0, current_date)  # -10.8%

    current_date += timedelta(days=30)
    portfolio._add_financial_investment_with_date("Bonds", 98.0, 35, current_date, "Bond", "France")

    # === YEAR 2 - MAY - Continued decline ===
    current_date += timedelta(days=30)
    portfolio._update_investment_with_date("Bitcoin", 19000.0, current_date)  # -32.1%
    portfolio._update_investment_with_date("Tesla Stock", 145.0, current_date)  # -17.1%
    portfolio._update_investment_with_date("Europe ETF", 37.0, current_date)  # -11.9%

    # === YEAR 2 - JULY - Bottom reached ===
    current_date += timedelta(days=60)
    portfolio._update_investment_with_date("S&P 500 ETF", 295.0, current_date)  # -15.7% from initial

    # Real Estate + mortgage
    current_date += timedelta(days=30)
    portfolio._add_credit_with_date("Japanese Mortgage", 200000.0, 1.5, 950, current_date)

    current_date += timedelta(days=3)
    portfolio._add_real_estate_investment_with_date("Tokyo Apartment", 200000.0, 1, current_date, "Apartment", "Tokyo, Japan", 0.0)

    # === YEAR 2 - OCTOBER - Slow recovery begins ===
    current_date += timedelta(days=60)
    portfolio._update_investment_with_date("Bitcoin", 25000.0, current_date)  # Recovery
    portfolio._update_investment_with_date("Apple Stock", 125.0, current_date)

    # === YEAR 2 - DECEMBER ===
    current_date += timedelta(days=60)
    portfolio._add_cash_with_date(3000.0, current_date, "Year-end bonus")
    current_date += timedelta(days=5)
    portfolio._add_financial_investment_with_date("Sony Stock", 85.0, 25, current_date, "Stock", "Japan")
    current_date += timedelta(days=10)
    portfolio._pay_credit_with_date("Japanese Mortgage", 2000.0, current_date)

    # === YEAR 3 - JANUARY ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(4500.0, current_date, "Quarterly bonus")

    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Paris Office SCPI", 210.0, 20, current_date, "SCPI", "France")

    # === YEAR 3 - MARCH - Strong recovery ===
    current_date += timedelta(days=60)
    portfolio._update_investment_with_date("Bitcoin", 42000.0, current_date)  # Strong recovery
    portfolio._update_investment_with_date("Tesla Stock", 220.0, current_date)
    portfolio._update_investment_with_date("S&P 500 ETF", 380.0, current_date)
    portfolio._update_investment_with_date("Amazon Stock", 3100.0, current_date)

    # === YEAR 3 - JUNE ===
    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("US Residential REIT", 75.0, 35, current_date, "REIT", "United States")
    current_date += timedelta(days=15)
    portfolio._sell_investment_with_date("Tesla Stock", 6, current_date)

    # === YEAR 3 - AUGUST - Mid-year correction ===
    current_date += timedelta(days=60)
    portfolio._update_investment_with_date("Apple Stock", 118.0, current_date)  # -5.6%
    portfolio._update_investment_with_date("Bonds", 90.0, current_date)  # -8.2%
    portfolio._update_investment_with_date("Europe ETF", 39.0, current_date)  # -7.1%

    # === YEAR 3 - SEPTEMBER ===
    current_date += timedelta(days=30)
    portfolio._add_cash_with_date(3500.0, current_date, "Freelance income")
    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Gold ETF", 160.0, 18, current_date, "ETF", "Global")
    current_date += timedelta(days=20)
    portfolio._pay_credit_with_date("Car Loan", 1500.0, current_date)

    # === YEAR 3 - DECEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(4000.0, current_date, "Year-end bonus")
    current_date += timedelta(days=10)
    portfolio._update_investment_with_date("Tokyo Apartment", 215000.0, current_date)
    portfolio._update_investment_with_date("Tokyo TOPIX ETF", 195.0, current_date)
    portfolio._update_investment_with_date("Bitcoin", 38000.0, current_date)  # Pullback

    # === YEAR 4 - JANUARY ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(6000.0, current_date, "Annual bonus")

    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Microsoft Stock", 300.0, 9, current_date, "Stock", "United States")
    current_date += timedelta(days=15)
    portfolio._add_financial_investment_with_date("China Tech ETF", 55.0, 45, current_date, "ETF", "China")

    # === YEAR 4 - MARCH - Flash crash ===
    current_date += timedelta(days=60)
    portfolio._update_investment_with_date("Apple Stock", 108.0, current_date)  # -8.5%
    portfolio._update_investment_with_date("Microsoft Stock", 270.0, current_date)  # -10%
    portfolio._update_investment_with_date("China Tech ETF", 48.0, current_date)  # -12.7%
    portfolio._update_investment_with_date("Bitcoin", 32000.0, current_date)  # -15.8%

    # === YEAR 4 - JUNE - Recovery and new highs ===
    current_date += timedelta(days=90)
    portfolio._update_investment_with_date("Apple Stock", 165.0, current_date)
    portfolio._update_investment_with_date("Bitcoin", 50000.0, current_date)
    portfolio._update_investment_with_date("Amazon Stock", 3200.0, current_date)
    portfolio._update_investment_with_date("Microsoft Stock", 340.0, current_date)

    current_date += timedelta(days=20)
    portfolio._add_cash_with_date(5000.0, current_date, "Investment gains distribution")
    current_date += timedelta(days=5)
    portfolio._add_real_estate_investment_with_date("Lyon Residential SCPI", 180.0, 25, current_date, "SCPI", "Lyon, France", 4.5)

    # === YEAR 4 - SEPTEMBER ===
    current_date += timedelta(days=90)
    portfolio._add_financial_investment_with_date("Nvidia Stock", 420.0, 7, current_date, "Stock", "United States")
    current_date += timedelta(days=15)
    portfolio._pay_credit_with_date("Japanese Mortgage", 3000.0, current_date)

    # === YEAR 4 - NOVEMBER - Emerging markets crisis ===
    current_date += timedelta(days=60)
    portfolio._update_investment_with_date("China Tech ETF", 38.0, current_date)  # -30.9% total
    portfolio._update_investment_with_date("Bonds", 82.0, current_date)  # -16.3% total

    # === YEAR 4 - DECEMBER ===
    current_date += timedelta(days=30)
    portfolio._add_cash_with_date(5500.0, current_date, "Year-end bonus + profit sharing")
    current_date += timedelta(days=10)
    portfolio._update_investment_with_date("Microsoft Stock", 350.0, current_date)
    portfolio._update_investment_with_date("Sony Stock", 95.0, current_date)
    portfolio._update_investment_with_date("LVMH Stock", 720.0, current_date)

    # === YEAR 5 - JANUARY ===
    current_date += timedelta(days=90)
    portfolio._add_cash_with_date(7500.0, current_date, "Promotion bonus")
    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Singapore REIT", 2.5, 800, current_date, "REIT", "Singapore")

    # === YEAR 5 - MARCH - Tech sector correction ===
    current_date += timedelta(days=60)
    portfolio._update_investment_with_date("Nvidia Stock", 380.0, current_date)  # -9.5%
    portfolio._update_investment_with_date("Microsoft Stock", 320.0, current_date)  # -8.6%
    portfolio._update_investment_with_date("Apple Stock", 152.0, current_date)  # -7.9%

    current_date += timedelta(days=30)
    portfolio._add_cash_with_date(4000.0, current_date, "Quarterly bonus")
    current_date += timedelta(days=10)
    portfolio._add_financial_investment_with_date("Emerging Markets ETF", 38.0, 60, current_date, "ETF", "Emerging Markets")

    # === YEAR 5 - JUNE - Recovery begins ===
    current_date += timedelta(days=60)
    portfolio._update_investment_with_date("Nvidia Stock", 580.0, current_date)
    portfolio._update_investment_with_date("Bitcoin", 62000.0, current_date)
    portfolio._update_investment_with_date("Apple Stock", 170.0, current_date)

    # === YEAR 5 - AUGUST - Another pullback ===
    current_date += timedelta(days=60)
    portfolio._update_investment_with_date("Bitcoin", 54000.0, current_date)  # -12.9%
    portfolio._update_investment_with_date("S&P 500 ETF", 365.0, current_date)  # -4.0%
    portfolio._update_investment_with_date("Europe ETF", 36.5, current_date)  # -8.8%

    # === YEAR 5 - SEPTEMBER ===
    current_date += timedelta(days=30)
    portfolio._sell_investment_with_date("Apple Stock", 10, current_date)
    current_date += timedelta(days=15)
    portfolio._add_cash_with_date(3500.0, current_date, "Consulting income")
    current_date += timedelta(days=5)
    portfolio._add_real_estate_investment_with_date("Berlin Residential REIT", 92.0, 30, current_date, "REIT", "Berlin, Germany", 3.9)

    # === YEAR 5 - NOVEMBER ===
    current_date += timedelta(days=60)
    portfolio._add_cash_with_date(6000.0, current_date, "Year-end bonus")

    # === YEAR 5 - RECENT UPDATES ===
    current_date = datetime.now() - timedelta(days=30)
    portfolio._update_investment_with_date("Tokyo Apartment", 228000.0, current_date)
    portfolio._update_investment_with_date("Paris Office SCPI", 225.0, current_date)
    portfolio._update_investment_with_date("Lyon Residential SCPI", 192.0, current_date)
    portfolio._update_investment_with_date("Bonds", 78.0, current_date)  # Further decline -20.4% total

    current_date = datetime.now() - timedelta(days=14)
    portfolio._update_investment_with_date("Tesla Stock", 240.0, current_date)
    portfolio._update_investment_with_date("S&P 500 ETF", 430.0, current_date)  # Recovery
    portfolio._update_investment_with_date("Europe ETF", 40.0, current_date)
    portfolio._update_investment_with_date("China Tech ETF", 35.0, current_date)  # -36.4% total

    current_date = datetime.now() - timedelta(days=7)
    portfolio._pay_credit_with_date("Japanese Mortgage", 2500.0, current_date)

    current_date = datetime.now() - timedelta(days=3)
    portfolio._update_investment_with_date("Bitcoin", 58000.0, current_date)
    portfolio._update_investment_with_date("Microsoft Stock", 370.0, current_date)
    portfolio._update_investment_with_date("Tokyo TOPIX ETF", 205.0, current_date)
    portfolio._update_investment_with_date("Nvidia Stock", 560.0, current_date)  # Slight pullback

    return portfolio