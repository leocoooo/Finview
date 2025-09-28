import streamlit as st
import pandas as pd
from datetime import datetime
import json
import plotly.express as px
from pdf import generate_portfolio_pdf

from portfolio_package.models import Portfolio

from portfolio_package.interface_functions import (
    _add_investment_with_date,
    _update_investment_with_date,
    _sell_investment_with_date,
    _add_credit_with_date,
    _pay_credit_with_date,
    create_demo_portfolio
)

from portfolio_package.save_load_ptf_functions import save_portfolio, load_portfolio

from portfolio_package.charts import create_portfolio_pie_chart, create_portfolio_chart, create_performance_chart, create_world_investment_map
from portfolio_package.yahoo_search import asset_search_tab
import yfinance as yf


# Configuration de la page
st.set_page_config(
    page_title="Gestionnaire de Portefeuille",
    page_icon="💰",
    layout="wide"
)

# Ajout des méthodes à la classe Portfolio
Portfolio._add_investment_with_date = _add_investment_with_date
Portfolio._update_investment_with_date = _update_investment_with_date
Portfolio._sell_investment_with_date = _sell_investment_with_date
Portfolio._add_credit_with_date = _add_credit_with_date
Portfolio._pay_credit_with_date = _pay_credit_with_date


# Initialisation du state avec sauvegarde/chargement automatique
if 'portfolio' not in st.session_state:
    # Essayer de charger un portefeuille existant
    loaded_portfolio = load_portfolio()
    if loaded_portfolio:
        st.session_state.portfolio = loaded_portfolio
    else:
        st.session_state.portfolio = Portfolio(initial_cash=0.0)

# Interface principale
def main():
    st.title("💰 Gestionnaire de Portefeuille Financier")
    
    # Sidebar pour les actions
    st.sidebar.image(
        "logo/FullLogo.png",
        width='stretch' # Ajuste automatiquement la largeur
    )
    st.sidebar.title("Choix de l'onglet")
    
    action = st.sidebar.selectbox(
        "Selectionnez une page",
        ["🏠 Tableau de bord", "💵 Gérer les liquidités", "📈 Investissements",
        "💳 Crédits", "🌍 Carte du monde", "📊 Analyses", "📋 Historique"]
    )

    # Boutons de sauvegarde/chargement
    st.sidebar.subheader("💾 Importer / exporter mon portefeuille")

    # Bouton Sauvegarder
    if st.sidebar.button("Sauvegarder", help="Sauvegarde automatique à chaque modification"):
        if save_portfolio(st.session_state.portfolio):
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
    
    # Bouton pour créer des données de démonstration
    st.sidebar.subheader("🎭 Données de test")
    if st.sidebar.button("Créer un portefeuille de démonstration", help="Crée un historique simulé sur 6 mois"):
        st.session_state.portfolio = create_demo_portfolio()
        save_portfolio(st.session_state.portfolio)
        st.sidebar.success("🎉 Portefeuille de démo créé!")
        st.rerun()
    
    if st.sidebar.button("Réinitialiser portefeuille"):
        st.session_state.portfolio = Portfolio(initial_cash=1000.0)
        save_portfolio(st.session_state.portfolio)
        st.sidebar.success("🔄 Portefeuille réinitialisé!")
        st.rerun()

    # Bouton d'export
    if st.sidebar.button("Télécharger sauvegarde"):
        portfolio_data = st.session_state.portfolio.to_dict()
        st.sidebar.download_button(
            label="📥 Télécharger JSON",
            data=json.dumps(portfolio_data, indent=2, ensure_ascii=False),
            file_name=f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime=
            "application/json"
        )
        pdf_filename = f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        generate_portfolio_pdf(st.session_state.portfolio, filename=pdf_filename)
        with open(pdf_filename, "rb") as f:
            st.sidebar.download_button(
        label="📄 Télécharger PDF",
        data=f,
        file_name=pdf_filename,
        mime="application/pdf"
    )

    

    
    portfolio = st.session_state.portfolio
    
    if action == "🏠 Tableau de bord":
        show_dashboard(portfolio)
    elif action == "💵 Gérer les liquidités":
        manage_cash(portfolio)
    elif action == "📈 Investissements":
        manage_investments(portfolio)
    elif action == "💳 Crédits":
        manage_credits(portfolio)
    elif action == "🌍 Carte du monde":
        show_world_map(portfolio)
    elif action == "📊 Analyses":
        show_analytics(portfolio)
    elif action == "📋 Historique":
        show_history(portfolio)

