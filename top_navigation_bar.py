"""
Module de navigation horizontale pour l'application FinView
"""
import streamlit as st
import json
from datetime import datetime


def create_horizontal_menu():
    """
    Crée un menu horizontal en utilisant st.columns et des boutons
    Retourne la page sélectionnée
    """
    # Style CSS pour la navigation
    st.markdown("""
        <style>
        /* Réduire l'espace en haut */
        .main .block-container {
            padding-top: 1rem;
        }
        
        /* Style pour l'en-tête principal */
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
        
        /* Styler les boutons de navigation */
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
        
        /* Bouton actif */
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
        
        /* Sidebar optimisée */
        section[data-testid="stSidebar"] {
            width: 280px !important;
        }
        
        section[data-testid="stSidebar"] > div {
            padding-top: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # En-tête avec titre
    st.markdown("""
        <div class="nav-header">
            <div>
                <h1>💰 Gestionnaire de Portefeuille Financier</h1>
                <p class="nav-subtitle">Gérez vos investissements en toute simplicité</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Initialiser la page actuelle dans session_state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 Tableau de bord"

    # Définir les pages avec leurs icônes
    pages_config = [
        ("🏠 Tableau de bord", "🏠"),
        ("💵 Gérer les liquidités", "💵"),
        ("📈 Investissements", "📈"),
        ("💳 Crédits", "💳"),
        ("🌍 Carte du monde", "🌍"),
        ("📊 Analyses", "📊"),
        ("📋 Historique", "📋")
    ]

    # Créer les colonnes pour la navigation
    cols = st.columns(len(pages_config))

    for idx, (col, (page_name, icon)) in enumerate(zip(cols, pages_config)):
        with col:
            # Déterminer si le bouton doit être en mode "primary" (actif)
            is_active = st.session_state.current_page == page_name
            button_type = "primary" if is_active else "secondary"

            # Créer le label du bouton (sans l'emoji du nom de page)
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
    Crée la sidebar avec les actions de sauvegarde/chargement

    Args:
        portfolio: L'objet portfolio actuel
        save_portfolio_func: La fonction de sauvegarde du portfolio
        Portfolio: La classe Portfolio pour créer de nouvelles instances
        create_demo_portfolio_func: Fonction pour créer un portfolio de démonstration
        generate_pdf_func: Fonction optionnelle pour générer un PDF
    """
    # Logo en haut de la sidebar
    try:
        st.sidebar.image(
            "logo/FullLogo.png",
            use_container_width=True
        )
    except:
        st.sidebar.title("⚙️ Actions")

    st.sidebar.markdown("---")

    # Section Sauvegarde/Chargement
    st.sidebar.subheader("💾 Importer / exporter mon portefeuille")

    # Bouton Sauvegarder
    if st.sidebar.button("💾 Sauvegarder", help="Sauvegarde automatique à chaque modification", use_container_width=True):
        if save_portfolio_func(portfolio):
            st.sidebar.success("✅ Sauvegardé!")

    # Importer un fichier JSON
    uploaded_file = st.sidebar.file_uploader(
        "Importer",
        type="json",
        help="Importer un fichier de sauvegarde",
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            st.session_state.portfolio = Portfolio.from_dict(data)
            st.sidebar.success("✅ Importé!")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Erreur d'import: {e}")

    st.sidebar.markdown("---")

    # Section Données de test
    st.sidebar.subheader("🎭 Données de test")

    if st.sidebar.button("Créer un portefeuille de démonstration", help="Crée un historique simulé sur 6 mois", use_container_width=True):
        st.session_state.portfolio = create_demo_portfolio_func()
        save_portfolio_func(st.session_state.portfolio)
        st.sidebar.success("🎉 Portefeuille de démo créé!")
        st.rerun()

    if st.sidebar.button("Réinitialiser portefeuille", use_container_width=True):
        st.session_state.portfolio = Portfolio(initial_cash=1000.0)
        save_portfolio_func(st.session_state.portfolio)
        st.sidebar.success("🔄 Portefeuille réinitialisé!")
        st.rerun()

    st.sidebar.markdown("---")

    # Section Export
    st.sidebar.subheader("📥 Télécharger sauvegarde")

    # Export JSON
    portfolio_data = portfolio.to_dict()
    json_str = json.dumps(portfolio_data, indent=2, ensure_ascii=False)

    st.sidebar.download_button(
        label="📥 Télécharger JSON",
        data=json_str,
        file_name=f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        use_container_width=True
    )

    # Export PDF si la fonction est fournie
    if generate_pdf_func:
        if st.sidebar.button("📄 Générer et télécharger PDF", use_container_width=True):
            pdf_filename = f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            try:
                generate_pdf_func(portfolio, filename=pdf_filename)
                with open(pdf_filename, "rb") as f:
                    pdf_data = f.read()

                # Nettoyer le fichier temporaire
                import os
                try:
                    os.remove(pdf_filename)
                except:
                    pass

                st.sidebar.download_button(
                    label="📥 Télécharger le PDF",
                    data=pdf_data,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    use_container_width=True,
                    key="pdf_download"
                )
            except Exception as e:
                st.sidebar.error(f"Erreur PDF: {e}")

    # Informations du portfolio
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Infos rapides")
    st.sidebar.metric("💰 Liquidités", f"{portfolio.cash:.2f}€")

    if portfolio.investments:
        total_inv = sum(inv.current_value * inv.quantity for inv in portfolio.investments.values())
        st.sidebar.metric("📈 Investissements", f"{total_inv:.2f}€")

    if portfolio.credits:
        total_debt = sum(credit.get_remaining_balance() for credit in portfolio.credits.values())
        st.sidebar.metric("💳 Dettes", f"{total_debt:.2f}€")