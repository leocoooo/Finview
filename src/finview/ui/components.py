"""
Reusable UI components for the application
"""

import os
import json
from datetime import datetime

import streamlit as st

from .styles import NAVIGATION_STYLES
from .formatting import format_currency


def create_horizontal_menu():
    """
    Creates a horizontal menu using st.columns and buttons
    Returns the selected page
    """
    # CSS style for navigation
    st.markdown(NAVIGATION_STYLES, unsafe_allow_html=True)

    # Initialize current page in session_state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "📊 Summary"

    # Define pages with their icons
    pages_config = [
        ("📊 Summary", "📊"),
        ("💼 Wealth Management", "💼"),
        ("📈 Dashboard", "📈"),
        ("🔮 Predictions", "🔮"),
        ("📰 News", "📰"),
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
                width='stretch',
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
    except Exception:
        st.sidebar.title("⚙️ Actions")

    st.sidebar.markdown("---")

    # Save/Load Section
    st.sidebar.subheader("💾 Import Portfolio")

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
            imported_portfolio = Portfolio.from_dict(data)
            
            # Directly update session state with imported portfolio
            st.session_state.portfolio = imported_portfolio
            
            # Save to disk for persistence
            save_portfolio_func(imported_portfolio)
            
            st.sidebar.success("✅ Portfolio imported successfully!")
            st.rerun()
            
        except Exception as e:
            st.sidebar.error(f"❌ Import error: {str(e)}")


    st.sidebar.markdown("---")

    # Test Data Section
    st.sidebar.subheader("🎭 Test Data")

    if st.sidebar.button("Create demo portfolio", help="Creates a simulated 6-month history", width='stretch'):
        demo_portfolio = create_demo_portfolio_func()
        st.session_state.portfolio = demo_portfolio
        save_portfolio_func(demo_portfolio)
        st.sidebar.success("🎉 Demo portfolio created!")
        st.rerun()

    if st.sidebar.button("Reset portfolio", width='stretch'):
        reset_portfolio = Portfolio(initial_cash=0)
        st.session_state.portfolio = reset_portfolio
        save_portfolio_func(reset_portfolio)
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
        width='stretch'
    )

    # PDF Export if function is provided
    if generate_pdf_func:
        if st.sidebar.button("📄 Generate and download portfolio analysis", width='stretch'):
            pdf_filename = f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            try:
                generate_pdf_func(portfolio, filename=pdf_filename)
                with open(pdf_filename, "rb") as f:
                    pdf_data = f.read()

                # Clean up temporary file
                try:
                    os.remove(pdf_filename)
                except Exception:
                    pass

                st.sidebar.download_button(
                    label="📥 Download PDF",
                    data=pdf_data,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    width='stretch',
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