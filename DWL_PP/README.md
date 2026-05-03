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

Pour faire tourner le projet sur votre machine, veuillez suivre attentivement les étapes ci-dessous.

1. **Télécharger les données :** Le modèle d'IA a besoin de fichiers de données volumineux pour fonctionner. Comme ils sont ignorés par Git (.gitignore), vous devez les récupérer manuellement :
- Dans le dossier app, créez un dossier nommé data s'il n'existe pas déjà.
- Allez sur https://drive.google.com/drive/folders/19ti2-82yTjm8DlCH-d22emAAJSQcunXa?usp=sharing et téléchargez le dossier contenant ces trois fichiers exacts :

    - corpus.json (situé dans Dataset_Projet_TAL/collection_test/)
    - embeddings_films.pt (situé à la racine)
    - une video montrant toutes les fonctionnalités de notre projet

Glissez **UNIQUEMENT** le dossier data de telle sorte que l'arborescence ressemble exactement à ça :

```text
DWL_PP/
└── app/
    ├── data/
    │   ├── corpus.json
    │   └── embeddings_films.pt
    ├── app.py
    └── ...
```

2. **Lancer les conteneurs avec Docker** : Une fois les données en place, ouvrez un terminal à la racine du projet (DWL_PP) et lancez la commande suivante :

```bash
docker-compose up --build -d
```

3. **Accéder à l'application** : Une fois les conteneurs démarrés (le backend Python peut prendre quelques secondes pour charger le modèle PyTorch en mémoire), vous pouvez accéder à l'application via votre navigateur :

Site Web (Interface Utilisateur) : http://localhost:8000

## Arborescence du Projet

```text
DWL_PP/
├── app/                  # Backend Python (Flask, IA, CRUD)
├── siteweb/              # Frontend PHP (Interface, Proxy API, Assets)
├── tests/                # Suite de tests automatisés (Unitaires, Intégration, E2E)
├── docker-compose.yml    # Fichier d'orchestration Docker
├── .env.example          # Modèle pour les variables d'environnement secrètes
└── README.md             # Documentation globale (vous êtes ici)
```
