from fpdf import FPDF
import plotly.express as px
import os
from portfolio_package.patrimoine_prediction import simulate_portfolio_future, create_prediction_chart, create_statistics_summary

# Function to convert hex to RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Theme colors
background_color = hex_to_rgb("#1d293d")  # page background
text_color = hex_to_rgb("#e2e8f0")        # general text
border_color = hex_to_rgb("#314158")      # borders
header_bg_color = hex_to_rgb("#1d293d")   # table header background

def generate_portfolio_pdf(portfolio, filename="portfolio.pdf", logo_path="../logo/FullLogo.png"):
    pdf = FPDF()

    # === COVER PAGE ===
    pdf.add_page()

    # Cover page background
    pdf.set_fill_color(*background_color)
    pdf.rect(0, 0, pdf.w, pdf.h, 'F')

    # Absolute path to logo (going up one level from portfolio_package to project root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_logo_path = os.path.join(script_dir, logo_path)

    # Logo centered vertically
    if os.path.exists(full_logo_path):
        # Center the logo (width 80mm, proportional height)
        logo_width = 150
        logo_x = (pdf.w - logo_width) / 2
        logo_y = 70  # Vertical position
        pdf.image(full_logo_path, x=logo_x, y=logo_y, w=logo_width)

    # FINVIEW title centered below logo
    pdf.set_y(150)
    pdf.set_font("Arial", 'B', 32)
    pdf.set_text_color(*text_color)
    pdf.cell(0, 15, "", ln=True, align="C")

    # Separator line
    pdf.ln(10)
    pdf.set_draw_color(*text_color)
    pdf.set_line_width(0.3)
    line_margin = 60
    pdf.line(line_margin, pdf.get_y(), pdf.w - line_margin, pdf.get_y())

    # Authors' names centered
    pdf.ln(15)
    pdf.set_font("Arial", '', 14)
    pdf.set_text_color(*text_color)
    pdf.cell(0, 8, "Antonin BENARD", ln=True, align="C")
    pdf.cell(0, 8, "Leo COLIN", ln=True, align="C")
    pdf.cell(0, 8, "Pierre QUINTIN de KERCADIO", ln=True, align="C")

    # === PAGE 1: Portfolio Performance ===
    pdf.add_page()

    # Page background
    pdf.set_fill_color(*background_color)
    pdf.rect(0, 0, pdf.w, pdf.h, 'F')

    # Logo at top left
    if os.path.exists(full_logo_path):
        pdf.image(full_logo_path, x=5, y=5, w=50)

    # Centered title
    pdf.ln(15)  # space for logo
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(*text_color)
    pdf.cell(0, 10, "Portfolio Performance", ln=True, align="C")
    pdf.ln(5)

    # White separator line
    pdf.set_draw_color(*text_color)
    pdf.set_line_width(0.5)
    pdf.line(20, pdf.get_y(), pdf.w - 20, pdf.get_y())
    pdf.ln(10)

    # Investment analysis (clean text)
    if portfolio.investments:
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(*text_color)
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

        # Diversification level
        if num_investments >= 8:
            diversification = "High"
        elif num_investments >= 5:
            diversification = "Medium"
        else:
            diversification = "Low"

        # Analysis text
        pdf.set_font("Arial", '', 12)
        pdf.set_text_color(*text_color)

        # Portfolio summary text
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
        pdf.set_text_color(*text_color)
        pdf.cell(0, 10, "No investments", ln=True)

    # Add transaction history
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(*text_color)
    pdf.cell(0, 10, "Transaction History", ln=True)
    pdf.ln(5)

    if portfolio.transaction_history:
        pdf.set_draw_color(*border_color)
        pdf.set_fill_color(*header_bg_color)
        pdf.set_font("Arial", 'B', 10)

        # History header
        pdf.cell(45, 10, "Date", border=1, fill=True)
        pdf.cell(50, 10, "Type", border=1, fill=True)
        pdf.cell(30, 10, "Amount", border=1, fill=True)
        pdf.cell(65, 10, "Description", border=1, fill=True)
        pdf.ln()

        # History content (last 10 transactions)
        pdf.set_font("Arial", '', 9)
        last_transactions = portfolio.transaction_history[-10:]
        for transaction in last_transactions:
            # Replace unsupported special characters
            description = transaction['description'][:30]
            description = description.replace('€', 'EUR').replace('→', '->')
            pdf.cell(45, 8, transaction['date'], border=1)
            pdf.cell(50, 8, transaction['type'], border=1)
            pdf.cell(30, 8, f"{transaction['amount']:.2f} EUR", border=1)
            pdf.cell(65, 8, description, border=1)
            pdf.ln()

        # Analysis of recent actions
        pdf.ln(5)
        pdf.set_font("Arial", '', 11)
        pdf.set_text_color(*text_color)

        # Count recent transaction types
        recent_buys = sum(1 for t in last_transactions if 'BUY' in t['type'])
        recent_sells = sum(1 for t in last_transactions if 'SELL' in t['type'])
        recent_updates = sum(1 for t in last_transactions if 'UPDATE' in t['type'])

        # Generate analysis text
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
        pdf.set_text_color(*text_color)
        pdf.cell(0, 10, "No transactions", ln=True)

    # === PAGE 2: Investment Charts ===
    if portfolio.investments:
        pdf.add_page()

        # Page 2 background (same color as page 1)
        pdf.set_fill_color(*background_color)
        pdf.rect(0, 0, pdf.w, pdf.h, 'F')

        # Logo at top left (page 2)
        if os.path.exists(full_logo_path):
            pdf.image(full_logo_path, x=5, y=5, w=50)

        # Page 2 title
        pdf.ln(15)  # space for logo
        pdf.set_font("Arial", 'B', 16)
        pdf.set_text_color(*text_color)
        pdf.cell(0, 10, "Investment Allocation", ln=True, align="C")
        pdf.ln(5)

        # White separator line
        pdf.set_draw_color(*text_color)
        pdf.set_line_width(0.5)
        pdf.line(20, pdf.get_y(), pdf.w - 20, pdf.get_y())
        pdf.ln(10)

        # Pie chart with custom colors - LARGER SIZE
        # Get all investments with their values
        all_investments = [(name, inv.get_total_value()) for name, inv in portfolio.investments.items()]
        total_value = sum(v for _, v in all_investments)

        # Show all investments without grouping
        labels = []
        values = []

        # Sort by value descending
        all_investments.sort(key=lambda x: x[1], reverse=True)

        for name, value in all_investments:
            labels.append(name)
            values.append(value)

        # Varied colors for assets - modern palette
        colors = ['#0EA5E9', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6',
                  '#EC4899', '#14B8A6', '#F97316', '#06B6D4', '#84CC16']

        fig = px.pie(
            values=values,
            names=labels,
            color_discrete_sequence=colors,
            hole=0.45  # Donut chart for better readability
        )
        fig.update_traces(
            textposition='auto',
            textinfo='percent',
            textfont=dict(size=18, color='white'),
            marker=dict(
                line=dict(color='#1d293d', width=3),
                pattern=dict(shape="")
            ),
            pull=[0.05] * len(values)  # Slight pull effect for all slices
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
        # High quality image
        fig.write_image("graphique_pie.png", width=900, height=1000, scale=2)
        pdf.image("graphique_pie.png", x=5, y=pdf.get_y(), w=200, h=220)

        # === NEW PAGE FOR INVESTMENT DETAILS TABLE ===
        pdf.add_page()

        # Page background
        pdf.set_fill_color(*background_color)
        pdf.rect(0, 0, pdf.w, pdf.h, 'F')

        # Logo at top left
        if os.path.exists(full_logo_path):
            pdf.image(full_logo_path, x=5, y=5, w=50)

        # Page title
        pdf.ln(15)  # space for logo
        pdf.set_font("Arial", 'B', 16)
        pdf.set_text_color(*text_color)
        pdf.cell(0, 10, "Investment Details", ln=True, align="C")
        pdf.ln(5)

        # White separator line
        pdf.set_draw_color(*text_color)
        pdf.set_line_width(0.5)
        pdf.line(20, pdf.get_y(), pdf.w - 20, pdf.get_y())
        pdf.ln(10)

        # Detail by investment
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(*text_color)
        pdf.cell(0, 10, "Detail by asset", ln=True)
        pdf.ln(5)

        # Detailed table
        pdf.set_draw_color(*border_color)
        pdf.set_fill_color(*header_bg_color)
        pdf.set_font("Arial", 'B', 10)

        pdf.cell(60, 10, "Asset", border=1, fill=True)
        pdf.cell(40, 10, "Total value", border=1, fill=True)
        pdf.cell(45, 10, "% of portfolio", border=1, fill=True)
        pdf.cell(45, 10, "Performance", border=1, fill=True)
        pdf.ln()

        # Calculate total portfolio value
        total_portfolio = sum(inv.get_total_value() for inv in portfolio.investments.values())

        # Content
        pdf.set_font("Arial", '', 10)
        for name, inv in portfolio.investments.items():
            value = inv.get_total_value()
            percentage = (value / total_portfolio * 100) if total_portfolio > 0 else 0
            perf = inv.get_gain_loss_percentage()

            pdf.cell(60, 8, name[:25], border=1)
            pdf.cell(40, 8, f"{value:.2f} EUR", border=1)
            pdf.cell(45, 8, f"{percentage:.1f}%", border=1)
            pdf.cell(45, 8, f"{perf:+.1f}%", border=1)
            pdf.ln()

    # === PAGE 3: Portfolio Predictions ===
    pdf.add_page()

    # Page 3 background
    pdf.set_fill_color(*background_color)
    pdf.rect(0, 0, pdf.w, pdf.h, 'F')

    # Logo at top left (page 3)
    if os.path.exists(full_logo_path):
        pdf.image(full_logo_path, x=5, y=5, w=50)

    # Page 3 title
    pdf.ln(15)  # space for logo
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(*text_color)
    pdf.cell(0, 10, "Portfolio Predictions", ln=True, align="C")
    pdf.ln(5)

    # White separator line
    pdf.set_draw_color(*text_color)
    pdf.set_line_width(0.5)
    pdf.line(20, pdf.get_y(), pdf.w - 20, pdf.get_y())
    pdf.ln(10)

    # Generate predictions if portfolio contains investments
    if portfolio.investments:
        # Generate simulation
        try:
            prediction_results = simulate_portfolio_future(portfolio, years=10, num_simulations=1000)
            stats = create_statistics_summary(prediction_results)

            # Prediction chart
            fig = create_prediction_chart(prediction_results)
            fig.write_image("prediction_chart.png", width=800, height=400)
            pdf.image("prediction_chart.png", x=10, y=pdf.get_y(), w=190)
            pdf.ln(110)

            # Key statistics
            pdf.set_font("Arial", 'B', 13)
            pdf.set_text_color(*text_color)
            pdf.cell(0, 8, "10-year forecast scenarios", ln=True)
            pdf.ln(3)

            # Scenarios table
            pdf.set_draw_color(*border_color)
            pdf.set_fill_color(*header_bg_color)
            pdf.set_font("Arial", 'B', 9)

            pdf.cell(55, 8, "Scenario", border=1, fill=True)
            pdf.cell(45, 8, "Final value", border=1, fill=True)
            pdf.cell(45, 8, "Gain/Loss", border=1, fill=True)
            pdf.cell(45, 8, "Annualized return", border=1, fill=True)
            pdf.ln()

            # Scenario content
            pdf.set_font("Arial", '', 9)
            scenarios = [
                ("Very optimistic (P90)", stats['final']['p90'], stats['gains']['p90'], stats['returns']['p90']),
                ("Optimistic (P75)", stats['final']['p75'], stats['gains']['p75'], stats['returns']['p75']),
                ("Median (P50)", stats['final']['p50'], stats['gains']['p50'], stats['returns']['p50']),
                ("Cautious (P25)", stats['final']['p25'], stats['gains']['p25'], stats['returns']['p25']),
                ("Pessimistic (P10)", stats['final']['p10'], stats['gains']['p10'], stats['returns']['p10'])
            ]

            for scenario_name, final_val, gain, return_pct in scenarios:
                pdf.cell(55, 7, scenario_name, border=1)
                pdf.cell(45, 7, f"{final_val:.0f} EUR", border=1)
                pdf.cell(45, 7, f"{gain:+.0f} EUR", border=1)
                pdf.cell(45, 7, f"{return_pct:+.1f}%/yr", border=1)
                pdf.ln()

            pdf.ln(5)

            # Warning note
            pdf.set_font("Arial", 'I', 9)
            pdf.set_text_color(*text_color)
            warning = (
                "These predictions are based on Monte Carlo simulations using average historical returns. "
                "Actual results may vary considerably depending on many unforeseen factors (economic crises, "
                "innovations, regulatory changes, etc.). This simulation does not constitute investment advice."
            )
            pdf.multi_cell(0, 5, warning)

            # Clean up temporary file
            try:
                os.remove("prediction_chart.png")
            except:
                pass

        except Exception as e:
            pdf.set_font("Arial", '', 11)
            pdf.set_text_color(*text_color)
            pdf.multi_cell(0, 6, f"Unable to generate predictions: {str(e)}")
    else:
        pdf.set_font("Arial", '', 11)
        pdf.set_text_color(*text_color)
        pdf.multi_cell(0, 6, "No investments to generate predictions.")

    # === PAGE 4: Investment Advice ===
    pdf.add_page()

    # Page 4 background
    pdf.set_fill_color(*background_color)
    pdf.rect(0, 0, pdf.w, pdf.h, 'F')

    # Logo at top left (page 4)
    if os.path.exists(full_logo_path):
        pdf.image(full_logo_path, x=5, y=5, w=50)

    # Page 4 title
    pdf.ln(15)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(*text_color)
    pdf.cell(0, 10, "Investment Advice", ln=True, align="C")
    pdf.ln(5)

    # White separator line
    pdf.set_draw_color(*text_color)
    pdf.set_line_width(0.5)
    pdf.line(20, pdf.get_y(), pdf.w - 20, pdf.get_y())
    pdf.ln(10)

    # Analyze portfolio to give personalized advice
    if portfolio.investments:
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
        pdf.set_font("Arial", 'B', 13)
        pdf.set_text_color(*text_color)
        pdf.cell(0, 8, "1. Portfolio diversification", ln=True)
        pdf.ln(3)
        pdf.set_font("Arial", '', 11)

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
        pdf.set_font("Arial", 'B', 13)
        pdf.cell(0, 8, "2. Financial / real estate balance", ln=True)
        pdf.ln(3)
        pdf.set_font("Arial", '', 11)

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
        pdf.set_font("Arial", 'B', 13)
        pdf.cell(0, 8, "3. Risk management", ln=True)
        pdf.ln(3)
        pdf.set_font("Arial", '', 11)

        advice3 = (
            "Regularly review your investments and rebalance your portfolio "
            "if necessary. Maintain a cash reserve (3-6 months of expenses) "
            "to handle unforeseen events without having to sell your assets in an emergency."
        )

        pdf.multi_cell(0, 6, advice3)
        pdf.ln(5)

        # Advice 4: Investment horizon
        pdf.set_font("Arial", 'B', 13)
        pdf.cell(0, 8, "4. Long-term vision", ln=True)
        pdf.ln(3)
        pdf.set_font("Arial", '', 11)

        advice4 = (
            "The best returns are achieved over the long term (minimum 5-10 years). "
            "Avoid impulsive decisions based on short-term fluctuations. "
            "Invest regularly to benefit from dollar-cost averaging."
        )

        pdf.multi_cell(0, 6, advice4)
        pdf.ln(5)

        # Final note
        pdf.set_font("Arial", 'I', 10)
        pdf.set_text_color(*text_color)
        final_note = (
            "Note: This advice is indicative and based on the analysis of your current portfolio. "
            "For personalized recommendations, consult a professional financial advisor."
        )
        pdf.multi_cell(0, 5, final_note)

    pdf.output(filename)
    return filename
