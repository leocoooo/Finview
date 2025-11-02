"""
CSS styles for the application
"""

NAVIGATION_STYLES = """
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
"""

COMPACT_LAYOUT_STYLES = """
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
"""