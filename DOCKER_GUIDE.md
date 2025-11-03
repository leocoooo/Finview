# Guide Dockerisation de Finview

## 📚 Table des matières

1. [Qu'est-ce que Docker ?](#quest-ce-que-docker--)
2. [Pourquoi dockeriser votre application ?](#pourquoi-dockeriser-votre-application-)
3. [Structure des fichiers créés](#structure-des-fichiers-créés)
4. [Explications détaillées](#explications-détaillées)
5. [Utilisation pas à pas](#utilisation-pas-à-pas)
6. [Commandes utiles](#commandes-utiles)
7. [Dépannage](#dépannage)

---

## Qu'est-ce que Docker ?

**Docker** est une technologie de **containerisation** qui empaquette votre application et ses dépendances dans une boîte hermétique appelée **conteneur**.

### Analogie utile 🚢

Imaginez Docker comme des **conteneurs de cargo** :
- **Sans Docker** : Vous envoyez votre application à quelqu'un d'autre, et ils doivent installer individuellement tous les outils (Python 3.13, Streamlit, Pandas, etc.). C'est compliqué et ça casse souvent.
- **Avec Docker** : Vous envoyez un **conteneur scellé** avec TOUT à l'intérieur. Peu importe où on l'ouvre, tout fonctionne identiquement.

### Avantages de Docker 🎯

| Avantage | Explication |
|----------|-----------|
| **Portabilité** | Votre app fonctionne de la même façon sur Windows, Mac, Linux, Cloud, etc. |
| **Reproducibilité** | Chaque développeur, chaque machine exécute exactement la même version |
| **Isolation** | Docker isole votre app des autres, évite les conflits de dépendances |
| **Facilité de déploiement** | Une seule commande pour déployer partout |
| **Scalabilité** | Facile de créer plusieurs instances de votre app |

---

## Pourquoi dockeriser votre application ?

Pour votre cours DevOps et votre exigence "Mon application doit tourner sur n'importe quelle machine" :

✅ **Docker résout ce problème** : Il garantit que votre app Finview tournera identiquement sur n'importe quel ordinateur.

### Sans Docker
```
Machine A (Windows)         Machine B (Linux)        Machine C (Mac)
Installation manuelle  →    Installation manuelle  →  Installation manuelle
↓                           ↓                         ↓
Conflits de versions   ✗    Python 3.12 au lieu 3.13  Package manquant
"Ça marche chez moi"   ✗    "Ça marche pas chez toi"  Dépendances cassées
```

### Avec Docker
```
Dockerfile + docker-compose.yml
↓
Une seule image Docker = UNE SEULE FAÇON d'exécuter l'app
↓
Machine A ✓        Machine B ✓        Machine C ✓        Cloud ✓
Identique         Identique          Identique          Identique
```

---

## Structure des fichiers créés

Voici ce qui a été créé dans votre projet :

```
Finview/
├── Dockerfile                # ← Comment construire l'image Docker
├── docker-compose.yml        # ← Configuration pour lancer l'app
├── install.sh               # ← Script d'installation (setup initial)
├── launch.sh                # ← Script de lancement (démarrer l'app)
├── .dockerignore            # ← Fichiers à exclure de l'image
└── DOCKER_GUIDE.md          # ← Ce guide!
```

---

## Explications détaillées

### 1️⃣ Dockerfile - "La recette de construction"

**Chemin** : `Dockerfile`

**Rôle** : Définit comment construire l'image Docker étape par étape.

```dockerfile
FROM python:3.13-slim
```
**Pourquoi** : Commence avec une image de base contenant Python 3.13. On utilise `slim` (léger) pour réduire la taille.

```dockerfile
WORKDIR /app
```
**Pourquoi** : Définit `/app` comme répertoire de travail. Tous les fichiers seront dans `/app` à l'intérieur du conteneur.

```dockerfile
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    ca-certificates
```
**Pourquoi** : Installe les dépendances système que Streamlit et Kaleido (export d'images) nécessitent.

```dockerfile
COPY pyproject.toml poetry.lock* ./
```
**Pourquoi** : Copie vos fichiers de configuration Poetry. Poetry gère vos dépendances Python.

```dockerfile
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-dev
```
**Pourquoi** : Installe toutes les dépendances de votre `pyproject.toml` (pandas, streamlit, plotly, etc.).

```dockerfile
COPY . .
```
**Pourquoi** : Copie tout le code de votre projet dans le conteneur.

```dockerfile
EXPOSE 8501
```
**Pourquoi** : Déclare que le conteneur écoute sur le port 8501 (port par défaut de Streamlit).

```dockerfile
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0
```
**Pourquoi** : Configure Streamlit pour fonctionner correctement en conteneur.

```dockerfile
CMD ["streamlit", "run", "main.py"]
```
**Pourquoi** : Commande par défaut = lancer Streamlit avec votre `main.py`.

---

### 2️⃣ docker-compose.yml - "L'orchestrateur de services"

**Chemin** : `docker-compose.yml`

**Rôle** : Définit comment exécuter les conteneurs Docker.

```yaml
version: '3.8'
```
**Pourquoi** : Spécifie la version de Docker Compose.

```yaml
services:
  finview:
    build:
      context: .
      dockerfile: Dockerfile
```
**Pourquoi** : Définit un service appelé `finview` et comment le construire (en utilisant le Dockerfile).

```yaml
ports:
  - "8501:8501"
```
**Pourquoi** : Mappe le port 8501 du conteneur au port 8501 de votre machine hôte.
- Côté gauche (8501) = port de votre machine
- Côté droit (8501) = port du conteneur

```yaml
volumes:
  - ./saved_json_data:/app/saved_json_data
  - ./reports:/app/reports
```
**Pourquoi** : Crée des **volumes persistants**. Les fichiers sauvegardés dans le conteneur restent accessibles sur votre machine:
- `./saved_json_data` = vos fichiers d'accueil sur votre machine
- `/app/saved_json_data` = chemin dans le conteneur
- Les données **survivent** à l'arrêt du conteneur

```yaml
environment:
  - STREAMLIT_SERVER_HEADLESS=true
```
**Pourquoi** : Variables d'environnement pour configurer Streamlit en mode headless (sans interface graphique).

```yaml
restart: unless-stopped
```
**Pourquoi** : Le conteneur redémarre automatiquement s'il s'arrête (crash, erreur, etc.), SAUF si vous l'arrêtez volontairement.

---

### 3️⃣ install.sh - "Script d'installation"

**Chemin** : `install.sh`

**Rôle** : Prépare votre environnement Docker et construit l'image.

**Ce qu'il fait** :

```bash
# 1. Vérifie que Docker est installé
if ! command -v docker &> /dev/null; then
    echo "Docker n'est pas installé"
fi
```
**Pourquoi** : S'assure que Docker Desktop est bien installé sur votre machine.

```bash
# 2. Vérifie que Docker est en cours d'exécution
if ! docker ps &> /dev/null; then
    echo "Docker n'est pas en cours d'exécution"
fi
```
**Pourquoi** : Docker Desktop doit être lancé. Si ce n'est pas le cas, ça affiche un message d'erreur.

```bash
# 3. Crée les répertoires
mkdir -p saved_json_data
mkdir -p reports
```
**Pourquoi** : Prépare les dossiers où les fichiers seront sauvegardés (portfolios JSON, rapports PDF).

```bash
# 4. Construit l'image
docker-compose build
```
**Pourquoi** : Construit l'image Docker en suivant les instructions du Dockerfile. Cette étape télécharge Python 3.13, installe toutes les dépendances, copie votre code, etc.

**Première exécution** : Peut prendre **5-10 minutes** (télécharges 500 MB de fichiers).

**Exécutions suivantes** : Beaucoup plus rapide (utilise le cache).

---

### 4️⃣ launch.sh - "Script de lancement"

**Chemin** : `launch.sh`

**Rôle** : Démarre votre application dans Docker.

```bash
# Vérifie que Docker est en cours d'exécution
if ! docker ps &> /dev/null; then
    echo "Docker n'est pas en cours d'exécution"
fi
```
**Pourquoi** : Assure que Docker Desktop a été lancé.

```bash
# Démarre les conteneurs
docker-compose up
```
**Pourquoi** : Lance le conteneur défini dans `docker-compose.yml`:
- Crée le conteneur s'il n'existe pas
- Démarre Streamlit
- Affiche les logs en temps réel
- Vous pouvez appuyer sur `Ctrl+C` pour arrêter

---

### 5️⃣ .dockerignore - "Fichiers à ignorer"

**Chemin** : `.dockerignore`

**Rôle** : Liste les fichiers/dossiers à NE PAS inclure dans l'image Docker.

```
__pycache__/
*.pyc
.git/
.env
```

**Pourquoi** : 
- `__pycache__/` : Fichiers compilés Python (inutiles en Docker)
- `.git/` : Historique Git (inutile dans l'image)
- `.env` : Fichier de configuration local (utiliser des variables d'environnement)

**Résultat** : L'image Docker est plus petite et se construit plus rapidement.

---

## Utilisation pas à pas

### Première utilisation : Installation

#### Sur Windows avec Git Bash ou PowerShell :

```bash
# 1. Ouvrez un terminal dans le dossier du projet
cd C:\Users\leoco\Documents\cours\M2_MOSEF\devops\Finview

# 2. Lancez le script d'installation
bash install.sh
```

**Ce qui se passe** :
1. ✓ Docker Desktop est vérifié
2. ✓ Les répertoires sont créés
3. ⏳ L'image Docker est construite (patience!)
4. ✓ Done!

**Temps estimé** : 5-10 minutes la première fois

### Lancer l'application

```bash
# Dans le même dossier
bash launch.sh
```

**Ce qui se passe** :
1. Docker vérifie les prérequis
2. Le conteneur démarre
3. Streamlit lance votre application
4. Vous voyez :
   ```
   Collecting usage statistics. ...
     You can now view your Streamlit app in your browser.
     URL: http://localhost:8501
   ```

**Accéder à l'app** :
- Ouvrez votre navigateur
- Allez à `http://localhost:8501`
- Finview apparaît!

### Arrêter l'application

Dans le terminal où `launch.sh` s'exécute :

```bash
# Appuyez sur Ctrl+C
```

Le conteneur s'arrête proprement.

---

## Commandes utiles

### Vérifier que Docker fonctionne

```bash
docker ps
```
**Affiche** : Les conteneurs en cours d'exécution.

### Voir tous les conteneurs (actifs et arrêtés)

```bash
docker ps -a
```

### Voir les logs du conteneur

```bash
docker-compose logs
```

### Voir les logs en temps réel

```bash
docker-compose logs -f
```

### Arrêter tous les conteneurs

```bash
docker-compose stop
```

### Redémarrer les conteneurs

```bash
docker-compose restart
```

### Reconstruire l'image après modification du Dockerfile

```bash
docker-compose build --no-cache
```

### Supprimer l'image (libère de l'espace disque)

```bash
docker image rm finview_finview
```
(Remplacez le nom par celui donné par `docker images`)

### Voir la taille de l'image

```bash
docker images
```

---

## Dépannage

### ❌ "Docker n'est pas installé"

**Solution** :
1. Téléchargez Docker Desktop : https://www.docker.com/products/docker-desktop
2. Installez et redémarrez votre ordinateur
3. Lancez `bash install.sh` à nouveau

### ❌ "Docker n'est pas en cours d'exécution"

**Solution** :
1. Ouvrez Docker Desktop (cherchez l'icône Docker dans le menu Démarrer)
2. Attendez qu'il démarre complètement (icône Docker dans la barre d'état système)
3. Lancez `bash launch.sh` à nouveau

### ❌ "Port 8501 déjà utilisé"

**Cause** : Une autre instance de Finview tournait déjà sur le port 8501.

**Solutions** :
```bash
# Option 1 : Arrêtez tous les conteneurs
docker-compose stop

# Option 2 : Utilisez un port différent (modifiez docker-compose.yml)
# Changez "8501:8501" en "8502:8501"
# Accédez alors à http://localhost:8502
```

### ❌ "Permission denied" (sur Mac/Linux)

**Solution** : Donnez les permissions au script :
```bash
chmod +x install.sh launch.sh
```

### ❌ La construction échoue (erreur pendant `install.sh`)

**Causes possibles** :
1. Pas assez d'espace disque (Docker a besoin de 2-3 GB)
2. Connexion Internet instable
3. Firewall bloquant Docker

**Solutions** :
```bash
# Nettoyez les vieux fichiers Docker
docker system prune -a

# Reconstruisez
docker-compose build --no-cache
```

### ❌ Les fichiers sauvegardés disparaissent après arrêt du conteneur

**Vérifiez** que les volumes sont configurés dans `docker-compose.yml`:

```yaml
volumes:
  - ./saved_json_data:/app/saved_json_data
```

Si vous avez supprimé l'image, les données persisten tant dans `./saved_json_data/` sur votre machine.

### ❌ Streamlit dit "Port cannot be used"

```bash
# Trouvez le processus utilisant le port
lsof -i :8501  # Mac/Linux

# Tuez le processus
kill -9 <PID>

# Ou utilisez un port différent dans docker-compose.yml
```

---

## Architecture finale

Voici comment tout fonctionne ensemble :

```
┌─────────────────────────────────────────────────────────────┐
│                       Votre Machine                          │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │                   Docker Desktop                        │ │
│ │  ┌──────────────────────────────────────────────────┐  │ │
│ │  │         Conteneur Finview                        │  │ │
│ │  │  ┌────────────────────────────────────────────┐  │  │ │
│ │  │  │ Python 3.13 + Streamlit + Pandas + Plotly │  │  │ │
│ │  │  │ /app/main.py                              │  │  │ │
│ │  │  │ Port interne: 8501                        │  │  │ │
│ │  │  └────────────────────────────────────────────┘  │  │ │
│ │  └──────────────────────────────────────────────────┘  │ │
│ │         ↑                              ↑                 │ │
│ │    Port: 8501 ←────────────────→ localhost:8501         │ │
│ │         ↑                              ↑                 │ │
│ └─────────────────────────────────────────────────────────┘ │
│         ↓ (Volumes montés)                                   │
│    ./saved_json_data ←────────→ /app/saved_json_data        │
│         ./reports ←────────────→ /app/reports               │
└─────────────────────────────────────────────────────────────┘
                          ↓
                    Navigateur Web
               http://localhost:8501
                          ↓
                      Finview App
```

---

## Points clés à retenir 🎓

| Concept | Explication |
|---------|-----------|
| **Image Docker** | "Template" (recette) pour créer un conteneur |
| **Conteneur** | Instance en cours d'exécution de l'image |
| **Dockerfile** | Fichier définissant comment construire l'image |
| **docker-compose.yml** | Fichier définissant comment exécuter les conteneurs |
| **Volume** | Dossier partagé entre votre machine et le conteneur |
| **Port** | Communication entre votre machine et le conteneur |

---

## Résumé pour votre cours DevOps ✅

**Votre exigence** : "Mon application doit tourner sur n'importe quelle machine"

**Solution Docker** :
1. ✅ Utilisateur A (Windows) : `bash install.sh` → `bash launch.sh` → App fonctionne
2. ✅ Utilisateur B (Linux) : `bash install.sh` → `bash launch.sh` → App fonctionne
3. ✅ Utilisateur C (Mac) : `bash install.sh` → `bash launch.sh` → App fonctionne
4. ✅ Serveur Cloud : `bash install.sh` → `bash launch.sh` → App fonctionne

**Deux commandes comme demandé** :
- `bash install.sh` : Installation initiale
- `bash launch.sh` : Lancement de l'application

---

## Besoin d'aide ?

Consultez la documentation officielle :
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Streamlit Docker Guide](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker)

Bonne chance avec votre projet Finview! 🚀
