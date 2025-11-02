#!/bin/bash

echo "🚀 Installation de Finview..."
echo ""

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez installer Docker d'abord."
    echo "   Visitez: https://docs.docker.com/get-docker/"
    exit 1
fi

# Vérifier que Docker Compose est installé
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez installer Docker Compose d'abord."
    exit 1
fi

echo "✅ Docker et Docker Compose sont installés"
echo ""

# Vérifier si le fichier .env existe
if [ ! -f .env ]; then
    echo "⚠️  Le fichier .env n'existe pas."
    echo "📝 Création d'un fichier .env depuis .env.example..."
    
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Fichier .env créé. N'oubliez pas de configurer votre NEWS_API_KEY !"
        echo ""
    else
        echo "❌ .env.example n'existe pas. Création d'un .env minimal..."
        echo "NEWS_API_KEY=your_api_key_here" > .env
        echo "✅ Fichier .env créé. N'oubliez pas de configurer votre NEWS_API_KEY !"
        echo ""
    fi
fi

# Build de l'image Docker
echo "🔨 Construction de l'image Docker..."
docker-compose build

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Installation terminée avec succès !"
    echo ""
    echo "Pour lancer l'application, exécutez:"
    echo "  ./run.sh"
    echo ""
else
    echo ""
    echo "❌ Erreur lors de la construction de l'image Docker"
    exit 1
fi