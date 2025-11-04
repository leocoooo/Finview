FROM python:3.13-slim

WORKDIR /app

# Installer curl ET chromium pour Plotly/Kaleido
RUN apt-get update && \
    apt-get install -y curl chromium && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_SYSTEM_PYTHON=1

# Copier les fichiers nécessaires pour le build
COPY pyproject.toml uv.lock* README.md ./
COPY src/ ./src/               

# Maintenant uv sync peut builder ton package
RUN uv sync --no-dev --frozen

# Copier le reste
COPY . .

# Exposer le port
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Lancer
CMD ["uv", "run", "streamlit", "run", "main.py", "--server.address", "0.0.0.0"]