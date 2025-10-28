from datetime import datetime, timedelta
from src.finview.models.portfolio import Portfolio


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