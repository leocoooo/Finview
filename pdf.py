from fpdf import FPDF
import plotly.express as px
import os
from portfolio_package.patrimoine_prediction import simulate_portfolio_future, create_prediction_chart, create_statistics_summary

# Fonction pour convertir hex en RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Couleurs thème
background_color = hex_to_rgb("#1d293d")  # fond page
text_color = hex_to_rgb("#e2e8f0")        # texte général
border_color = hex_to_rgb("#314158")      # bordures
header_bg_color = hex_to_rgb("#1d293d")   # fond header tableau

def generate_portfolio_pdf(portfolio, filename="portfolio.pdf", logo_path="logo/FullLogo.png"):
    pdf = FPDF()

    # === PAGE DE GARDE ===
    pdf.add_page()

    # Fond page de garde
    pdf.set_fill_color(*background_color)
    pdf.rect(0, 0, pdf.w, pdf.h, 'F')

    # Chemin absolu du logo
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_logo_path = os.path.join(script_dir, logo_path)

    # Logo centre verticalement
    if os.path.exists(full_logo_path):
        # Centrer le logo (largeur 80mm, hauteur proportionnelle)
        logo_width = 80
        logo_x = (pdf.w - logo_width) / 2
        logo_y = 70  # Position verticale
        pdf.image(full_logo_path, x=logo_x, y=logo_y, w=logo_width)

    # Titre FINVIEW centre sous le logo
    pdf.set_y(130)
    pdf.set_font("Arial", 'B', 32)
    pdf.set_text_color(*text_color)
    pdf.cell(0, 15, "FINVIEW", ln=True, align="C")

    # Ligne de separation
    pdf.ln(10)
    pdf.set_draw_color(*text_color)
    pdf.set_line_width(0.3)
    line_margin = 60
    pdf.line(line_margin, pdf.get_y(), pdf.w - line_margin, pdf.get_y())

    # Noms des auteurs centres
    pdf.ln(15)
    pdf.set_font("Arial", '', 14)
    pdf.set_text_color(*text_color)
    pdf.cell(0, 8, "Antonin BENARD", ln=True, align="C")
    pdf.cell(0, 8, "Leo COLIN", ln=True, align="C")
    pdf.cell(0, 8, "Pierre QUINTIN de KERCADIO", ln=True, align="C")

    # === PAGE 1: Performance du Portefeuille ===
    pdf.add_page()

    # Fond page
    pdf.set_fill_color(*background_color)
    pdf.rect(0, 0, pdf.w, pdf.h, 'F')

    # Logo en haut à gauche
    if os.path.exists(full_logo_path):
        pdf.image(full_logo_path, x=5, y=5, w=50)

    # Titre centré
    pdf.ln(15)  # espace pour le logo
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(*text_color)
    pdf.cell(0, 10, "Performance du Portefeuille", ln=True, align="C")
    pdf.ln(5)

    # Ligne de séparation blanche
    pdf.set_draw_color(*text_color)
    pdf.set_line_width(0.5)
    pdf.line(20, pdf.get_y(), pdf.w - 20, pdf.get_y())
    pdf.ln(10)

    # Opinion de l'investissement (texte propre)
    if portfolio.investments:
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(*text_color)
        pdf.cell(0, 10, "Analyse du Portefeuille", ln=True)
        pdf.ln(5)

        # Calculer les statistiques
        num_investments = len(portfolio.investments)
        financial_total = portfolio.get_financial_investments_value()
        real_estate_total = portfolio.get_real_estate_investments_value()
        total_value = financial_total + real_estate_total
        annual_rental = portfolio.get_total_annual_rental_income()

        # Pourcentages de répartition
        if total_value > 0:
            financial_pct = (financial_total / total_value) * 100
            real_estate_pct = (real_estate_total / total_value) * 100
        else:
            financial_pct = real_estate_pct = 0

        # Niveau de diversification
        if num_investments >= 8:
            diversification = "Elevee"
        elif num_investments >= 5:
            diversification = "Moyenne"
        else:
            diversification = "Faible"

        # Texte de l'analyse
        pdf.set_font("Arial", '', 12)
        pdf.set_text_color(*text_color)

        # Texte de synthèse patrimoniale
        synthese_text = (
            f"Votre patrimoine genere un revenu locatif annuel de {annual_rental:.2f} EUR, "
            f"soit environ {annual_rental/12:.2f} EUR par mois. "
            f"Votre portefeuille presente une diversification {diversification.lower()} "
            f"avec {num_investments} investissements repartis entre "
            f"{financial_pct:.0f}% d'actifs financiers et {real_estate_pct:.0f}% d'immobilier."
        )

        pdf.multi_cell(0, 8, synthese_text)
        pdf.ln(5)
    else:
        pdf.set_text_color(*text_color)
        pdf.cell(0, 10, "Aucun investissement", ln=True)

    # Ajouter historique des transactions
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(*text_color)
    pdf.cell(0, 10, "Historique des transactions", ln=True)
    pdf.ln(5)

    if portfolio.transaction_history:
        pdf.set_draw_color(*border_color)
        pdf.set_fill_color(*header_bg_color)
        pdf.set_font("Arial", 'B', 10)

        # Header historique
        pdf.cell(45, 10, "Date", border=1, fill=True)
        pdf.cell(50, 10, "Type", border=1, fill=True)
        pdf.cell(30, 10, "Montant", border=1, fill=True)
        pdf.cell(65, 10, "Description", border=1, fill=True)
        pdf.ln()

        # Contenu historique (dernières 10 transactions)
        pdf.set_font("Arial", '', 9)
        last_transactions = portfolio.transaction_history[-10:]
        for transaction in last_transactions:
            # Remplacer caractères spéciaux non supportés
            description = transaction['description'][:30]
            description = description.replace('€', 'EUR').replace('→', '->')
            pdf.cell(45, 8, transaction['date'], border=1)
            pdf.cell(50, 8, transaction['type'], border=1)
            pdf.cell(30, 8, f"{transaction['amount']:.2f} EUR", border=1)
            pdf.cell(65, 8, description, border=1)
            pdf.ln()

        # Analyse des dernières actions
        pdf.ln(5)
        pdf.set_font("Arial", '', 11)
        pdf.set_text_color(*text_color)

        # Compter les types de transactions récentes
        recent_buys = sum(1 for t in last_transactions if 'BUY' in t['type'])
        recent_sells = sum(1 for t in last_transactions if 'SELL' in t['type'])
        recent_updates = sum(1 for t in last_transactions if 'UPDATE' in t['type'])

        # Générer le texte d'analyse
        if recent_buys > 0:
            analysis_text = f"Vos dernieres operations montrent {recent_buys} achat(s) d'actifs, "
        else:
            analysis_text = "Aucun achat recent d'actifs. "

        if recent_updates > 0:
            analysis_text += f"{recent_updates} mise(s) a jour de valeur, "

        if recent_sells > 0:
            analysis_text += f"et {recent_sells} vente(s). "
        else:
            analysis_text += "sans vente recente. "

        analysis_text += f"Au total, {len(last_transactions)} transactions ont ete enregistrees dans cette periode."

        pdf.multi_cell(0, 6, analysis_text)
    else:
        pdf.set_text_color(*text_color)
        pdf.cell(0, 10, "Aucune transaction", ln=True)

    # === PAGE 2: Graphiques des investissements ===
    if portfolio.investments:
        pdf.add_page()

        # Fond page 2 (même couleur que page 1)
        pdf.set_fill_color(*background_color)
        pdf.rect(0, 0, pdf.w, pdf.h, 'F')

        # Logo en haut à gauche (page 2)
        if os.path.exists(full_logo_path):
            pdf.image(full_logo_path, x=5, y=5, w=50)

        # Titre page 2
        pdf.ln(15)  # espace pour le logo
        pdf.set_font("Arial", 'B', 16)
        pdf.set_text_color(*text_color)
        pdf.cell(0, 10, "Repartition des Investissements", ln=True, align="C")
        pdf.ln(5)

        # Ligne de séparation blanche
        pdf.set_draw_color(*text_color)
        pdf.set_line_width(0.5)
        pdf.line(20, pdf.get_y(), pdf.w - 20, pdf.get_y())
        pdf.ln(10)

        # Graphique en cercle (pie chart) avec couleurs personnalisées
        labels = [name for name in portfolio.investments]
        values = [inv.get_total_value() for inv in portfolio.investments.values()]

        # Couleurs variées pour les actifs
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
                  '#ec4899', '#14b8a6', '#f97316', '#06b6d4', '#84cc16']

        fig = px.pie(values=values, names=labels, title="Repartition par actif",
                     color_discrete_sequence=colors)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12)
        )
        fig.write_image("graphique_pie.png")
        pdf.image("graphique_pie.png", x=10, y=pdf.get_y(), w=180)

        pdf.ln(120)  # Espace après le graphique

        # Détail par investissement
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(*text_color)
        pdf.cell(0, 10, "Detail par actif", ln=True)
        pdf.ln(5)

        # Tableau détaillé
        pdf.set_draw_color(*border_color)
        pdf.set_fill_color(*header_bg_color)
        pdf.set_font("Arial", 'B', 10)

        pdf.cell(60, 10, "Actif", border=1, fill=True)
        pdf.cell(40, 10, "Valeur totale", border=1, fill=True)
        pdf.cell(45, 10, "% du portefeuille", border=1, fill=True)
        pdf.cell(45, 10, "Performance", border=1, fill=True)
        pdf.ln()

        # Calculer valeur totale du portefeuille
        total_portfolio = sum(inv.get_total_value() for inv in portfolio.investments.values())

        # Contenu
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

    # === PAGE 3: Prédictions du patrimoine ===
    pdf.add_page()

    # Fond page 3
    pdf.set_fill_color(*background_color)
    pdf.rect(0, 0, pdf.w, pdf.h, 'F')

    # Logo en haut à gauche (page 3)
    if os.path.exists(full_logo_path):
        pdf.image(full_logo_path, x=5, y=5, w=50)

    # Titre page 3
    pdf.ln(15)  # espace pour le logo
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(*text_color)
    pdf.cell(0, 10, "Predictions du Patrimoine", ln=True, align="C")
    pdf.ln(5)

    # Ligne de séparation blanche
    pdf.set_draw_color(*text_color)
    pdf.set_line_width(0.5)
    pdf.line(20, pdf.get_y(), pdf.w - 20, pdf.get_y())
    pdf.ln(10)

    # Générer les prédictions si le portefeuille contient des investissements
    if portfolio.investments:
        # Générer la simulation
        try:
            prediction_results = simulate_portfolio_future(portfolio, years=10, num_simulations=1000)
            stats = create_statistics_summary(prediction_results)

            # Graphique de prédiction
            fig = create_prediction_chart(prediction_results)
            fig.write_image("prediction_chart.png", width=800, height=400)
            pdf.image("prediction_chart.png", x=10, y=pdf.get_y(), w=190)
            pdf.ln(110)

            # Statistiques clés
            pdf.set_font("Arial", 'B', 13)
            pdf.set_text_color(*text_color)
            pdf.cell(0, 8, "Scenarios de prevision sur 10 ans", ln=True)
            pdf.ln(3)

            # Tableau des scénarios
            pdf.set_draw_color(*border_color)
            pdf.set_fill_color(*header_bg_color)
            pdf.set_font("Arial", 'B', 9)

            pdf.cell(55, 8, "Scenario", border=1, fill=True)
            pdf.cell(45, 8, "Valeur finale", border=1, fill=True)
            pdf.cell(45, 8, "Gain/Perte", border=1, fill=True)
            pdf.cell(45, 8, "Rdt annualise", border=1, fill=True)
            pdf.ln()

            # Contenu des scénarios
            pdf.set_font("Arial", '', 9)
            scenarios = [
                ("Tres optimiste (P90)", stats['final']['p90'], stats['gains']['p90'], stats['returns']['p90']),
                ("Optimiste (P75)", stats['final']['p75'], stats['gains']['p75'], stats['returns']['p75']),
                ("Mediane (P50)", stats['final']['p50'], stats['gains']['p50'], stats['returns']['p50']),
                ("Prudent (P25)", stats['final']['p25'], stats['gains']['p25'], stats['returns']['p25']),
                ("Pessimiste (P10)", stats['final']['p10'], stats['gains']['p10'], stats['returns']['p10'])
            ]

            for scenario_name, final_val, gain, return_pct in scenarios:
                pdf.cell(55, 7, scenario_name, border=1)
                pdf.cell(45, 7, f"{final_val:.0f} EUR", border=1)
                pdf.cell(45, 7, f"{gain:+.0f} EUR", border=1)
                pdf.cell(45, 7, f"{return_pct:+.1f}%/an", border=1)
                pdf.ln()

            pdf.ln(5)

            # Note d'avertissement
            pdf.set_font("Arial", 'I', 9)
            pdf.set_text_color(*text_color)
            avertissement = (
                "Ces predictions sont basees sur des simulations Monte Carlo utilisant des rendements "
                "historiques moyens. Les resultats reels peuvent varier considerablement en fonction "
                "de nombreux facteurs imprevus (crises economiques, innovations, changements reglementaires, etc.). "
                "Cette simulation ne constitue pas un conseil en investissement."
            )
            pdf.multi_cell(0, 5, avertissement)

            # Nettoyer le fichier temporaire
            try:
                os.remove("prediction_chart.png")
            except:
                pass

        except Exception as e:
            pdf.set_font("Arial", '', 11)
            pdf.set_text_color(*text_color)
            pdf.multi_cell(0, 6, f"Impossible de generer les predictions: {str(e)}")
    else:
        pdf.set_font("Arial", '', 11)
        pdf.set_text_color(*text_color)
        pdf.multi_cell(0, 6, "Aucun investissement pour generer des predictions.")

    # === PAGE 4: Conseils d'investissement ===
    pdf.add_page()

    # Fond page 4
    pdf.set_fill_color(*background_color)
    pdf.rect(0, 0, pdf.w, pdf.h, 'F')

    # Logo en haut à gauche (page 4)
    if os.path.exists(full_logo_path):
        pdf.image(full_logo_path, x=5, y=5, w=50)

    # Titre page 4
    pdf.ln(15)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(*text_color)
    pdf.cell(0, 10, "Conseils d'Investissement", ln=True, align="C")
    pdf.ln(5)

    # Ligne de séparation blanche
    pdf.set_draw_color(*text_color)
    pdf.set_line_width(0.5)
    pdf.line(20, pdf.get_y(), pdf.w - 20, pdf.get_y())
    pdf.ln(10)

    # Analyser le portefeuille pour donner des conseils personnalisés
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

        # Conseil 1: Diversification
        pdf.set_font("Arial", 'B', 13)
        pdf.set_text_color(*text_color)
        pdf.cell(0, 8, "1. Diversification du portefeuille", ln=True)
        pdf.ln(3)
        pdf.set_font("Arial", '', 11)

        if num_investments < 5:
            conseil1 = (
                "Votre portefeuille pourrait beneficier d'une meilleure diversification. "
                "Il est recommande d'avoir au moins 5 a 8 actifs differents pour reduire les risques. "
                "Envisagez d'ajouter des investissements dans differents secteurs et zones geographiques."
            )
        elif num_investments < 8:
            conseil1 = (
                "Votre diversification est correcte. Pour optimiser davantage, "
                "vous pourriez ajouter quelques actifs supplementaires dans des secteurs complementaires."
            )
        else:
            conseil1 = (
                "Excellente diversification ! Votre portefeuille est bien reparti. "
                "Continuez a maintenir cet equilibre tout en surveillant la correlation entre vos actifs."
            )

        pdf.multi_cell(0, 6, conseil1)
        pdf.ln(5)

        # Conseil 2: Repartition actifs
        pdf.set_font("Arial", 'B', 13)
        pdf.cell(0, 8, "2. Equilibre financier / immobilier", ln=True)
        pdf.ln(3)
        pdf.set_font("Arial", '', 11)

        if real_estate_pct < 10:
            conseil2 = (
                "Votre exposition immobiliere est faible. L'immobilier peut offrir "
                "une stabilite et des revenus recurrents interessants. Envisagez d'augmenter "
                "cette part a 15-30% pour un meilleur equilibre."
            )
        elif real_estate_pct > 50:
            conseil2 = (
                "Votre portefeuille est fortement concentre sur l'immobilier. "
                "Il serait prudent de renforcer votre exposition aux actifs financiers "
                "pour une meilleure liquidite et flexibilite."
            )
        else:
            conseil2 = (
                "Votre repartition entre actifs financiers et immobiliers est equilibree. "
                "Cette diversification vous offre un bon compromis entre croissance et stabilite."
            )

        pdf.multi_cell(0, 6, conseil2)
        pdf.ln(5)

        # Conseil 3: Gestion des risques
        pdf.set_font("Arial", 'B', 13)
        pdf.cell(0, 8, "3. Gestion des risques", ln=True)
        pdf.ln(3)
        pdf.set_font("Arial", '', 11)

        conseil3 = (
            "Verifiez regulierement vos investissements et reequilibrez votre portefeuille "
            "si necessaire. Gardez une reserve de liquidites (3-6 mois de depenses) "
            "pour faire face aux imprevus sans avoir a vendre vos actifs en urgence."
        )

        pdf.multi_cell(0, 6, conseil3)
        pdf.ln(5)

        # Conseil 4: Horizon d'investissement
        pdf.set_font("Arial", 'B', 13)
        pdf.cell(0, 8, "4. Vision long terme", ln=True)
        pdf.ln(3)
        pdf.set_font("Arial", '', 11)

        conseil4 = (
            "Les meilleurs rendements s'obtiennent sur le long terme (5-10 ans minimum). "
            "Evitez les decisions impulsives basees sur les fluctuations court terme. "
            "Investissez regulierement pour beneficier de l'effet de moyenne d'achat."
        )

        pdf.multi_cell(0, 6, conseil4)
        pdf.ln(5)

        # Note finale
        pdf.set_font("Arial", 'I', 10)
        pdf.set_text_color(*text_color)
        note_finale = (
            "Note: Ces conseils sont indicatifs et bases sur l'analyse de votre portefeuille actuel. "
            "Pour des recommandations personnalisees, consultez un conseiller financier professionnel."
        )
        pdf.multi_cell(0, 5, note_finale)

    pdf.output(filename)
    return filename
