# Stage 1 : Image de base avec Python 3.13
FROM python:3.13-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Installer les dépendances système nécessaires pour Streamlit et Kaleido
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de configuration du projet
COPY pyproject.toml poetry.lock* ./

# Installer Poetry
RUN pip install --no-cache-dir poetry==1.7.1

# Installer les dépendances du projet via Poetry
# --no-interaction : ne pas poser de questions
# --no-dev : ne pas installer les dépendances de développement
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-dev

# Copier tout le code du projet
COPY . .

# Créer les répertoires nécessaires
RUN mkdir -p /app/saved_json_data /app/reports

# Exposer le port utilisé par Streamlit (8501 par défaut)
EXPOSE 8501

# Configuration de Streamlit pour fonctionner correctement en conteneur
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_LOGGER_LEVEL=info

# Commande par défaut : lancer Streamlit
CMD ["streamlit", "run", "main.py"]
