## Datasets

Les données du projet étant trop volumineuses pour GitHub, elles sont hébergées sur Google Drive. Pour exécuter le code et reproduire les résultats, veuillez suivre ces étapes :

1. Téléchargez l'archive en cliquant sur ce lien : https://drive.google.com/file/d/1hduf-4T8FU6ckJjoNA6cKthIVLw175U-/view?usp=sharing.
2. Décompressez le fichier `.zip`.
3. Placez les dossiers extraits dans le répertoire `DWL_TAL/Dataset_Projet_TAL/`.

L'arborescence finale sera comme suit :
```text
└── DWL_TAL/
    ├── README.md
    ├── Projet_TAL_json.py
    ├── solution_pb1.py
    └── Dataset_Projet_TAL/
        ├── generer_collection.py
        ├── collection_test/   <-- Partagé via Drive
        │   ├── corpus.csv
        │   ├── corpus.json
        │   ├── qrels.csv
        │   └── queries.json
        ├── raw/               <-- Partagé via Drive
        │   ├── metadata_updated.json
        │   └── tags.json
        └── scores/            <-- Partagé via Drive
            └── tagdl.csv
```

Une fois ces dossiers en place, vous pourrez exécuter le script Python Projet_TAL_json.py (vous n'aurez pas besoin d'exécuter generer_collection.py car le dossier collection_test est déjà transmis via le Drive) normalement, car ils trouveront les données au bon endroit !