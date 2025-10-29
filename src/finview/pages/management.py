"""
Wealth management page - Cash, Investments, and Credits management
"""

import streamlit as st
import yfinance as yf

from src.finview.ui.formatting import format_currency
from src.finview.ui.portfolio_persistence import save_portfolio
from src.finview.market import asset_search_tab


def show_wealth_management(portfolio):
    """Gestion patrimoniale (Cash / Investissements / Crédits)"""
    st.header("💼 Wealth Management")
    tab1, tab2, tab3 = st.tabs(["💵 Manage Cash", "📈 Investments", "💳 Credits"])
    
    with tab1: 
        manage_cash(portfolio)
    with tab2: 
        manage_investments(portfolio)
    with tab3: 
        manage_credits(portfolio)


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
            max_withdraw = portfolio.cash
            withdraw_amount = st.number_input("Amount to withdraw", min_value=0.01, max_value=max_withdraw, step=0.01, key="withdraw_cash")
            withdraw_description = st.text_input("Description", value="Cash withdrawal", key="withdraw_desc")
            can_withdraw = portfolio.cash >= withdraw_amount
            
            if st.button("Withdraw", key="btn_withdraw", disabled=not can_withdraw):
                if portfolio.withdraw_cash(withdraw_amount, withdraw_description):
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
        _add_investment_manually(portfolio)

    with tab2:
        _search_and_add_asset(portfolio)

    with tab3:
        _update_investment(portfolio)

    with tab4:
        _sell_investment(portfolio)


def _add_investment_manually(portfolio):
    """Add investment manually"""
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


def _search_and_add_asset(portfolio):
    """Search and add asset from Yahoo Finance"""
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


def _update_investment(portfolio):
    """Update investment values"""
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
            except Exception:
                st.warning("⚠️ Unable to retrieve real-time price. Use manual input.")

        if st.button("Update"):
            portfolio.update_investment_value(inv_to_update, new_value)
            save_portfolio(portfolio)
            st.success(f"Value of '{inv_to_update}' updated!")
            st.rerun()
    else:
        st.info("No investments to update")


def _sell_investment(portfolio):
    """Sell investments"""
    st.markdown("#### Sell investments")
    if portfolio.investments:
        inv_to_sell = st.selectbox("Investment", list(portfolio.investments.keys()), key="sell_select")
        current_quantity = float(portfolio.investments[inv_to_sell].quantity)
        
        if current_quantity > 0:
            max_sell_quantity = current_quantity
            default_sell_quantity = min(current_quantity, max_sell_quantity)
            sell_quantity = st.number_input(
                "Quantity to sell",
                min_value=0.01,
                max_value=max_sell_quantity,
                value=default_sell_quantity,
                step=0.01
            )
            sale_value = portfolio.investments[inv_to_sell].current_value * sell_quantity
            st.info(f"Sale value: {format_currency(sale_value)}")

            can_sell = current_quantity >= sell_quantity
            if st.button("Sell", disabled=not can_sell):
                portfolio.sell_investment(inv_to_sell, sell_quantity)
                save_portfolio(portfolio)
                st.success("Sale completed successfully!")
                st.rerun()
        else:
            st.warning("This investment has a quantity of 0 and cannot be sold.")
    else:
        st.info("No investments to sell")


def manage_credits(portfolio):
    """Credit management sub-tab"""
    st.subheader("💳 Credit Management")

    tab1, tab2 = st.tabs(["Add credit", "Pay credit"])

    with tab1:
        _add_credit(portfolio)

    with tab2:
        _pay_credit(portfolio)


def _add_credit(portfolio):
    """Add a new credit"""
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


def _pay_credit(portfolio):
    """Make a credit payment"""
    st.markdown("#### Make a payment")
    if portfolio.credits:
        credit_to_pay = st.selectbox("Credit", list(portfolio.credits.keys()))
        remaining_balance = portfolio.credits[credit_to_pay].get_remaining_balance()
        
        if portfolio.cash > 0 and remaining_balance > 0:
            max_payment = min(portfolio.cash, remaining_balance)
            payment_amount = st.number_input("Payment amount", min_value=0.01, max_value=max_payment, step=0.01)
            st.info(f"Remaining balance: {format_currency(remaining_balance)} | Available cash: {format_currency(portfolio.cash)}")

            can_pay = portfolio.cash >= payment_amount
            if st.button("Pay", disabled=not can_pay):
                if portfolio.pay_credit(credit_to_pay, payment_amount):
                    save_portfolio(portfolio)
                    st.success(f"Payment of {format_currency(payment_amount)} completed!")
                    st.rerun()
                else:
                    st.error("Unable to make payment!")
        else:
            st.warning("Insufficient cash or credit already fully paid.")
    else:
        st.info("No credits to pay")