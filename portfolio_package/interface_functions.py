import pandas as pd
import streamlit as st
import yfinance as yf
from portfolio_package.save_load_ptf_functions import save_portfolio
from portfolio_package.yahoo_search import asset_search_tab
from portfolio_package.patrimoine_prediction import simulate_portfolio_future, create_statistics_summary

# Import des visualisations externalisées
from portfolio_package.visualizations import (
    display_portfolio_pie,
    display_portfolio_evolution,
    display_financial_investments,
    display_performance_chart,
    display_world_map,
)


# === UTILITAIRES ===
def format_currency(value):
    """Formate une valeur monétaire avec séparateurs et €"""
    if value == int(value):
        return f"{int(value):,}€".replace(',', ' ')
    return f"{value:,.2f}€".replace(',', ' ')


def format_percentage(value):
    """Formate un pourcentage avec signe si négatif"""
    if value == int(value):
        return f"{int(value):+d}%" if value != abs(value) or value < 0 else f"{int(value)}%"
    return f"{value:+.1f}%" if value != abs(value) or value < 0 else f"{value:.1f}%"


# === PAGES PRINCIPALES ===
def show_summary(portfolio):
    """Résumé global avec métriques et tableaux"""
    st.header("Summary")

    # --- Métriques principales ---
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.metric("💰 Cash", format_currency(portfolio.cash))
    with col2: st.metric("📈 Financial Inv.", format_currency(portfolio.get_financial_investments_value()))
    with col3: st.metric("🏠 Real Estate Inv.", format_currency(portfolio.get_real_estate_investments_value()))
    with col4: st.metric("💳 Credits", f"-{format_currency(portfolio.get_total_credits_balance())}"[:-1] + "€")
    with col5: st.metric("🏆 Net Worth", format_currency(portfolio.get_net_worth()))

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
        additional_info.append(f"⚖️ Allocation: {fin_ratio:.0f}% financial / {re_ratio:.0f}% real estate")

    if additional_info:
        for info in additional_info:
            st.info(info)

    st.markdown("---")

    # --- Tableaux par type ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📈 Financial Investments")
        if portfolio.financial_investments:
            fin_data = []
            for name, inv in portfolio.financial_investments.items():
                inv_type = getattr(inv, 'investment_type', 'N/A')
                fin_data.append({
                    "Name": name,
                    "Type": inv_type,
                    "Quantity": inv.quantity,
                    "Unit value": format_currency(inv.current_value),
                    "Total value": format_currency(inv.get_total_value()),
                    "Gain/Loss": f"{format_currency(inv.get_gain_loss())[:-1] if inv.get_gain_loss() >= 0 else '-' + format_currency(abs(inv.get_gain_loss()))[:-1]}€",
                    "Performance": format_percentage(inv.get_gain_loss_percentage())
                })
            st.dataframe(pd.DataFrame(fin_data), use_container_width=True)
        else:
            st.info("No financial investments")

    with col2:
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

    with col3:
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


def manage_cash(portfolio):
    """Cash management sub-tab"""
    st.subheader("💵 Cash Management")
    st.metric("Current cash", format_currency(portfolio.cash))

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Add cash")
        add_amount = st.number_input("Amount to add", min_value=0.01, step=0.01, key="add_cash")
        add_description = st.text_input("Description", value="Cash addition", key="add_desc")
        if st.button("Add", key="btn_add"):
            portfolio.add_cash(add_amount, add_description)
            save_portfolio(portfolio)
            st.success(f"{format_currency(add_amount)} added successfully!")
            st.rerun()

    with col2:
        st.markdown("#### Withdraw cash")
        if portfolio.cash > 0.01:
            max_withdraw = max(0.01, portfolio.cash)
            withdraw_amount = st.number_input("Amount to withdraw", min_value=0.01, max_value=max_withdraw, step=0.01, key="withdraw_cash")
            withdraw_description = st.text_input("Description", value="Cash withdrawal", key="withdraw_desc")
            can_withdraw = portfolio.cash >= withdraw_amount
            if st.button("Withdraw", key="btn_withdraw", disabled=not can_withdraw):
                if can_withdraw and portfolio.withdraw_cash(withdraw_amount, withdraw_description):
                    save_portfolio(portfolio)
                    st.success(f"{format_currency(withdraw_amount)} withdrawn successfully!")
                    st.rerun()
                else:
                    st.error("Insufficient funds!")
        else:
            st.info("Not enough cash available to make a withdrawal")


