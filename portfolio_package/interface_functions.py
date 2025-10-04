import pandas as pd
import streamlit as st
import yfinance as yf
import json
from datetime import datetime

from portfolio_package.visualizations import create_monthly_transactions_chart
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
    display_predictions
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


# === menus horizontal et vertical ===
def create_horizontal_menu():
    """
    Creates a horizontal menu using st.columns and buttons
    Returns the selected page
    """
    # CSS style for navigation
    st.markdown("""
        <style>
        /* Reduce top space */
        .main .block-container {
            padding-top: 1rem;
        }

        /* Style for main header */
        .nav-header {
            background: linear-gradient(90deg, #1f77b4 0%, #2a9fd6 100%);
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .nav-header h1 {
            color: white;
            margin: 0;
            font-size: 28px;
            font-weight: 600;
        }

        .nav-subtitle {
            color: rgba(255,255,255,0.9);
            font-size: 14px;
            margin-top: 5px;
        }

        /* Style navigation buttons */
        div[data-testid="column"] button[kind="secondary"] {
            width: 100%;
            border-radius: 8px;
            border: 2px solid #e0e0e0;
            background: white;
            padding: 12px 8px;
            font-weight: 500;
            transition: all 0.3s;
            height: 70px;
        }

        div[data-testid="column"] button[kind="secondary"]:hover {
            background: #f0f8ff;
            border-color: #1f77b4;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(31,119,180,0.2);
        }

        /* Active button */
        div[data-testid="column"] button[kind="primary"] {
            width: 100%;
            border-radius: 8px;
            background: #1f77b4;
            color: white;
            padding: 12px 8px;
            font-weight: 600;
            height: 70px;
            border: 2px solid #1f77b4;
            box-shadow: 0 2px 8px rgba(31,119,180,0.3);
        }

        /* Optimized sidebar */
        section[data-testid="stSidebar"] {
            width: 280px !important;
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header with title
    st.markdown("""
        <div class="nav-header">
            <div>
                <h1>💰 Financial Portfolio Manager</h1>
                <p class="nav-subtitle">Manage your investments with ease</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Initialize current page in session_state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "📊 Summary"

    # Define pages with their icons - Updated structure
    pages_config = [
        ("📊 Summary", "📊"),
        ("💼 Wealth Management", "💼"),
        ("📈 Dashboard", "📈"),
        ("🔮 Predictions", "🔮"),
        ("📚 Definitions", "📚")
    ]

    # Create columns for navigation
    cols = st.columns(len(pages_config))

    for idx, (col, (page_name, icon)) in enumerate(zip(cols, pages_config)):
        with col:
            # Determine if button should be in "primary" mode (active)
            is_active = st.session_state.current_page == page_name
            button_type = "primary" if is_active else "secondary"

            # Create button label (without the emoji from page name)
            page_label = page_name.split(" ", 1)[1] if " " in page_name else page_name
            button_label = f"{icon}\n\n{page_label}"

            if st.button(
                button_label,
                key=f"nav_btn_{page_name}",
                use_container_width=True,
                type=button_type
            ):
                st.session_state.current_page = page_name
                st.rerun()

    st.markdown("---")

    return st.session_state.current_page


def create_sidebar_actions(portfolio, save_portfolio_func, Portfolio, create_demo_portfolio_func, generate_pdf_func=None):
    """
    Creates the sidebar with save/load actions

    Args:
        portfolio: The current portfolio object
        save_portfolio_func: The portfolio save function
        Portfolio: The Portfolio class to create new instances
        create_demo_portfolio_func: Function to create a demo portfolio
        generate_pdf_func: Optional function to generate a PDF
    """
    # Logo at the top of the sidebar
    try:
        st.sidebar.image(
            "logo/FullLogo.png",
            use_container_width=True
        )
    except:
        st.sidebar.title("⚙️ Actions")

    st.sidebar.markdown("---")

    # Save/Load Section
    st.sidebar.subheader("💾 Import / Export Portfolio")

    # Save Button
    if st.sidebar.button("💾 Save", help="Automatic save on every change", use_container_width=True):
        if save_portfolio_func(portfolio):
            st.sidebar.success("✅ Saved!")

    # Import JSON file
    uploaded_file = st.sidebar.file_uploader(
        "Import",
        type="json",
        help="Import a save file",
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            st.session_state.portfolio = Portfolio.from_dict(data)
            st.sidebar.success("✅ Imported!")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Import error: {e}")

    st.sidebar.markdown("---")

    # Test Data Section
    st.sidebar.subheader("🎭 Test Data")

    if st.sidebar.button("Create demo portfolio", help="Creates a simulated 6-month history", use_container_width=True):
        st.session_state.portfolio = create_demo_portfolio_func()
        save_portfolio_func(st.session_state.portfolio)
        st.sidebar.success("🎉 Demo portfolio created!")
        st.rerun()

    if st.sidebar.button("Reset portfolio", use_container_width=True):
        st.session_state.portfolio = Portfolio(initial_cash=1000.0)
        save_portfolio_func(st.session_state.portfolio)
        st.sidebar.success("🔄 Portfolio reset!")
        st.rerun()

    st.sidebar.markdown("---")

    # Export Section
    st.sidebar.subheader("📥 Download Backup")

    # JSON Export
    portfolio_data = portfolio.to_dict()
    json_str = json.dumps(portfolio_data, indent=2, ensure_ascii=False)

    st.sidebar.download_button(
        label="📥 Download JSON",
        data=json_str,
        file_name=f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        use_container_width=True
    )

    # PDF Export if function is provided
    if generate_pdf_func:
        if st.sidebar.button("📄 Generate and download PDF", use_container_width=True):
            pdf_filename = f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            try:
                generate_pdf_func(portfolio, filename=pdf_filename)
                with open(pdf_filename, "rb") as f:
                    pdf_data = f.read()

                # Clean up temporary file
                import os
                try:
                    os.remove(pdf_filename)
                except:
                    pass

                st.sidebar.download_button(
                    label="📥 Download PDF",
                    data=pdf_data,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    use_container_width=True,
                    key="pdf_download"
                )
            except Exception as e:
                st.sidebar.error(f"PDF error: {e}")

    # Portfolio information
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Quick Info")
    st.sidebar.metric("💰 Cash", f"{format_currency(portfolio.cash)}")

    if portfolio.investments:
        total_inv = sum(inv.current_value * inv.quantity for inv in portfolio.investments.values())
        st.sidebar.metric("📈 Investments", f"{format_currency(total_inv)}")

    if portfolio.credits:
        total_debt = sum(credit.get_remaining_balance() for credit in portfolio.credits.values())
        st.sidebar.metric("💳 Debts", f"{format_currency(total_debt)}")


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
        additional_info.append(f"⚖️ Allocation: {format_percentage(fin_ratio)} financial / {format_percentage(re_ratio)} real estate")

    if additional_info:
        for info in additional_info:
            st.info(info)

    st.markdown("---")

    # --- Onglets Portfolio Vision et History ---
    tab1, tab2 = st.tabs(["📊 Portfolio Vision", "📋 Portfolio History"])

    with tab1:
        # --- Tableaux récapitulatifs de tous les produits du portefeuille ---

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

    with tab2:
        # --- Transaction History ---
        if portfolio.transaction_history:
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
                investment_buys = df_history[df_history['type'] == 'INVESTMENT_BUY']['amount'].sum()
                st.metric("Investments", f"{format_currency(investment_buys)}")

            with col4:
                credit_payments = df_history[df_history['type'] == 'CREDIT_PAYMENT']['amount'].sum()
                st.metric("Credit payments", f"{format_currency(credit_payments)}")

            # Chart of transaction evolution by month
            df_history['month'] = pd.to_datetime(df_history['date']).dt.to_period('M').astype(str)
            monthly_transactions = df_history.groupby(['month', 'type']).size().reset_index(name='count')

            if len(monthly_transactions) > 0:
                fig = create_monthly_transactions_chart(df_history)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            # Filters
            col1, col2 = st.columns(2)
            with col1:
                type_filter = st.selectbox("Filter by type",
                                         ["All"] + list(df_history['type'].unique()))
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
            display_df['Type'] = display_df['type'].map({
                'CASH_ADD': '💰 Cash addition',
                'CASH_WITHDRAW': '💸 Cash withdrawal',
                'INVESTMENT_BUY': '📈 Investment purchase',
                'INVESTMENT_SELL': '📉 Investment sale',
                'INVESTMENT_UPDATE': '🔄 Price update',
                'CREDIT_ADD': '🏦 New credit',
                'CREDIT_PAYMENT': '💳 Credit payment',
                'CREDIT_INTEREST': '📊 Credit interest'
            })
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
                        st.write(f"📈 **{event_date}**: {event['description']} ({format_currency(event['amount'])}")
                    elif event['type'] == 'CREDIT_ADD':
                        st.write(f"🏦 **{event_date}**: {event['description']} ({format_currency(event['amount'])})")
                    elif event['type'] == 'INVESTMENT_SELL':
                        st.write(f"📉 **{event_date}**: {event['description']} ({format_currency(event['amount'])})")

        else:
            st.info("No transactions recorded")
            st.markdown("💡 **Tip**: Use the 'Create demo portfolio' button in the sidebar to see a full history example!")


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
     """Financial definitions page""" 
     st.header("📚 Financial Definitions") 
     st.markdown(""" Welcome to the financial glossary! Browse the definitions of terms used in the application. """) 
     st.markdown("---") 
     st.subheader("💰 Cash") 
     st.markdown(""" **Definition**: Money immediately available in your portfolio. 
                 Cash represents money you can use instantly to: - Make new investments - Pay credits - Handle unexpected expenses 
                 💡 **Tip**: Always keep a cash reserve (3 to 6 months of expenses) for emergencies. """) 
     st.markdown("---") 
     st.subheader("📈 Financial Investments") 
     col1, col2 = st.columns(2) 
     with col1: 
         st.markdown(""" **Stocks** 📊 - Ownership shares in a company - High potential return - Medium to high risk - Example: Apple, Microsoft, Total **ETF** (Exchange Traded Fund) 📦 - Diversified basket of stocks - Tracks a stock index - Low fees - Example: S&P 500, CAC 40 **Bonds** 💼 - Loan to a company or state - Fixed and predictable return - Low to medium risk - Example: French OATs """) 
     with col2: 
            st.markdown(""" **Cryptocurrencies** ₿ - Decentralized digital currency - Very high volatility - High gain potential - 
                        Example: Bitcoin, Ethereum **Investment Funds** 🏦 - Portfolio managed by professionals - Automatic diversification - 
                        Management fees - Example: Mutual funds **Other Assets** 💎 - Gold, commodities - Art, collectibles - 
                        Alternative investments """) 
            st.markdown("---") 
            st.subheader("🏠 Real Estate Investments") 
            st.markdown(""" **SCPI** (Société Civile de Placement Immobilier) 
                        🏢 - Collective real estate investment - Management delegated to professionals - 
                        Regular rental income (4-6% per year) - Accessible from a few hundred euros - 
                        Example: SCPI Corum, Primonial **REIT** (Real Estate Investment Trust) 🌆 - 
                        American equivalent of SCPI - Listed on stock exchange, highly liquid - 
                        Invests in commercial real estate - Example: Simon Property Group **Direct Real Estate** 
                        🏡 - Physical property held directly - Rental management is your responsibility - 
                        Significant capital appreciation potential - Requires high initial capital **Rental Yield** 
                        📊 - Annual income generated / Property value × 100 - Indicates investment profitability - 
                        Typically between 2% and 8% depending on property type """) 
            st.markdown("---") 
            st.subheader("💳 Credits") 
            st.markdown(""" **Remaining Balance** 💰 - Total amount still owed on the credit - 
                        Decreases with each repayment - Principal + Remaining interest **Interest Rate** 
                        📈 - Annual cost of credit expressed in % - Can be fixed or variable - The lower the rate, 
                        the less expensive the credit - Example: 1.5% for a mortgage, 3-5% for consumer credit **Monthly Payment** 
                        💸 - Amount to repay each month - Includes a portion of principal and a portion of interest -
                         Generally remains constant over the credit term **Amortization** 
                        📉 - Progressive repayment of borrowed principal - At the start: more interest, less principal - 
                        At the end: more principal, less interest """) 
            st.markdown("---") 
            st.subheader("📊 Performance Indicators") 
            st.markdown(""" **Net Worth** 🏆 - Total wealth = (Cash + Investments) - Credits - Represents your real wealth -
                         Key indicator of financial health **Performance** 📈 - Percentage variation in investment value - 
                        (Current value - Initial value) / Initial value × 100 - Example: +15% = 15% gain compared to purchase 
                        **Diversification** 💾 - Distribution of investments across different assets - Reduces overall portfolio risk - 
                        "Don't put all your eggs in one basket" **Annualized Return** 📅 - Average performance per year over several years - 
                        Allows comparison of different investments - Smooths out short-term variations """) 
            st.markdown("---") 
            st.info(""" 💡 **Need more information?** These definitions are simplifications for educational purposes. 
                    For personalized advice on your investments, consult a professional financial advisor. """)
