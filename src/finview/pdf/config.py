"""Configuration constants for PDF generation."""

# Theme colors (RGB tuples)
BACKGROUND_COLOR = (29, 41, 61)  # #1d293d
TEXT_COLOR = (226, 232, 240)     # #e2e8f0
BORDER_COLOR = (49, 65, 88)      # #314158
HEADER_BG_COLOR = (29, 41, 61)   # #1d293d

# Chart colors - modern palette
CHART_COLORS = [
    '#0EA5E9', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6',
    '#EC4899', '#14B8A6', '#F97316', '#06B6D4', '#84CC16'
]

# Logo dimensions
LOGO_WIDTH_COVER = 150
LOGO_WIDTH_HEADER = 50
LOGO_Y_COVER = 70
LOGO_X_HEADER = 5
LOGO_Y_HEADER = 5

# Page layout
LINE_MARGIN = 60
SEPARATOR_MARGIN_LR = 20
SEPARATOR_LINE_WIDTH = 0.5
TITLE_LINE_WIDTH = 0.3

# Font sizes
FONT_SIZE_COVER_TITLE = 32
FONT_SIZE_PAGE_TITLE = 16
FONT_SIZE_SECTION_TITLE = 14
FONT_SIZE_SECTION_SUBTITLE = 13
FONT_SIZE_NORMAL = 12
FONT_SIZE_SMALL = 11
FONT_SIZE_TABLE_HEADER = 10
FONT_SIZE_TABLE_CONTENT = 10
FONT_SIZE_TABLE_SMALL = 9
FONT_SIZE_NOTE = 9
FONT_SIZE_AUTHORS = 14

# Spacing
SPACE_AFTER_LOGO = 15
SPACE_AFTER_TITLE = 5
SPACE_AFTER_SEPARATOR = 10
SPACE_SECTION = 10

# Table column widths
TABLE_TRANSACTION_WIDTHS = {
    'date': 35,
    'type': 40,
    'amount': 30,
    'description': 85
}

TABLE_DETAILS_WIDTHS = {
    'asset': 60,
    'value': 40,
    'percentage': 45,
    'performance': 45
}

TABLE_SCENARIOS_WIDTHS = {
    'scenario': 55,
    'final_value': 45,
    'gain_loss': 45,
    'return': 45
}

# Chart dimensions
CHART_PIE_WIDTH = 1000
CHART_PIE_HEIGHT = 550
CHART_PERFORMANCE_WIDTH = 1200
CHART_PERFORMANCE_HEIGHT = 450
CHART_PREDICTION_WIDTH = 800
CHART_PREDICTION_HEIGHT = 400

# Image dimensions in PDF
IMAGE_DASHBOARD_PIE = {'x': 20, 'y': None, 'w': 150, 'h': 105}
IMAGE_DASHBOARD_PERF = {'x': 10, 'y': None, 'w': 150, 'h': 100}
IMAGE_ALLOCATION_PIE = {'x': 5, 'y': None, 'w': 200, 'h': 220}
IMAGE_PREDICTION = {'x': 10, 'y': None, 'w': 190, 'h': None}

# Diversification thresholds
DIVERSIFICATION_HIGH = 8
DIVERSIFICATION_MEDIUM = 5

# Authors
AUTHORS = [
    "Antonin BENARD",
    "Leo COLIN",
    "Pierre QUINTIN de KERCADIO",
    "FOURNIER Clément"
]