def show_dashboard(portfolio):
    st.header("Tableau de bord")
    
    # Métriques principales
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("💰 Liquidités", f"{portfolio.cash:.2f}€")

    with col2:
        financial_value = portfolio.get_financial_investments_value()
        st.metric("📈 Inv. Financiers", f"{financial_value:.2f}€")

    with col3:
        real_estate_value = portfolio.get_real_estate_investments_value()
        st.metric("🏠 Inv. Immobiliers", f"{real_estate_value:.2f}€")

    with col4:
        credits_balance = portfolio.get_total_credits_balance()
        st.metric("💳 Crédits", f"-{credits_balance:.2f}€")

    with col5:
        net_worth = portfolio.get_net_worth()
        st.metric("🏆 Valeur nette", f"{net_worth:.2f}€")

    # Indicateurs supplémentaires et affichage du revenu locatif
    additional_info = []

    # Revenu locatif
    if portfolio.real_estate_investments:
        annual_rental_income = portfolio.get_total_annual_rental_income()
        if annual_rental_income > 0:
            additional_info.append(f"💰 Revenu locatif annuel : {annual_rental_income:.2f}€ ({annual_rental_income/12:.2f}€/mois)")

    # Indicateur de diversification
    total_investments = len(portfolio.financial_investments) + len(portfolio.real_estate_investments)
    if total_investments > 0:
        diversification_score = "Élevée" if total_investments >= 5 else "Moyenne" if total_investments >= 3 else "Faible"
        diversification_color = "🟢" if total_investments >= 5 else "🟡" if total_investments >= 3 else "🔴"
        additional_info.append(f"{diversification_color} Diversification : {diversification_score} ({total_investments} investissements)")

    # Répartition équilibrée
    if portfolio.financial_investments and portfolio.real_estate_investments:
        fin_ratio = portfolio.get_financial_investments_value() / (portfolio.get_financial_investments_value() + portfolio.get_real_estate_investments_value()) * 100
        re_ratio = 100 - fin_ratio
        additional_info.append(f"⚖️ Répartition : {fin_ratio:.0f}% financier / {re_ratio:.0f}% immobilier")

    # Affichage des informations
    if additional_info:
        for info in additional_info:
            st.info(info)
    
    # Section graphique principal
    st.markdown("---")

    # Graphique en secteurs professionnel et lisible
    if portfolio.investments or portfolio.cash > 0:
        fig = create_portfolio_pie_chart(portfolio)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Ligne de séparation
    st.markdown("---")

    # Tableaux des investissements séparés par type
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📈 Investissements Financiers")
        if portfolio.financial_investments:
            fin_data = []
            for name, inv in portfolio.financial_investments.items():
                inv_type = getattr(inv, 'investment_type', 'N/A')
                fin_data.append({
                    "Nom": name,
                    "Type": inv_type,
                    "Quantité": inv.quantity,
                    "Valeur unit.": f"{inv.current_value:.2f}€",
                    "Valeur totale": f"{inv.get_total_value():.2f}€",
                    "Gain/Perte": f"{inv.get_gain_loss():+.2f}€",
                    "Performance": f"{inv.get_gain_loss_percentage():+.1f}%"
                })
            st.dataframe(pd.DataFrame(fin_data), use_container_width=True)
        else:
            st.info("Aucun investissement financier")

    with col2:
        st.subheader("🏠 Investissements Immobiliers")
        if portfolio.real_estate_investments:
            re_data = []
            for name, inv in portfolio.real_estate_investments.items():
                property_type = getattr(inv, 'property_type', 'N/A')
                location = getattr(inv, 'location', 'N/A')
                rental_yield = getattr(inv, 'rental_yield', 0)
                annual_income = inv.get_annual_rental_income() if hasattr(inv, 'get_annual_rental_income') else 0

                re_data.append({
                    "Nom": name,
                    "Type": property_type,
                    "Localisation": location if location else "N/A",
                    "Rendement": f"{rental_yield:.1f}%" if rental_yield > 0 else "N/A",
                    "Valeur totale": f"{inv.get_total_value():.2f}€",
                    "Revenu annuel": f"{annual_income:.2f}€" if annual_income > 0 else "N/A",
                    "Performance": f"{inv.get_gain_loss_percentage():+.1f}%"
                })
            st.dataframe(pd.DataFrame(re_data), use_container_width=True)
        else:
            st.info("Aucun investissement immobilier")

    with col3:
        st.subheader("💳 Crédits")
        if portfolio.credits:
            credit_data = []
            for name, credit in portfolio.credits.items():
                credit_data.append({
                    "Nom": name,
                    "Solde restant": f"{credit.get_remaining_balance():.2f}€",
                    "Taux": f"{credit.interest_rate:.1f}%",
                    "Paiement mensuel": f"{credit.monthly_payment:.2f}€"
                })
            st.dataframe(pd.DataFrame(credit_data), use_container_width=True)
        else:
            st.info("Aucun crédit")

