# Interface Web (Frontend) - Projet "Don't Watchlist"

Ce dossier `siteweb` contient toute l'interface utilisateur de notre application. Développé en PHP, HTML, CSS et JavaScript, il agit comme le client direct de notre API Flask (backend). Il a été conçu pour offrir une expérience utilisateur fluide, immersive et asynchrone (architecture type Single Page Application sur certaines interactions).

---

## Architecture du Projet

Le code a été structuré en séparant les responsabilités (inspiré du modèle MVC) afin de garder un code propre et maintenable :

* **`/` (Racine)** : Contient les contrôleurs principaux (`MoteurRecherche.php` et `DWL.php`) qui orchestrent la logique de la page.
* **`view/`** : Contient les templates d'affichage HTML/PHP (`affichage_Search.php` et `affichage_DWL.php`).
* **`service/`** : Contient la logique de communication avec l'API backend (`MovieService.php`).
* **`config/`** : Centralise les variables globales de l'environnement (`configuration.php`).
* **`assets/`** : Regroupe les ressources statiques divisées en sous-dossiers (`css`, `images`, `js`).

---

## Le Moteur de Recherche (`MoteurRecherche.php`)

Cette page est le point d'entrée principal. Elle permet à l'utilisateur de soumettre sa requête sémantique ("*What are you afraid of ?*").

### 1. Affichage des résultats
Lorsqu'une recherche est effectuée, le PHP interroge le backend. Les résultats sont affichés sous forme de liste. Le code couleur de chaque résultat (Rouge, Orange, Vert) est calculé et transmis directement par l'API Python en fonction du score de pertinence, ce qui permet au frontend de se concentrer uniquement sur le rendu visuel.

### 2. Modale Interactive et Requêtes Asynchrones
Pour éviter de recharger la page à chaque interaction, nous avons implémenté une modale détaillée gérée par JavaScript (`script.js`) :
* **Récupération des détails :** Au clic sur un film, une requête `fetch` asynchrone est envoyée au fichier PHP local, qui agit comme un proxy vers l'API TMDB/Flask. Les métadonnées (titre, synopsis, affiche) sont ensuite injectées dynamiquement dans le DOM.
* **Jauge de Score Animée :** Le score du film est converti en pourcentage et affiché via une jauge de progression animée (`rating-fill`). Sa couleur (vert, jaune ou rouge) s'adapte dynamiquement au résultat grâce à l'ajout de classes CSS spécifiques.
* **Ajout à la Watchlist :** Un formulaire asynchrone permet d'ajouter le film à la base de données sans quitter la page de recherche.

---

## La Watchlist (`DWL.php`)

Cette page affiche les films sauvegardés par l'utilisateur dans une interface très visuelle, inspirée des plateformes de streaming modernes.

### 1. Carrousel de Navigation
Les films sont affichés via un carrousel horizontal. L'utilisateur peut naviguer en cliquant sur les flèches ou directement sur les affiches.

### 2. Arrière-plan Dynamique
Une fonctionnalité clé de l'immersion est la gestion de l'arrière-plan. Lorsqu'un film est sélectionné dans le carrousel, JavaScript intercepte l'événement et met à jour dynamiquement le `background-image` de la page avec l'image de fond (backdrop) récupérée via TMDB, le tout couplé à une transition CSS fluide.

### 3. Gestion des films
Directement depuis l'interface de la Watchlist, l'utilisateur peut interagir avec le film sélectionné :

- Mise à jour de l'état : L'utilisateur peut modifier le statut de visionnage d'un film via un menu déroulant ("En Attente", "Survécu", "Abandon"). Le frontend envoie alors une requête HTTP PUT via le proxy PHP.

- Suppression : L'utilisateur peut retirer définitivement un film de sa liste, ce qui déclenche une requête HTTP DELETE.

---

## Communication avec l'API (`MovieService.php`)

Pour des raisons de sécurité et d'architecture, le client (navigateur) ne communique jamais directement avec le backend Python ou la base de données.

* **Proxy PHP :** C'est la classe `MovieService` qui se charge d'effectuer les requêtes HTTP vers notre API interne (`http://application:4000`) en utilisant `file_get_contents` et les contextes de flux (`stream_context_create` pour les requêtes POST).
* **Avantages :** Cela nous évite les problèmes de CORS (Cross-Origin Resource Sharing) dans le navigateur, masque l'adresse et le port réels de l'API IA aux utilisateurs finaux, et centralise la gestion des endpoints.

---

## UI/UX & Design System

L'ensemble de l'application suit une charte graphique cohérente basée sur un thème sombre (nuances de violet et de noir : `#3f2257`, `#0f0a18`).

* **CSS Custom Properties :** L'utilisation de variables CSS (ex: `--primary-color`, `--transition`) dans `search.css` et `DWL.css` nous a permis d'unifier les couleurs et les animations sur l'ensemble du site.
* **Composants modernes :** Effets de glassmorphism sur les modales (utilisation de `backdrop-filter: blur`), ombres portées dynamiques (`box-shadow`), et respect des principes du responsive design (Flexbox) pour s'assurer que l'interface s'adapte aux différentes tailles d'écran, notamment pour la modale de détails.