import yfinance as yf
import psycopg2
from datetime import datetime
import pandas as pd

# Connexion à Render PostgreSQL
conn = psycopg2.connect(
    "postgresql://yahoo_finance_db_user:xjFZCkONdWsGbmq6ALBIJxRWzQQqpGes@dpg-d44b4u3e5dus73av7iq0-a.frankfurt-postgres.render.com/yahoo_finance_db"
)
cursor = conn.cursor()

# Création de la table
cursor.execute("""
CREATE TABLE IF NOT EXISTS stock_data (
    symbol TEXT,
    category TEXT,
    date DATE,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION,
    volume BIGINT
);
""")

symbols = {
    'Actions US': ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'NVDA'],
    'Actions FR': ['MC.PA', 'OR.PA', 'SAN.PA', 'AIR.PA'],
    'Indices': ['^GSPC', '^DJI', '^IXIC', '^FCHI'],
    'Cryptos': ['BTC-USD', 'ETH-USD', 'BNB-USD'],
    'ETF': ['SPY', 'QQQ', 'VOO', 'VTI'],
    'Matières premières': ['GC=F', 'SI=F', 'CL=F']
}

start_date = "2023-01-01"
end_date = datetime.today().strftime('%Y-%m-%d')

for category, tickers in symbols.items():
    for ticker in tickers:
        print(f"⏳ Téléchargement de {ticker} ({category})...")
        data = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=False)

        if data.empty:
            print(f"⚠️ Aucun résultat pour {ticker}")
            continue

        # Normalisation du DataFrame
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(-1)  # garde juste le dernier niveau
        data = data.reset_index()

        # Vérifie le nom de la colonne date
        date_col = 'Date' if 'Date' in data.columns else 'index'
        data.rename(columns={date_col: 'Date'}, inplace=True)

        # Nettoyage des volumes
        if 'Volume' not in data.columns:
            data['Volume'] = 0
        data['Volume'] = data['Volume'].fillna(0).astype(int)

        # Insertion en base
        for _, row in data.iterrows():
            cursor.execute("""
                INSERT INTO stock_data (symbol, category, date, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                ticker,
                category,
                row["Date"].date() if isinstance(row["Date"], pd.Timestamp) else row["Date"],
                float(row.get("Open", 0)),
                float(row.get("High", 0)),
                float(row.get("Low", 0)),
                float(row.get("Close", 0)),
                int(row.get("Volume", 0))
            ))
        print(f"✅ Données insérées pour {ticker}")

conn.commit()
cursor.close()
conn.close()

print("🎉 Import terminé avec succès !")
