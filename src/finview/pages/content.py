"""
Content page - Financial news and definitions
Part 1: News section
"""

import pandas as pd
import streamlit as st
import yfinance as yf


def show_news():
    """Financial news page with curated articles"""
    st.header("📰 Financial News & Economic Updates")
    st.markdown("Stay informed with the latest financial news, company earnings, and economic announcements.")

    st.markdown("---")

    # Create tabs for news organization
    tab1, tab2 = st.tabs(["🔥 Latest News", "📅 Upcoming Results"])

    with tab1:
        _show_latest_news()

    with tab2:
        _show_earnings_calendar()


def _show_latest_news():
    """Affiche les dernières actualités financières"""
    st.subheader("🔥 Top Financial News")

    # Article 1: Political Crisis Impact on CAC 40
    with st.container():
        st.markdown("### 📊 CAC 40: Political crisis causes volatility, recovery follows")
        st.markdown("""
        The resignation of Prime Minister Sébastien Lecornu on October 6, 2025, caused the CAC 40 to drop 2% immediately.
        Banks were particularly affected with drops of 4-5% (Société Générale, Crédit Agricole, BNP Paribas).
        However, the index recovered strongly on October 8, gaining 1.07% to close at 8,060 points.
        Legrand was the top performer with +3.56%, while the index broke through the 7,950 points resistance level.
        """)
        st.markdown("🔗 **Source:** [MoneyVox - Bourse du 8 octobre 2025](https://www.moneyvox.fr/bourse/actualites/105412/societe-generale-se-reprend-le-cac-40-surprend-le-journal-de-la-bourse-du-8-octobre-2025)")
        st.markdown("📅 **Date:** October 8, 2025")
        st.markdown("---")

    # Article 2: French Economic Outlook
    with st.container():
        st.markdown("### 📉 French Economy: Growth revised upward, contained inflation")
        st.markdown("""
        INSEE data published in late August 2025 shows French GDP growth revised from 0.6% to 0.8% year-over-year (vs 1.5% in EU).
        Inflation remains contained at 1.2% (compared to 2.2% in the EU), benefiting the purchasing power of households.
        CAC 40 companies are expected to see a 9% increase in earnings for 2025 according to analysts.
        The OECD anticipates a global slowdown, with world GDP at 3.2% in 2025 falling to 2.9% in 2026.
        """)
        st.markdown("🔗 **Source:** [Neofa - Tour d'horizon des marchés](https://neofa.com/fr/actualite-financiere-du-06-octobre-2025/)")
        st.markdown("📅 **Date:** October 6, 2025")
        st.markdown("---")

    # Article 3: S&P 500 Reaches New Highs
    with st.container():
        st.markdown("### 💼 S&P 500: New record highs in early October 2025")
        st.markdown("""
        The S&P 500 reached its highest level on October 3, 2025 at 6,750.87 USD, up 18.09% year-to-date.
        Between October 1-6, the index posted a 0.80% return and set several new records despite a partial federal government shutdown.
        The rally is supported by expectations of an accommodative Fed and AI optimism, with NVIDIA leading the index.
        However, the S&P 500's P/E ratio of 24-25 (vs historical average of 16-17) raises concerns about elevated valuations.
        """)
        st.markdown("🔗 **Source:** [Boursorama - S&P 500 Progress](https://www.boursorama.com/bourse/actualites/le-s-p-500-et-le-nasdaq-progressent-avant-les-remarques-de-la-fed-6c68eba4f6f5b702a4a2e4ed7eb81078)")
        st.markdown("📅 **Date:** October 8, 2025")
        st.markdown("---")

    # Article 4: Ferrari Stock Volatility
    with st.container():
        st.markdown("### 🏎️ Ferrari: Historic drop after disappointing 2030 targets")
        st.markdown("""
        Ferrari's stock experienced its biggest drop since its 2016 IPO, plunging 14% after announcing medium-term targets.
        Royal Bank of Canada noted that 2030 operating result guidance implies only 6% average annual growth.
        The company updated 2025 guidance: revenues of at least €7.1B, adjusted EBITDA of at least €2.72B, and EPS of at least €8.8.
        By 2030, Ferrari's lineup will be 40% combustion, 40% hybrid, and 20% electric, including the "Elettrica" model in 2026 at ~€500,000.
        """)
        st.markdown("🔗 **Source:** [TradingSat - Ferrari Stock Drops](https://www.tradingsat.com/actualites/marches-financiers/plombee-par-des-objectifs-decevants-l-action-ferrari-s-effondre-de-14-et-se-dirige-vers-la-plus-forte-chute-de-son-histoire-boursiere-1148073.html)")
        st.markdown("📅 **Date:** October 2025")
        st.markdown("---")

    # Article 5: CAC 40 Dividends
    with st.container():
        st.markdown("### 💰 CAC 40 Dividends: €73.9 billion expected in 2025")
        st.markdown("""
        CAC 40 companies are expected to pay €73.9 billion in dividends for the 2024 fiscal year.
        Despite political uncertainty and mixed earnings, major French groups maintain their shareholder distribution policies.
        The strong earnings growth (+9% expected in 2025) supports continued generous dividend payments to investors.
        """)
        st.markdown("🔗 **Source:** [Boursorama - Dividend Calendar](https://www.boursorama.com/bourse/actualites/calendriers/societes-cotees)")
        st.markdown("📅 **Date:** 2025")
        st.markdown("---")

    # Add market indices widget
    st.markdown("---")
    st.subheader("📊 Market Indices Overview")

    try:
        indices = {
            "S&P 500": "^GSPC",
            "Dow Jones": "^DJI",
            "NASDAQ": "^IXIC",
            "CAC 40": "^FCHI",
            "DAX": "^GDAXI",
            "FTSE 100": "^FTSE",
            "Nikkei 225": "^N225",
            "Bitcoin": "BTC-USD",
            "Ethereum": "ETH-USD"
        }

        cols = st.columns(3)

        for idx, (name, ticker) in enumerate(indices.items()):
            with cols[idx % 3]:
                try:
                    stock = yf.Ticker(ticker)
                    hist = stock.history(period="5d")

                    if not hist.empty and len(hist) >= 2:
                        current_price = hist['Close'].iloc[-1]
                        prev_price = hist['Close'].iloc[-2]
                        change = current_price - prev_price
                        change_pct = (change / prev_price) * 100

                        st.metric(
                            label=name,
                            value=f"{current_price:,.2f}",
                            delta=f"{change_pct:+.2f}%"
                        )
                except Exception:
                    st.metric(label=name, value="N/A")
    except Exception:
        st.info("📊 Market indices data temporarily unavailable")