def manage_cash(portfolio):
    st.header("💵 Gestion des liquidités")
    st.metric("Liquidités actuelles", f"{portfolio.cash:.2f}€")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Ajouter des liquidités")
        add_amount = st.number_input("Montant à ajouter", min_value=0.01, step=0.01, key="add_cash")
        add_description = st.text_input("Description", value="Ajout de liquidités", key="add_desc")
        if st.button("Ajouter", key="btn_add"):
            portfolio.add_cash(add_amount, add_description)
            save_portfolio(portfolio)  # Sauvegarde automatique
            st.success(f"{add_amount:.2f}€ ajoutés avec succès!")
            st.rerun()
    
    with col2:
        st.subheader("Retirer des liquidités")
        if portfolio.cash > 0.01:
            max_withdraw = max(0.01, portfolio.cash)
            withdraw_amount = st.number_input("Montant à retirer", min_value=0.01, max_value=max_withdraw, step=0.01, key="withdraw_cash")
            withdraw_description = st.text_input("Description", value="Retrait de liquidités", key="withdraw_desc")
            can_withdraw = portfolio.cash >= withdraw_amount
            if st.button("Retirer", key="btn_withdraw", disabled=not can_withdraw):
                if can_withdraw and portfolio.withdraw_cash(withdraw_amount, withdraw_description):
                    save_portfolio(portfolio)  # Sauvegarde automatique
                    st.success(f"{withdraw_amount:.2f}€ retirés avec succès!")
                    st.rerun()
                else:
                    st.error("Fonds insuffisants!")
        else:
            st.info("Pas assez de liquidités disponibles pour effectuer un retrait")

