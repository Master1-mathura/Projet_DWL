import os # Pour éviter les deadlocks sur macOS
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"
os.environ["USE_TF"] = "0"
os.environ["USE_TORCH"] = "1"

import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util

# ----- AJOUT POUR PP : variables globales pour éviter pour Flask
model = None
doc_embedding = None
dico_films = None
liste_ids_films = None
# ----- FIN AJOUT POUR PP

# ******************************************************************************** #
# ********************** Étape 1 : Prétraitement du texte ************************ #
# ******************************************************************************** #

def decouper_texte(texte, taille_morceau=200,chevauchement = 50):
    mots = texte.split()
    liste_morceaux = []

    pas = taille_morceau - chevauchement
    for i in range(0, len(mots), pas):
        morceau = " ".join(mots[i : i + taille_morceau])
        liste_morceaux.append(morceau)
    return liste_morceaux

def parsing_script(script):
    script = script.replace("<", " <").replace(">","> ")
    script = script.split()
    scene_description = []
    dans_balise_scene = False
    for mot in script:
        if mot == "<scene_description>":
            dans_balise_scene = True
            continue

        if mot == "</scene_description>":
            dans_balise_scene = False
            continue

        if dans_balise_scene :
            scene_description.append(mot)
    script_decoupe = decouper_texte(" ".join(scene_description))
    return script_decoupe

# ******************************************************************************** #
# ****************** Étape 2 : Initialisation du modèle + ************************ #
#                              + Chargement et parsing des données *************** #
# ******************************************************************************** #
# cette fonction est appelée au démarrage de Flask
def init_model():
    global model, doc_embedding, liste_ids_films, dico_films
    model = SentenceTransformer('all-MiniLM-L6-v2')

    df = pd.read_json("data/corpus.json", encoding="utf-8")
    df['text'] = df['text'].apply(parsing_script)
    dico_films = df.set_index('doc_id').to_dict(orient='index')
    liste_ids_films = list(dico_films.keys())
    liste_textes_films = [dico_films[doc_id]["text"] for doc_id in liste_ids_films]
    sauvegarde = "data/embeddings_films.pt"
    # ******************************************************************************** #
    # ****************** Étape 3 : Encodage des scripts (Embeddings) ***************** #
    # ******************************************************************************** #
    if os.path.exists(sauvegarde):
        doc_embedding = torch.load(sauvegarde)
    else :
        doc_embedding = []
        total_films = len(liste_textes_films)
        for i,film in enumerate(liste_textes_films):
            if len(film) == 0:
                vecteurs_liste_morceaux = torch.zeros((1,384))
            else :
                vecteurs_liste_morceaux = model.encode(film,convert_to_tensor=True,show_progress_bar=False,batch_size = 62)

            doc_embedding.append(vecteurs_liste_morceaux)
            print(f"Encodage du film {i + 1} / {total_films}...", end="\r")
        torch.save(doc_embedding,sauvegarde)

# ******************************************************************************** #
# **************** Étape 4 : Traitement de la requête et scoring ***************** #
# ******************************************************************************** #

def traitement_requete(query):
    vecteur_requete = model.encode(query, convert_to_tensor=True)
    return vecteur_requete

def scores_simi(vecteur_requete, n = 100, k = 5):
    liste_scores_films = []
    for i, doc_embd in enumerate(doc_embedding):

        doc_embd = doc_embd.to(vecteur_requete.device) # alignement matériel (mac/windows)
        scores_morceaux = util.cos_sim(vecteur_requete,doc_embd)[0]

        vrai_k = min(k,len(scores_morceaux))
        meilleurs_scores = torch.topk(scores_morceaux,vrai_k).values

        score_global = meilleurs_scores.mean() * 0.5 + torch.max(scores_morceaux) * 0.5

        id_film_courant = liste_ids_films[i]
        liste_scores_films.append((id_film_courant,score_global))

    liste_scores_films_trie = sorted(liste_scores_films,key=lambda x:x[1],reverse=True)
    return liste_scores_films_trie[:n]

# ******************************************************************************** #
# ****************** Étape 5 : Pseudo-Relevance Feedback (PRF) ******************* #
# ******************************************************************************** #

def pseudo_relevance_feedback(query_vector, top_results, doc_embeddings, liste_ids_films, alpha = 0.7, k =10):
    doc_id_to_idx = {id : i for i, id in enumerate(liste_ids_films)}

    pseudo_pertinents_id = [docID for docID, score in top_results[:k]]

    if len(pseudo_pertinents_id) == 0:
        return query_vector

    vecteurs_films_pertinents = []
    for docID in pseudo_pertinents_id:
        idx = doc_id_to_idx[docID]
        morceaux_film_pertinent = doc_embeddings[idx]

        # alignement matériel (mac/windows)
        morceaux_film_pertinent = morceaux_film_pertinent.to(query_vector.device)

        vecteur_moyen_film = torch.mean(morceaux_film_pertinent,dim=0)
        vecteurs_films_pertinents.append(vecteur_moyen_film)

    moyenne_pertinent = torch.mean(torch.stack(vecteurs_films_pertinents), dim = 0)
    vecteur_requete_augmente = query_vector + alpha * moyenne_pertinent

    return vecteur_requete_augmente

# ******************************************************************************** #
# ************************ Étape 6 : Exécution principale ************************ #
# ******************************************************************************** #
def rechercher(query):
    res_recherche_init  = 5

    vect_requete = traitement_requete(query)
    top_res = scores_simi(vect_requete)

    vect_prf = pseudo_relevance_feedback(vect_requete, top_res, doc_embedding, liste_ids_films)
    res_finaux = scores_simi(vect_prf)

    # ----- AJOUT POUR PP : on affiche plus les resultat par des print mais on les stocke et on les envoiçe à app.py
    resultats_pour_flask = []

    for id, score in res_finaux[:res_recherche_init]:
        resultats_pour_flask.append({
            "id": dico_films[id]["imdbID"],
            "film_name": dico_films[id]['title'],
            "score": float(score) # On convertit le Tenseur PyTorch en chiffre standard pour le JSON
        })
    return resultats_pour_flask