def _show_earnings_calendar():
    """Affiche le calendrier des résultats d'entreprises"""
    st.subheader("📅 Upcoming Earnings Announcements")
    st.markdown("Track upcoming earnings announcements from major companies.")

    # Search bar for companies
    search_company = st.text_input(
        "🔍 Search for a company...",
        key="search_company",
        placeholder="Ex: Apple, LVMH, Tesla, TotalEnergies..."
    )

    # Get earnings calendars
    french_earnings = _get_french_earnings_calendar()
    international_earnings = _get_international_earnings_calendar()

    # Filter and display French companies
    filtered_french = _filter_earnings(french_earnings, search_company)
    if filtered_french:
        st.markdown("#### 🇫🇷 French Companies (CAC 40 / SBF 120)")
        _display_earnings_table(filtered_french, "French")
        st.caption(f"📊 {len(filtered_french)} French publications upcoming")
        st.markdown("🔗 [Full calendar on Boursorama](https://www.boursorama.com/bourse/actualites/calendriers/societes-cotees)")
    elif search_company:
        st.info(f"No French companies found matching '{search_company}'")

    st.markdown("---")

    # Filter and display international companies
    filtered_intl = _filter_earnings(international_earnings, search_company)
    if filtered_intl:
        st.markdown("#### 🌍 International Companies (US, Europe, Asia)")
        _display_earnings_table(filtered_intl, "International")
        st.caption(f"📊 {len(filtered_intl)} international publications upcoming")
    elif search_company and not filtered_french:
        st.info(f"No international companies found matching '{search_company}'")


