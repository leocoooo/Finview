import streamlit as st

# Imports depuis le package principal
from src.finview import (
    Portfolio,
    create_demo_portfolio_4,
    generate_portfolio_pdf
)

from src.finview.ui.portfolio_persistence import save_portfolio, load_portfolio
from src.finview.ui.components import create_horizontal_menu, create_sidebar_actions
from src.finview.pages.summary import show_summary
from src.finview.pages.management import show_wealth_management
from src.finview.pages.analytics import show_dashboard_tabs
from src.finview.pages.predictions import show_predictions
from src.finview.pages.content import show_news, show_definitions

# Page configuration

st.set_page_config(
    page_title="Portfolio Manager",
    page_icon="logo/FullLogo.png",
    layout="wide"
)


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
        create_demo_portfolio_func=create_demo_portfolio_4,
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

    elif action == "📰 Actuality":
        show_news()

    elif action == "📚 Definitions":
        show_definitions()


if __name__ == "__main__":
    main()