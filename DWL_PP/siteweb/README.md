# Interface Web (Frontend) - Projet "Don't Watchlist"

Ce dossier `siteweb` contient toute l'interface utilisateur de notre application. Développé en PHP, HTML, CSS et JavaScript, il agit comme le client direct de notre API Flask (backend). Il a été conçu pour offrir une expérience utilisateur fluide, immersive et asynchrone (architecture type Single Page Application sur certaines interactions).

---

## Architecture du Projet

Le code a été structuré en séparant les responsabilités afin de garder un code propre et maintenable :

* **`/` (Racine)** : Contient les contrôleurs principaux et les pages de rendu (`MoteurRecherche.php`, `DWL.php`, `Login.php`, `MyProfile.php`) qui orchestrent la logique de l'application.
* **`view/`** : Contient les templates d'affichage HTML/PHP pour séparer la logique PHP du rendu visuel (ex: `affichage_Search.php`).
* **`service/`** : Contient la logique de communication avec l'API backend (`MovieService.php`).
* **`config/`** : Centralise les variables globales de l'environnement (`configuration.php`).
* **`assets/`** : Regroupe les ressources statiques divisées en sous-dossiers (`css`, `images`, `js`).

---

## Le Moteur de Recherche (`MoteurRecherche.php`)

Cette page est le point d'entrée principal. Elle permet à l'utilisateur de soumettre sa requête sémantique ("*What are you afraid of ?*").

### 1. Affichage des résultats
Lorsqu'une recherche est effectuée, le PHP interroge le backend. Les résultats sont affichés sous forme de liste. Le code couleur de chaque résultat (Rouge, Orange, Vert) est calculé et transmis directement par l'API Python en fonction du score de pertinence, ce qui permet au frontend de se concentrer uniquement sur le rendu visuel.
Si le modèle d'Intelligence Artificielle est toujours en cours de chargement sur le serveur, une page d'attente interactive (intégrant un mini-jeu Dino) s'affiche avec un script de rafraîchissement automatique (`setInterval`).

### 2. Modale Interactive et Requêtes Asynchrones
Pour éviter de recharger la page à chaque interaction, nous avons implémenté une modale détaillée gérée par JavaScript (`script_moteur.js`) :
* **Récupération des détails :** Au clic sur un film, une requête `fetch` asynchrone est envoyée au fichier PHP local. Les métadonnées (titre, synopsis, affiche) sont ensuite injectées dynamiquement dans le DOM.
* **Jauge de Score :** Le score du film est converti en pourcentage et affiché via une jauge de progression animée (`rating-fill`). Sa couleur (vert, jaune ou rouge) s'adapte dynamiquement au résultat grâce à l'ajout de classes CSS spécifiques.
* **Ajout à la Watchlist Sécurisé :** Un formulaire asynchrone permet d'ajouter le film à la base de données. 
  * **Sécurité & Redirection :** Si l'utilisateur n'est pas connecté (statut "Unknown"), JavaScript bloque la requête et le redirige instantanément vers la page de connexion (`Login.php`).
  * **Notifications Fluides :** L'alerte JavaScript native bloquante a été remplacée par un système de notification "Toast" asynchrone (non-bloquant) avec un retour visuel élégant lors de l'ajout d'un film.

---

## Système d'Authentification et Profil

L'application intègre un système complet de gestion de session utilisateur via PHP (`$_SESSION`).

### 1. Inscription et Connexion (`Login.php` & `Register.php`)
* **Sécurité :** Les utilisateurs peuvent créer un compte et se connecter. Les formulaires communiquent avec l'API Flask via `MovieService.php` pour valider et enregistrer les identifiants en base de données.
* **Redirection :** Si un utilisateur non connecté tente d'accéder à son profil ou à ses paramètres, il est automatiquement redirigé vers la page de connexion.

### 2. Le Tableau de Bord Utilisateur (`MyProfile.php`)
* **Statistiques :** Affiche un résumé de l'activité, comme le nombre total de films dans la Watchlist, ainsi que le nombre de films "Survécu" et "Abandon" calculés dynamiquement.
* **Paramètres d'Apparence (Settings UI) :** L'utilisateur peut personnaliser son interface en basculant entre le "Dark Mode" et le "Light Mode". Il peut également activer ou désactiver un effet de flou ("Blur Effect") sur les affiches de films. Ces préférences sont sauvegardées en base de données et appliquées au DOM de chaque page.
* **Gamification (Badges) :** Un système de succès récompense l'engagement de l'utilisateur. Les badges sont débloqués dynamiquement en JavaScript en fonction des statistiques de l'utilisateur (ex: nombre de films ajoutés ou survécus). Lorsqu'un badge est débloqué, une requête asynchrone (`fetch`) l'enregistre en base de données. Une modale interactive permet de consulter les détails et l'état de chaque badge.