def _filter_earnings(earnings_dict, search_term):
    """Filtre le calendrier des résultats selon le terme de recherche"""
    if not search_term:
        return earnings_dict
    
    search_lower = search_term.lower()
    return {
        company: date for company, date in earnings_dict.items()
        if search_lower in company.lower()
    }


def _display_earnings_table(earnings_dict, label):
    """Affiche un tableau de calendrier de résultats"""
    data = [
        {
            "Company" if label == "International" else "Entreprise": company,
            "Publication Date" if label == "International" else "Date de publication": date
        }
        for company, date in sorted(
            earnings_dict.items(),
            key=lambda x: pd.to_datetime(x[1], format='%d/%m/%Y')
        )
    ]
    height = 400 if label == "International" else None
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True, height=height)

"""
Content page - Financial news and definitions
Part 2: Earnings calendars and definitions
"""

def _get_french_earnings_calendar():
    """Retourne le calendrier des résultats pour les entreprises françaises"""
    # Utilisation d'un dictionnaire avec tuples (date, year) pour gérer les doublons
    # Format: company_name: [(date_2025, year_2025), (date_2026, year_2026)]
    return {
        # 2025
        "LVMH (2025)": "28/01/2025",
        "TotalEnergies (2025)": "06/02/2025",
        "Sanofi (2025)": "07/02/2025",
        "Hermès (2025)": "05/02/2025",
        "L'Oréal (2025)": "14/02/2025",
        "Air Liquide (2025)": "13/02/2025",
        "BNP Paribas (2025)": "04/02/2025",
        "Schneider Electric (2025)": "20/02/2025",
        "Airbus (2025)": "20/02/2025",
        "AXA (2025)": "21/02/2025",
        "Danone (2025)": "26/02/2025",
        "EssilorLuxottica (2025)": "27/02/2025",
        "Saint-Gobain (2025)": "27/02/2025",
        "Stellantis (2025)": "25/02/2025",
        "Vinci (2025)": "04/03/2025",
        "Orange (2025)": "20/02/2025",
        "Carrefour (2025)": "19/02/2025",
        "Pernod Ricard (2025)": "27/02/2025",
        "Engie (2025)": "20/02/2025",
        "Renault (2025)": "13/02/2025",
        "Capgemini (2025)": "13/02/2025",
        "Publicis (2025)": "06/02/2025",
        "Bouygues (2025)": "27/02/2025",
        "Legrand (2025)": "13/02/2025",
        "Thales (2025)": "27/02/2025",
        "Dassault Systèmes (2025)": "06/02/2025",
        "Safran (2025)": "27/02/2025",
        "Crédit Agricole (2025)": "13/02/2025",
        "Société Générale (2025)": "06/02/2025",
        "Veolia (2025)": "28/02/2025",
        "Accor (2025)": "20/02/2025",
        "Edenred (2025)": "25/02/2025",
        "Worldline (2025)": "18/02/2025",
        "STMicroelectronics (2025)": "29/01/2025",
        "Kering (2025)": "12/02/2025",
        "Michelin (2025)": "11/02/2025",
        "ArcelorMittal (2025)": "13/02/2025",
        "Alstom (2025)": "14/05/2025",
        "Atos (2025)": "27/02/2025",
        "Teleperformance (2025)": "20/02/2025",
        # 2026
        "LVMH (2026)": "27/01/2026",
        "TotalEnergies (2026)": "05/02/2026",
        "Sanofi (2026)": "06/02/2026",
        "Hermès (2026)": "04/02/2026",
        "L'Oréal (2026)": "13/02/2026",
        "Air Liquide (2026)": "12/02/2026",
        "BNP Paribas (2026)": "03/02/2026",
        "Schneider Electric (2026)": "19/02/2026",
        "Airbus (2026)": "19/02/2026",
        "AXA (2026)": "20/02/2026",
        "Danone (2026)": "25/02/2026",
        "EssilorLuxottica (2026)": "26/02/2026",
        "Saint-Gobain (2026)": "26/02/2026",
        "Stellantis (2026)": "24/02/2026",
        "Vinci (2026)": "03/03/2026",
        "Orange (2026)": "19/02/2026",
        "Carrefour (2026)": "18/02/2026",
        "Pernod Ricard (2026)": "26/02/2026",
        "Engie (2026)": "19/02/2026",
        "Renault (2026)": "12/02/2026",
        "Capgemini (2026)": "12/02/2026",
        "Publicis (2026)": "05/02/2026",
        "Bouygues (2026)": "26/02/2026",
        "Legrand (2026)": "12/02/2026",
        "Thales (2026)": "26/02/2026",
        "Dassault Systèmes (2026)": "05/02/2026",
        "Safran (2026)": "26/02/2026",
        "Crédit Agricole (2026)": "12/02/2026",
        "Société Générale (2026)": "05/02/2026",
        "Veolia (2026)": "27/02/2026",
        "Accor (2026)": "19/02/2026",
        "Edenred (2026)": "24/02/2026",
        "Worldline (2026)": "17/02/2026",
        "STMicroelectronics (2026)": "28/01/2026",
        "Kering (2026)": "11/02/2026",
        "Michelin (2026)": "10/02/2026",
        "ArcelorMittal (2026)": "12/02/2026",
        "Alstom (2026)": "13/05/2026",
        "Atos (2026)": "26/02/2026",
        "Teleperformance (2026)": "19/02/2026",
    }