def manage_investments(portfolio):
    """Investment management sub-tab"""
    st.subheader("📈 Investment Management")

    tab1, tab2, tab3, tab4 = st.tabs(["Add manually", "🔍 Search asset", "Update", "Sell"])

    with tab1:
        st.markdown("#### New manual investment")

        investment_type = st.selectbox("Investment type",
                                     ["💰 Financial", "🏠 Real Estate"],
                                     key="investment_type_select")

        inv_name = st.text_input("Investment name")
        inv_price = st.number_input("Unit price", min_value=0.01, step=0.01)
        inv_quantity = st.number_input("Quantity", min_value=0.01, step=0.01)

        if investment_type == "💰 Financial":
            col1, col2 = st.columns(2)
            with col1:
                financial_type = st.selectbox("Category",
                                            ["Stock", "ETF", "Bond", "Crypto", "Fund", "Other"],
                                            key="financial_category")
            with col2:
                location = st.text_input("🌍 Location (optional)",
                                       placeholder="Ex: United States, Europe, Japan",
                                       key="financial_location",
                                       help="Allows you to locate the investment on the world map")
        else:
            col1, col2 = st.columns(2)
            with col1:
                property_type = st.selectbox("Property type",
                                           ["SCPI", "REIT", "Direct real estate", "Real estate company", "Other"],
                                           key="property_category")
            with col2:
                location = st.text_input("🌍 Location",
                                       placeholder="Ex: Paris, United States, London",
                                       key="real_estate_location",
                                       help="Geographic location of the real estate property")

            rental_yield = st.number_input("Annual rental yield (%)",
                                         min_value=0.0, max_value=20.0,
                                         value=0.0, step=0.1,
                                         key="rental_yield",
                                         help="Estimated annual rental yield in %")

        total_cost = inv_price * inv_quantity
        st.info(f"Total cost: {format_currency(total_cost)} (Available cash: {format_currency(portfolio.cash)})")

        if st.button("Buy", key="manual_buy"):
            if inv_name and inv_name not in portfolio.investments:
                success = False
                if investment_type == "💰 Financial":
                    success = portfolio.add_financial_investment(inv_name, inv_price, inv_quantity, financial_type, location)
                else:
                    success = portfolio.add_real_estate_investment(inv_name, inv_price, inv_quantity,
                                                                 property_type, location, rental_yield)

                if success:
                    save_portfolio(portfolio)
                    location_msg = f" (📍 {location})" if location else ""
                    st.success(f"Investment '{inv_name}' added successfully!{location_msg}")
                    if location:
                        st.info("🌍 Check the 'Investments Map' tab to see your geolocated investment!")
                    st.rerun()
                else:
                    st.error("Insufficient funds!")
            else:
                st.error("Invalid name or investment already exists!")

    with tab2:
        portfolio_addition = asset_search_tab()

        if portfolio_addition:
            asset_name = portfolio_addition['name']
            asset_price = portfolio_addition['price']
            asset_quantity = portfolio_addition['quantity']

            if asset_name not in portfolio.investments:
                if portfolio.add_investment(asset_name, asset_price, asset_quantity):
                    save_portfolio(portfolio)
                    st.success(f"🎉 Asset '{asset_name}' added to portfolio successfully!")
                    for key in ['searched_ticker', 'searched_price', 'add_to_portfolio']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
                else:
                    st.error("💸 Insufficient funds for this purchase!")
            else:
                st.warning(f"⚠️ Asset '{asset_name}' already exists in your portfolio. Use the 'Update' tab to modify its values.")

    with tab3:
        st.markdown("#### Update values")
        if portfolio.investments:
            inv_to_update = st.selectbox("Investment", list(portfolio.investments.keys()))
            current_value = portfolio.investments[inv_to_update].current_value
            new_value = st.number_input("New unit value", value=current_value, step=0.01)

            if st.checkbox("🔄 Get current price from Yahoo Finance"):
                try:
                    ticker_test = yf.Ticker(inv_to_update)
                    current_data = ticker_test.history(period="1d")
                    if not current_data.empty:
                        live_price = current_data['Close'].iloc[-1]
                        new_value = st.number_input(
                            "New unit value",
                            value=float(live_price),
                            step=0.01,
                            key="live_price_update"
                        )
                        st.info(f"💹 Real-time price retrieved: {live_price:.2f}")
                except:
                    st.warning("⚠️ Unable to retrieve real-time price. Use manual input.")

            if st.button("Update"):
                portfolio.update_investment_value(inv_to_update, new_value)
                save_portfolio(portfolio)
                st.success(f"Value of '{inv_to_update}' updated!")
                st.rerun()
        else:
            st.info("No investments to update")

    with tab4:
        st.markdown("#### Sell investments")
        if portfolio.investments:
            inv_to_sell = st.selectbox("Investment", list(portfolio.investments.keys()), key="sell_select")
            current_quantity = float(portfolio.investments[inv_to_sell].quantity)
            max_sell_quantity = max(0.01, current_quantity) if current_quantity > 0 else 0.01
            default_sell_quantity = min(current_quantity, max_sell_quantity) if current_quantity > 0 else 0.01
            sell_quantity = st.number_input(
                            "Quantity to sell",
                            min_value=0.01,
                            max_value=max_sell_quantity,
                            value=default_sell_quantity,
                            step=0.01
                        )
            sale_value = portfolio.investments[inv_to_sell].current_value * sell_quantity
            st.info(f"Sale value: {format_currency(sale_value)}")

            can_sell = current_quantity >= sell_quantity and current_quantity > 0
            if st.button("Sell", disabled=not can_sell):
                if can_sell:
                    portfolio.sell_investment(inv_to_sell, sell_quantity)
                    save_portfolio(portfolio)
                    st.success(f"Sale completed successfully!")
                    st.rerun()
                else:
                    st.error("Insufficient quantity for sale!")
        else:
            st.info("No investments to sell")


