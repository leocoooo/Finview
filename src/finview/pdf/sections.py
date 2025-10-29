"""PDF section generators for each page of the portfolio report."""

import os
import plotly.express as px
from .config import *
from .components import (
    add_page_background, add_header_with_logo, add_section_title,
    add_separator_line, create_table_header, cleanup_temp_files,
    sanitize_text, get_diversification_level
)
from src.finview.predictions import simulate_portfolio_future, create_prediction_chart, create_statistics_summary
from src.finview.charts import create_portfolio_pie_chart, create_performance_chart_filtered


def add_cover_page(pdf, logo_path):
    """Add cover page with logo and authors.
    
    Args:
        pdf: FPDF instance
        logo_path: Relative path to logo file
    """
    pdf.add_page()
    add_page_background(pdf)
    
    # Get full logo path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_logo_path = os.path.join(script_dir, '..', '..', '..', logo_path)
    
    # Logo centered vertically
    if os.path.exists(full_logo_path):
        logo_x = (pdf.w - LOGO_WIDTH_COVER) / 2
        pdf.image(full_logo_path, x=logo_x, y=LOGO_Y_COVER, w=LOGO_WIDTH_COVER)
    
    # Position below logo
    pdf.set_y(150)
    pdf.set_font("Arial", 'B', FONT_SIZE_COVER_TITLE)
    pdf.set_text_color(*TEXT_COLOR)
    pdf.cell(0, 15, "", ln=True, align="C")
    
    # Separator line
    pdf.ln(10)
    pdf.set_draw_color(*TEXT_COLOR)
    pdf.set_line_width(TITLE_LINE_WIDTH)
    pdf.line(LINE_MARGIN, pdf.get_y(), pdf.w - LINE_MARGIN, pdf.get_y())
    
    # Authors' names centered
    pdf.ln(15)
    pdf.set_font("Arial", '', FONT_SIZE_AUTHORS)
    pdf.set_text_color(*TEXT_COLOR)
    for author in AUTHORS:
        pdf.cell(0, 8, author, ln=True, align="C")