def manage_investments(portfolio):
    st.header("📈 Gestion des investissements")

    # Ajout du nouveau tab pour la recherche d'actifs
    tab1, tab2, tab3, tab4 = st.tabs(["Ajouter manuellement", "🔍 Rechercher actif", "Mettre à jour", "Vendre"])

    with tab1:
        st.subheader("Nouvel investissement manuel")

        # Choix du type d'investissement
        investment_type = st.selectbox("Type d'investissement",
                                     ["💰 Financier", "🏠 Immobilier"],
                                     key="investment_type_select")

        inv_name = st.text_input("Nom de l'investissement")
        inv_price = st.number_input("Prix unitaire", min_value=0.01, step=0.01)
        inv_quantity = st.number_input("Quantité", min_value=0.01, step=0.01)

        # Champs spécifiques selon le type d'investissement
        if investment_type == "💰 Financier":
            col1, col2 = st.columns(2)
            with col1:
                financial_type = st.selectbox("Catégorie",
                                            ["Action", "ETF", "Obligation", "Crypto", "Fonds", "Autre"],
                                            key="financial_category")
            with col2:
                location = st.text_input("🌍 Localisation (optionnel)",
                                       placeholder="Ex: États-Unis, Europe, Japon",
                                       key="financial_location",
                                       help="Permet de localiser l'investissement sur la carte du monde")
        else:  # Immobilier
            col1, col2 = st.columns(2)
            with col1:
                property_type = st.selectbox("Type de bien",
                                           ["SCPI", "REIT", "Immobilier direct", "Foncière", "Autre"],
                                           key="property_category")
            with col2:
                location = st.text_input("🌍 Localisation",
                                       placeholder="Ex: Paris, États-Unis, Londres",
                                       key="real_estate_location",
                                       help="Localisation géographique du bien immobilier")

            rental_yield = st.number_input("Rendement locatif annuel (%)",
                                         min_value=0.0, max_value=20.0,
                                         value=0.0, step=0.1,
                                         key="rental_yield",
                                         help="Rendement locatif annuel estimé en %")

        total_cost = inv_price * inv_quantity
        st.info(f"Coût total: {total_cost:.2f}€ (Liquidités disponibles: {portfolio.cash:.2f}€)")

        if st.button("Acheter", key="manual_buy"):
            if inv_name and inv_name not in portfolio.investments:
                success = False
                if investment_type == "💰 Financier":
                    success = portfolio.add_financial_investment(inv_name, inv_price, inv_quantity, financial_type, location)
                else:
                    success = portfolio.add_real_estate_investment(inv_name, inv_price, inv_quantity,
                                                                 property_type, location, rental_yield)

                if success:
                    save_portfolio(portfolio)  # Sauvegarde automatique
                    location_msg = f" (📍 {location})" if location else ""
                    st.success(f"Investissement '{inv_name}' ajouté avec succès!{location_msg}")
                    if location:
                        st.info("🌍 Consultez l'onglet 'Carte du monde' pour voir votre investissement géolocalisé!")
                    st.rerun()
                else:
                    st.error("Fonds insuffisants!")
            else:
                st.error("Nom invalide ou investissement déjà existant!")

    with tab2:
        # Utilisation de la nouvelle fonction de recherche
        portfolio_addition = asset_search_tab()

        # Si un actif a été sélectionné pour ajout au portefeuille
        if portfolio_addition:
            asset_name = portfolio_addition['name']
            asset_price = portfolio_addition['price']
            asset_quantity = portfolio_addition['quantity']

            # Vérifier si l'actif existe déjà dans le portefeuille
            if asset_name not in portfolio.investments:
                if portfolio.add_investment(asset_name, asset_price, asset_quantity):
                    save_portfolio(portfolio)
                    st.success(f"🎉 Actif '{asset_name}' ajouté au portefeuille avec succès!")
                    # Nettoyer les variables de session
                    for key in ['searched_ticker', 'searched_price', 'add_to_portfolio']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
                else:
                    st.error("💸 Fonds insuffisants pour cet achat!")
            else:
                st.warning(f"⚠️ L'actif '{asset_name}' existe déjà dans votre portefeuille. Utilisez l'onglet 'Mettre à jour' pour modifier ses valeurs.")

    with tab3:
        st.subheader("Mettre à jour les valeurs")
        if portfolio.investments:
            inv_to_update = st.selectbox("Investissement", list(portfolio.investments.keys()))
            current_value = portfolio.investments[inv_to_update].current_value
            new_value = st.number_input("Nouvelle valeur unitaire", value=current_value, step=0.01)

            # Option pour mettre à jour automatiquement depuis Yahoo Finance
            if st.checkbox("🔄 Récupérer le prix actuel depuis Yahoo Finance"):
                try:
                    # Essayer de récupérer le prix actuel si le nom ressemble à un ticker
                    ticker_test = yf.Ticker(inv_to_update)
                    current_data = ticker_test.history(period="1d")
                    if not current_data.empty:
                        live_price = current_data['Close'].iloc[-1]
                        new_value = st.number_input(
                            "Nouvelle valeur unitaire",
                            value=float(live_price),
                            step=0.01,
                            key="live_price_update"
                        )
                        st.info(f"💹 Prix en temps réel récupéré: {live_price:.2f}")
                except:
                    st.warning("⚠️ Impossible de récupérer le prix en temps réel. Utilisez la saisie manuelle.")

            if st.button("Mettre à jour"):
                portfolio.update_investment_value(inv_to_update, new_value)
                save_portfolio(portfolio)  # Sauvegarde automatique
                st.success(f"Valeur de '{inv_to_update}' mise à jour!")
                st.rerun()
        else:
            st.info("Aucun investissement à mettre à jour")

    with tab4:
        st.subheader("Vendre des investissements")
        if portfolio.investments:
            inv_to_sell = st.selectbox("Investissement", list(portfolio.investments.keys()), key="sell_select")
            current_quantity = float(portfolio.investments[inv_to_sell].quantity)
            max_sell_quantity = max(0.01, current_quantity) if current_quantity > 0 else 0.01
            default_sell_quantity = min(current_quantity, max_sell_quantity) if current_quantity > 0 else 0.01
            sell_quantity = st.number_input(
                            "Quantité à vendre",
                            min_value=0.01,
                            max_value=max_sell_quantity,
                            value=default_sell_quantity,
                            step=0.01
                        )
            sale_value = portfolio.investments[inv_to_sell].current_value * sell_quantity
            st.info(f"Valeur de la vente: {sale_value:.2f}€")
            
            can_sell = current_quantity >= sell_quantity and current_quantity > 0
            if st.button("Vendre", disabled=not can_sell):
                if can_sell:
                    portfolio.sell_investment(inv_to_sell, sell_quantity)
                    save_portfolio(portfolio)  # Sauvegarde automatique
                    st.success(f"Vente effectuée avec succès!")
                    st.rerun()
                else:
                    st.error("Quantité insuffisante pour la vente!")
        else:
            st.info("Aucun investissement à vendre")

