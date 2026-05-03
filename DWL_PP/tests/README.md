# Tests Automatisés - Projet "Don't Watchlist"

Ce dossier contient l'ensemble de notre suite de tests automatisés. Afin de garantir la robustesse de notre application et de valider notre architecture, nous avons implémenté une stratégie de test sur trois niveaux : des tests unitaires isolés, des tests d'intégration avec la base de données, et des tests End-to-End simulant le parcours d'un véritable utilisateur.

---

## Structure du dossier

* **`test_unitaire.py`** : tests isolés des routes de l'API avec simulation (mocking) des dépendances
* **`test_integration.py`** : tests de bout en bout du backend, validant l'interaction entre l'API Flask et la base de données SQLAlchemy
* **`test_end_to_end.py`** : tests d'interface automatisés utilisant le navigateur Chromium via Playwright
* **`screenshots/`** : dossier généré automatiquement par Playwright contenant les captures d'écran des tests E2E

---

## Les tests

### 1. `test_unitaire.py`
Ces tests vérifient la logique interne de notre API Flask de manière totalement isolée. 
* **Méthode** : on utilise `monkeypatch` de Pytest pour mocker (simuler) les retours de la base de données (`repository.py`) et du modèle d'Intelligence Artificielle (`search_moteur.py`)
* **Avantage** : permet de tester rapidement toutes les conditions d'erreurs (400, 401, 403, 404, 409) sans avoir besoin de charger les modèles ni de dépendre d'un serveur MySQL

### 2. `test_integration.py`
Ces tests valident que notre ORM communique bien avec la base de données
* **Scénarios validés** : création d'un compte, connexion avec vérification de la session, ajout d'un film (Harry Potter) à la watchlist, modification de son état ("En Attente" vers "Abandon"), et suppression du film

### 3. `test_end_to_end.py`
On a utilisé Playwright pour simuler un utilisateur ouvrant un navigateur, cliquant sur les boutons et remplissant les formulaires
* **Scénarios validés** : 
  * Inscription d'un nouvel utilisateur ("Testeur1") depuis la page `Register.php` et connexion réussie
  * Recherche d'une phobie ("I am afraid of spiders") depuis la page `MoteurRecherche.php`, clic sur le premier résultat et vérification de l'ouverture avec le bon titre de film
* On sauvegarde le tout sous forme d'images dans le dossier `screenshots/`

---

## Jeu de données minimal de test

Pour garantir des tests fiables, reproductibles et indépendants de l'environnement nous avons choisi de générer notre jeu de données minimal dynamiquement en mémoire :

1. **Base de données isolée** : Lorsque la suite de tests est lancée, l'application détecte la variable d'environnement `TESTING = True`, le fichier `db.py` bascule alors automatiquement la connexion MySQL vers une base de données **SQLite in-memory** (`sqlite:///:memory:`)
2. **Création du schéma** : La fixture `client` de Pytest appelle `init_db()` avant chaque test pour générer un schéma SQL vierge et parfait
3. **Script d'import dynamique** : Au lieu d'utiliser un fichier `.sql` statique notre script `test_integration.py` donne lui-même le jeu de données minimal requis pour les tests via des requêtes API (ex: insertion de l'utilisateur "Testeur1" et du film "tt0295297")

Cette approche garantit que les tests peuvent être exécutés à l'infini sans jamais polluer la base de données de production.

---

## Lancement

Pour exécuter la suite de tests unitaires et d'intégration :
```bash
pytest test_unitaire.py test_integration.py -v
```