def add_dashboard_page(pdf, portfolio, logo_path):
    """Add dashboard overview page with charts.
    
    Args:
        pdf: FPDF instance
        portfolio: Portfolio instance
        logo_path: Relative path to logo file
    """
    if not portfolio.investments:
        return
    
    pdf.add_page()
    add_page_background(pdf)
    full_logo_path = add_header_with_logo(pdf, logo_path)
    add_section_title(pdf, "Dashboard Overview")
    add_separator_line(pdf)
    
    try:
        # Portfolio pie chart (donut)
        fig_pie = create_portfolio_pie_chart(portfolio)
        fig_pie.update_layout(
            width=CHART_PIE_WIDTH,
            height=CHART_PIE_HEIGHT,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        fig_pie.write_image("dashboard_pie.png", scale=2)
        pdf.image("dashboard_pie.png", x=IMAGE_DASHBOARD_PIE['x'], y=pdf.get_y(), 
                  w=IMAGE_DASHBOARD_PIE['w'], h=IMAGE_DASHBOARD_PIE['h'])
        pdf.ln(110)
        
        # Performance chart filtered
        fig_perf = create_performance_chart_filtered(portfolio)
        fig_perf.update_layout(
            width=CHART_PERFORMANCE_WIDTH,
            height=CHART_PERFORMANCE_HEIGHT,
            paper_bgcolor='#1d293d',
            plot_bgcolor='#1d293d',
            font=dict(color='#e2e8f0', size=12),
            title=dict(
                text="📈 Key Assets Performance",
                font=dict(size=16, color='#e2e8f0'),
                x=0.5,
                xanchor='center'
            ),
            margin=dict(l=60, r=40, t=60, b=50)
        )
        fig_perf.write_image("dashboard_perf.png", scale=2)
        pdf.image("dashboard_perf.png", x=IMAGE_DASHBOARD_PERF['x'], y=pdf.get_y(), 
                  w=IMAGE_DASHBOARD_PERF['w'], h=IMAGE_DASHBOARD_PERF['h'])
        
        cleanup_temp_files("dashboard_pie.png", "dashboard_perf.png")
        
    except Exception as e:
        pdf.set_font("Arial", '', FONT_SIZE_SMALL)
        pdf.set_text_color(*TEXT_COLOR)
        pdf.multi_cell(0, 6, f"Unable to generate dashboard charts: {str(e)}")


def add_performance_analysis_page(pdf, portfolio, logo_path):
    """Add portfolio performance analysis page.
    
    Args:
        pdf: FPDF instance
        portfolio: Portfolio instance
        logo_path: Relative path to logo file
    """
    pdf.add_page()
    add_page_background(pdf)
    add_header_with_logo(pdf, logo_path)
    add_section_title(pdf, "Portfolio Performance Analysis")
    add_separator_line(pdf)
    
    # Investment analysis
    if portfolio.investments:
        pdf.set_font("Arial", 'B', FONT_SIZE_SECTION_TITLE)
        pdf.set_text_color(*TEXT_COLOR)
        pdf.cell(0, 10, "Portfolio Analysis", ln=True)
        pdf.ln(5)
        
        # Calculate statistics
        num_investments = len(portfolio.investments)
        financial_total = portfolio.get_financial_investments_value()
        real_estate_total = portfolio.get_real_estate_investments_value()
        total_value = financial_total + real_estate_total
        annual_rental = portfolio.get_total_annual_rental_income()
        
        # Allocation percentages
        if total_value > 0:
            financial_pct = (financial_total / total_value) * 100
            real_estate_pct = (real_estate_total / total_value) * 100
        else:
            financial_pct = real_estate_pct = 0
        
        diversification = get_diversification_level(num_investments)
        
        # Analysis text
        pdf.set_font("Arial", '', FONT_SIZE_NORMAL)
        pdf.set_text_color(*TEXT_COLOR)
        
        summary_text = (
            f"Your portfolio generates an annual rental income of {annual_rental:.2f} EUR, "
            f"approximately {annual_rental/12:.2f} EUR per month. "
            f"Your portfolio shows a {diversification.lower()} diversification "
            f"with {num_investments} investments distributed between "
            f"{financial_pct:.0f}% financial assets and {real_estate_pct:.0f}% real estate."
        )
        
        pdf.multi_cell(0, 8, summary_text)
        pdf.ln(5)
    else:
        pdf.set_text_color(*TEXT_COLOR)
        pdf.cell(0, 10, "No investments", ln=True)
    
    # Add transaction history
    pdf.ln(10)
    pdf.set_font("Arial", 'B', FONT_SIZE_SECTION_TITLE)
    pdf.set_text_color(*TEXT_COLOR)
    pdf.cell(0, 10, "Transaction History", ln=True)
    pdf.ln(5)
    
    if portfolio.transaction_history:
        # Transaction table header
        columns = [
            (TABLE_TRANSACTION_WIDTHS['date'], "Date"),
            (TABLE_TRANSACTION_WIDTHS['type'], "Type"),
            (TABLE_TRANSACTION_WIDTHS['amount'], "Amount"),
            (TABLE_TRANSACTION_WIDTHS['description'], "Description")
        ]
        create_table_header(pdf, columns)
        
        # Transaction content (last 10 transactions)
        pdf.set_font("Arial", '', FONT_SIZE_TABLE_SMALL)
        last_transactions = portfolio.transaction_history[-10:]
        for transaction in last_transactions:
            description = sanitize_text(transaction['description'], 50)
            pdf.cell(TABLE_TRANSACTION_WIDTHS['date'], 8, transaction['date'], border=1)
            pdf.cell(TABLE_TRANSACTION_WIDTHS['type'], 8, transaction['type'], border=1)
            pdf.cell(TABLE_TRANSACTION_WIDTHS['amount'], 8, f"{transaction['amount']:.2f} EUR", border=1)
            pdf.cell(TABLE_TRANSACTION_WIDTHS['description'], 8, description, border=1)
            pdf.ln()
        
        # Analysis of recent actions
        pdf.ln(5)
        pdf.set_font("Arial", '', FONT_SIZE_SMALL)
        pdf.set_text_color(*TEXT_COLOR)
        
        recent_buys = sum(1 for t in last_transactions if 'BUY' in t['type'])
        recent_sells = sum(1 for t in last_transactions if 'SELL' in t['type'])
        recent_updates = sum(1 for t in last_transactions if 'UPDATE' in t['type'])
        
        analysis_text = ""
        if recent_buys > 0:
            analysis_text = f"Your recent transactions show {recent_buys} asset purchase(s), "
        else:
            analysis_text = "No recent asset purchases. "
        
        if recent_updates > 0:
            analysis_text += f"{recent_updates} value update(s), "
        
        if recent_sells > 0:
            analysis_text += f"and {recent_sells} sale(s). "
        else:
            analysis_text += "without recent sales. "
        
        analysis_text += f"In total, {len(last_transactions)} transactions were recorded in this period."
        
        pdf.multi_cell(0, 6, analysis_text)
    else:
        pdf.set_text_color(*TEXT_COLOR)
        pdf.cell(0, 10, "No transactions", ln=True)


def add_allocation_page(pdf, portfolio, logo_path):
    """Add investment allocation page with pie chart.
    
    Args:
        pdf: FPDF instance
        portfolio: Portfolio instance
        logo_path: Relative path to logo file
    """
    if not portfolio.investments:
        return
    
    pdf.add_page()
    add_page_background(pdf)
    add_header_with_logo(pdf, logo_path)
    add_section_title(pdf, "Investment Allocation")
    add_separator_line(pdf)
    
    # Get all investments with their values
    all_investments = [(name, inv.get_total_value()) for name, inv in portfolio.investments.items()]
    all_investments.sort(key=lambda x: x[1], reverse=True)
    
    labels = [name for name, _ in all_investments]
    values = [value for _, value in all_investments]
    
    # Create pie chart
    fig = px.pie(
        values=values,
        names=labels,
        color_discrete_sequence=CHART_COLORS,
        hole=0.45
    )
    fig.update_traces(
        textposition='auto',
        textinfo='percent',
        textfont=dict(size=18, color='white'),
        marker=dict(
            line=dict(color='#1d293d', width=3),
            pattern=dict(shape="")
        ),
        pull=[0.05] * len(values)
    )
    fig.update_layout(
        paper_bgcolor='#1d293d',
        plot_bgcolor='#1d293d',
        font=dict(color='#e2e8f0', size=14, family='Arial'),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='top',
            y=-0.15,
            xanchor='center',
            x=0.5,
            font=dict(size=14),
            bgcolor='rgba(29,41,61,0.8)',
            bordercolor='#314158',
            borderwidth=1
        ),
        margin=dict(l=20, r=20, t=20, b=60)
    )
    
    fig.write_image("graphique_pie.png", width=900, height=1000, scale=2)
    pdf.image("graphique_pie.png", x=IMAGE_ALLOCATION_PIE['x'], y=pdf.get_y(), 
              w=IMAGE_ALLOCATION_PIE['w'], h=IMAGE_ALLOCATION_PIE['h'])
    
    cleanup_temp_files("graphique_pie.png")


