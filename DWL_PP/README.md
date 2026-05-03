# Projet "Don't Watchlist" - Moteur de Recherche Sémantique

Il s'agit d'une application web complète (Full-Stack) qui intègre un moteur de recherche basé sur le Traitement Automatique des Langues. L'utilisateur peut y rechercher des films en décrivant ses peurs, visualiser les détails via l'API TMDB, et gérer sa propre liste de films à surmonter (Watchlist) au sein d'une interface immersive et gamifiée..

---

## Architecture Globale

Le projet est divisé en trois grands modules indépendants et orchestrés par **Docker** :

1. **Le Backend (`app/`)** : Une API REST développée en Python (Flask). Elle embarque notre modèle d'IA sémantique (PyTorch / SentenceTransformers) et gère la persistance des données via l'ORM SQLAlchemy.
2. **Le Frontend (`siteweb/`)** : Une interface utilisateur dynamique en PHP, HTML, CSS et JavaScript. Elle agit comme client sécurisé de notre API (via un proxy PHP) et propose une expérience fluide (requêtes asynchrones, thèmes dynamiques, gamification).
3. **La Base de Données (Cloud)** : L'application est connectée à une base de données MySQL hébergée dans le cloud sur **TiDB Serverless**, garantissant haute disponibilité et sécurité (SSL/TLS).

***Note : Chaque sous-dossier contient son propre fichier `README.md` détaillant son fonctionnement technique approfondi.***

---

## Guide d'Installation et de Lancement

Le déploiement de l'application a été simplifié pour les utilisateurs finaux. Nos images Docker pré-compilées (embarquant déjà l'environnement, le code et l'IA) sont disponibles publiquement sur [Docker Hub](https://hub.docker.com/repository/docker/vidur28/dwl-frontend/).

Pour faire tourner le projet sur votre machine, veuillez suivre attentivement les étapes ci-dessous. Vous n'avez besoin que de deux fichiers.

### 1. Le fichier `.env`

**[IMPORTANT] Il est crucial de noter que sans les clés d'accès, vous n'aurez pas accès à l'application !**

Dans un dossier vide sur votre machine, créez un fichier `.env` et insérez-y les clés d'accès (fournies séparément pour des raisons de sécurité) :
```env
DB_PASSWORD=votre_mot_de_passe_tidb
HF_TOKEN=votre_token_hugging_face
```
### 2. Le fichier docker-compose.yml
Dans ce même dossier, créez un fichier docker-compose.yml avec la configuration suivante :

```yaml
services:
  application:
    image: vidur28/dwl-backend:latest
    platform: linux/amd64
    ports:
      - 4000:4000
    environment:
      DB_HOST: "gateway01.eu-central-1.prod.aws.tidbcloud.com"
      DB_USER: "2wBLzwP8VbUog4z.root"
      DB_PASSWORD: ${DB_PASSWORD}
      HF_TOKEN: ${HF_TOKEN}
      DB_NAME: "test" 
      DB_PORT: "4000"

  pageweb:
    image: vidur28/dwl-frontend:latest
    platform: linux/amd64
    ports:
      - 8000:80
    depends_on:
      - application
```

*Note : L'attribut platform: linux/amd64 permet d'assurer la compatibilité sur les Mac équipés de puces Apple Silicon ARM.*

### 3. Lancer les conteneurs avec Docker
Ouvrez un terminal dans ce dossier et lancez la commande suivante. Docker se chargera de tout télécharger et de démarrer l'infrastructure en arrière-plan :
```bash
docker compose up --build -d
```
### 4. Accéder à l'application
Une fois les conteneurs démarrés, vous pouvez accéder à l'application via votre navigateur : Site Web (Interface Utilisateur) : http://localhost:8000/MoteurRecherche.php

## Arborescence du Projet
```txt
DWL_PP/
├── app/                  # Backend Python (Flask, IA, CRUD)
├── siteweb/              # Frontend PHP (Interface, Proxy API, Assets)
├── tests/                # Suite de tests automatisés (Unitaires, Intégration, E2E)
├── docker-compose.yml    # Fichier d'orchestration Docker
├── .env.example          # Modèle pour les variables d'environnement secrètes
└── README.md             # Documentation globale (vous êtes ici)
```