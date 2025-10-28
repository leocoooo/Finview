import streamlit as st
from src.finview.pdf import generate_portfolio_pdf


from src.finview.models import Portfolio


from src.finview.wealth_management_functions import (
    _add_investment_with_date,
    _update_investment_with_date,
    _sell_investment_with_date,
    _add_credit_with_date,
    _pay_credit_with_date,
)


from src.finview.create_demo_portfolio import create_demo_portfolio_4

from src.finview.save_load_ptf_functions import save_portfolio, load_portfolio

from src.finview.interface_functions import (

    create_horizontal_menu,

    create_sidebar_actions,

    show_summary,

    show_wealth_management,

    show_dashboard_tabs,

    show_predictions,

    show_news,

    show_definitions,

)


# Page configuration

st.set_page_config(

    page_title="Portfolio Manager",

    page_icon="logo/FullLogo.png",

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