import pandas as pd
import streamlit as st
import yfinance as yf
import json
from datetime import datetime

from portfolio_package.visualizations import create_monthly_transactions_chart
from portfolio_package.save_load_ptf_functions import save_portfolio
from portfolio_package.yahoo_search import asset_search_tab
from portfolio_package.patrimoine_prediction import simulate_portfolio_future, create_statistics_summary, HISTORICAL_RETURNS

# Import des visualisations externalisées
from portfolio_package.visualizations import (
    display_portfolio_pie,
    #display_portfolio_evolution,
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

    # Initialize current page in session_state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "📊 Summary"

    # Define pages with their icons - Updated structure
    pages_config = [
        ("📊 Summary", "📊"),
        ("💼 Wealth Management", "💼"),
        ("📈 Dashboard", "📈"),
        ("🔮 Predictions", "🔮"),
        ("📰 Actuality", "📰"),
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
            width=300
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
        st.session_state.portfolio = Portfolio(initial_cash=0)
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
    with col1: 
        st.metric("💰 Cash", format_currency(portfolio.cash))
    with col2: 
        st.metric("📈 Financial Inv.", format_currency(portfolio.get_financial_investments_value()))
    with col3: 
        st.metric("🏠 Real Estate Inv.", format_currency(portfolio.get_real_estate_investments_value()))
    with col4: 
        st.metric("💳 Credits", f"-{format_currency(portfolio.get_total_credits_balance())}"[:-1] + "€")
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

            # Utiliser type_filter pour filtrer votre DataFrame
            if type_filter != "All":
                df_history[df_history['type'] == type_filter]
            else:
                df_history

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
            display_df['Type'] = display_df['type'].map(mapping_type_dictionnary)
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
        stats = create_statistics_summary(results)

        # Create tabs to display results
        tab1, tab2 = st.tabs(["📊 Chart", "📋 Projection Table"])

        with tab1:
            display_predictions(results)

            st.markdown("---")
            st.subheader("📈 Simulation Statistics")

            col1, col2, col3, col4 = st.columns(4)
            with col1: st.metric("Current Wealth", format_currency(stats['initial']))
            with col2: st.metric(f"Median ({years} years)", format_currency(stats['final']['p50']))
            with col3: st.metric("Optimistic (P75)", format_currency(stats['final']['p75']))
            with col4: st.metric("Conservative (P25)", format_currency(stats['final']['p25']))

        with tab2:
            st.subheader("📋 Detailed Year-by-Year Projections")

            # Create data table
            projection_data = []
            percentiles = results['percentiles']

            for year in range(results['years'] + 1):
                projection_data.append({
                    'Year': year,
                    'P10 (Pessimistic)': format_currency(percentiles['p10'][year]),
                    'P25 (Conservative)': format_currency(percentiles['p25'][year]),
                    'P50 (Median)': format_currency(percentiles['p50'][year]),
                    'P75 (Optimistic)': format_currency(percentiles['p75'][year]),
                    'P90 (Very Optimistic)': format_currency(percentiles['p90'][year]),
                    'Average': format_currency(percentiles['mean'][year])
                })

            df_projections = pd.DataFrame(projection_data)

            # Display the table
            st.dataframe(
                df_projections,
                use_container_width=True,
                height=min(600, (results['years'] + 2) * 35),
                hide_index=True
            )

            # Additional information
            st.markdown("---")
            st.info("""
**Percentile Legend:**
- **P10**: 10% of simulations give a lower result (pessimistic scenario)
- **P25**: 25% of simulations give a lower result (conservative scenario)
- **P50**: Median - 50% of simulations above/below (median scenario)
- **P75**: 75% of simulations give a lower result (optimistic scenario)
- **P90**: 90% of simulations give a lower result (very optimistic scenario)
            """)


# === ONGLET DEFINITIONS ===

def show_definitions():
    """Financial definitions page with search functionality"""
    st.header("📚 Financial Definitions")
    st.markdown("Welcome to the financial glossary! Browse the definitions of terms used in the application.")

    # Onglets principaux
    tab1, tab2 = st.tabs(["📖 General Definitions", "💹 Asset Returns Database"])

    with tab1:
        # Barre de recherche pour les définitions générales
        search_general = st.text_input("🔍 Search for a term...", key="search_general", placeholder="Ex: SCPI, ETF, Diversification...")

        st.markdown("---")

        # Définitions organisées
        all_sections = {
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
"""
        }

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

    with tab2:
        st.markdown("""
This database contains historical return parameters used for portfolio predictions.
Each asset has an **average annual return** and a **volatility (standard deviation)**.
""")

        # Barre de recherche pour les actifs
        search_asset = st.text_input(
            "🔍 Search for an asset...",
            key="search_asset",
            placeholder="Ex: Bitcoin, S&P 500, SCPI..."
        )

        # Filtres par catégorie
        col1, col2 = st.columns([1, 3])
        with col1:
            category_filter = st.selectbox(
                "Filter by category",
                ["All", "Cryptocurrencies", "Stocks", "ETF", "Real Estate", "Bonds", "Commodities", "Funds & Cash"]
            )

        # Créer un DataFrame à partir de HISTORICAL_RETURNS
        assets_data = []
        for asset_name, params in HISTORICAL_RETURNS.items():
            # Déterminer la catégorie
            if any(x in asset_name for x in ['Bitcoin', 'Ethereum', 'Crypto', 'Altcoin']):
                category = "Cryptocurrencies"
            elif any(x in asset_name for x in ['Actions', 'Action']):
                category = "Stocks"
            elif 'ETF' in asset_name:
                category = "ETF"
            elif any(x in asset_name for x in ['SCPI', 'REIT', 'Immobilier']):
                category = "Real Estate"
            elif 'Obligation' in asset_name:
                category = "Bonds"
            elif any(x in asset_name for x in ['Or', 'Argent', 'Commodities', 'Private Equity']):
                category = "Commodities"
            else:
                category = "Funds & Cash"

            assets_data.append({
                'Asset': asset_name,
                'Category': category,
                'Avg Return (%)': params['mean'],
                'Volatility (%)': params['std'],
                'Distribution': params['distribution']
            })

        df_assets = pd.DataFrame(assets_data)

        # Appliquer les filtres
        filtered_df = df_assets.copy()

        if search_asset:
            search_lower = search_asset.lower()
            filtered_df = filtered_df[filtered_df['Asset'].str.lower().str.contains(search_lower)]

        if category_filter != "All":
            filtered_df = filtered_df[filtered_df['Category'] == category_filter]

        # Trier par catégorie puis par rendement
        filtered_df = filtered_df.sort_values(['Category', 'Avg Return (%)'], ascending=[True, False])

        # Afficher les statistiques
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Total Assets", len(filtered_df))
        with col2:
            avg_return = filtered_df['Avg Return (%)'].mean()
            st.metric("📈 Avg Return", f"{avg_return:.1f}%")
        with col3:
            max_return = filtered_df['Avg Return (%)'].max()
            st.metric("🚀 Max Return", f"{max_return:.1f}%")
        with col4:
            avg_vol = filtered_df['Volatility (%)'].mean()
            st.metric("📊 Avg Volatility", f"{avg_vol:.1f}%")

        # Tableau des actifs
        st.markdown("---")
        st.subheader(f"📋 Asset Database ({len(filtered_df)} results)")

        # Styling du DataFrame
        def highlight_row(row):
            if row['Avg Return (%)'] > 15:
                return ['background-color: rgba(0, 255, 0, 0.1)'] * len(row)
            elif row['Avg Return (%)'] < 5:
                return ['background-color: rgba(255, 165, 0, 0.1)'] * len(row)
            return [''] * len(row)

        styled_df = filtered_df.style.apply(highlight_row, axis=1)

        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=500,
            hide_index=True
        )

        # Légende
        st.markdown("""
**Legend:**
- **Avg Return (%)**: Expected average annual return
- **Volatility (%)**: Standard deviation (risk measure)
- **Distribution**: Statistical distribution used for simulations
  - `normal`: Normal distribution (traditional assets)
  - `lognormal`: Log-normal distribution (high volatility assets)

💡 **Note**: These values are estimates based on historical data and do not guarantee future performance.
""")


def show_news():
    """Financial news page with curated articles"""
    st.header("📰 Financial News & Economic Updates")
    st.markdown("Stay informed with the latest financial news, company earnings, and economic announcements.")

    st.markdown("---")

    # Create tabs for news organization
    tab1, tab2 = st.tabs(["🔥 Latest News", "📅 Upcoming Results"])

    with tab1:
        # Curated financial news articles
        st.subheader("🔥 Top Financial News")

        # Article 1: CAC 40 Results
        with st.container():
            st.markdown("### 📊 CAC 40: Half-year 2025 earnings season ends in pain")
            st.markdown("""
            The first half 2025 earnings season for CAC 40 companies disappointed markets with numerous stock penalties.
            Teleperformance (-20.7%), Renault (-18.5%) and STMicroelectronics (-16.62%) were particularly affected by downward revised forecasts.
            Despite a strong year start with +12% in January-February, the index suffered from US customs tariffs in April.
            """)
            st.markdown("🔗 **Source:** [TradingSat - CAC 40 Results](https://www.tradingsat.com/cac-40-FR0003500008/actualites/cac-40-quels-groupes-du-cac-40-ont-le-mieux-et-le-moins-bien-resiste-a-la-terrible-saison-des-resultats-semestriels-1143776.html)")
            st.markdown("📅 **Date:** August 2025")
            st.markdown("---")

        # Article 2: French Economic Outlook
        with st.container():
            st.markdown("### 📉 French Economy: Declining inflation, slight unemployment rise")
            st.markdown("""
            The Bank of France forecasts 1% inflation for 2025 (down from 2% in 2024), thanks notably to falling energy prices.
            The unemployment rate is expected to reach 7.6% mid-2025 according to Insee, with approximately 112,000 job losses.
            Economic growth is revised to 0.7% for 2025, down from 1.1% in 2024.
            """)
            st.markdown("🔗 **Source:** [France Info - Economic Forecasts 2025](https://www.franceinfo.fr/economie/croissance/croissance-inflation-chomage-a-quoi-faut-il-s-attendre-pour-l-economie-francaise-en-2025_6990509.html)")
            st.markdown("📅 **Date:** September 2025")
            st.markdown("---")

        # Article 3: S&P 500 Earnings
        with st.container():
            st.markdown("### 💼 S&P 500: Ninth consecutive quarter of earnings growth")
            st.markdown("""
            The third quarter earnings season begins with major US banks (JPMorgan Chase, Citigroup, Wells Fargo).
            FactSet estimates 7.9% earnings growth for S&P 500 companies, marking the ninth consecutive quarter of growth.
            Investors closely monitor publication calendars on MarketBeat, Yahoo Finance and Nasdaq.
            """)
            st.markdown("🔗 **Source:** [MarketBeat - S&P 500 Earnings Calendar](https://www.marketbeat.com/earnings/latest/)")
            st.markdown("📅 **Date:** October 2025")
            st.markdown("---")

        # Article 4: CAC 40 Dividends
        with st.container():
            st.markdown("### 💰 CAC 40 Dividends: €73.9 billion expected in 2025")
            st.markdown("""
            CAC 40 companies are expected to pay €73.9 billion in dividends for the 2024 fiscal year.
            Despite a mixed earnings season, major French groups maintain their shareholder distribution policies.
            Publication and payment calendars are available on Boursorama and ABC Bourse.
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
                    except:
                        st.metric(label=name, value="N/A")
        except Exception as e:
            st.info("📊 Market indices data temporarily unavailable")

    with tab2:
        # Earnings calendar section
        st.subheader("📅 Upcoming Earnings Announcements")

        st.markdown("""
        Track upcoming earnings announcements from major companies.
        """)

        # Search bar for companies
        search_company = st.text_input(
            "🔍 Search for a company...",
            key="search_company",
            placeholder="Ex: Apple, LVMH, Tesla, TotalEnergies..."
        )

        # French companies earnings calendar (from Boursorama)
        french_earnings = {
            # Format: "Company Name": "DD/MM/YYYY"
            # CAC 40 et grandes entreprises françaises
            "LVMH": "28/01/2025",
            "TotalEnergies": "06/02/2025",
            "Sanofi": "07/02/2025",
            "Hermès": "05/02/2025",
            "L'Oréal": "14/02/2025",
            "Air Liquide": "13/02/2025",
            "BNP Paribas": "04/02/2025",
            "Schneider Electric": "20/02/2025",
            "Airbus": "20/02/2025",
            "AXA": "21/02/2025",
            "Danone": "26/02/2025",
            "EssilorLuxottica": "27/02/2025",
            "Saint-Gobain": "27/02/2025",
            "Stellantis": "25/02/2025",
            "Vinci": "04/03/2025",
            "Orange": "20/02/2025",
            "Carrefour": "19/02/2025",
            "Pernod Ricard": "27/02/2025",
            "Engie": "20/02/2025",
            "Renault": "13/02/2025",
            "Capgemini": "13/02/2025",
            "Publicis": "06/02/2025",
            "Bouygues": "27/02/2025",
            "Legrand": "13/02/2025",
            "Thales": "27/02/2025",
            "Dassault Systèmes": "06/02/2025",
            "Safran": "27/02/2025",
            "Crédit Agricole": "13/02/2025",
            "Société Générale": "06/02/2025",
            "Veolia": "28/02/2025",
            "Accor": "20/02/2025",
            "Edenred": "25/02/2025",
            "Worldline": "18/02/2025",
            "STMicroelectronics": "29/01/2025",
            "Kering": "12/02/2025",
            "Michelin": "11/02/2025",
            "ArcelorMittal": "13/02/2025",
            "Alstom": "14/05/2025",
            "Atos": "27/02/2025",
            "Teleperformance": "20/02/2025",
            # 2026
            "LVMH": "27/01/2026",
            "TotalEnergies": "05/02/2026",
            "Sanofi": "06/02/2026",
            "Hermès": "04/02/2026",
            "L'Oréal": "13/02/2026",
            "Air Liquide": "12/02/2026",
            "BNP Paribas": "03/02/2026",
            "Schneider Electric": "19/02/2026",
            "Airbus": "19/02/2026",
            "AXA": "20/02/2026",
            "Danone": "25/02/2026",
            "EssilorLuxottica": "26/02/2026",
            "Saint-Gobain": "26/02/2026",
            "Stellantis": "24/02/2026",
            "Vinci": "03/03/2026",
            "Orange": "19/02/2026",
            "Carrefour": "18/02/2026",
            "Pernod Ricard": "26/02/2026",
            "Engie": "19/02/2026",
            "Renault": "12/02/2026",
            "Capgemini": "12/02/2026",
            "Publicis": "05/02/2026",
            "Bouygues": "26/02/2026",
            "Legrand": "12/02/2026",
            "Thales": "26/02/2026",
            "Dassault Systèmes": "05/02/2026",
            "Safran": "26/02/2026",
            "Crédit Agricole": "12/02/2026",
            "Société Générale": "05/02/2026",
            "Veolia": "27/02/2026",
            "Accor": "19/02/2026",
            "Edenred": "24/02/2026",
            "Worldline": "17/02/2026",
            "STMicroelectronics": "28/01/2026",
            "Kering": "11/02/2026",
            "Michelin": "10/02/2026",
            "ArcelorMittal": "12/02/2026",
            "Alstom": "13/05/2026",
            "Atos": "26/02/2026",
            "Teleperformance": "19/02/2026",
        }

        # International companies earnings calendar
        international_earnings = {
            # Format: "Company Name": "DD/MM/YYYY"
            # 🇺🇸 US Tech Giants
            "Apple": "30/01/2025",
            "Microsoft": "23/01/2025",
            "Alphabet (Google)": "04/02/2025",
            "Amazon": "06/02/2025",
            "Meta (Facebook)": "29/01/2025",
            "Tesla": "22/01/2025",
            "NVIDIA": "26/02/2025",
            "Netflix": "16/01/2025",
            "Adobe": "13/03/2025",
            "Intel": "23/01/2025",
            "AMD": "04/02/2025",
            "Salesforce": "27/02/2025",
            "Oracle": "10/03/2025",
            "IBM": "29/01/2025",
            "Cisco": "12/02/2025",
            # 🇺🇸 US Finance
            "JPMorgan Chase": "14/01/2025",
            "Bank of America": "14/01/2025",
            "Wells Fargo": "15/01/2025",
            "Goldman Sachs": "15/01/2025",
            "Morgan Stanley": "16/01/2025",
            "Citigroup": "14/01/2025",
            "American Express": "24/01/2025",
            "Visa": "23/01/2025",
            "Mastercard": "30/01/2025",
            "BlackRock": "17/01/2025",
            # 🇺🇸 US Consumer & Retail
            "Walmart": "20/02/2025",
            "Coca-Cola": "11/02/2025",
            "PepsiCo": "06/02/2025",
            "Procter & Gamble": "22/01/2025",
            "Nike": "20/03/2025",
            "McDonald's": "10/02/2025",
            "Starbucks": "28/01/2025",
            "Home Depot": "25/02/2025",
            "Target": "04/03/2025",
            "Costco": "27/02/2025",
            # 🇺🇸 US Healthcare & Pharma
            "Johnson & Johnson": "21/01/2025",
            "UnitedHealth": "17/01/2025",
            "Pfizer": "04/02/2025",
            "AbbVie": "31/01/2025",
            "Eli Lilly": "06/02/2025",
            "Merck": "06/02/2025",
            "Bristol Myers Squibb": "06/02/2025",
            # 🇺🇸 US Energy
            "Exxon Mobil": "31/01/2025",
            "Chevron": "31/01/2025",
            "ConocoPhillips": "06/02/2025",
            # 🇩🇪 German Companies
            "SAP": "23/01/2025",
            "Siemens": "13/02/2025",
            "Volkswagen": "13/03/2025",
            "BMW": "19/03/2025",
            "Mercedes-Benz": "20/02/2025",
            "Allianz": "21/02/2025",
            "BASF": "27/02/2025",
            "Deutsche Bank": "30/01/2025",
            "Adidas": "05/03/2025",
            "Bayer": "26/02/2025",
            # 🇳🇱 Dutch Companies
            "ASML": "22/01/2025",
            "Shell": "30/01/2025",
            "Unilever": "13/02/2025",
            "Philips": "27/01/2025",
            "ING Group": "07/02/2025",
            # 🇨🇭 Swiss Companies
            "Nestlé": "13/02/2025",
            "Novartis": "30/01/2025",
            "Roche": "30/01/2025",
            "UBS": "31/01/2025",
            "Zurich Insurance": "13/02/2025",
            "ABB": "06/02/2025",
            "Richemont": "16/05/2025",
            # 🇬🇧 UK Companies
            "AstraZeneca": "13/02/2025",
            "BP": "04/02/2025",
            "HSBC": "18/02/2025",
            "Unilever": "13/02/2025",
            "Diageo": "30/01/2025",
            "GSK": "12/02/2025",
            "Rio Tinto": "26/02/2025",
            # 🇯🇵 Japanese Companies
            "Toyota": "06/02/2025",
            "Sony": "14/02/2025",
            "Honda": "07/02/2025",
            "Nintendo": "04/02/2025",
            "SoftBank": "13/02/2025",
            "Mitsubishi": "07/02/2025",
            # 🇰🇷 South Korean Companies
            "Samsung Electronics": "31/01/2025",
            "Hyundai": "23/01/2025",
            "SK Hynix": "23/01/2025",
            "LG Electronics": "29/01/2025",
            # 🇨🇳 Chinese Companies
            "Alibaba": "20/02/2025",
            "Tencent": "19/03/2025",
            "BYD": "28/04/2025",
            "ICBC": "28/03/2025",
            "PetroChina": "27/03/2025",
            # 🇨🇦 Canadian Companies
            "Royal Bank of Canada": "27/02/2025",
            "Toronto-Dominion Bank": "27/02/2025",
            "Shopify": "13/02/2025",
            "Canadian National Railway": "28/01/2025",
            # === 2026 ===
            # 🇺🇸 US Tech Giants 2026
            "Apple": "29/01/2026",
            "Microsoft": "22/01/2026",
            "Alphabet (Google)": "03/02/2026",
            "Amazon": "05/02/2026",
            "Meta (Facebook)": "28/01/2026",
            "Tesla": "21/01/2026",
            "NVIDIA": "25/02/2026",
            "Netflix": "15/01/2026",
            "Adobe": "12/03/2026",
            "Intel": "22/01/2026",
            "AMD": "03/02/2026",
            "Salesforce": "26/02/2026",
            "Oracle": "09/03/2026",
            "IBM": "28/01/2026",
            "Cisco": "11/02/2026",
            # 🇺🇸 US Finance 2026
            "JPMorgan Chase": "13/01/2026",
            "Bank of America": "13/01/2026",
            "Wells Fargo": "14/01/2026",
            "Goldman Sachs": "14/01/2026",
            "Morgan Stanley": "15/01/2026",
            "Citigroup": "13/01/2026",
            "American Express": "23/01/2026",
            "Visa": "22/01/2026",
            "Mastercard": "29/01/2026",
            "BlackRock": "16/01/2026",
            # 🇺🇸 US Consumer & Retail 2026
            "Walmart": "19/02/2026",
            "Coca-Cola": "10/02/2026",
            "PepsiCo": "05/02/2026",
            "Procter & Gamble": "21/01/2026",
            "Nike": "19/03/2026",
            "McDonald's": "09/02/2026",
            "Starbucks": "27/01/2026",
            "Home Depot": "24/02/2026",
            "Target": "03/03/2026",
            "Costco": "26/02/2026",
            # 🇺🇸 US Healthcare & Pharma 2026
            "Johnson & Johnson": "20/01/2026",
            "UnitedHealth": "16/01/2026",
            "Pfizer": "03/02/2026",
            "AbbVie": "30/01/2026",
            "Eli Lilly": "05/02/2026",
            "Merck": "05/02/2026",
            "Bristol Myers Squibb": "05/02/2026",
            # 🇺🇸 US Energy 2026
            "Exxon Mobil": "30/01/2026",
            "Chevron": "30/01/2026",
            "ConocoPhillips": "05/02/2026",
            # 🇩🇪 German Companies 2026
            "SAP": "22/01/2026",
            "Siemens": "12/02/2026",
            "Volkswagen": "12/03/2026",
            "BMW": "18/03/2026",
            "Mercedes-Benz": "19/02/2026",
            "Allianz": "20/02/2026",
            "BASF": "26/02/2026",
            "Deutsche Bank": "29/01/2026",
            "Adidas": "04/03/2026",
            "Bayer": "25/02/2026",
            # 🇳🇱 Dutch Companies 2026
            "ASML": "21/01/2026",
            "Shell": "29/01/2026",
            "Unilever": "12/02/2026",
            "Philips": "26/01/2026",
            "ING Group": "06/02/2026",
            # 🇨🇭 Swiss Companies 2026
            "Nestlé": "12/02/2026",
            "Novartis": "29/01/2026",
            "Roche": "29/01/2026",
            "UBS": "30/01/2026",
            "Zurich Insurance": "12/02/2026",
            "ABB": "05/02/2026",
            "Richemont": "15/05/2026",
            # 🇬🇧 UK Companies 2026
            "AstraZeneca": "12/02/2026",
            "BP": "03/02/2026",
            "HSBC": "17/02/2026",
            "Unilever": "12/02/2026",
            "Diageo": "29/01/2026",
            "GSK": "11/02/2026",
            "Rio Tinto": "25/02/2026",
            # 🇯🇵 Japanese Companies 2026
            "Toyota": "05/02/2026",
            "Sony": "13/02/2026",
            "Honda": "06/02/2026",
            "Nintendo": "03/02/2026",
            "SoftBank": "12/02/2026",
            "Mitsubishi": "06/02/2026",
            # 🇰🇷 South Korean Companies 2026
            "Samsung Electronics": "30/01/2026",
            "Hyundai": "22/01/2026",
            "SK Hynix": "22/01/2026",
            "LG Electronics": "28/01/2026",
            # 🇨🇳 Chinese Companies 2026
            "Alibaba": "19/02/2026",
            "Tencent": "18/03/2026",
            "BYD": "27/04/2026",
            "ICBC": "27/03/2026",
            "PetroChina": "26/03/2026",
            # 🇨🇦 Canadian Companies 2026
            "Royal Bank of Canada": "26/02/2026",
            "Toronto-Dominion Bank": "26/02/2026",
            "Shopify": "12/02/2026",
            "Canadian National Railway": "27/01/2026",
        }

        # Filter French companies based on search
        filtered_french_earnings = french_earnings
        if search_company:
            search_lower = search_company.lower()
            filtered_french_earnings = {
                company: date for company, date in french_earnings.items()
                if search_lower in company.lower()
            }

        if filtered_french_earnings:
            st.markdown("#### 🇫🇷 French Companies (CAC 40 / SBF 120)")
            french_data = [{"Entreprise": company, "Date de publication": date}
                          for company, date in sorted(filtered_french_earnings.items(),
                                                     key=lambda x: pd.to_datetime(x[1], format='%d/%m/%Y'))]
            st.dataframe(pd.DataFrame(french_data), use_container_width=True, hide_index=True)
            st.caption(f"📊 {len(filtered_french_earnings)} publications françaises à venir")
            st.markdown("🔗 [Calendrier complet sur Boursorama](https://www.boursorama.com/bourse/actualites/calendriers/societes-cotees)")
        elif search_company:
            st.info(f"No French companies found matching '{search_company}'")

        st.markdown("---")

        # Filter international companies based on search
        filtered_international_earnings = international_earnings
        if search_company:
            search_lower = search_company.lower()
            filtered_international_earnings = {
                company: date for company, date in international_earnings.items()
                if search_lower in company.lower()
            }

        if filtered_international_earnings:
            st.markdown("#### 🌍 International Companies (US, Europe, Asia)")
            intl_data = [{"Company": company, "Publication Date": date}
                        for company, date in sorted(filtered_international_earnings.items(),
                                                   key=lambda x: pd.to_datetime(x[1], format='%d/%m/%Y'))]
            st.dataframe(pd.DataFrame(intl_data), use_container_width=True, hide_index=True, height=400)
            st.caption(f"📊 {len(filtered_international_earnings)} international publications upcoming")
        elif search_company and not filtered_french_earnings:
            st.info(f"No international companies found matching '{search_company}'")


def display_kpi_row(portfolio):
    """Affiche la rangée de KPIs en haut du dashboard"""
    from portfolio_package.visualizations import create_kpi_metrics, get_cac40_data, get_dji_data, get_btc_data

    kpis = create_kpi_metrics(portfolio)
    cac40_value, cac40_change = get_cac40_data()
    dji_value, dji_change = get_dji_data()
    btc_value, btc_change = get_btc_data()


    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="💰 Net Worth",
            value=format_currency(kpis['net_worth']),
            delta=None
        )

    with col2:
        st.metric(
            label="📈 Investments",
            value=format_currency(kpis['investment_value']),
            delta=f"{kpis['investment_change']:+.1f}%"
        )

    with col3:
        st.metric(
            label="📊 BTC-USD",
            value=format_currency(round(btc_value, -1)),
            delta=f"{btc_change:+.2f}%"
        )
    with col4:
        st.metric(
            label="📊 CAC40",
            value=format_currency(round(cac40_value,0)),
            delta=f"{cac40_change:+.2f}%"
        )

    with col5:
        st.metric(
            label="📊 DJI",
            value=format_currency(round(dji_value, 0)),
            delta=f"{dji_change:+.2f}%"
        )


def display_dashboard_charts(portfolio):
    """Affiche les graphiques principaux du dashboard"""

    from portfolio_package.visualizations import (
        create_financial_portfolio_vs_cac40_chart,
        create_portfolio_pie_chart,
        create_performance_chart_filtered
    )
    #st.markdown("<style>div.block-container{padding-top:0.5rem;padding-bottom:0rem;}</style>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:-1rem;'></div>", unsafe_allow_html=True)

    # Graphique principal en pleine largeur
    fig_evolution = create_financial_portfolio_vs_cac40_chart(portfolio)
    st.plotly_chart(
        fig_evolution,
        use_container_width=True,
        config={"displayModeBar": False,
        "staticPlot": False,
        "responsive": True,
        "height": 290   # 👈 tu peux définir la hauteur ici maintenan
        },
    )
    col1, col2 = st.columns(2)
    with col1:
        fig_pie = create_portfolio_pie_chart(portfolio)
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False, "height": 390}
        )

    with col2:
        fig_perf = create_performance_chart_filtered(portfolio)
        st.plotly_chart(fig_perf, use_container_width=True, config={"displayModeBar": False, "height": 390})


def show_portfolio_charts(portfolio):
    """Fonction principale pour l'onglet Portfolio"""
    import streamlit as st

    #remove_streamlit_spacing()

    # KPIs en haut
    display_kpi_row(portfolio)

    # Graphiques
    display_dashboard_charts(portfolio)


def remove_streamlit_spacing():
    """Réduit les espaces entre les éléments Streamlit"""
    import streamlit as st

    st.markdown("""
        <style>
        /* Réduire l'espace entre les graphiques */
        .element-container {
            margin-bottom: -1rem !important;
        }

        /* Réduire l'espace des graphiques Plotly */
        .js-plotly-plot {
            margin-bottom: -1rem !important;
        }

        /* Réduire l'espace vertical général */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
        }

        /* Réduire l'espace entre métriques */
        [data-testid="stMetricValue"] {
            margin-bottom: 0rem !important;
        }

        /* Réduire l'espace des dividers */
        hr {
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }

        /* Réduire l'espace entre colonnes */
        [data-testid="column"] {
            padding: 0.5rem !important;
        }

        /* Réduire l'espace des subheaders */
        h3 {
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }
        </style>
    """, unsafe_allow_html=True)



