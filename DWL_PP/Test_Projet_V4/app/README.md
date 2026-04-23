# Backend API & Moteur de Recherche - Projet "Don't Watchlist"

Ce dossier `app` contient le cœur algorithmique et le serveur backend de notre projet. Développé en Python, il expose une API REST via Flask et orchestre la communication entre le frontend, notre moteur de recherche sémantique basé sur l'Intelligence Artificielle, l'API externe TMDB et notre base de données MySQL.

---

## Architecture du Dossier

L'architecture a été pensée de manière modulaire, séparant clairement les responsabilités (routage, logique métier, accès aux données) :

* **`app.py`** : Le point d'entrée de l'API Flask. Il gère les routes, les requêtes entrantes, et communique avec le moteur de recherche et la base de données.
* **`search_moteur.py`** : Le cœur de notre Intelligence Artificielle. Il contient toute la logique de Traitement Automatique des Langues (TAL) pour la recherche sémantique.
* **`config.py`**, **`db.py`**, **`repository.py`** : La couche d'accès aux données (DAO). Gestion de la connexion MySQL et exécution des requêtes SQL.
* **`donnees.sql`** : Le script d'initialisation de notre base de données.
* **`Dockerfile` & `requirements.txt`** : Les fichiers nécessaires à la conteneurisation et au déploiement de l'application.

---

## Moteur de Recherche Sémantique (`search_moteur.py`)

Nous avons conçu un moteur de recherche capable de comprendre le contexte des requêtes utilisateurs (recherche vectorielle) en utilisant `sentence-transformers` et `torch`. 

Le processus complet comprend plusieurs étapes clés :

### 1. Prétraitement des Données
Lors de l'initialisation, le système lit le corpus de scripts (`corpus.json`). Il isole le texte pertinent en parsant spécifiquement les balises `<scene_description>`. Ce texte est ensuite découpé en morceaux (chunks) de 200 mots avec un chevauchement de 50 mots pour conserver le contexte d'une phrase à l'autre.

### 2. Encodage (Embeddings)
Nous utilisons le modèle pré-entraîné `all-MiniLM-L6-v2` pour transformer ces morceaux de texte en vecteurs mathématiques (embeddings). Pour optimiser les temps de démarrage ultérieurs, ces tenseurs PyTorch sont sauvegardés localement dans `data/embeddings_films.pt`.

### 3. Calcul de Similarité
Lorsqu'un utilisateur effectue une recherche, sa requête est vectorisée. Nous calculons ensuite la similarité cosinus entre la requête et les morceaux de films.
Le score final d'un film est une combinaison équilibrée (50/50) entre la moyenne de ses meilleurs morceaux (top 5) et son score maximum absolu.

### 4. Pseudo-Relevance Feedback (PRF)
Pour accroître la précision, nous avons implémenté un système de PRF. Le moteur effectue une première passe, isole les résultats les plus pertinents, extrait leur vecteur moyen, et l'ajoute à la requête initiale (avec un poids alpha de 0.7) pour effectuer une seconde recherche affinée.

---

## Endpoints de l'API REST (`app.py`)

L'application Flask (tournant sur le port `4000`) expose les routes suivantes pour le frontend :

| Route | Méthode | Rôle & Traitement effectué |
| :--- | :---: | :--- |
| `/` | `GET` | Route de vérification renvoyant un message de bienvenue. |
| `/search` | `GET` | Reçoit la requête utilisateur (`?q=...`). Interroge le moteur de recherche et renvoie les 5 meilleurs films. **Traitement visuel :** Le backend attribue dynamiquement un code couleur (rouge `#9b2c3b`, orange `#b87322`, vert `#2e7d52`) selon le score de pertinence. |
| `/movies/<imdbID>` | `GET` | Reçoit un identifiant IMDB, effectue une requête vers l'API TMDB, et reformate les données pour renvoyer un objet JSON propre (titre, synopsis, poster, background, note globale). |
| `/watchlist` | `GET` | Interroge la base de données et renvoie tous les films enregistrés. |
| `/watchlist` | `POST` | Reçoit les métadonnées d'un film depuis le front et l'ajoute à la base de données via le repository. |

---

## Persistance des Données

La gestion de la base de données MySQL est centralisée et sécurisée :

* **Structure (`donnees.sql`)** : Une table `watchlist` stockant l'ID, le nom du film, les liens vers les images (poster et background) et l'état de visionnage (défini par défaut sur "En Attente" lors de l'insertion).
* **Variables d'environnement (`config.py`)** : Les identifiants de connexion s'adaptent automatiquement à l'environnement (récupération des variables `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` définies par Docker, avec une valeur de repli pour le développement local).
* **Repository Pattern (`repository.py`)** : Les fonctions `get_all()` et `add_movies()` encapsulent les requêtes SQL, séparant ainsi la logique base de données des contrôleurs Flask.

---

## Déploiement et Conteneurisation (`Dockerfile`)

Afin de garantir un environnement de production stable, l'application backend est dockerisée :

1.  **Image de base** : Utilisation de `python:3.11`.
2.  **Optimisation IA** : Installation spécifique de `torch` en version CPU (`--extra-index-url https://download.pytorch.org/whl/cpu`) afin de réduire drastiquement le poids de l'image (pas de bibliothèques CUDA inutiles pour notre déploiement).
3.  **Dépendances** : Installation des paquets via `requirements.txt` (Flask, pandas, sentence-transformers, mysql-connector-python, etc.).
4.  **Exposition** : L'API est servie sur le port `4000` via la commande `python app.py`.