import streamlit as st
import pandas as pd
from datetime import datetime
import json
import plotly.express as px

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

from portfolio_package.charts import create_portfolio_pie_chart

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
    st.sidebar.title("Actions")
    
    action = st.sidebar.selectbox(
        "Choix de l'onglet",
        ["🏠 Tableau de bord", "💵 Gérer les liquidités", "📈 Investissements", 
         "💳 Crédits", "📊 Analyses", "📋 Historique"]
    )

    # Boutons de sauvegarde/chargement
    st.sidebar.subheader("💾 Gestion des données")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Sauvegarder", help="Sauvegarde automatique à chaque modification"):
            if save_portfolio(st.session_state.portfolio):
                st.sidebar.success("✅ Sauvegardé!")
    with col2:
        uploaded_file = st.file_uploader("Importer", type="json", help="Importer un fichier de sauvegarde", label_visibility="collapsed")
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
    if st.sidebar.button("Créer portefeuille de démonstration", help="Crée un historique simulé sur 6 mois"):
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
            mime="application/json"
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
    elif action == "📊 Analyses":
        show_analytics(portfolio)
    elif action == "📋 Historique":
        show_history(portfolio)

def show_dashboard(portfolio):
    st.header("Tableau de bord")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Liquidités", f"{portfolio.cash:.2f}€")
    
    with col2:
        investments_value = portfolio.get_total_investments_value()
        st.metric("📈 Investissements", f"{investments_value:.2f}€")
    
    with col3:
        credits_balance = portfolio.get_total_credits_balance()
        st.metric("💳 Crédits", f"-{credits_balance:.2f}€")
    
    with col4:
        net_worth = portfolio.get_net_worth()
        st.metric("🏆 Valeur nette", f"{net_worth:.2f}€")
    
    # Graphique en secteurs de la répartition
    if portfolio.investments or portfolio.cash > 0:
        fig = create_portfolio_pie_chart(portfolio)
        st.plotly_chart(fig, config={})
    
    # Tableaux des investissements et crédits
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Investissements")
        if portfolio.investments:
            inv_data = []
            for name, inv in portfolio.investments.items():
                inv_data.append({
                    "Nom": name,
                    "Quantité": inv.quantity,
                    "Valeur unitaire": f"{inv.current_value:.2f}€",
                    "Valeur totale": f"{inv.get_total_value():.2f}€",
                    "Gain/Perte": f"{inv.get_gain_loss():+.2f}€",
                    "Performance": f"{inv.get_gain_loss_percentage():+.1f}%"
                })
            st.dataframe(pd.DataFrame(inv_data), width='stretch')
        else:
            st.info("Aucun investissement")
    
    with col2:
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
            st.dataframe(pd.DataFrame(credit_data), width='stretch')
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
        withdraw_amount = st.number_input("Montant à retirer", min_value=0.01, max_value=portfolio.cash, step=0.01, key="withdraw_cash")
        withdraw_description = st.text_input("Description", value="Retrait de liquidités", key="withdraw_desc")
        if st.button("Retirer", key="btn_withdraw"):
            if portfolio.withdraw_cash(withdraw_amount, withdraw_description):
                save_portfolio(portfolio)  # Sauvegarde automatique
                st.success(f"{withdraw_amount:.2f}€ retirés avec succès!")
                st.rerun()
            else:
                st.error("Fonds insuffisants!")

def manage_investments(portfolio):
    st.header("📈 Gestion des investissements")
    
    tab1, tab2, tab3 = st.tabs(["Ajouter", "Mettre à jour", "Vendre"])
    
    with tab1:
        st.subheader("Nouvel investissement")
        inv_name = st.text_input("Nom de l'investissement")
        inv_price = st.number_input("Prix unitaire", min_value=0.01, step=0.01)
        inv_quantity = st.number_input("Quantité", min_value=0.01, step=0.01)
        total_cost = inv_price * inv_quantity
        st.info(f"Coût total: {total_cost:.2f}€ (Liquidités disponibles: {portfolio.cash:.2f}€)")
        
        if st.button("Acheter"):
            if inv_name and inv_name not in portfolio.investments:
                if portfolio.add_investment(inv_name, inv_price, inv_quantity):
                    save_portfolio(portfolio)  # Sauvegarde automatique
                    st.success(f"Investissement '{inv_name}' ajouté avec succès!")
                    st.rerun()
                else:
                    st.error("Fonds insuffisants!")
            else:
                st.error("Nom invalide ou investissement déjà existant!")
    
    with tab2:
        st.subheader("Mettre à jour les valeurs")
        if portfolio.investments:
            inv_to_update = st.selectbox("Investissement", list(portfolio.investments.keys()))
            current_value = portfolio.investments[inv_to_update].current_value
            new_value = st.number_input("Nouvelle valeur unitaire", value=current_value, step=0.01)
            
            if st.button("Mettre à jour"):
                portfolio.update_investment_value(inv_to_update, new_value)
                save_portfolio(portfolio)  # Sauvegarde automatique
                st.success(f"Valeur de '{inv_to_update}' mise à jour!")
                st.rerun()
        else:
            st.info("Aucun investissement à mettre à jour")
    
    with tab3:
        st.subheader("Vendre des investissements")
        if portfolio.investments:
            inv_to_sell = st.selectbox("Investissement", list(portfolio.investments.keys()), key="sell_select")
            current_quantity = float(portfolio.investments[inv_to_sell].quantity)
            sell_quantity = st.number_input(
                            "Quantité à vendre",
                            min_value=0.01,
                            max_value=current_quantity,
                            value=current_quantity,
                            step=0.01
                        )
            sale_value = portfolio.investments[inv_to_sell].current_value * sell_quantity
            st.info(f"Valeur de la vente: {sale_value:.2f}€")
            
            if st.button("Vendre"):
                portfolio.sell_investment(inv_to_sell, sell_quantity)
                save_portfolio(portfolio)  # Sauvegarde automatique
                st.success(f"Vente effectuée avec succès!")
                st.rerun()
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
            payment_amount = st.number_input("Montant du paiement", min_value=0.01, max_value=min(portfolio.cash, remaining_balance), step=0.01)
            st.info(f"Solde restant: {remaining_balance:.2f}€ | Liquidités disponibles: {portfolio.cash:.2f}€")
            
            if st.button("Payer"):
                if portfolio.pay_credit(credit_to_pay, payment_amount):
                    save_portfolio(portfolio)  # Sauvegarde automatique
                    st.success(f"Paiement de {payment_amount:.2f}€ effectué!")
                    st.rerun()
                else:
                    st.error("Impossible d'effectuer le paiement!")
        else:
            st.info("Aucun crédit à payer")

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
            width='stretch',
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