def manage_credits(portfolio):
    st.header("💳 Gestion des crédits")
    
    tab1, tab2 = st.tabs(["Ajouter crédit", "Payer crédit"])
    
    with tab1:
        st.subheader("Nouveau crédit")
        credit_name = st.text_input("Nom du crédit")
        credit_amount = st.number_input("Montant", min_value=0.01, step=0.01)
        credit_rate = st.number_input("Taux d'intérêt annuel (%)", min_value=0.0, step=0.1)
        credit_payment = st.number_input("Paiement mensuel (optionnel)", min_value=0.0, step=0.01)
        
        if st.button("Ajouter crédit"):
            if credit_name and credit_name not in portfolio.credits:
                portfolio.add_credit(credit_name, credit_amount, credit_rate, credit_payment)
                save_portfolio(portfolio)  # Sauvegarde automatique
                st.success(f"Crédit '{credit_name}' ajouté avec succès!")
                st.rerun()
            else:
                st.error("Nom invalide ou crédit déjà existant!")
    
    with tab2:
        st.subheader("Effectuer un paiement")
        if portfolio.credits:
            credit_to_pay = st.selectbox("Crédit", list(portfolio.credits.keys()))
            remaining_balance = portfolio.credits[credit_to_pay].get_remaining_balance()
            max_payment = max(0.01, min(portfolio.cash, remaining_balance)) if min(portfolio.cash, remaining_balance) > 0 else 0.01
            payment_amount = st.number_input("Montant du paiement", min_value=0.01, max_value=max_payment, step=0.01)
            st.info(f"Solde restant: {remaining_balance:.2f}€ | Liquidités disponibles: {portfolio.cash:.2f}€")
            
            can_pay = portfolio.cash >= payment_amount and portfolio.cash > 0 and remaining_balance > 0
            if st.button("Payer", disabled=not can_pay):
                if can_pay and portfolio.pay_credit(credit_to_pay, payment_amount):
                    save_portfolio(portfolio)  # Sauvegarde automatique
                    st.success(f"Paiement de {payment_amount:.2f}€ effectué!")
                    st.rerun()
                else:
                    st.error("Impossible d'effectuer le paiement!")
        else:
            st.info("Aucun crédit à payer")

