"""
Summary page - Portfolio overview
"""

import pandas as pd
import streamlit as st

from src.finview.ui.formatting import format_currency, format_percentage
from src.finview.visualizations import create_monthly_transactions_chart


def show_summary(portfolio):
    """Résumé global avec métriques et tableaux"""
    st.header("Summary")

    # --- Métriques principales ---
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: 
        st.metric("💰 Cash", format_currency(portfolio.cash))
    with col2: 
        st.metric("📈 Financial Inv.", format_currency(portfolio.get_financial_investments_value()))
    with col3: 
        st.metric("🏠 Real Estate Inv.", format_currency(portfolio.get_real_estate_investments_value()))
    with col4:
        total_credits = portfolio.get_total_credits_balance()
        st.metric("💳 Credits", format_currency(total_credits) if total_credits > 0 else "0€")
    with col5: 
        st.metric("🏆 Net Worth", format_currency(portfolio.get_net_worth()))

    # --- Infos supplémentaires ---
    additional_info = []
    if portfolio.real_estate_investments:
        annual_rental_income = portfolio.get_total_annual_rental_income()
        if annual_rental_income > 0:
            monthly_income = annual_rental_income / 12
            additional_info.append(
                f"💰 Annual rental income: {format_currency(annual_rental_income)} "
                f"({format_currency(monthly_income)}/month)"
            )

    total_investments = len(portfolio.financial_investments) + len(portfolio.real_estate_investments)
    if total_investments > 0:
        diversification_score = "High" if total_investments >= 5 else "Medium" if total_investments >= 3 else "Low"
        diversification_color = "🟢" if total_investments >= 5 else "🟡" if total_investments >= 3 else "🔴"
        additional_info.append(f"{diversification_color} Diversification: {diversification_score} ({total_investments} investments)")

    if portfolio.financial_investments and portfolio.real_estate_investments:
        fin_ratio = portfolio.get_financial_investments_value() / (
            portfolio.get_financial_investments_value() + portfolio.get_real_estate_investments_value()
        ) * 100
        re_ratio = 100 - fin_ratio
        additional_info.append(f"⚖️ Allocation: {format_percentage(fin_ratio)} financial / {format_percentage(re_ratio)} real estate")

    if additional_info:
        for info in additional_info:
            st.info(info)

    st.markdown("---")

    # --- Onglets Portfolio Vision et History ---
    tab1, tab2 = st.tabs(["📊 Portfolio Vision", "📋 Portfolio History"])

    with tab1:
        _show_portfolio_vision(portfolio)

    with tab2:
        _show_transaction_history(portfolio)


def _show_portfolio_vision(portfolio):
    """Affiche les tableaux récapitulatifs de tous les produits du portefeuille"""
    
    st.subheader("📈 Financial Investments")
    if portfolio.financial_investments:
        fin_data = []
        for name, inv in portfolio.financial_investments.items():
            inv_type = getattr(inv, 'investment_type', 'N/A')
            gain_loss = inv.get_gain_loss()
            gain_loss_str = format_currency(abs(gain_loss))
            if gain_loss < 0:
                gain_loss_str = f"-{gain_loss_str}"
            
            fin_data.append({
                "Name": name,
                "Type": inv_type,
                "Quantity": inv.quantity,
                "Unit value": format_currency(inv.current_value),
                "Total value": format_currency(inv.get_total_value()),
                "Gain/Loss": gain_loss_str,
                "Performance": format_percentage(inv.get_gain_loss_percentage())
            })
        st.dataframe(pd.DataFrame(fin_data), use_container_width=True)
    else:
        st.info("No financial investments")

    st.subheader("🏠 Real Estate Investments")
    if portfolio.real_estate_investments:
        re_data = []
        for name, inv in portfolio.real_estate_investments.items():
            property_type = getattr(inv, 'property_type', 'N/A')
            location = getattr(inv, 'location', 'N/A')
            rental_yield = getattr(inv, 'rental_yield', 0)
            annual_income = inv.get_annual_rental_income() if hasattr(inv, 'get_annual_rental_income') else 0
            re_data.append({
                "Name": name,
                "Type": property_type,
                "Location": location if location else "N/A",
                "Yield": f"{rental_yield:.1f}%" if rental_yield > 0 and rental_yield != int(rental_yield) else f"{int(rental_yield)}%" if rental_yield > 0 else "N/A",
                "Total value": format_currency(inv.get_total_value()),
                "Annual income": format_currency(annual_income) if annual_income > 0 else "N/A",
                "Performance": format_percentage(inv.get_gain_loss_percentage())
            })
        st.dataframe(pd.DataFrame(re_data), use_container_width=True)
    else:
        st.info("No real estate investments")

    st.subheader("💳 Credits")
    if portfolio.credits:
        credit_data = []
        for name, credit in portfolio.credits.items():
            credit_data.append({
                "Name": name,
                "Remaining balance": format_currency(credit.get_remaining_balance()),
                "Rate": f"{credit.interest_rate:.1f}%" if credit.interest_rate != int(credit.interest_rate) else f"{int(credit.interest_rate)}%",
                "Monthly payment": format_currency(credit.monthly_payment)
            })
        st.dataframe(pd.DataFrame(credit_data), use_container_width=True)
    else:
        st.info("No credits")


