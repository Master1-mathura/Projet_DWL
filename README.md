# Projet "Don't Watchlist" : De l'Algorithme à l'Application Full-Stack

Bienvenue sur le dépôt principal du projet **"Don't Watchlist"**. 

Ce dépôt illustre l'évolution complète d'un projet étudiant : la transformation d'un moteur d'Intelligence Artificielle expérimental en une véritable application web Full-Stack, interactive, gamifiée et déployable. 

L'idée originale ? Proposer un moteur de recherche inversé basé sur les peurs des utilisateurs. Si vous tapez *"I am afraid of snakes"*, le système analyse sémantiquement les scripts de films pour vous recommander les œuvres à **absolument éviter**.

---

## Navigation dans le dépôt

Ce dépôt est scindé en deux grandes parties correspondant à la genèse et à la finalisation du projet. **Pour explorer l'application web finale, rendez-vous dans `DWL_PP`**.

### 1. [DWL_PP](./DWL_PP) : L'Application Web (Branche Principale)
C'est l'aboutissement du projet. Nous avons extrait le cœur de notre moteur IA pour l'intégrer dans une architecture orientée microservices :
* **Backend (`app/`)** : API REST en Python (Flask) gérant le modèle PyTorch, la logique métier et l'ORM SQLAlchemy.
* **Frontend (`siteweb/`)** : Interface immersive (PHP/JS/CSS) agissant comme un proxy sécurisé, avec requêtes asynchrones, thèmes dynamiques et animations.
* **Base de Données Cloud** : Persistance des données (Watchlist, Profils, Badges) sur **TiDB Serverless** sécurisée via SSL.
* **Déploiement** : L'ensemble est conteneurisé et orchestré via **Docker** (`docker-compose.yml`).

### 2. [DWL_TAL](./DWL_TAL) : La Recherche et l'Algorithmique (Archives)
Ce dossier contient nos travaux de recherche initiaux en Traitement Automatique des Langues (TAL). Il retrace la création du moteur de recherche.
* Implémentation et comparaison de deux modèles : Vectoriel Classique (TF-IDF enrichi via WordNet) vs Deep Learning (Embeddings avec SentenceTransformers).
* Implémentation de techniques d'amélioration comme le Pseudo-Relevance Feedback (PRF).
* Scripts d'évaluation scientifique (Rappel, MAP, nDCG).