def add_details_page(pdf, portfolio, logo_path):
    """Add investment details page with table.
    
    Args:
        pdf: FPDF instance
        portfolio: Portfolio instance
        logo_path: Relative path to logo file
    """
    pdf.add_page()
    add_page_background(pdf)
    add_header_with_logo(pdf, logo_path)
    add_section_title(pdf, "Investment Details")
    add_separator_line(pdf)
    
    pdf.set_font("Arial", 'B', FONT_SIZE_SECTION_TITLE)
    pdf.set_text_color(*TEXT_COLOR)
    pdf.cell(0, 10, "Detail by asset", ln=True)
    pdf.ln(5)
    
    # Details table header
    columns = [
        (TABLE_DETAILS_WIDTHS['asset'], "Asset"),
        (TABLE_DETAILS_WIDTHS['value'], "Total value"),
        (TABLE_DETAILS_WIDTHS['percentage'], "% of portfolio"),
        (TABLE_DETAILS_WIDTHS['performance'], "Performance")
    ]
    create_table_header(pdf, columns)
    
    # Calculate total portfolio value
    total_portfolio = sum(inv.get_total_value() for inv in portfolio.investments.values())
    
    # Table content
    pdf.set_font("Arial", '', FONT_SIZE_TABLE_CONTENT)
    for name, inv in portfolio.investments.items():
        value = inv.get_total_value()
        percentage = (value / total_portfolio * 100) if total_portfolio > 0 else 0
        perf = inv.get_gain_loss_percentage()
        
        pdf.cell(TABLE_DETAILS_WIDTHS['asset'], 8, name[:25], border=1)
        pdf.cell(TABLE_DETAILS_WIDTHS['value'], 8, f"{value:.2f} EUR", border=1)
        pdf.cell(TABLE_DETAILS_WIDTHS['percentage'], 8, f"{percentage:.1f}%", border=1)
        pdf.cell(TABLE_DETAILS_WIDTHS['performance'], 8, f"{perf:+.1f}%", border=1)
        pdf.ln()


