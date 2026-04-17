1. Préparer le dossier de données
Dans le dossier app de notre projet web, créez un dossier nommé data s'il n'existe pas déjà.

2. Télécharger les fichiers lourds
Allez sur notre Google Drive (celui du projet TAL) et téléchargez ces deux fichiers exacts :

corpus.json (dans Dataset_Projet_TAL/collection_test/)

embeddings_films.pt (à la racine)

3. Placer les fichiers au bon endroit
Glissez ces deux fichiers dans le dossier data. Votre arborescence DOIT ressembler exactement à ça :

```text
DWL_PP/
└── app/
    ├── data/
    │   ├── corpus.json
    │   └── embeddings_films.pt
    ├── app.py
    ├── search_moteur.py
    └── ...
```