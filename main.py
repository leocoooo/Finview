import streamlit as st
import pandas as pd
from datetime import datetime
import json
import plotly.express as px
from portfolio_package.pdf import generate_portfolio_pdf

from portfolio_package.models import Portfolio

from portfolio_package.interface_functions import (
    _add_investment_with_date,
    _update_investment_with_date,
    _sell_investment_with_date,
    _add_credit_with_date,
    _pay_credit_with_date,
    create_demo_portfolio
)

from portfolio_package.save_load_ptf_functions import save_portfolio, load_portfolio

from portfolio_package.charts import create_portfolio_pie_chart, create_portfolio_chart, create_performance_chart, create_world_investment_map
from portfolio_package.yahoo_search import asset_search_tab
import yfinance as yf
from portfolio_package.top_navigation_bar import create_horizontal_menu, create_sidebar_actions
from portfolio_package.patrimoine_prediction import simulate_portfolio_future, create_prediction_chart, create_statistics_summary

# Page configuration
st.set_page_config(
    page_title="Portfolio Manager",
    page_icon="💰",
    layout="wide"
)

# Adding methods to the Portfolio class
Portfolio._add_investment_with_date = _add_investment_with_date
Portfolio._update_investment_with_date = _update_investment_with_date
Portfolio._sell_investment_with_date = _sell_investment_with_date
Portfolio._add_credit_with_date = _add_credit_with_date
Portfolio._pay_credit_with_date = _pay_credit_with_date


# State initialization with automatic save/load
if 'portfolio' not in st.session_state:
    # Try to load an existing portfolio
    loaded_portfolio = load_portfolio()
    if loaded_portfolio:
        st.session_state.portfolio = loaded_portfolio
    else:
        st.session_state.portfolio = Portfolio(initial_cash=0.0)

# Main interface
def main():
    """Main interface with horizontal navigation at the top"""

    # Create the horizontal menu and get the selected page
    action = create_horizontal_menu()

    # Create the sidebar with actions
    create_sidebar_actions(
        portfolio=st.session_state.portfolio,
        save_portfolio_func=save_portfolio,
        Portfolio=Portfolio,
        create_demo_portfolio_func=create_demo_portfolio,
        generate_pdf_func=generate_portfolio_pdf
    )

    # Get the portfolio
    portfolio = st.session_state.portfolio

    # Route to the correct page based on selection
    if action == "📊 Summary":
        show_summary(portfolio)
    elif action == "💼 Wealth Management":
        show_wealth_management(portfolio)
    elif action == "📈 Dashboard":
        show_dashboard_tabs(portfolio)
    elif action == "🔮 Predictions":
        show_predictions(portfolio)
    elif action == "📚 Definitions":
        show_definitions()