def _show_transaction_history(portfolio):
    """Affiche l'historique des transactions"""
    
    if not portfolio.transaction_history:
        st.info("No transactions recorded")
        st.markdown("💡 **Tip**: Use the 'Create demo portfolio' button in the sidebar to see a full history example!")
        return

    df_history = pd.DataFrame(portfolio.transaction_history)
    df_history = df_history.sort_values('date', ascending=False)

    # Adding history metrics
    st.subheader("📊 Activity Summary")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_transactions = len(df_history)
        st.metric("Total transactions", total_transactions)

    with col2:
        cash_transactions = df_history[df_history['type'].str.contains('CASH')]['amount'].sum()
        st.metric("Cash movements", f"{format_currency(cash_transactions)}")

    with col3:
        total_investments_value = portfolio.get_financial_investments_value() + portfolio.get_real_estate_investments_value()
        st.metric("Investments", f"{format_currency(total_investments_value)}")

    with col4:
        credit_payments = df_history[df_history['type'] == 'CREDIT_PAYMENT']['amount'].sum()
        st.metric("Credit payments", f"{format_currency(credit_payments)}")

    # Chart of transaction evolution by month
    df_history['month'] = pd.to_datetime(df_history['date']).dt.to_period('M').astype(str)
    monthly_transactions = df_history.groupby(['month', 'type']).size().reset_index(name='count')

    if len(monthly_transactions) > 0:
        fig = create_monthly_transactions_chart(df_history)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Transaction type mapping
    mapping_type_dictionnary = {
        'CASH_ADD': '💰 Cash addition',
        'CASH_WITHDRAW': '💸 Cash withdrawal',
        'FINANCIAL_INVESTMENT_BUY': '📈 Investment purchase',
        'REAL_ESTATE_INVESTMENT_BUY': '🏠 Real estate purchase',
        'INVESTMENT_SELL': '📉 Investment sale',
        'INVESTMENT_UPDATE': '🔄 Price update',
        'CREDIT_ADD': '🏦 New credit',
        'CREDIT_PAYMENT': '💳 Credit payment',
        'CREDIT_INTEREST': '📊 Credit interest'
    }

    # Créer un mapping inversé pour retrouver la clé originale
    reverse_mapping = {v: k for k, v in mapping_type_dictionnary.items()}

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        # Obtenir les types uniques du DataFrame
        unique_types = df_history['type'].unique()
        
        # Mapper les types vers leurs labels affichables
        display_options = ["All"] + [mapping_type_dictionnary.get(t, t) for t in unique_types]
        
        # Créer la selectbox avec les labels affichables
        type_filter_display = st.selectbox("Filter by type", display_options)
        
        # Convertir le choix affiché vers la valeur originale pour le filtrage
        if type_filter_display == "All":
            type_filter = "All"
        else:
            type_filter = reverse_mapping.get(type_filter_display, type_filter_display)

    with col2:
        date_filter = st.date_input("Minimum date", value=None)

    # Apply filters
    filtered_df = df_history.copy()
    if type_filter != "All":
        filtered_df = filtered_df[filtered_df['type'] == type_filter]
    if date_filter:
        filtered_df = filtered_df[pd.to_datetime(filtered_df['date']).dt.date >= date_filter]

    # Improved table display
    display_df = filtered_df.copy()
    display_df['Type'] = display_df['type'].map(mapping_type_dictionnary).fillna(display_df['type'])
    display_df['Amount'] = display_df['amount'].apply(lambda x: f"{x:.2f}€" if x > 0 else "")
    display_df['Date'] = pd.to_datetime(display_df['date']).dt.strftime('%d/%m/%Y %H:%M')

    # Display table
    st.subheader(f"📋 Transactions ({len(filtered_df)} results)")
    st.dataframe(
        display_df[['Date', 'Type', 'Amount', 'description']].rename(columns={'description': 'Description'}),
        use_container_width=True,
        height=400
    )

    # Detailed statistics
    st.subheader("📈 Detailed Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Number of transactions", len(filtered_df))
    with col2:
        total_amount = filtered_df['amount'].sum()
        st.metric("Total amount", f"{format_currency(total_amount)}")
    with col3:
        avg_amount = filtered_df['amount'].mean() if len(filtered_df) > 0 else 0
        st.metric("Average amount", f"{format_currency(avg_amount)}")

    # Timeline of major events
    if len(df_history) > 5:
        st.subheader("🕒 Major Events Timeline")
        major_events = df_history[df_history['type'].isin(['INVESTMENT_BUY', 'CREDIT_ADD', 'INVESTMENT_SELL'])].head(10)
        for _, event in major_events.iterrows():
            event_date = pd.to_datetime(event['date']).strftime('%d/%m/%Y')
            if event['type'] == 'INVESTMENT_BUY':
                st.write(f"📈 **{event_date}**: {event['description']} ({format_currency(event['amount'])})")
            elif event['type'] == 'CREDIT_ADD':
                st.write(f"🏦 **{event_date}**: {event['description']} ({format_currency(event['amount'])})")
            elif event['type'] == 'INVESTMENT_SELL':
                st.write(f"📉 **{event_date}**: {event['description']} ({format_currency(event['amount'])})")