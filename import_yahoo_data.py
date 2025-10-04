import yfinance as yf
import pandas as pd
import os

# Definition of Yahoo Finance tickers
tickers = {
    "S&P500": "^GSPC",      # S&P 500 Index
    "Nasdaq100": "^NDX",    # Nasdaq 100 Index
    "CAC40": "^FCHI",       # CAC 40 Index
    "ETF Monde": "URTH"     # iShares MSCI World ETF
}

# Period since 2015
start_date = "2015-01-01"

# Download monthly data (adjusted closing prices)
data = {}
for name, ticker in tickers.items():
    df = yf.download(ticker, start=start_date, interval="1mo")
    # Use "Close" as prices are already adjusted
    data[name] = df["Close"]

prices = pd.concat(data.values(), axis=1)
prices.columns = data.keys()

# Calculate monthly returns as percentages
returns = prices.pct_change().dropna() * 100

# Display a preview
print(returns.head())

# Save to CSV
os.makedirs("data", exist_ok=True)
returns.to_excel("data/rendements_mensuels_indices.xlsx")