def show_summary(portfolio):
    """Summary page with only metrics and tables"""
    st.header("Summary")

    # Main metrics
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("💰 Cash", f"{portfolio.cash:.2f}€")

    with col2:
        financial_value = portfolio.get_financial_investments_value()
        st.metric("📈 Financial Inv.", f"{financial_value:.2f}€")

    with col3:
        real_estate_value = portfolio.get_real_estate_investments_value()
        st.metric("🏠 Real Estate Inv.", f"{real_estate_value:.2f}€")

    with col4:
        credits_balance = portfolio.get_total_credits_balance()
        st.metric("💳 Credits", f"-{credits_balance:.2f}€")

    with col5:
        net_worth = portfolio.get_net_worth()
        st.metric("🏆 Net Worth", f"{net_worth:.2f}€")

    # Additional indicators and rental income display
    additional_info = []

    # Rental income
    if portfolio.real_estate_investments:
        annual_rental_income = portfolio.get_total_annual_rental_income()
        if annual_rental_income > 0:
            additional_info.append(
                f"💰 Annual rental income: {annual_rental_income:.2f}€ ({annual_rental_income / 12:.2f}€/month)")

    # Diversification indicator
    total_investments = len(portfolio.financial_investments) + len(portfolio.real_estate_investments)
    if total_investments > 0:
        diversification_score = "High" if total_investments >= 5 else "Medium" if total_investments >= 3 else "Low"
        diversification_color = "🟢" if total_investments >= 5 else "🟡" if total_investments >= 3 else "🔴"
        additional_info.append(
            f"{diversification_color} Diversification: {diversification_score} ({total_investments} investments)")

    # Balanced allocation
    if portfolio.financial_investments and portfolio.real_estate_investments:
        fin_ratio = portfolio.get_financial_investments_value() / (
                    portfolio.get_financial_investments_value() + portfolio.get_real_estate_investments_value()) * 100
        re_ratio = 100 - fin_ratio
        additional_info.append(f"⚖️ Allocation: {fin_ratio:.0f}% financial / {re_ratio:.0f}% real estate")

    # Display information
    if additional_info:
        for info in additional_info:
            st.info(info)

    st.markdown("---")

    # Investment tables separated by type
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
                    "Unit value": f"{inv.current_value:.2f}€",
                    "Total value": f"{inv.get_total_value():.2f}€",
                    "Gain/Loss": f"{inv.get_gain_loss():+.2f}€",
                    "Performance": f"{inv.get_gain_loss_percentage():+.1f}%"
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
                    "Yield": f"{rental_yield:.1f}%" if rental_yield > 0 else "N/A",
                    "Total value": f"{inv.get_total_value():.2f}€",
                    "Annual income": f"{annual_income:.2f}€" if annual_income > 0 else "N/A",
                    "Performance": f"{inv.get_gain_loss_percentage():+.1f}%"
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
                    "Remaining balance": f"{credit.get_remaining_balance():.2f}€",
                    "Rate": f"{credit.interest_rate:.1f}%",
                    "Monthly payment": f"{credit.monthly_payment:.2f}€"
                })
            st.dataframe(pd.DataFrame(credit_data), use_container_width=True)
        else:
            st.info("No credits")


def show_wealth_management(portfolio):
    """Wealth Management page with 3 sub-tabs"""
    st.header("💼 Wealth Management")
    
    tab1, tab2, tab3 = st.tabs(["💵 Manage Cash", "📈 Investments", "💳 Credits"])
    
    with tab1:
        manage_cash(portfolio)
    
    with tab2:
        manage_investments(portfolio)
    
    with tab3:
        manage_credits(portfolio)


