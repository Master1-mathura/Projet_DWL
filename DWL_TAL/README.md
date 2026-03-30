# Projet - Don't Watch List, TAL : Moteur de Recherche.

## Description du Projet
Ce projet a été réalisé dans le cadre d'un module de **Traitement Automatique des Langues (TAL)**. 
L'objectif est de développer un moteur de recherche basé sur les peurs et phobies des utilisateurs. Si un utilisateur tape une requête comme *"I am afraid of snakes"*, le système analyse les scripts de films pour lui recommander les films à **absolument éviter**.

Pour cela, nous avons implémenté, comparé et évalué deux approches de recherche d'information textuelle :
1. Une approche classique basée sur le modèle vectoriel **TF-IDF**.
2. Une approche Deep Learning basée sur les **Embeddings** (Sentence Transformers).

## Datasets

Les données du projet étant trop volumineuses pour GitHub, elles sont hébergées sur Google Drive. Pour exécuter le code et reproduire les résultats, veuillez suivre ces étapes :

1. Téléchargez l'archive en cliquant sur ce lien : https://drive.google.com/drive/folders/19ti2-82yTjm8DlCH-d22emAAJSQcunXa?usp=sharing.
2. Placez les dossiers extraits dans le répertoire `DWL_TAL/Dataset_Projet_TAL/`.

L'arborescence finale est comme suit :
```text
└── [Dossier Racine]/
    ├── README.md                  <-- Vous êtes ici
    ├── embeddings_films.pt        <-- Sauvegarde des tenseurs (créé par projet_emb.py)
    ├── evaluation_emb.py          <-- Script d'évaluation du modèle Embeddings
    ├── evaluation_tfidf.py        <-- Script d'évaluation du modèle TF-IDF
    ├── projet_emb.py              <-- Moteur de recherche interactif via Embeddings
    ├── projet_tfidf.py            <-- Moteur de recherche interactif via TF-IDF
    └── Dataset_Projet_TAL/
        ├── generer_collection.py  
        ├── collection_test/       <-- Partagé via Drive
        │   ├── corpus.csv
        │   ├── corpus.json
        │   ├── qrels.csv
        │   └── queries.json
        ├── raw/                   <-- Partagé via Drive
        │   ├── metadata_updated.json
        │   └── tags.json
        └── scores/                <-- Partagé via Drive
            └── tagdl.csv
```

Une fois ces dossiers en place, vous pourrez exécuter les différents scripts Python (projet_tfidf.py, projet_emb.py, ou les scripts d'évaluation) normalement.
Note : Vous n'aurez pas besoin d'exécuter generer_collection.py car le dossier collection_test est déjà transmis via le Drive. Les scripts trouveront les données au bon endroit !

## Pipeline de Prétraitement des Données
Le corpus est constitué de scripts de films au format JSON. Pour maximiser la pertinence de la recherche, nous appliquons un pipeline de prétraitement rigoureux :
1. Extraction des scènes : Le texte est parsé pour ne conserver que les actions contenues entre les balises <scene_description>.
2. Enrichissement Sémantique (**WordNet**) : Pour capter tout le champ lexical d'une phobie (ex: mygale, toile, veuve noire), nous utilisons la base de données WordNet. Nous extrayons les synsets et hyponymes des peurs ciblées pour injecter des **"tokens virtuels"** dans le texte (ex: THEME_VIOLENCE, THEME_ARACHNID)
3. Nettoyage Linguistique :
        - **Suppression des Stopwords**.
        - **Lemmatisation** : Réduction des mots à leur forme canonique.
        - **POS Tagging** : Filtrage morphosyntaxique pour exclure le "bruit" comme les noms propre(NNP, NNPS) ou les verbes modaux (MD), afin de se concentrer sur le sens de l'action.

## Modèles de Recherche

### Modèle Vectoriel Classique : TF-IDF
Ce modèle repose sur la création d'un index inversé à partir du vocabulaire filtré.
    - **Scoring** : Calcul des poids Term Frequency-Inverse Document Frequency pour chaque mot du corpus
    - **Recherche** : La requête utilisateur subit le même prétraitement, puis nous calculons la similarité cosinus entre le vecteur de la requête et les vecteurs des films pour extraire les pires correspondances.

### Modèle Deep Learning : Embeddings (MiniLM)
Pour dépasser les limites de correspondances exactes du TF-IDF, nous utilisons le modèle de langage `all-MiniLM-L6-v2` via la librairie **SentenceTransformers**.
    - **Gestion des longs textes (Chunking)** : Les modèles de type Transformer ayant une limite de tokens, les scripts sont découpés en morceaux (chunks) de 200 mots avec un chevauchement de 50 mots pour ne pas perdre le contexte.
    - **Scoring Spécifique** : Le score de dangerosité d'un film n'est pas une simple moyenne. Nous utilisons une formule hybride combinant la moyenne des meilleurs chunks et le score maximum absolu trouvé dans un script :`Score = (mean \times 0.5) + (max \times 0.5)`.
    
## Amélioration : Pseudo-Relevance Feedback (PRF)
Pour booster les performances de nos deux modèles, nous avons implémenté une technique d'expansion de requête : le Pseudo-Relevance Feedback.
    - **Concept** : Le système fait une première recherche. Il suppose ensuite que les $k$ premiers résultats sont parfaitement pertinents.
    - **Augmentation** : Il calcule le vecteur moyen de ces $k$ documents et l'ajoute au vecteur de la requête initiale (pondéré par un facteur $\alpha$). La recherche finale est relancée avec cette "super-requête".
    
## Évaluation Scientifique
Afin de départager objectivement le modèle TF-IDF et le modèle Embeddings (avec et sans PRF), nous avons évalué notre système à l'aide d'un jeu de requêtes (queries.json) et d'une vérité terrain (qrels.csv - jugements de pertinence).
Une boucle d'évaluation confronte les prédictions aux Qrels sur 3 métriques majeures :
    - **Rappel (Recall)** : Capacité du système à retrouver tous les films à éviter présents dans la vérité terrain.
    - **MAP (Mean Average Precision)** : Capacité du système à classer les films pertinents le plus haut possible dans la liste des résultats.
    - **nDCG (Normalized Discounted Cumulative Gain)** : Évaluation fine du classement qui prend en compte les différents niveaux de pertinence (les "notes") des films, en pénalisant les résultats très critiques qui seraient classés trop bas.

## Analyse des résultats
L'analyse de nos résultats met en évidence une compétition très intéressante entre nos deux approches, avec une victoire globale de notre modèle classique.

| MODÈLES | TF-IDF | EMBEDDING |
| :--- | :---: | :---: |
| **Modèles de base** | | |
| **RAPPEL** | 73% | 72% |
| **MAP** | 59% | 55% |
| **nDCG** | 53% | 57% |
| **↓ PSEUDO-RELEVANCE FEEDBACK ↓** | | |
| **RAPPEL** | 77% | 73% |
| **MAP** | 71% | 55% |
| **nDCG** | 54% | 59% |

En résumé, notre approche classique basée sur le TF-IDF et l'enrichissement sémantique surpasse le modèle Deep Learning, prouvant définitivement son efficacité grâce au boost de performance majeur apporté par le Pseudo-Relevance Feedback.