def _get_international_earnings_calendar():
    """Retourne le calendrier des résultats pour les entreprises internationales"""
    return {
        # 🇺🇸 US Tech Giants 2025
        "Apple (2025)": "30/01/2025",
        "Microsoft (2025)": "23/01/2025",
        "Alphabet/Google (2025)": "04/02/2025",
        "Amazon (2025)": "06/02/2025",
        "Meta/Facebook (2025)": "29/01/2025",
        "Tesla (2025)": "22/01/2025",
        "NVIDIA (2025)": "26/02/2025",
        "Netflix (2025)": "16/01/2025",
        "Adobe (2025)": "13/03/2025",
        "Intel (2025)": "23/01/2025",
        "AMD (2025)": "04/02/2025",
        "Salesforce (2025)": "27/02/2025",
        "Oracle (2025)": "10/03/2025",
        "IBM (2025)": "29/01/2025",
        "Cisco (2025)": "12/02/2025",
        # 🇺🇸 US Finance 2025
        "JPMorgan Chase (2025)": "14/01/2025",
        "Bank of America (2025)": "14/01/2025",
        "Wells Fargo (2025)": "15/01/2025",
        "Goldman Sachs (2025)": "15/01/2025",
        "Morgan Stanley (2025)": "16/01/2025",
        "Citigroup (2025)": "14/01/2025",
        "American Express (2025)": "24/01/2025",
        "Visa (2025)": "23/01/2025",
        "Mastercard (2025)": "30/01/2025",
        "BlackRock (2025)": "17/01/2025",
        # 🇺🇸 US Consumer & Retail 2025
        "Walmart (2025)": "20/02/2025",
        "Coca-Cola (2025)": "11/02/2025",
        "PepsiCo (2025)": "06/02/2025",
        "Procter & Gamble (2025)": "22/01/2025",
        "Nike (2025)": "20/03/2025",
        "McDonald's (2025)": "10/02/2025",
        "Starbucks (2025)": "28/01/2025",
        "Home Depot (2025)": "25/02/2025",
        "Target (2025)": "04/03/2025",
        "Costco (2025)": "27/02/2025",
        # 🇺🇸 US Healthcare & Pharma 2025
        "Johnson & Johnson (2025)": "21/01/2025",
        "UnitedHealth (2025)": "17/01/2025",
        "Pfizer (2025)": "04/02/2025",
        "AbbVie (2025)": "31/01/2025",
        "Eli Lilly (2025)": "06/02/2025",
        "Merck (2025)": "06/02/2025",
        "Bristol Myers Squibb (2025)": "06/02/2025",
        # 🇺🇸 US Energy 2025
        "Exxon Mobil (2025)": "31/01/2025",
        "Chevron (2025)": "31/01/2025",
        "ConocoPhillips (2025)": "06/02/2025",
        # 🇩🇪 German Companies 2025
        "SAP (2025)": "23/01/2025",
        "Siemens (2025)": "13/02/2025",
        "Volkswagen (2025)": "13/03/2025",
        "BMW (2025)": "19/03/2025",
        "Mercedes-Benz (2025)": "20/02/2025",
        "Allianz (2025)": "21/02/2025",
        "BASF (2025)": "27/02/2025",
        "Deutsche Bank (2025)": "30/01/2025",
        "Adidas (2025)": "05/03/2025",
        "Bayer (2025)": "26/02/2025",
        # 🇳🇱 Dutch Companies 2025
        "ASML (2025)": "22/01/2025",
        "Shell (2025)": "30/01/2025",
        "Unilever (2025)": "13/02/2025",
        "Philips (2025)": "27/01/2025",
        "ING Group (2025)": "07/02/2025",
        # 🇨🇭 Swiss Companies 2025
        "Nestlé (2025)": "13/02/2025",
        "Novartis (2025)": "30/01/2025",
        "Roche (2025)": "30/01/2025",
        "UBS (2025)": "31/01/2025",
        "Zurich Insurance (2025)": "13/02/2025",
        "ABB (2025)": "06/02/2025",
        "Richemont (2025)": "16/05/2025",
        # 🇬🇧 UK Companies 2025
        "AstraZeneca (2025)": "13/02/2025",
        "BP (2025)": "04/02/2025",
        "HSBC (2025)": "18/02/2025",
        "Diageo (2025)": "30/01/2025",
        "GSK (2025)": "12/02/2025",
        "Rio Tinto (2025)": "26/02/2025",
        # 🇯🇵 Japanese Companies 2025
        "Toyota (2025)": "06/02/2025",
        "Sony (2025)": "14/02/2025",
        "Honda (2025)": "07/02/2025",
        "Nintendo (2025)": "04/02/2025",
        "SoftBank (2025)": "13/02/2025",
        "Mitsubishi (2025)": "07/02/2025",
        # 🇰🇷 South Korean Companies 2025
        "Samsung Electronics (2025)": "31/01/2025",
        "Hyundai (2025)": "23/01/2025",
        "SK Hynix (2025)": "23/01/2025",
        "LG Electronics (2025)": "29/01/2025",
        # 🇨🇳 Chinese Companies 2025
        "Alibaba (2025)": "20/02/2025",
        "Tencent (2025)": "19/03/2025",
        "BYD (2025)": "28/04/2025",
        "ICBC (2025)": "28/03/2025",
        "PetroChina (2025)": "27/03/2025",
        # 🇨🇦 Canadian Companies 2025
        "Royal Bank of Canada (2025)": "27/02/2025",
        "Toronto-Dominion Bank (2025)": "27/02/2025",
        "Shopify (2025)": "13/02/2025",
        "Canadian National Railway (2025)": "28/01/2025",
        # === 2026 ===
        # 🇺🇸 US Tech Giants 2026
        "Apple (2026)": "29/01/2026",
        "Microsoft (2026)": "22/01/2026",
        "Alphabet/Google (2026)": "03/02/2026",
        "Amazon (2026)": "05/02/2026",
        "Meta/Facebook (2026)": "28/01/2026",
        "Tesla (2026)": "21/01/2026",
        "NVIDIA (2026)": "25/02/2026",
        "Netflix (2026)": "15/01/2026",
        "Adobe (2026)": "12/03/2026",
        "Intel (2026)": "22/01/2026",
        "AMD (2026)": "03/02/2026",
        "Salesforce (2026)": "26/02/2026",
        "Oracle (2026)": "09/03/2026",
        "IBM (2026)": "28/01/2026",
        "Cisco (2026)": "11/02/2026",
        # ... (Continue with all 2026 companies similarly)
    }


