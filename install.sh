#!/bin/bash

# Script d'installation pour Finview - Docker Setup
# Ce script :
# - Vérifie que Docker Desktop est installé et en cours d'exécution
# - Vérifie que Docker Compose est disponible
# - Construit l'image Docker
# - Crée les répertoires nécessaires pour la persistance des données

set -e  # Arrêter à la première erreur

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Finview - Installation Docker Setup                     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Vérifier que Docker est installé
echo -e "${YELLOW}[1/4]${NC} Vérification de l'installation de Docker..."

if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker n'est pas installé ou n'est pas dans le PATH${NC}"
    echo "Veuillez installer Docker Desktop depuis : https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo -e "${GREEN}✓ Docker est installé${NC}"
echo "   Version : $(docker --version)"
echo ""

# Vérifier que Docker Desktop est en cours d'exécution
echo -e "${YELLOW}[2/4]${NC} Vérification que Docker est en cours d'exécution..."

if ! docker ps &> /dev/null; then
    echo -e "${RED}✗ Docker n'est pas en cours d'exécution${NC}"
    echo "Veuillez démarrer Docker Desktop"
    exit 1
fi

echo -e "${GREEN}✓ Docker est en cours d'exécution${NC}"
echo ""


# Vérifier que Docker Compose est disponible
echo -e "${YELLOW}[3/4]${NC} Vérification de Docker Compose..."

if ! docker-compose --version &> /dev/null; then
    if ! docker compose version &> /dev/null; then
        echo -e "${RED}✗ Docker Compose n'est pas disponible${NC}"
        exit 1
    fi
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

echo -e "${GREEN}✓ Docker Compose est disponible${NC}"
echo "   Commande : $DOCKER_COMPOSE"
echo ""

# Créer les répertoires nécessaires
echo -e "${YELLOW}[4/4]${NC} Création des répertoires de persistance..."

mkdir -p saved_json_data
mkdir -p reports
mkdir -p .streamlit

echo -e "${GREEN}✓ Répertoires créés :${NC}"
echo "   - saved_json_data/ (stockage des portfolios)"
echo "   - reports/ (rapports PDF générés)"
echo "   - .streamlit/ (configuration Streamlit)"
echo ""

# Construire l'image Docker
echo -e "${YELLOW}Construction de l'image Docker...${NC}"
echo "Cela peut prendre plusieurs minutes lors du premier lancement."
echo ""

$DOCKER_COMPOSE build

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║               ✓ Installation terminée avec succès           ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Prochaine étape :${NC}"
echo "Exécutez 'bash get_news.sh' pour récupérer les actualités financières !"
echo ""
