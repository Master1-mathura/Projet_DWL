# sur mac, encode() déclenche plusieurs calculs (tokenizers, pytorch etc.) => plusieurs threads => deadlock
import os
os.environ["USE_TF"] = "0"
os.environ["USE_TORCH"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"
import torch
torch.set_num_threads(1)

# début du code
import pandas as pd
import time
from sentence_transformers import SentenceTransformer, util # importation du SBERT

model = SentenceTransformer('all-MiniLM-L6-v2') # dimension des vecteurs = 384

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
    return " ".join(scene_description)

# chargement des données :
df = pd.read_json("Dataset_Projet_TAL/collection_test/corpus.json", encoding="utf-8")
df['text'] = df['text'].apply(parsing_script)
docs = df.set_index('doc_id').to_dict(orient='index')

# Récupération des id des films et de leur script :
doc_ids = list(docs.keys())
doc_texts = [docs[doc_id]["text"] for doc_id in doc_ids] # liste où chaque case = 1 script

# Mettre en matrice (vecteurs) les scripts via SBERT :
# print("Début d'encodage des scripts")
# doc_embedding = model.encode(doc_texts, convert_to_tensor=True)
print("Début d'encodage des scripts")
# pas juste embedding sur tout, mais on calcule 16 scripts à la fois (diminue à 8 si ça rame) et on affiche une barre de progression
doc_embedding = model.encode(doc_texts, convert_to_tensor=True, batch_size=16, show_progress_bar=True) 
print("Fin d'encodage des scripts")
print("Fin d'encodage des scripts")

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

# # à régler :
# sauvegarder la partie mise en matrice pour éviter d'avoir à la faire toçut le temps

# gemini propose :
# # --- Mettre en matrice (vecteurs) les scripts via SBERT ---

# chemin_sauvegarde = "embeddings_films.pt"

# # On vérifie si on a déjà fait le calcul avant
# if os.path.exists(chemin_sauvegarde):
#     print("Fichier de vecteurs trouvé ! Chargement en cours...")
#     doc_embedding = torch.load(chemin_sauvegarde)
#     print("Chargement terminé.")
# else:
#     print("Début d'encodage des scripts (ça peut prendre un peu de temps...)")
#     doc_embedding = model.encode(
#         doc_texts, 
#         convert_to_tensor=True,
#         batch_size=16,          
#         show_progress_bar=True  
#     ) 
#     print("Fin d'encodage des scripts")
    
#     # Sauvegarde du tenseur sur ton disque dur
#     torch.save(doc_embedding, chemin_sauvegarde)
#     print(f"Vecteurs sauvegardés avec succès dans : {chemin_sauvegarde}")

# # --- Traitement de la requête (la suite de ton code) ---
# def traitement_requete(query):
# # ...
    
# 2) SBERT (all-MiniLM-L6-v2) a une mémoire courte : il ne lit que les ~250 premiers mots.

# Si, après ton nettoyage (parsing_script), la description de ta scène pour un film fait 3000 mots, SBERT va ignorer les 2750 derniers mots. Ton encodage se fera sans erreur, le code va marcher, mais tes recherches de similarité se baseront uniquement sur le tout début de chaque script.

# éviter la limite des 250 mots ? (La méthode du "Chunking")
# Puisque all-MiniLM-L6-v2 ne peut lire que de petits blocs de texte, la solution standard en TAL s'appelle le Chunking (le découpage). L'idée est simple :

# Tu découpes le script d'un film en plusieurs petits "morceaux" de 200 mots.

# Tu demandes à SBERT de transformer chaque morceau en vecteur.

# Tu fais la moyenne de tous ces vecteurs pour obtenir un seul "Vecteur Global" qui représente tout le film.

# pour ça :
# def decouper_texte(texte, taille_morceau=200):
#     """Découpe un long texte en une liste de petits morceaux de N mots."""
#     mots = texte.split()
#     morceaux = []
#     for i in range(0, len(mots), taille_morceau):
#         morceau = " ".join(mots[i : i + taille_morceau])
#         morceaux.append(morceau)
#     return morceaux