def manage_credits(portfolio):
    """Credit management sub-tab"""
    st.subheader("💳 Credit Management")

    tab1, tab2 = st.tabs(["Add credit", "Pay credit"])

    with tab1:
        st.markdown("#### New credit")
        credit_name = st.text_input("Credit name")
        credit_amount = st.number_input("Amount", min_value=0.01, step=0.01)
        credit_rate = st.number_input("Annual interest rate (%)", min_value=0.0, step=0.1)
        credit_payment = st.number_input("Monthly payment (optional)", min_value=0.0, step=0.01)

        if st.button("Add credit"):
            if credit_name and credit_name not in portfolio.credits:
                portfolio.add_credit(credit_name, credit_amount, credit_rate, credit_payment)
                save_portfolio(portfolio)
                st.success(f"Credit '{credit_name}' added successfully!")
                st.rerun()
            else:
                st.error("Invalid name or credit already exists!")

    with tab2:
        st.markdown("#### Make a payment")
        if portfolio.credits:
            credit_to_pay = st.selectbox("Credit", list(portfolio.credits.keys()))
            remaining_balance = portfolio.credits[credit_to_pay].get_remaining_balance()
            max_payment = max(0.01, min(portfolio.cash, remaining_balance)) if min(portfolio.cash, remaining_balance) > 0 else 0.01
            payment_amount = st.number_input("Payment amount", min_value=0.01, max_value=max_payment, step=0.01)
            st.info(f"Remaining balance: {format_currency(remaining_balance)} | Available cash: {format_currency(portfolio.cash)}")

            can_pay = portfolio.cash >= payment_amount and portfolio.cash > 0 and remaining_balance > 0
            if st.button("Pay", disabled=not can_pay):
                if can_pay and portfolio.pay_credit(credit_to_pay, payment_amount):
                    save_portfolio(portfolio)
                    st.success(f"Payment of {format_currency(payment_amount)} completed!")
                    st.rerun()
                else:
                    st.error("Unable to make payment!")
        else:
            st.info("No credits to pay")


def show_wealth_management(portfolio):
    """Gestion patrimoniale (Cash / Investissements / Crédits)"""
    st.header("💼 Wealth Management")
    tab1, tab2, tab3 = st.tabs(["💵 Manage Cash", "📈 Investments", "💳 Credits"])
    with tab1: manage_cash(portfolio)
    with tab2: manage_investments(portfolio)
    with tab3: manage_credits(portfolio)


def show_dashboard_tabs(portfolio):
    """Dashboard avec onglets graphiques"""
    st.header("📈 Dashboard")
    tab1, tab2, tab3 = st.tabs(["📊 Portfolio", "💎 Assets", "🌍 Investments Map"])
    with tab1: show_portfolio_charts(portfolio)
    with tab2: show_assets_analytics(portfolio)
    with tab3: show_world_map(portfolio)


# === SOUS-PAGES VISUALISATION ===
def show_portfolio_charts(portfolio):
    display_portfolio_pie(portfolio)
    display_portfolio_evolution(portfolio)


def show_assets_analytics(portfolio):
    if not portfolio.investments:
        st.info("No investments to analyze")
        return
    display_financial_investments(portfolio)
    st.markdown("---")
    display_performance_chart(portfolio)


def show_world_map(portfolio):
    if len(portfolio.financial_investments) + len(portfolio.real_estate_investments) > 0:
        display_world_map(portfolio)
    else:
        st.info("🌍 No investments to locate at the moment")


def show_predictions(portfolio):
    st.header("🔮 Wealth Predictions")
    if not portfolio.investments:
        st.info("Add investments to see predictions")
        return

    years = st.selectbox("Prediction horizon", options=[1, 5, 10, 20, 30], index=2)
    num_simulations = st.selectbox("Number of simulations", options=[100, 500, 1000, 2000], index=2)
    run_prediction = st.button("🚀 Run", type="primary")

    if run_prediction:
        with st.spinner(f"Simulating {num_simulations} scenarios over {years} years..."):
            prediction_results = simulate_portfolio_future(portfolio, years=years, num_simulations=num_simulations)
            st.session_state.prediction_results = prediction_results
            st.session_state.prediction_years = years

    if 'prediction_results' in st.session_state:
        results = st.session_state.prediction_results
        display_predictions(results)

        st.markdown("---")
        st.subheader("📈 Simulation Statistics")
        stats = create_statistics_summary(results)

        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Current Wealth", format_currency(stats['initial']))
        with col2: st.metric(f"Median ({years} years)", format_currency(stats['final']['p50']))
        with col3: st.metric("Optimistic (P75)", format_currency(stats['final']['p75']))
        with col4: st.metric("Conservative (P25)", format_currency(stats['final']['p25']))


# === ONGLET DEFINITIONS ===
def show_definitions():
    st.header("📚 Financial Definitions")
    st.markdown("Welcome to the financial glossary! Browse the definitions of terms used in the application.")
    # (Définitions conservées identiques à ton script original)
