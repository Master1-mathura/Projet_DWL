# Backend API & Moteur de Recherche - Projet "Don't Watchlist"

Ce dossier `app` constitue le cœur de notre application. Développé en Python (Flask), il orchestre l'API REST, la persistance des données via un ORM, et intègre notre moteur de recherche sémantique basé sur l'IA. 

---

## Architecture
On a séparé les rôles :

* **Routage (`app.py`)** : Le contrôleur principal. Il gère la réception des requêtes HTTP, l'extraction des paramètres JSON, et le formatage des réponses
* **Data Access Object (`repository.py`)** : Cette couche encapsule toute la logique d'interaction avec la base de données. Le contrôleur Flask n'écrit jamais de logique métier ou de requêtes SQL directement.
* **Modélisation (`orm.py`)** : Définition des entités de la base de données sous forme de classes Python avec SQLAlchemy.
* **Configuration (`config.py` & `db.py`)** : Centralisation de la connexion à la base de données, avec une bascule entre l'environnement de production (MySQL) et l'environnement de test (SQLite in-memory)
* **Moteur IA (`search_moteur.py`)** : Isole la logique de traitement NLP (Sentence Transformers, calcul de similarité cosinus) et d'expansion de requêtes.

---

## Fonctionnalités et Opérations CRUD

L'API implémente un **CRUD complet** sur les différentes entités de l'application :

### 1. Entité Utilisateur (User)
* **Create** : Inscription sécurisée d'un nouvel utilisateur (`POST /compte`)
* **Read** : Authentification (`POST /connexion`)
* **Update** : Modification du profil (nom d'utilisateur, mot de passe) (`PUT /compte/<id>`)
* **Delete** : Suppression du compte utilisateur (`DELETE /compte/<id>`)

### 2. Entité Watchlist
* **Create** : Ajout d'un film avec métadonnées à la watchlist d'un utilisateur (`POST /watchlist`)
* **Read** : Récupération de tous les films d'un utilisateur (`GET /watchlist/<user_id>`)
* **Update** : Modification de l'état de visionnage d'un film (`PUT /watchlist/<user_id>/<imdbID>`)
* **Delete** : Retrait d'un film de la liste (`DELETE /watchlist/<user_id>/<imdbID>`)

---

## Persistance des Données & ORM

La persistance des données repose sur **SQLAlchemy**.

* **Modélisation des classes** : Les tables `users` et `watchlist` sont utilisées via `declarative_base()`.
* **Gestion des Relations (1-n)** : Une relation One-to-Many connecte les utilisateurs à leurs films dans la watchlist.
* **Intégrité Référentielle** : Des suppressions en cascade sont configurées pour maintenir l'intégrité de la base de données lors de la suppression de profils.
* **Résilience** : Lors du lancement en mode non-test, le backend effectue jusqu'à 10 tentatives de connexion à la base de données pour pallier les éventuels délais de démarrage du conteneur de base de données
* **Configuration des environnements** : L'environnement de test utilise une base de données SQLite en mémoire (`sqlite:///:memory:`) pour des exécutions rapides et isolées, tandis que l'environnement de production s'appuie sur MySQL

---

## Gestion des Erreurs et Exceptions
La gestion des erreurs garantit une API robuste et informative :
* **Gestionnaire Global** : L'utilisation de `@app.errorhandler(Exception)` permet de capturer les erreurs non gérées et de retourner des réponses JSON structurées avec un statut HTTP 500, évitant le plantage de l'application
* **Codes HTTP Sémantiques** : L'API retourne des codes de statut précis selon le contexte : 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), et 409 (Conflict)

---

## Conteneurisation et Déploiement

Le backend est conçu pour un déploiement via Docker :
* L'application utilise `python:3.11`.
* Les dépendances incluent Flask, SQLAlchemy, et Pytest pour les tests
* La configuration `db.py` s'adapte dynamiquement selon les variables d'environnement (`TESTING`, `DB_HOST`, etc.) pour faciliter les déploiements locaux et CI/CD