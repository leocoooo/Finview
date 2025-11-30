# Charger les variables d'environnement depuis .env
if [ -f .env ]; then
	set -a
	source .env
	set +a
fi
# ============================================================================
# Script de récupération des actualités financières via NewsAPI
# ============================================================================
# Ce script :
# 1. Récupère les actualités via l'API NewsAPI
# 2. Stocke la réponse JSON dans saved_json_data/news.json
# ============================================================================

set -e  # Arrêter à la première erreur

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Affichage d'en-tête
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Finview - Récupération des actualités financières        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Vérification de la clé API
if [ -z "$NEWS_API_KEY" ]; then
	echo -e "${RED}✗ La clé API NewsAPI n'est pas définie (variable NEWSAPI_KEY)${NC}"
	echo "Veuillez définir la variable d'environnement NEWSAPI_KEY."
	exit 1
fi

# Paramètres de la requête
CATEGORY="${1:-business}"
COUNTRY="${2:-us}"
PAGE_SIZE=10

# Construction de l'URL
BASE_URL="https://newsapi.org/v2/top-headlines"
URL="${BASE_URL}?category=${CATEGORY}&country=${COUNTRY}&pageSize=${PAGE_SIZE}&apiKey=${NEWS_API_KEY}"

# Récupération des actualités
echo -e "${YELLOW}Récupération des actualités...${NC}"
RESPONSE=$(curl -s "$URL")

# Vérification de la réponse
if [ -z "$RESPONSE" ]; then
	echo -e "${RED}✗ Aucune réponse reçue de l'API NewsAPI${NC}"
	exit 1
fi

# Vérification du statut dans la réponse JSON
STATUS=$(echo "$RESPONSE" | grep -o '"status":"[^"]*"' | cut -d':' -f2 | tr -d '"')
if [ "$STATUS" != "ok" ]; then
	MESSAGE=$(echo "$RESPONSE" | grep -o '"message":"[^"]*"' | cut -d':' -f2 | tr -d '"')
	echo -e "${RED}✗ Erreur API NewsAPI : $MESSAGE${NC}"
	exit 1
fi

# Création du dossier de sauvegarde si nécessaire
mkdir -p saved_json_data

# Sauvegarde de la réponse JSON
echo "$RESPONSE" > saved_json_data/news.json

echo -e "${GREEN}✓ Actualités sauvegardées dans saved_json_data/news.json${NC}"
echo -e "${BLUE}Prochaine étape :${NC}"
echo "Exécutez 'bash launch.sh' pour démarrer l'application Finview"
echo ""
echo ""
echo "La réponse à la vie est 42"
echo ""
