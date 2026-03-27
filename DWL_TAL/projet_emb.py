# Pour éviter les erreurs sur mac (car encode() déclenche plusieurs calculs (tokenizers, pytorch etc.) => plusieurs threads => deadlock) :
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"
os.environ["USE_TF"] = "0"
os.environ["USE_TORCH"] = "1"

# Début du code
import pandas as pd
import time
import torch
from sentence_transformers import SentenceTransformer, util # importation du SBERT et ses fonctionnalités

model = SentenceTransformer('all-MiniLM-L6-v2') # dimension des vecteurs = 384

def decouper_texte(texte, taille_morceau=200,chevauchement = 50):
    #Découpe un long texte en une liste de petits morceaux de N mots.
    mots = texte.split()
    morceaux = []
    
    pas = taille_morceau - chevauchement
    for i in range(0, len(mots), pas):
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
            #torch.zeros attend un tuple 
            vecteurs_morceaux = torch.zeros((1,384))
        else : 
            #batch_size : Le nombre de texte qu'on envoie en meme temps au processeur
            vecteurs_morceaux = model.encode(film,convert_to_tensor=True,show_progress_bar=False,batch_size = 62)

        doc_embedding.append(vecteurs_morceaux)
        print(f"Encodage du film {i + 1} / {total_films}...", end="\r")
    torch.save(doc_embedding,sauvegarde)
print("Ok")

# Traitement de la requête :
def traitement_requete(query):
    print("Début d'encodage des queries")
    query_embedding = model.encode(query, convert_to_tensor=True)
    print("Fin d'encodage des queries")
    return query_embedding


# Calcul des scores (cosinus similarité):
def scores_simi(query_embedding, n = 100, k = 5):
    # semantic_search : peut traiter plusieurs requetes en même temps => ça donne une liste de liste
    # "traiter" :
        # SBERT prend le vecteur de la requête
        # il calcule la similarité cos avec chaque film
        # il les trie en fonction de leurs score (si proche de 1 alors ++ pertinent)
        # il choisit les k premiers films
    # sauf que nous on envoie qu'une seule requête d'où [0]
    # liste_films = util.semantic_search(query_embedding, doc_embedding, top_k = n)[0]

    resultat = []
    # on va parcourir les films affichés pour chaque requête
    #Vidur : Revoir le max et top-k
    for i, doc_embd in enumerate(doc_embedding):
        
        # alignement matériel (mac/windows)
        doc_embd = doc_embd.to(query_embedding.device)

        scores_morceaux = util.cos_sim(query_embedding,doc_embd)[0]
        
        vrai_k = min(k,len(scores_morceaux))

        meilleurs_scores = torch.topk(scores_morceaux,vrai_k).values

        #scores_final = torch.max(meilleurs_scores).item()
        scores_final = meilleurs_scores.mean() * 0.5 + torch.max(scores_morceaux) * 0.5

        vrai_doc_id = doc_ids[i]
        resultat.append((vrai_doc_id,scores_final))
    
    resultat_trie = sorted(resultat,key=lambda x:x[1],reverse=True)
    return resultat_trie[:n]

query = input("Write your phobie ... : ")
nb_films_envoyer_a_user  = 5
output = scores_simi(traitement_requete(query))
print(f"TOP {nb_films_envoyer_a_user} : \n")
for id,score in output[:nb_films_envoyer_a_user]: 
    print(f"FILM : {docs[id]['title']} avec score : {score}\n")
end = time.time()
print(f"Temps d'exécution total du programme : {end - start}")