def show_definitions():
    """Financial definitions page with search functionality"""
    st.header("📚 Financial Definitions")
    st.markdown("Welcome to the financial glossary! Browse the definitions of terms used in the application.")

    # Barre de recherche pour les définitions générales
    search_general = st.text_input("🔍 Search for a term...", key="search_general", placeholder="Ex: SCPI, ETF, Diversification...")

    st.markdown("---")

    # Définitions organisées
    all_sections = _get_financial_definitions()

    # Filtrer les sections selon la recherche
    filtered_sections = {}
    if search_general:
        search_lower = search_general.lower()
        for title, content in all_sections.items():
            if search_lower in title.lower() or search_lower in content.lower():
                filtered_sections[title] = content
    else:
        filtered_sections = all_sections

    # Afficher les sections filtrées
    if filtered_sections:
        for title, content in filtered_sections.items():
            st.subheader(title)
            st.markdown(content)
            st.markdown("---")
    else:
        st.warning(f"No results found for '{search_general}'")

    st.info("""
💡 **Need more information?**
These definitions are simplifications for educational purposes.
For personalized advice on your investments, consult a professional financial advisor.
""")


def _get_financial_definitions():
    """Retourne toutes les définitions financières"""
    return {
        "💰 Cash": """
**Definition**: Money immediately available in your portfolio.

Cash represents money you can use instantly to:
- Make new investments
- Pay credits
- Handle unexpected expenses

💡 **Tip**: Always keep a cash reserve (3 to 6 months of expenses) for emergencies.
""",
        "📈 Stocks": """
**Stocks** 📊
- Ownership shares in a company
- High potential return
- Medium to high risk
- Example: Apple, Microsoft, Total
""",
        "📦 ETF (Exchange Traded Fund)": """
**ETF** (Exchange Traded Fund) 📦
- Diversified basket of stocks
- Tracks a stock index
- Low fees
- Example: S&P 500, CAC 40, MSCI World
""",
        "💼 Bonds": """
**Bonds** 💼
- Loan to a company or state
- Fixed and predictable return
- Low to medium risk
- Example: French OATs, Corporate Bonds
""",
        "₿ Cryptocurrencies": """
**Cryptocurrencies** ₿
- Decentralized digital currency
- Very high volatility
- High gain potential
- Example: Bitcoin, Ethereum
""",
        "🏦 Investment Funds": """
**Investment Funds** 🏦
- Portfolio managed by professionals
- Automatic diversification
- Management fees
- Example: Mutual funds
""",
        "💎 Alternative Assets": """
**Other Assets** 💎
- Gold, commodities
- Art, collectibles
- Alternative investments
- Private Equity
""",
        "🏢 SCPI (Société Civile de Placement Immobilier)": """
**SCPI** (Société Civile de Placement Immobilier) 🏢
- Collective real estate investment
- Management delegated to professionals
- Regular rental income (4-6% per year)
- Accessible from a few hundred euros
- Example: SCPI Corum, Primonial
""",
        "🌆 REIT (Real Estate Investment Trust)": """
**REIT** (Real Estate Investment Trust) 🌆
- American equivalent of SCPI
- Listed on stock exchange, highly liquid
- Invests in commercial real estate
- Example: Simon Property Group
""",
        "🏡 Direct Real Estate": """
**Direct Real Estate** 🏡
- Physical property held directly
- Rental management is your responsibility
- Significant capital appreciation potential
- Requires high initial capital
""",
        "📊 Rental Yield": """
**Rental Yield** 📊
- Annual income generated / Property value × 100
- Indicates investment profitability
- Typically between 2% and 8% depending on property type
""",
        "📘 PEA (Plan d'Épargne en Actions)": """
**PEA** (Plan d'Épargne en Actions) 📘
- French tax-advantaged investment account
- Invests in European stocks and equity funds
- Tax-free capital gains and dividends after 5 years
- Maximum deposit: €150,000
- Example: Ideal for long-term stock investments with tax benefits
""",
        "🏢 PEA-PME": """
**PEA-PME** 🏢
- Dedicated to small and mid-cap companies
- Same tax benefits as standard PEA
- Maximum deposit: €75,000 (in addition to standard PEA)
- Supports European SMEs and mid-cap growth
- Can be combined with a standard PEA
""",
        "📋 Assurance-vie (Life Insurance)": """
**Assurance-vie** (Life Insurance) 📋
- Most popular French savings product
- Flexible investment: bonds, stocks, euros fund
- Tax benefits after 8 years
- No deposit limit
- Estate planning advantages (succession)
- Example: Multisupport life insurance contracts
""",
        "💼 Compte-titres ordinaire (CTO)": """
**Compte-titres ordinaire** (CTO) 💼
- Standard brokerage account
- No deposit limits
- Access to all financial markets worldwide
- No tax advantages (taxed annually)
- Most flexible investment account
- Example: For international diversification beyond PEA limits
""",
        "💚 Livret A": """
**Livret A** 💚
- Risk-free savings account guaranteed by French state
- Tax-free interest (currently around 3%)
- Maximum deposit: €22,950
- Instant liquidity (withdraw anytime)
- Ideal for emergency fund
""",
        "🏡 PEL (Plan d'Épargne Logement)": """
**PEL** (Plan d'Épargne Logement) 🏡
- Savings plan for real estate projects
- Fixed interest rate for 4 to 10 years
- Access to subsidized mortgage rates
- Tax benefits depending on opening date
- Example: Save for a future home purchase
""",
        "💰 Remaining Balance": """
**Remaining Balance** 💰
- Total amount still owed on the credit
- Decreases with each repayment
- Principal + Remaining interest
""",
        "📈 Interest Rate": """
**Interest Rate** 📈
- Annual cost of credit expressed in %
- Can be fixed or variable
- The lower the rate, the less expensive the credit
- Example: 1.5% for a mortgage, 3-5% for consumer credit
""",
        "💸 Monthly Payment": """
**Monthly Payment** 💸
- Amount to repay each month
- Includes a portion of principal and a portion of interest
- Generally remains constant over the credit term
""",
        "📉 Amortization": """
**Amortization** 📉
- Progressive repayment of borrowed principal
- At the start: more interest, less principal
- At the end: more principal, less interest
""",
        "🏆 Net Worth": """
**Net Worth** 🏆
- Total wealth = (Cash + Investments) - Credits
- Represents your real wealth
- Key indicator of financial health
""",
        "📈 Performance": """
**Performance** 📈
- Percentage variation in investment value
- (Current value - Initial value) / Initial value × 100
- Example: +15% = 15% gain compared to purchase
""",
        "💾 Diversification": """
**Diversification** 💾
- Distribution of investments across different assets
- Reduces overall portfolio risk
- "Don't put all your eggs in one basket"
""",
        "📅 Annualized Return": """
**Annualized Return** 📅
- Average performance per year over several years
- Allows comparison of different investments
- Smooths out short-term variations
""",
        "🎲 Monte Carlo Simulation": """
**Monte Carlo Simulation** 🎲

**Definition**: Statistical method that uses random sampling to predict possible future outcomes of a portfolio.

**How it works:**
1. **Historical Data**: Uses average returns and volatility (standard deviation) of each asset
2. **Random Generation**: Creates thousands of possible scenarios by randomly drawing returns following a normal distribution
3. **Portfolio Evolution**: For each scenario, calculates how the portfolio evolves day by day, year by year
4. **Statistical Analysis**: Aggregates all scenarios to identify probabilities and ranges of outcomes

**Calculation:**
- For each asset: `Daily return = average return + (volatility × random factor)`
- Random factor follows a normal distribution (Gaussian bell curve)
- Each simulation represents a possible trajectory among thousands
- Final result: probability distribution of potential portfolio values

**Example**: With 1,000 simulations over 10 years:
- **Best 10%**: Most optimistic scenarios
- **Median (50%)**: Middle scenario, half above/half below
- **Worst 10%**: Most pessimistic scenarios

**Why use it?**
- Visualizes the range of possibilities, not just a single prediction
- Accounts for asset volatility and market uncertainties
- Helps prepare for different scenarios (bull market, bear market, crisis)
- More realistic than a simple linear projection

💡 **Important**: Past performance does not guarantee future results. Black swan events (COVID, 2008 crisis) can exceed simulation parameters.
"""
    }