def show_dashboard_tabs(portfolio):
    """Dashboard page with 3 sub-tabs"""
    st.header("📈 Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["📊 Portfolio", "💎 Assets", "🌍 Investments Map"])
    
    with tab1:
        show_portfolio_charts(portfolio)
    
    with tab2:
        show_assets_analytics(portfolio)
    
    with tab3:
        show_world_map(portfolio)


def show_portfolio_charts(portfolio):
    """Portfolio charts: pie chart and evolution"""
    st.subheader("Portfolio Distribution")
    
    # Professional and readable pie chart
    if portfolio.investments or portfolio.cash > 0:
        fig = create_portfolio_pie_chart(portfolio)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("No data to display")

    st.markdown("---")
    st.subheader("📈 Historical Evolution")

    # Period selector
    col1, col2 = st.columns([3, 1])

    with col1:
        years_option = st.selectbox(
            "Display period",
            options=[1, 2, 5, 10],
            index=2,
            help="Select the historical period to display",
            key="evolution_years"
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Refresh", help="Regenerate simulated history", key="refresh_evolution"):
            if 'evolution_seed' in st.session_state:
                st.session_state.evolution_seed += 1
            else:
                st.session_state.evolution_seed = 1
            st.rerun()

    # Generate and display the chart
    from portfolio_package.portfolio_evolution import create_portfolio_evolution_chart
    fig_evolution = create_portfolio_evolution_chart(portfolio, years=years_option)
    st.plotly_chart(fig_evolution, use_container_width=True, config={'displayModeBar': False})

    st.info("""
    💡 **Note**: This history is a retrospective simulation based on your current value.
    For real history, your future transactions will be automatically recorded.
    """)


def show_assets_analytics(portfolio):
    """Assets analytics: distribution and performance"""
    st.subheader("Asset Analytics")

    if not portfolio.investments:
        st.info("No investments to analyze")
        return

    # Asset distribution
    st.markdown("### Wealth Distribution")
    labels = ['Cash']
    values = [portfolio.cash]

    for name, inv in portfolio.investments.items():
        labels.append(name)
        values.append(inv.get_total_value())

    if values and sum(values) > 0:
        fig = px.pie(values=values, names=labels, title="Asset Distribution")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")

    # Investment performance
    st.markdown("### Investment Performance")
    performance_data = []
    for name, inv in portfolio.investments.items():
        performance_data.append({
            'Investment': name,
            'Initial value': inv.initial_value * inv.quantity,
            'Current value': inv.get_total_value(),
            'Performance (%)': inv.get_gain_loss_percentage()
        })

    df_perf = pd.DataFrame(performance_data)
    fig = px.bar(df_perf, x='Investment', y='Performance (%)',
                title="Investment Performance (%)",
                color='Performance (%)',
                color_continuous_scale=['red', 'yellow', 'green'])
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def manage_cash(portfolio):
    """Cash management sub-tab"""
    st.subheader("💵 Cash Management")
    st.metric("Current cash", f"{portfolio.cash:.2f}€")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Add cash")
        add_amount = st.number_input("Amount to add", min_value=0.01, step=0.01, key="add_cash")
        add_description = st.text_input("Description", value="Cash addition", key="add_desc")
        if st.button("Add", key="btn_add"):
            portfolio.add_cash(add_amount, add_description)
            save_portfolio(portfolio)
            st.success(f"{add_amount:.2f}€ added successfully!")
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
                    st.success(f"{withdraw_amount:.2f}€ withdrawn successfully!")
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
        st.info(f"Total cost: {total_cost:.2f}€ (Available cash: {portfolio.cash:.2f}€)")

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
            st.info(f"Sale value: {sale_value:.2f}€")

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
            st.info(f"Remaining balance: {remaining_balance:.2f}€ | Available cash: {portfolio.cash:.2f}€")

            can_pay = portfolio.cash >= payment_amount and portfolio.cash > 0 and remaining_balance > 0
            if st.button("Pay", disabled=not can_pay):
                if can_pay and portfolio.pay_credit(credit_to_pay, payment_amount):
                    save_portfolio(portfolio)
                    st.success(f"Payment of {payment_amount:.2f}€ completed!")
                    st.rerun()
                else:
                    st.error("Unable to make payment!")
        else:
            st.info("No credits to pay")


def show_world_map(portfolio):
    """Display the world map of investments"""
    st.subheader("🌍 World Investment Map")

    total_investments = len(portfolio.financial_investments) + len(portfolio.real_estate_investments)
    financial_count = len(portfolio.financial_investments)
    real_estate_count = len(portfolio.real_estate_investments)

    if total_investments > 0:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("🎯 Total Investments", total_investments)
        with col2:
            st.metric("📈 Financial", financial_count)
        with col3:
            st.metric("🏠 Real Estate", real_estate_count)
        with col4:
            financial_value = portfolio.get_financial_investments_value()
            real_estate_value = portfolio.get_real_estate_investments_value()
            total_value = financial_value + real_estate_value
            st.metric("💰 Total Value", f"{total_value:.0f}€")

        st.markdown("---")

        st.markdown("#### 📍 Geographic Distribution")

        locations = {}

        for name, inv in portfolio.financial_investments.items():
            location = getattr(inv, 'location', 'France')
            inv_type = getattr(inv, 'investment_type', 'Financial')
            value = inv.get_total_value()

            if location not in locations:
                locations[location] = {'financial': 0, 'real_estate': 0, 'count': 0}
            locations[location]['financial'] += value
            locations[location]['count'] += 1

        for name, inv in portfolio.real_estate_investments.items():
            location = getattr(inv, 'location', 'France')
            value = inv.get_total_value()

            if location not in locations:
                locations[location] = {'financial': 0, 'real_estate': 0, 'count': 0}
            locations[location]['real_estate'] += value
            locations[location]['count'] += 1

        if locations:
            location_data = []
            for loc, data in locations.items():
                total_loc_value = data['financial'] + data['real_estate']
                location_data.append({
                    'Location': loc,
                    'Nb. Investments': data['count'],
                    'Financial Value': f"{data['financial']:.2f}€" if data['financial'] > 0 else "-",
                    'Real Estate Value': f"{data['real_estate']:.2f}€" if data['real_estate'] > 0 else "-",
                    'Total Value': f"{total_loc_value:.2f}€"
                })

            st.dataframe(pd.DataFrame(location_data), use_container_width=True)

        st.markdown("---")

        st.markdown("#### 🗺️ Interactive Map")
        fig_map = create_world_investment_map(portfolio)
        fig_map.update_layout(height=700)

        st.plotly_chart(fig_map, use_container_width=True, config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d']
        })

        st.markdown("---")
        st.markdown("#### 💡 How to read this map")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🔵 Blue circles**: Financial investments
            - Size proportional to value
            - Click to see details
            - Performance displayed on hover
            """)

        with col2:
            st.markdown("""
            **🟠 Orange squares**: Real estate investments
            - Size proportional to value
            - Rental yield information
            - Precise location displayed
            """)

        st.info("💡 **Tip**: Zoom and navigate on the map to explore your investments by region")

    else:
        st.info("🌍 No investments to locate at the moment")
        st.markdown("""
        ### How to add geolocated investments:

        1. **📈 Go to the 'Wealth Management' → 'Investments' tab**
        2. **🌍 Enter the location** when adding:
           - For real estate: required field
           - For financial: optional but recommended
        3. **🗺️ Come back here** to see your investments on the map!

        ### Supported locations:
        - **Countries**: France, United States, Germany, Japan, etc.
        - **Cities**: Paris, New York, London, Tokyo, etc.
        - **Regions**: Europe, Asia, North America, etc.
        """)


def show_predictions(portfolio):
    st.header("🔮 Wealth Predictions")

    if not portfolio.investments:
        st.info("Add investments to see predictions")
        return

    st.markdown("""
    This simulation uses the average historical returns of each asset class
    to project the possible evolution of your wealth over several years.
    """)

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        years = st.selectbox(
            "Prediction horizon",
            options=[1, 5, 10, 20, 30],
            index=2,
            help="Number of years to simulate"
        )

    with col2:
        num_simulations = st.selectbox(
            "Number of simulations",
            options=[100, 500, 1000, 2000],
            index=2,
            help="More simulations = more accurate results but slower"
        )

    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        run_prediction = st.button("🚀 Run", use_container_width=True, type="primary")

    if run_prediction or 'prediction_results' in st.session_state:
        if run_prediction:
            with st.spinner(f"Simulating {num_simulations} scenarios over {years} years..."):
                prediction_results = simulate_portfolio_future(
                    portfolio,
                    years=years,
                    num_simulations=num_simulations
                )
                st.session_state.prediction_results = prediction_results
                st.session_state.prediction_years = years

        if 'prediction_results' in st.session_state:
            results = st.session_state.prediction_results

            fig = create_prediction_chart(results)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            st.markdown("---")
            st.subheader("📈 Simulation Statistics")

            stats = create_statistics_summary(results)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Current Wealth",
                    f"{stats['initial']:.0f}€",
                    help="Current net value of your portfolio"
                )

            with col2:
                median_final = stats['final']['p50']
                median_gain = stats['gains']['p50']
                median_return = stats['returns']['p50']
                st.metric(
                    f"Median ({years} years)",
                    f"{median_final:.0f}€",
                    f"+{median_gain:.0f}€ ({median_return:+.1f}%/year)",
                    help="Median scenario (50% chance of being above)"
                )

            with col3:
                optimistic_final = stats['final']['p75']
                optimistic_gain = stats['gains']['p75']
                st.metric(
                    "Optimistic Scenario (P75)",
                    f"{optimistic_final:.0f}€",
                    f"+{optimistic_gain:.0f}€",
                    help="25% chance of reaching or exceeding this value"
                )

            with col4:
                pessimistic_final = stats['final']['p25']
                pessimistic_gain = stats['gains']['p25']
                st.metric(
                    "Conservative Scenario (P25)",
                    f"{pessimistic_final:.0f}€",
                    f"+{pessimistic_gain:.0f}€" if pessimistic_gain >= 0 else f"{pessimistic_gain:.0f}€",
                    delta_color="normal" if pessimistic_gain >= 0 else "inverse",
                    help="75% chance of reaching or exceeding this value"
                )

            st.markdown("---")
            st.subheader("📊 Detailed Scenarios")

            scenarios_data = {
                'Scenario': [
                    '🔥 Very optimistic (P90)',
                    '✨ Optimistic (P75)',
                    '📊 Median (P50)',
                    '⚠️ Conservative (P25)',
                    '❄️ Pessimistic (P10)'
                ],
                f'Value after {years} years': [
                    f"{stats['final']['p90']:.0f}€",
                    f"{stats['final']['p75']:.0f}€",
                    f"{stats['final']['p50']:.0f}€",
                    f"{stats['final']['p25']:.0f}€",
                    f"{stats['final']['p10']:.0f}€"
                ],
                'Gain/Loss': [
                    f"{stats['gains']['p90']:+.0f}€",
                    f"{stats['gains']['p75']:+.0f}€",
                    f"{stats['gains']['p50']:+.0f}€",
                    f"{stats['gains']['p25']:+.0f}€",
                    f"{stats['gains']['p10']:+.0f}€"
                ],
                'Annualized return': [
                    f"{stats['returns']['p90']:+.1f}%",
                    f"{stats['returns']['p75']:+.1f}%",
                    f"{stats['returns']['p50']:+.1f}%",
                    f"{stats['returns']['p25']:+.1f}%",
                    f"{stats['returns']['p10']:+.1f}%"
                ],
                'Probability': [
                    '10% chance',
                    '25% chance',
                    '50% chance',
                    '75% chance',
                    '90% chance'
                ]
            }

            df_scenarios = pd.DataFrame(scenarios_data)
            st.dataframe(df_scenarios, use_container_width=True, hide_index=True)

            st.markdown("---")
            st.subheader("💼 Composition Used for Simulation")

            composition_data = []
            for asset in results['composition']:
                composition_data.append({
                    'Asset': asset['name'],
                    'Type': asset['type'],
                    'Current Value': f"{asset['value']:.2f}€",
                    'Expected Average Return': f"{asset['params']['mean']:.1f}%",
                    'Volatility': f"±{asset['params']['std']:.1f}%"
                })

            df_composition = pd.DataFrame(composition_data)
            st.dataframe(df_composition, use_container_width=True, hide_index=True)

            st.info("""
            ⚠️ **Important Warning**

            These predictions are based on average historical returns and use Monte Carlo simulations.
            Actual results may vary considerably and depend on many unpredictable factors
            (economic crises, technological innovations, regulatory changes, etc.).

            **This simulation does not constitute investment advice.**
            """)

    else:
        st.info("👆 Configure the parameters above and click 'Run' to see predictions")

        with st.expander("📚 How does the prediction work?"):
            st.markdown("""
            ### Monte Carlo Simulation Methodology

            1. **Historical Returns**: Each asset class has an average return and volatility based on history
                - **Crypto** (Bitcoin): ~100%/year ± 80% (very volatile)
                - **Tech Stocks**: ~20-25%/year ± 25-50%
                - **S&P 500 ETF**: ~10.5%/year ± 18%
                - **Real Estate/SCPI**: ~4-6%/year ± 7-12%
                - **Bonds**: ~3.5%/year ± 5%

            2. **Multiple Simulations**: Generation of hundreds/thousands of possible scenarios

            3. **Return Distribution**:
                - **Log-normal distribution** for cryptos (reflection of possible explosive growth)
                - **Normal distribution** for other traditional assets

            4. **Percentiles**:
                - **P90**: Only 10% chance of doing better (very optimistic)
                - **P50 (Median)**: 50% chance of doing better (central scenario)
                - **P10**: 90% chance of doing better (conservative scenario)

            💡 The more diversified your portfolio, the more stable and reliable the predictions.
            """)


def show_definitions():
    """Financial definitions page"""
    st.header("📚 Financial Definitions")

    st.markdown("""
    Welcome to the financial glossary! Browse the definitions of terms used in the application.
    """)

    st.markdown("---")

    st.subheader("💰 Cash")
    st.markdown("""
    **Definition**: Money immediately available in your portfolio.

    Cash represents money you can use instantly to:
    - Make new investments
    - Pay credits
    - Handle unexpected expenses

    💡 **Tip**: Always keep a cash reserve (3 to 6 months of expenses) for emergencies.
    """)

    st.markdown("---")

    st.subheader("📈 Financial Investments")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Stocks** 📊
        - Ownership shares in a company
        - High potential return
        - Medium to high risk
        - Example: Apple, Microsoft, Total

        **ETF** (Exchange Traded Fund) 📦
        - Diversified basket of stocks
        - Tracks a stock index
        - Low fees
        - Example: S&P 500, CAC 40

        **Bonds** 💼
        - Loan to a company or state
        - Fixed and predictable return
        - Low to medium risk
        - Example: French OATs
        """)

    with col2:
        st.markdown("""
        **Cryptocurrencies** ₿
        - Decentralized digital currency
        - Very high volatility
        - High gain potential
        - Example: Bitcoin, Ethereum

        **Investment Funds** 🏦
        - Portfolio managed by professionals
        - Automatic diversification
        - Management fees
        - Example: Mutual funds

        **Other Assets** 💎
        - Gold, commodities
        - Art, collectibles
        - Alternative investments
        """)

    st.markdown("---")

    st.subheader("🏠 Real Estate Investments")

    st.markdown("""
    **SCPI** (Société Civile de Placement Immobilier) 🏢
    - Collective real estate investment
    - Management delegated to professionals
    - Regular rental income (4-6% per year)
    - Accessible from a few hundred euros
    - Example: SCPI Corum, Primonial

    **REIT** (Real Estate Investment Trust) 🌆
    - American equivalent of SCPI
    - Listed on stock exchange, highly liquid
    - Invests in commercial real estate
    - Example: Simon Property Group

    **Direct Real Estate** 🏡
    - Physical property held directly
    - Rental management is your responsibility
    - Significant capital appreciation potential
    - Requires high initial capital

    **Rental Yield** 📊
    - Annual income generated / Property value × 100
    - Indicates investment profitability
    - Typically between 2% and 8% depending on property type
    """)

    st.markdown("---")

    st.subheader("💳 Credits")

    st.markdown("""
    **Remaining Balance** 💰
    - Total amount still owed on the credit
    - Decreases with each repayment
    - Principal + Remaining interest

    **Interest Rate** 📈
    - Annual cost of credit expressed in %
    - Can be fixed or variable
    - The lower the rate, the less expensive the credit
    - Example: 1.5% for a mortgage, 3-5% for consumer credit

    **Monthly Payment** 💸
    - Amount to repay each month
    - Includes a portion of principal and a portion of interest
    - Generally remains constant over the credit term

    **Amortization** 📉
    - Progressive repayment of borrowed principal
    - At the start: more interest, less principal
    - At the end: more principal, less interest
    """)

    st.markdown("---")

    st.subheader("📊 Performance Indicators")

    st.markdown("""
    **Net Worth** 🏆
    - Total wealth = (Cash + Investments) - Credits
    - Represents your real wealth
    - Key indicator of financial health

    **Performance** 📈
    - Percentage variation in investment value
    - (Current value - Initial value) / Initial value × 100
    - Example: +15% = 15% gain compared to purchase

    **Diversification** 💾
    - Distribution of investments across different assets
    - Reduces overall portfolio risk
    - "Don't put all your eggs in one basket"

    **Annualized Return** 📅
    - Average performance per year over several years
    - Allows comparison of different investments
    - Smooths out short-term variations
    """)

    st.markdown("---")

    st.info("""
    💡 **Need more information?**

    These definitions are simplifications for educational purposes. For personalized advice on your investments,
    consult a professional financial advisor.
    """)


if __name__ == "__main__":
    main()