def add_predictions_page(pdf, portfolio, logo_path):
    """Add portfolio predictions page with Monte Carlo simulation.
    
    Args:
        pdf: FPDF instance
        portfolio: Portfolio instance
        logo_path: Relative path to logo file
    """
    pdf.add_page()
    add_page_background(pdf)
    add_header_with_logo(pdf, logo_path)
    add_section_title(pdf, "Portfolio Predictions")
    add_separator_line(pdf)
    
    if not portfolio.investments:
        pdf.set_font("Arial", '', FONT_SIZE_SMALL)
        pdf.set_text_color(*TEXT_COLOR)
        pdf.multi_cell(0, 6, "No investments to generate predictions.")
        return
    
    try:
        prediction_results = simulate_portfolio_future(portfolio, years=10, num_simulations=1000)
        stats = create_statistics_summary(prediction_results)
        
        # Prediction chart
        fig = create_prediction_chart(prediction_results)
        fig.write_image("prediction_chart.png", width=CHART_PREDICTION_WIDTH, height=CHART_PREDICTION_HEIGHT)
        pdf.image("prediction_chart.png", x=IMAGE_PREDICTION['x'], y=pdf.get_y(), w=IMAGE_PREDICTION['w'])
        pdf.ln(110)
        
        # Key statistics
        pdf.set_font("Arial", 'B', FONT_SIZE_SECTION_SUBTITLE)
        pdf.set_text_color(*TEXT_COLOR)
        pdf.cell(0, 8, "10-year forecast scenarios", ln=True)
        pdf.ln(3)
        
        # Scenarios table header
        columns = [
            (TABLE_SCENARIOS_WIDTHS['scenario'], "Scenario"),
            (TABLE_SCENARIOS_WIDTHS['final_value'], "Final value"),
            (TABLE_SCENARIOS_WIDTHS['gain_loss'], "Gain/Loss"),
            (TABLE_SCENARIOS_WIDTHS['return'], "Annualized return")
        ]
        create_table_header(pdf, columns)
        
        # Scenario content
        pdf.set_font("Arial", '', FONT_SIZE_TABLE_SMALL)
        scenarios = [
            ("Very optimistic (P90)", stats['final']['p90'], stats['gains']['p90'], stats['returns']['p90']),
            ("Optimistic (P75)", stats['final']['p75'], stats['gains']['p75'], stats['returns']['p75']),
            ("Median (P50)", stats['final']['p50'], stats['gains']['p50'], stats['returns']['p50']),
            ("Cautious (P25)", stats['final']['p25'], stats['gains']['p25'], stats['returns']['p25']),
            ("Pessimistic (P10)", stats['final']['p10'], stats['gains']['p10'], stats['returns']['p10'])
        ]
        
        for scenario_name, final_val, gain, return_pct in scenarios:
            pdf.cell(TABLE_SCENARIOS_WIDTHS['scenario'], 7, scenario_name, border=1)
            pdf.cell(TABLE_SCENARIOS_WIDTHS['final_value'], 7, f"{final_val:.0f} EUR", border=1)
            pdf.cell(TABLE_SCENARIOS_WIDTHS['gain_loss'], 7, f"{gain:+.0f} EUR", border=1)
            pdf.cell(TABLE_SCENARIOS_WIDTHS['return'], 7, f"{return_pct:+.1f}%/yr", border=1)
            pdf.ln()
        
        pdf.ln(5)
        
        # Warning note
        pdf.set_font("Arial", 'I', FONT_SIZE_NOTE)
        pdf.set_text_color(*TEXT_COLOR)
        warning = (
            "These predictions are based on Monte Carlo simulations using average historical returns. "
            "Actual results may vary considerably depending on many unforeseen factors (economic crises, "
            "innovations, regulatory changes, etc.). This simulation does not constitute investment advice."
        )
        pdf.multi_cell(0, 5, warning)
        
        cleanup_temp_files("prediction_chart.png")
        
    except Exception as e:
        pdf.set_font("Arial", '', FONT_SIZE_SMALL)
        pdf.set_text_color(*TEXT_COLOR)
        pdf.multi_cell(0, 6, f"Unable to generate predictions: {str(e)}")