### 3. Paramètres du Compte (`Settings.php`)
* **Mise à jour des informations :** L'utilisateur peut modifier son nom d'utilisateur et son mot de passe (en fournissant l'ancien mot de passe pour des raisons de sécurité).
* **Suppression de compte sécurisée :** Un bouton permet la suppression définitive du compte. Pour éviter les erreurs de manipulation, cette action déclenche un "Overlay" de confirmation plein écran avec un compte à rebours de 5 secondes avant l'envoi définitif de la requête de suppression.
  
---

## La "Don't Watchlist" (`DWL.php`)

Cette page est l'espace personnel de l'utilisateur. Elle affiche les films qu'il a sauvegardés. L'accès à cette page est strictement protégé par session (redirection automatique vers le login si non connecté).

### 1. Navigation
* Les affiches des films sont présentées dans un **carrousel horizontal fluide** situé dans la partie inférieure droite de l'écran. 
* **Arrière-plan Dynamique (`#bg-layer`) :** Lorsqu'un film est sélectionné dans le carrousel, JavaScript extrait l'URL du fond (`data-bg`) et met à jour dynamiquement l'image de fond de toute la page.
* **Chargement Asynchrone du Synopsis :** Pour éviter de surcharger la page initiale avec des textes très longs, seul le synopsis du film sélectionné est chargé en temps réel via une requête `fetch` asynchrone vers le proxy PHP.

### 3. Gestion d'État des Films (CRUD Frontend)
La partie gauche de l'écran centralise les actions disponibles pour le film actif :
* **Mise à jour du statut (`update`) :** L'utilisateur peut modifier l'état de son visionnage via un menu déroulant (`select`) : *Waiting* (En Attente), *Survived* (Survécu), ou *Dropped* (Abandon). La soumission met à jour l'entrée en base de données via une requête HTTP PUT interceptée par PHP.
* **Suppression (`delete`) :** Un bouton rouge permet d'éjecter instantanément le film de la base de données de l'utilisateur.

---

## La Watchlist (`DWL.php`)

Cette page affiche les films sauvegardés par l'utilisateur dans une interface très visuelle, inspirée des plateformes de streaming modernes.

### 1. Carrousel de Navigation
Les films sont affichés via un carrousel horizontal. L'utilisateur peut naviguer en cliquant sur les flèches ou directement sur les affiches.

### 2. Arrière-plan Dynamique
Une fonctionnalité clé de l'immersion est la gestion de l'arrière-plan. Lorsqu'un film est sélectionné dans le carrousel, JavaScript intercepte l'événement et met à jour dynamiquement le `background-image` de la page avec l'image de fond (backdrop) récupérée via TMDB, le tout couplé à une transition CSS fluide.

### 3. Gestion des films
Directement depuis l'interface, l'utilisateur peut interagir avec le film sélectionné :
* **Mise à jour de l'état :** Modification du statut ("En Attente", "Survécu", "Abandon"). Le frontend envoie une requête HTTP PUT.
* **Suppression :** Retrait définitif via une requête HTTP DELETE.

---

## Communication avec l'API (`MovieService.php`)

Pour des raisons de sécurité et d'architecture, le client (navigateur) ne communique jamais directement avec le backend Python ou la base de données **TiDB Cloud**.

* **Proxy PHP :** C'est la classe `MovieService` qui se charge d'effectuer toutes les requêtes HTTP (GET, POST, PUT, DELETE) vers notre API interne (`http://application:4000`) en utilisant `file_get_contents` et les contextes de flux.
* **Avantages :** 
  * Masque l'adresse, le port réels de l'API et la logique IA aux utilisateurs finaux.
  * Centralise la gestion des endpoints pour la recherche, la Watchlist, et la gestion des comptes.
---

## UI/UX & Design System

L'ensemble de l'application suit une charte graphique cohérente avec des variables CSS globales.
* **Thématisation :** L'interface bascule du mode sombre au mode clair en appliquant la classe `.theme-light` au `<body>`, géré par les préférences du profil.
* **Responsive Design :** Interfaces optimisées pour mobile avec adaptation des grilles et des "Touch Targets".
* **Pop-ups et Feedback :** Utilisation de bannières de notification dynamiques (`popup-success`, `popup-error`) pour informer l'utilisateur des succès ou échecs lors des modifications de profil.