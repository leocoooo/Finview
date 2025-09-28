from fpdf import FPDF
import plotly.express as px

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
    pdf.add_page()

    # Fond page
    pdf.set_fill_color(*background_color)
    pdf.rect(0, 0, pdf.w, pdf.h, 'F')

    # Logo en haut à gauche
    pdf.image(logo_path, x=5, y=5, w=50)  # x=10mm, y=8mm, largeur=30mm

    # Titre centré
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(*text_color)
    pdf.cell(0, 10, "Performance du Portefeuille", ln=True, align="C")
    pdf.ln(15)  # espace après le titre pour ne pas chevaucher le logo

    # Préparer le tableau des investissements
    if portfolio.investments:
        pdf.set_draw_color(*border_color)       # couleur des bordures
        pdf.set_fill_color(*header_bg_color)   # fond entête
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(*text_color)
        
        # Header
        pdf.cell(50, 10, "Nom", border=1, fill=True)
        pdf.cell(30, 10, "Qté", border=1, fill=True)
        pdf.cell(40, 10, "Valeur unitaire", border=1, fill=True)
        pdf.cell(40, 10, "Valeur totale", border=1, fill=True)
        pdf.cell(30, 10, "Performance", border=1, fill=True)
        pdf.ln()

        # Contenu tableau
        pdf.set_font("Arial", '', 12)
        for name, inv in portfolio.investments.items():
            pdf.cell(50, 10, name, border=1)
            pdf.cell(30, 10, str(inv.quantity), border=1)
            pdf.cell(40, 10, f"{inv.current_value:.2f} EUR", border=1)
            pdf.cell(40, 10, f"{inv.get_total_value():.2f} EUR", border=1)
            pdf.cell(30, 10, f"{inv.get_gain_loss_percentage():+.1f}%", border=1)
            pdf.ln()
    else:
        pdf.set_text_color(*text_color)
        pdf.cell(0, 10, "Aucun investissement", ln=True)

    # Ajouter graphique
    if portfolio.investments:
        labels = [name for name in portfolio.investments]
        values = [inv.get_total_value() for inv in portfolio.investments.values()]
        fig = px.pie(values=values, names=labels, title="Répartition des investissements")
        fig.write_image("graphique.png")  # nécessite kaleido installé
        pdf.image("graphique.png", x=10, y=pdf.get_y()+10, w=180)

    pdf.output(filename)
    return filename
