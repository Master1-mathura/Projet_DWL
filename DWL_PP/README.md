# Projet "Don't Watchlist" - Moteur de Recherche Sémantique

Il s'agit d'une application web complète (Full-Stack) qui intègre un moteur de recherche basé sur le Traitement Automatique des Langues. L'utilisateur peut y rechercher des films en décrivant ses peurs, visualiser les détails via l'API TMDB, et gérer sa propre liste de films à surmonter (Watchlist).
*Par exemple, si l'utilisateur a peur des araignées, le sytème lui renvoie les films qu'il doit à tout prix éviter, mais si au vu du score d'un film, l'utilisateur considère que le film vaut la peine de surmonter sa phobie des araignées, il peut l'ajouter dans sa Watchlist.*

---

## Architecture Globale

Le projet est divisé en deux grandes parties, orchestrées par **Docker Compose** pour faciliter le déploiement. L'architecture repose sur 3 conteneurs communicants :

1. **Le Backend (`app/`)** : Une API Flask en Python qui embarque notre modèle d'IA (PyTorch / SentenceTransformers) pour la recherche sémantique. *(Exposé sur le port 4000)*.
2. **Le Frontend (`siteweb/`)** : Une interface utilisateur dynamique en PHP, HTML, CSS et JavaScript, qui agit comme client de notre API. *(Exposé sur le port 8000)*.
3. **La Base de Données (`db`)** : Un conteneur MySQL 8.0 qui stocke la Watchlist des utilisateurs de manière persistante (via des volumes Docker).

**Note :** Chaque sous-dossier (`app/` et `siteweb/`) contient son propre README détaillé si vous souhaitez comprendre en profondeur le fonctionnement du code.

---

## Arborescence du Projet

```text
DWL_PP/
├── app/                  # Backend Python (Flask, IA, Scripts de recherche)
├── siteweb/              # Frontend PHP (Vues, Styles, Scripts JS)
├── docker-compose.yml    # Fichier d'orchestration des conteneurs
└── README.md             # Documentation globale (ce fichier)
```

## Guide d'Installation et de Lancement

Pour faire tourner le projet sur votre machine, veuillez suivre attentivement les étapes ci-dessous.

1. Préparer le dossier de données (Fichiers lourds ignorés par Git)
Le modèle d'IA a besoin de fichiers de données volumineux pour fonctionner. Comme ils sont ignorés par Git (.gitignore), vous devez les récupérer manuellement.

Dans le dossier app, créez un dossier nommé data s'il n'existe pas déjà.

Allez sur https://drive.google.com/drive/folders/19ti2-82yTjm8DlCH-d22emAAJSQcunXa?usp=sharing et téléchargez le dossier contenant ces deux fichiers exacts :

- corpus.json (situé dans Dataset_Projet_TAL/collection_test/)
- embeddings_films.pt (situé à la racine)

Glissez ce dossier data de telle sorte que l'arborescence ressemble exactement à ça :

```text
DWL_PP/
└── app/
    ├── data/
    │   ├── corpus.json
    │   └── embeddings_films.pt
    ├── app.py
    └── ...
```

1. Lancer les conteneurs avec Docker
Une fois les données en place, ouvrez un terminal à la racine du projet (DWL_PP) et lancez la commande suivante :

```bash
docker-compose up --build -d
```

Le flag --build force la reconstruction des images (utile lors de la première installation) et -d lance les conteneurs en arrière-plan.

3. Accéder à l'application
Une fois les conteneurs démarrés (le backend Python peut prendre quelques secondes pour charger le modèle PyTorch en mémoire), vous pouvez accéder à l'application via votre navigateur :

- Site Web (Interface Utilisateur) : http://localhost:8000
- API Backend (Vérification) : http://localhost:4000

## Commandes Utiles
Arrêter le projet : docker-compose down

Arrêter et supprimer les données de la base (Reset de la Watchlist) : docker-compose down -v

Voir les logs du backend (pour déboguer l'IA) : docker-compose logs -f application