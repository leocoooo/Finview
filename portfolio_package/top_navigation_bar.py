"""
Horizontal navigation module for the FinView application
"""
import streamlit as st
import json
from datetime import datetime


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
    st.sidebar.metric("💰 Cash", f"{portfolio.cash:.2f}€")

    if portfolio.investments:
        total_inv = sum(inv.current_value * inv.quantity for inv in portfolio.investments.values())
        st.sidebar.metric("📈 Investments", f"{total_inv:.2f}€")

    if portfolio.credits:
        total_debt = sum(credit.get_remaining_balance() for credit in portfolio.credits.values())
        st.sidebar.metric("💳 Debts", f"{total_debt:.2f}€")