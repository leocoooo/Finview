import yfinance as yf
import pandas as pd
import os

# Définition des tickers Yahoo Finance
tickers = {
    "S&P500": "^GSPC",      # Indice S&P 500
    "Nasdaq100": "^NDX",    # Indice Nasdaq 100
    "CAC40": "^FCHI",       # Indice CAC 40
    "ETF Monde": "URTH"     # iShares MSCI World ETF
}

# Période depuis 2015
start_date = "2015-01-01"

# Téléchargement des données mensuelles (cours de clôture ajustés)
data = {}
for name, ticker in tickers.items():
    df = yf.download(ticker, start=start_date, interval="1mo")
    # Utiliser "Close" car les prix sont déjà ajustés
    data[name] = df["Close"]

prices = pd.concat(data.values(), axis=1)
prices.columns = data.keys()

# Calcul des rendements mensuels en pourcentage
returns = prices.pct_change().dropna() * 100

# Afficher un aperçu
print(returns.head())

# Sauvegarde en CSV
os.makedirs("data", exist_ok=True)
returns.to_excel("data/rendements_mensuels_indices.xlsx")