def add_advice_page(pdf, portfolio, logo_path):
    """Add investment advice page.
    
    Args:
        pdf: FPDF instance
        portfolio: Portfolio instance
        logo_path: Relative path to logo file
    """
    pdf.add_page()
    add_page_background(pdf)
    add_header_with_logo(pdf, logo_path)
    add_section_title(pdf, "Investment Advice")
    add_separator_line(pdf)
    
    if not portfolio.investments:
        return
    
    num_investments = len(portfolio.investments)
    financial_total = portfolio.get_financial_investments_value()
    real_estate_total = portfolio.get_real_estate_investments_value()
    total_value = financial_total + real_estate_total
    
    if total_value > 0:
        financial_pct = (financial_total / total_value) * 100
        real_estate_pct = (real_estate_total / total_value) * 100
    else:
        financial_pct = real_estate_pct = 0
    
    # Advice 1: Diversification
    pdf.set_font("Arial", 'B', FONT_SIZE_SECTION_SUBTITLE)
    pdf.set_text_color(*TEXT_COLOR)
    pdf.cell(0, 8, "1. Portfolio diversification", ln=True)
    pdf.ln(3)
    pdf.set_font("Arial", '', FONT_SIZE_SMALL)
    
    if num_investments < 5:
        advice1 = (
            "Your portfolio could benefit from better diversification. "
            "It is recommended to have at least 5 to 8 different assets to reduce risk. "
            "Consider adding investments in different sectors and geographical areas."
        )
    elif num_investments < 8:
        advice1 = (
            "Your diversification is adequate. To optimize further, "
            "you could add a few additional assets in complementary sectors."
        )
    else:
        advice1 = (
            "Excellent diversification! Your portfolio is well distributed. "
            "Continue to maintain this balance while monitoring the correlation between your assets."
        )
    
    pdf.multi_cell(0, 6, advice1)
    pdf.ln(5)
    
    # Advice 2: Asset allocation
    pdf.set_font("Arial", 'B', FONT_SIZE_SECTION_SUBTITLE)
    pdf.cell(0, 8, "2. Financial / real estate balance", ln=True)
    pdf.ln(3)
    pdf.set_font("Arial", '', FONT_SIZE_SMALL)
    
    if real_estate_pct < 10:
        advice2 = (
            "Your real estate exposure is low. Real estate can provide "
            "stability and attractive recurring income. Consider increasing "
            "this allocation to 15-30% for better balance."
        )
    elif real_estate_pct > 50:
        advice2 = (
            "Your portfolio is heavily concentrated in real estate. "
            "It would be prudent to strengthen your exposure to financial assets "
            "for better liquidity and flexibility."
        )
    else:
        advice2 = (
            "Your allocation between financial and real estate assets is balanced. "
            "This diversification offers a good compromise between growth and stability."
        )
    
    pdf.multi_cell(0, 6, advice2)
    pdf.ln(5)
    
    # Advice 3: Risk management
    pdf.set_font("Arial", 'B', FONT_SIZE_SECTION_SUBTITLE)
    pdf.cell(0, 8, "3. Risk management", ln=True)
    pdf.ln(3)
    pdf.set_font("Arial", '', FONT_SIZE_SMALL)
    
    advice3 = (
        "Regularly review your investments and rebalance your portfolio "
        "if necessary. Maintain a cash reserve (3-6 months of expenses) "
        "to handle unforeseen events without having to sell your assets in an emergency."
    )
    
    pdf.multi_cell(0, 6, advice3)
    pdf.ln(5)
    
    # Advice 4: Investment horizon
    pdf.set_font("Arial", 'B', FONT_SIZE_SECTION_SUBTITLE)
    pdf.cell(0, 8, "4. Long-term vision", ln=True)
    pdf.ln(3)
    pdf.set_font("Arial", '', FONT_SIZE_SMALL)
    
    advice4 = (
        "The best returns are achieved over the long term (minimum 5-10 years). "
        "Avoid impulsive decisions based on short-term fluctuations. "
        "Invest regularly to benefit from dollar-cost averaging."
    )
    
    pdf.multi_cell(0, 6, advice4)
    pdf.ln(5)
    
    # Final note
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(*TEXT_COLOR)
    final_note = (
        "Note: This advice is indicative and based on the analysis of your current portfolio. "
        "For personalized recommendations, consult a professional financial advisor."
    )
    pdf.multi_cell(0, 5, final_note)
