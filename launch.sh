#!/bin/bash

# ============================================================================
# Script de lancement pour Finview - Docker Launch
# ============================================================================
# Ce script :
# 1. Vérifie que les prérequis sont satisfaits
# 2. Démarre les conteneurs Docker avec Docker Compose
# 3. Affiche les instructions d'accès
# 4. Affiche les logs en temps réel
# ============================================================================

set -e  # Arrêter à la première erreur

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        Finview - Lancement de l'application Docker         ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ============================================================================
# Vérification de Docker
# ============================================================================
echo -e "${YELLOW}Vérification des prérequis...${NC}"

if ! docker ps &> /dev/null; then
    echo -e "${RED}✗ Docker n'est pas en cours d'exécution${NC}"
    echo "Veuillez démarrer Docker Desktop"
    exit 1
fi

if ! docker-compose --version &> /dev/null; then
    if ! docker compose version &> /dev/null; then
        echo -e "${RED}✗ Docker Compose n'est pas disponible${NC}"
        exit 1
    fi
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

echo -e "${GREEN}✓ Docker est opérationnel${NC}"
echo ""

# ============================================================================
# Démarrer les conteneurs
# ============================================================================
echo -e "${YELLOW}Démarrage de l'application Finview...${NC}"
echo ""

$DOCKER_COMPOSE up

# Note : Le script s'arrêtera ici et affichera les logs
# Pour arrêter l'application, appuyez sur Ctrl+C
# Les conteneurs continueront de tourner en arrière-plan si vous utilisez -d
