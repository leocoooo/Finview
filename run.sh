#!/bin/bash

echo "🚀 Démarrage de Finview..."
echo ""

# Vérifier que Docker est en cours d'exécution
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker ne semble pas être en cours d'exécution."
    echo "   Veuillez démarrer Docker et réessayer."
    exit 1
fi

# Vérifier si le fichier .env existe
if [ ! -f .env ]; then
    echo "❌ Le fichier .env n'existe pas."
    echo "   Veuillez exécuter ./install.sh d'abord."
    exit 1
fi

# Vérifier si la clé API est configurée
if grep -q "your_api_key_here" .env; then
    echo "⚠️  ATTENTION: La clé API n'est pas configurée dans le fichier .env"
    echo "   L'application peut ne pas fonctionner correctement."
    echo ""
fi

# Arrêter les containers existants (si présents)
docker-compose down > /dev/null 2>&1

# Lancer l'application en arrière-plan
echo "🐳 Démarrage des containers Docker..."
docker-compose up -d

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Application démarrée avec succès !"
    echo ""
    echo "📱 Accédez à l'application sur: http://localhost:8501"
    echo ""
    echo "📊 Pour voir les logs:"
    echo "  docker-compose logs -f"
    echo ""
    echo "🛑 Pour arrêter l'application:"
    echo "  docker-compose down"
    echo ""
else
    echo ""
    echo "❌ Erreur lors du démarrage de l'application"
    exit 1
fi