def show_world_map(portfolio):
    """Affiche la carte du monde des investissements"""
    st.header("🌍 Carte du Monde des Investissements")

    # Métriques de géolocalisation
    total_investments = len(portfolio.financial_investments) + len(portfolio.real_estate_investments)
    financial_count = len(portfolio.financial_investments)
    real_estate_count = len(portfolio.real_estate_investments)

    if total_investments > 0:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("🎯 Total Investissements", total_investments)
        with col2:
            st.metric("📈 Financiers", financial_count)
        with col3:
            st.metric("🏠 Immobiliers", real_estate_count)
        with col4:
            financial_value = portfolio.get_financial_investments_value()
            real_estate_value = portfolio.get_real_estate_investments_value()
            total_value = financial_value + real_estate_value
            st.metric("💰 Valeur Totale", f"{total_value:.0f}€")

        st.markdown("---")

        # Informations sur la répartition géographique
        st.subheader("📍 Répartition Géographique")

        # Analyser les localisations
        locations = {}

        # Investissements financiers
        for name, inv in portfolio.financial_investments.items():
            location = getattr(inv, 'location', 'France')  # Par défaut
            inv_type = getattr(inv, 'investment_type', 'Financier')
            value = inv.get_total_value()

            if location not in locations:
                locations[location] = {'financial': 0, 'real_estate': 0, 'count': 0}
            locations[location]['financial'] += value
            locations[location]['count'] += 1

        # Investissements immobiliers
        for name, inv in portfolio.real_estate_investments.items():
            location = getattr(inv, 'location', 'France')
            value = inv.get_total_value()

            if location not in locations:
                locations[location] = {'financial': 0, 'real_estate': 0, 'count': 0}
            locations[location]['real_estate'] += value
            locations[location]['count'] += 1

        # Afficher le résumé par localisation
        if locations:
            location_data = []
            for loc, data in locations.items():
                total_loc_value = data['financial'] + data['real_estate']
                location_data.append({
                    'Localisation': loc,
                    'Nb. Investissements': data['count'],
                    'Valeur Financière': f"{data['financial']:.2f}€" if data['financial'] > 0 else "-",
                    'Valeur Immobilière': f"{data['real_estate']:.2f}€" if data['real_estate'] > 0 else "-",
                    'Valeur Totale': f"{total_loc_value:.2f}€"
                })

            st.dataframe(pd.DataFrame(location_data), use_container_width=True)

        st.markdown("---")

        # Grande carte interactive
        st.subheader("🗺️ Carte Interactive")
        fig_map = create_world_investment_map(portfolio)

        # Ajuster la taille pour une meilleure visibilité
        fig_map.update_layout(height=700)

        st.plotly_chart(fig_map, use_container_width=True, config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d']
        })

        # Légende et conseils
        st.markdown("---")
        st.subheader("💡 Comment lire cette carte")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🔵 Cercles bleus** : Investissements financiers
            - Taille proportionnelle à la valeur
            - Cliquer pour voir les détails
            - Performance affichée au survol
            """)

        with col2:
            st.markdown("""
            **🟠 Carrés orange** : Investissements immobiliers
            - Taille proportionnelle à la valeur
            - Informations de rendement locatif
            - Localisation précise affichée
            """)

        st.info("💡 **Astuce** : Zoomez et naviguez sur la carte pour explorer vos investissements par région")

    else:
        # Aucun investissement
        st.info("🌍 Aucun investissement à localiser pour le moment")
        st.markdown("""
        ### Comment ajouter des investissements géolocalisés :

        1. **📈 Allez dans l'onglet 'Investissements'**
        2. **🌍 Renseignez la localisation** lors de l'ajout :
           - Pour l'immobilier : champ obligatoire
           - Pour le financier : optionnel mais recommandé
        3. **🗺️ Revenez ici** pour voir vos investissements sur la carte !

        ### Localisations supportées :
        - **Pays** : France, États-Unis, Allemagne, Japon, etc.
        - **Villes** : Paris, New York, Londres, Tokyo, etc.
        - **Régions** : Europe, Asie, Amérique du Nord, etc.
        """)

def show_analytics(portfolio):
    st.header("📊 Analyses et statistiques")
    
    if not portfolio.investments and not portfolio.credits:
        st.info("Pas assez de données pour générer des analyses")
        return
    
    # Performance des investissements
    if portfolio.investments:
        st.subheader("Performance des investissements")
        
        # Graphique de performance
        performance_data = []
        for name, inv in portfolio.investments.items():
            performance_data.append({
                'Investissement': name,
                'Valeur initiale': inv.initial_value * inv.quantity,
                'Valeur actuelle': inv.get_total_value(),
                'Performance (%)': inv.get_gain_loss_percentage()
            })
        
        df_perf = pd.DataFrame(performance_data)
        fig = px.bar(df_perf, x='Investissement', y='Performance (%)', 
                    title="Performance des investissements (%)",
                    color='Performance (%)',
                    color_continuous_scale=['red', 'yellow', 'green'])
        st.plotly_chart(fig, config={})
    
    # Évolution de la valeur nette (simulation)
    st.subheader("Répartition du patrimoine")
    labels = ['Liquidités']
    values = [portfolio.cash]
    
    for name, inv in portfolio.investments.items():
        labels.append(name)
        values.append(inv.get_total_value())
    
    if values and sum(values) > 0:
        fig = px.pie(values=values, names=labels, title="Répartition des actifs")
        st.plotly_chart(fig, config={})

def show_history(portfolio):
    st.header("📋 Historique des transactions")
    
    if portfolio.transaction_history:
        df_history = pd.DataFrame(portfolio.transaction_history)
        df_history = df_history.sort_values('date', ascending=False)
        
        # Ajout de métriques sur l'historique
        st.subheader("📊 Résumé de l'activité")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_transactions = len(df_history)
            st.metric("Total transactions", total_transactions)
        
        with col2:
            cash_transactions = df_history[df_history['type'].str.contains('CASH')]['amount'].sum()
            st.metric("Mouvements cash", f"{cash_transactions:.0f}€")
        
        with col3:
            investment_buys = df_history[df_history['type'] == 'INVESTMENT_BUY']['amount'].sum()
            st.metric("Investissements", f"{investment_buys:.0f}€")
        
        with col4:
            credit_payments = df_history[df_history['type'] == 'CREDIT_PAYMENT']['amount'].sum()
            st.metric("Paiements crédits", f"{credit_payments:.0f}€")
        
        # Graphique de l'évolution des transactions par mois
        df_history['month'] = pd.to_datetime(df_history['date']).dt.to_period('M').astype(str)
        monthly_transactions = df_history.groupby(['month', 'type']).size().reset_index(name='count')
        
        if len(monthly_transactions) > 0:
            fig = px.bar(monthly_transactions, x='month', y='count', color='type',
                        title="Nombre de transactions par mois et type",
                        labels={'month': 'Mois', 'count': 'Nombre de transactions', 'type': 'Type'})
            st.plotly_chart(fig, config={})
        
        # Filtres
        col1, col2 = st.columns(2)
        with col1:
            type_filter = st.selectbox("Filtrer par type", 
                                     ["Tous"] + list(df_history['type'].unique()))
        with col2:
            date_filter = st.date_input("Date minimum", value=None)
        
        # Application des filtres
        filtered_df = df_history.copy()
        if type_filter != "Tous":
            filtered_df = filtered_df[filtered_df['type'] == type_filter]
        if date_filter:
            filtered_df = filtered_df[pd.to_datetime(filtered_df['date']).dt.date >= date_filter]
        
        # Amélioration de l'affichage du tableau
        display_df = filtered_df.copy()
        display_df['Type'] = display_df['type'].map({
            'CASH_ADD': '💰 Ajout liquidités',
            'CASH_WITHDRAW': '💸 Retrait liquidités',
            'INVESTMENT_BUY': '📈 Achat investissement',
            'INVESTMENT_SELL': '📉 Vente investissement', 
            'INVESTMENT_UPDATE': '🔄 MAJ prix',
            'CREDIT_ADD': '🏦 Nouveau crédit',
            'CREDIT_PAYMENT': '💳 Paiement crédit',
            'CREDIT_INTEREST': '📊 Intérêts crédit'
        })
        display_df['Montant'] = display_df['amount'].apply(lambda x: f"{x:.2f}€" if x > 0 else "")
        display_df['Date'] = pd.to_datetime(display_df['date']).dt.strftime('%d/%m/%Y %H:%M')
        
        # Affichage du tableau
        st.subheader(f"📋 Transactions ({len(filtered_df)} résultats)")
        st.dataframe(
            display_df[['Date', 'Type', 'Montant', 'description']].rename(columns={'description': 'Description'}),
            use_container_width=True,
            height=400
        )
        
        # Statistiques détaillées
        st.subheader("📈 Statistiques détaillées")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Nombre de transactions", len(filtered_df))
        with col2:
            total_amount = filtered_df['amount'].sum()
            st.metric("Montant total", f"{total_amount:.2f}€")
        with col3:
            avg_amount = filtered_df['amount'].mean() if len(filtered_df) > 0 else 0
            st.metric("Montant moyen", f"{avg_amount:.2f}€")
        
        # Timeline des événements majeurs
        if len(df_history) > 5:
            st.subheader("🕒 Timeline des événements majeurs")
            major_events = df_history[df_history['type'].isin(['INVESTMENT_BUY', 'CREDIT_ADD', 'INVESTMENT_SELL'])].head(10)
            for _, event in major_events.iterrows():
                event_date = pd.to_datetime(event['date']).strftime('%d/%m/%Y')
                if event['type'] == 'INVESTMENT_BUY':
                    st.write(f"📈 **{event_date}** : {event['description']} ({event['amount']:.0f}€)")
                elif event['type'] == 'CREDIT_ADD':
                    st.write(f"🏦 **{event_date}** : {event['description']} ({event['amount']:.0f}€)")
                elif event['type'] == 'INVESTMENT_SELL':
                    st.write(f"📉 **{event_date}** : {event['description']} ({event['amount']:.0f}€)")
                    
    else:
        st.info("Aucune transaction enregistrée")
        st.markdown("💡 **Astuce** : Utilisez le bouton 'Créer portefeuille de démonstration' dans la sidebar pour voir un exemple d'historique complet !")




if __name__ == "__main__":
    main()