# sur mac, encode() déclenche plusieurs calculs (tokenizers, pytorch etc.) => plusieurs threads => deadlock
import os
os.environ["USE_TF"] = "0"
os.environ["USE_TORCH"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"

# début du code
import pandas as pd
import time
import torch
from sentence_transformers import SentenceTransformer, util # importation du SBERT

model = SentenceTransformer('all-MiniLM-L6-v2') # dimension des vecteurs = 384


def decouper_texte(texte, taille_morceau=200):
    #Découpe un long texte en une liste de petits morceaux de N mots.
    mots = texte.split()
    morceaux = []
    for i in range(0, len(mots), taille_morceau):
        morceau = " ".join(mots[i : i + taille_morceau])
        morceaux.append(morceau)
    return morceaux


# nettoyage des scripts
def parsing_script(script):
    # Extraction uniquement du texte compris entre les balises <scene_description>
    script = script.replace("<", " <").replace(">","> ")
    script = script.split()
    scene_description = []
    balise_scene = False
    for mot in script:
        if mot == "<scene_description>":
            balise_scene = True
            continue

        if mot == "</scene_description>":
            balise_scene = False 
            continue

        if balise_scene :
            scene_description.append(mot)
    test = decouper_texte(" ".join(scene_description))
    return test



# chargement des données :
start = time.time()
df = pd.read_json("Dataset_Projet_TAL/collection_test/corpus.json", encoding="utf-8")
df['text'] = df['text'].apply(parsing_script)
docs = df.set_index('doc_id').to_dict(orient='index')

# Récupération des id des films et de leur script :
doc_ids = list(docs.keys())
doc_texts = [docs[doc_id]["text"] for doc_id in doc_ids] # liste où chaque case = 1 script
# 1. On récupère l'ID du film à l'index 108
id_film_vide = doc_ids[108]

# 2. On utilise cet ID pour aller chercher le titre dans ton dictionnaire
nom_film_vide = docs[id_film_vide]['title']

# Mettre en matrice (vecteurs) les scripts via SBERT :
# print("Début d'encodage des scripts")
# doc_embedding = model.encode(doc_texts, convert_to_tensor=True)
# pas juste embedding sur tout, mais on calcule 16 scripts à la fois (diminue à 8 si ça rame) et on affiche une barre de progression

sauvegarde = "embeddings_films.pt"

if os.path.exists(sauvegarde):
    print("Fichier de vecteurs trouvé ! ")
    doc_embedding = torch.load(sauvegarde)
    print("Chargement terminé.")
else : 
    print("Debut encodage des scripts")
    doc_embedding = []
    total_films = len(doc_texts)
    for i,film in enumerate(doc_texts):
        if len(film) == 0:
            vecteur_moyen = torch.zeros(384)
        else : 
            vecteurs_morceaux = model.encode(film,convert_to_tensor=True,show_progress_bar=False,batch_size = 62)

            vecteur_moyen = torch.mean(vecteurs_morceaux,dim=0)

        doc_embedding.append(vecteur_moyen)
        print(f"Encodage du film {i + 1} / {total_films}...", end="\r")
    print("Fin d'encodage des scripts")
    torch.save(doc_embedding,sauvegarde)
print("Ok",i+1)

# Traitement de la requête :
def traitement_requete(query):
    print("Début d'encodage des queries")
    query_embedding = model.encode(query, convert_to_tensor=True)
    print("Fin d'encodage des queries")
    return query_embedding

# Calcul des scores (cosinus similarité):
def scores_simi(query_embedding, n = 5):
    # semantic_search : peut traiter plusieurs requetes en même temps => ça donne une liste de liste
    # "traiter" :
        # SBERT prend le vecteur de la requête
        # il calcule la similarité cos avec chaque film
        # il les trie en fonction de leurs score (si proche de 1 alors ++ pertinent)
        # il choisit les k premiers films
    # sauf que nous on envoie qu'une seule requête d'où [0]
    liste_films = util.semantic_search(query_embedding, doc_embedding, top_k = n)[0]

    resultat = []
    # on va parcourir les films affichés pour chaque requête
    for hit in liste_films:
        # rappel : on a donné que doc_texts à SBERT, donc il a pas retenu les ids de chaque films

        # En fait semantic_search a pour résultat un dictionnaire :
        # clé = corpus_id pour stocker l'index du script
        # valeur = score pour stocker la note de similarité cosinus
        # donc on va récupérer la position du film good dans la liste fournie à SBERT
        index = hit['corpus_id']
        vrai_doc_id = doc_ids[index]
        score = hit['score']
        resultat.append((vrai_doc_id,score))
    return resultat

query = "I am afraid of spider"
output = scores_simi(traitement_requete(query))
print("TOP 5 : \n")
for id,score in output : 
    print(f"FILM : {docs[id]['title']} avec score : {score}\n")
end = time.time()
print(f"Temps d'exécution total du programme : {end - start}")