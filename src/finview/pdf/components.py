"""Reusable PDF components and utilities."""

import os
from .config import (
    BACKGROUND_COLOR, TEXT_COLOR, BORDER_COLOR, HEADER_BG_COLOR,
    LOGO_WIDTH_HEADER, LOGO_X_HEADER, LOGO_Y_HEADER,
    SPACE_AFTER_LOGO, SPACE_AFTER_TITLE, SPACE_AFTER_SEPARATOR,
    SEPARATOR_MARGIN_LR, SEPARATOR_LINE_WIDTH,
    FONT_SIZE_PAGE_TITLE
)


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple.
    
    Args:
        hex_color: Hex color string (e.g., '#1d293d')
        
    Returns:
        Tuple of (R, G, B) values
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def add_page_background(pdf):
    """Add background color to current page.
    
    Args:
        pdf: FPDF instance
    """
    pdf.set_fill_color(*BACKGROUND_COLOR)
    pdf.rect(0, 0, pdf.w, pdf.h, 'F')


def add_header_with_logo(pdf, logo_path):
    """Add logo at top left of page.
    
    Args:
        pdf: FPDF instance
        logo_path: Relative path to logo file
        
    Returns:
        Full path to logo file
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up two levels (from pdf/ to finview/ to project root)
    full_logo_path = os.path.join(script_dir, '..', '..', '..', logo_path)
    
    if os.path.exists(full_logo_path):
        pdf.image(full_logo_path, x=LOGO_X_HEADER, y=LOGO_Y_HEADER, w=LOGO_WIDTH_HEADER)
    
    return full_logo_path


def add_section_title(pdf, title, centered=True):
    """Add a section title with separator line.
    
    Args:
        pdf: FPDF instance
        title: Title text
        centered: Whether to center the title
    """
    pdf.ln(SPACE_AFTER_LOGO)
    pdf.set_font("Arial", 'B', FONT_SIZE_PAGE_TITLE)
    pdf.set_text_color(*TEXT_COLOR)
    align = "C" if centered else "L"
    pdf.cell(0, 10, title, ln=True, align=align)
    pdf.ln(SPACE_AFTER_TITLE)


def add_separator_line(pdf):
    """Add a white separator line.
    
    Args:
        pdf: FPDF instance
    """
    pdf.set_draw_color(*TEXT_COLOR)
    pdf.set_line_width(SEPARATOR_LINE_WIDTH)
    pdf.line(SEPARATOR_MARGIN_LR, pdf.get_y(), pdf.w - SEPARATOR_MARGIN_LR, pdf.get_y())
    pdf.ln(SPACE_AFTER_SEPARATOR)


def create_table_header(pdf, columns):
    """Create a styled table header.
    
    Args:
        pdf: FPDF instance
        columns: List of tuples (width, text)
    """
    pdf.set_draw_color(*BORDER_COLOR)
    pdf.set_fill_color(*HEADER_BG_COLOR)
    pdf.set_font("Arial", 'B', 10)
    
    for width, text in columns:
        pdf.cell(width, 10, text, border=1, fill=True)
    pdf.ln()


def cleanup_temp_files(*filenames):
    """Remove temporary image files.
    
    Args:
        *filenames: Variable number of filenames to remove
    """
    for filename in filenames:
        try:
            if os.path.exists(filename):
                os.remove(filename)
        except Exception:
            pass


def sanitize_text(text, max_length=None):
    """Sanitize text for PDF (replace unsupported characters).
    
    Args:
        text: Text to sanitize
        max_length: Optional maximum length
        
    Returns:
        Sanitized text
    """
    if max_length:
        text = text[:max_length]
    return text.replace('€', 'EUR').replace('→', '->')


def get_diversification_level(num_investments):
    """Determine diversification level based on number of investments.
    
    Args:
        num_investments: Number of investments in portfolio
        
    Returns:
        String: "High", "Medium", or "Low"
    """
    from .config import DIVERSIFICATION_HIGH, DIVERSIFICATION_MEDIUM
    
    if num_investments >= DIVERSIFICATION_HIGH:
        return "High"
    elif num_investments >= DIVERSIFICATION_MEDIUM:
        return "Medium"
    else:
        return "Low"
