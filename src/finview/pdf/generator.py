"""Main PDF generator for portfolio reports."""

from fpdf import FPDF
from .sections import (
    add_cover_page,
    add_dashboard_page,
    add_performance_analysis_page,
    add_allocation_page,
    add_details_page,
    add_predictions_page,
    add_advice_page
)


def generate_portfolio_pdf(portfolio, filename="portfolio.pdf", logo_path="logo/FullLogo.png"):
    """Generate a complete portfolio PDF report.
    
    This function creates a comprehensive PDF report with the following sections:
    1. Cover page with logo and authors
    2. Dashboard overview with charts
    3. Performance analysis with transaction history
    4. Investment allocation pie chart
    5. Investment details table
    6. Portfolio predictions (Monte Carlo simulation)
    7. Investment advice
    
    Args:
        portfolio: Portfolio instance containing investments and transaction history
        filename: Output PDF filename (default: "portfolio.pdf")
        logo_path: Relative path to logo file from project root (default: "logo/FullLogo.png")
        
    Returns:
        str: The filename of the generated PDF
        
    Example:
        >>> from src.finview.models.portfolio import Portfolio
        >>> from src.finview.pdf import generate_portfolio_pdf
        >>> portfolio = Portfolio()
        >>> # ... add investments to portfolio ...
        >>> generate_portfolio_pdf(portfolio, "my_portfolio.pdf")
        'my_portfolio.pdf'
    """
    pdf = FPDF()
    
    # Generate all sections
    add_cover_page(pdf, logo_path)
    add_dashboard_page(pdf, portfolio, logo_path)
    add_performance_analysis_page(pdf, portfolio, logo_path)
    add_allocation_page(pdf, portfolio, logo_path)
    add_details_page(pdf, portfolio, logo_path)
    add_predictions_page(pdf, portfolio, logo_path)
    add_advice_page(pdf, portfolio, logo_path)
    
    # Save PDF
    pdf.output(filename)
    return filename
