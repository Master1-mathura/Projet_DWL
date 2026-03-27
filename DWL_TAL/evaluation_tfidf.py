import pandas as pd
import numpy as np
import math
import projet_tfidf

df = pd.read_json("Dataset_Projet_TAL/collection_test/queries.json", encoding="utf-8")
parse_queries = df.set_index('query_id').to_dict(orient='index')
doc_film = projet_tfidf.docs

# ******************************************************************************** #
# ********** Étape 1 : Chargement des jugements de pertinence (qrels) ************ #
# ******************************************************************************** #

def load_qrels(file_path):
    dico_qrels = {}

    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            queryID, docID, pertinence = line.strip().split(',')
            queryID = int(queryID)
            docID = int(docID)
            pertinence = float(pertinence)
            if queryID not in dico_qrels:
                dico_qrels[queryID] = []
            dico_qrels[queryID].append((int(docID), pertinence))
    return dico_qrels

chemin_fichier_qrels = "Dataset_Projet_TAL/collection_test/qrels.csv"
dico_qrels = load_qrels(chemin_fichier_qrels)

# ******************************************************************************** #
# ******** Étape 2 : Fonctions de calcul des métriques (Rappel, AP, nDCG) ******** #
# ******************************************************************************** 

def eval_rappel(liste_film_recuperer, liste_des_documents_pertinent): 
    nb_pertinents_trouves = 0
    for docID in liste_film_recuperer : 
        if docID in liste_des_documents_pertinent : 
            nb_pertinents_trouves += 1 
    rappel = nb_pertinents_trouves / len(liste_des_documents_pertinent)
    return rappel


def eval_AP(liste_film_recuperer, liste_doc_pertinent):
    if len(liste_doc_pertinent) == 0 : 
        return 0.0

    relevant_set = set(liste_doc_pertinent)
    nb_pertinents_trouves = 0
    somme_precision = 0.0

    for k, docid in enumerate(liste_film_recuperer,start=1):
        if docid in relevant_set : 
            nb_pertinents_trouves += 1 
            precision_at_k = nb_pertinents_trouves / k 
            somme_precision += precision_at_k
    
    score_avg_precision = somme_precision / len(relevant_set)
    return score_avg_precision


def compute_DCG(relscores):
    dgc = 0
    for i, rel in enumerate(relscores):
        num = 2**rel -1 
        den = math.log2(i+2)
        dgc += num / den
    return dgc

def eval_nDCG(liste_film_recuperer, liste_paires):
    score_perti_recup = []
    for docID in liste_film_recuperer:
        est_trouve = False
        for doc, tagdl_score in liste_paires : 
            if docID == doc:
                relscores = int(round(tagdl_score * 4))
                score_perti_recup.append(relscores)
                est_trouve = True
                break
        if not est_trouve : 
            score_perti_recup.append(0)
    
    score_dcg_actuel = compute_DCG(score_perti_recup)

    toute_les_notes = [int(round(score *4)) for _,score in liste_paires]
    note_triees = sorted(toute_les_notes, reverse=True)
    classement_ideal = note_triees[:len(liste_film_recuperer)]
    idcg = compute_DCG(classement_ideal)

    if idcg == 0:
        return 0.0 

    ndcg = score_dcg_actuel / idcg 
    return ndcg

# ******************************************************************************** #
# ************ Étape 3 : Boucle d'évaluation sur toutes les requêtes ************* #
# ******************************************************************************** #

ap_scores = []
rappel_scores = []
ndcg_scores = []
max_qrels = max(len(dico_qrels[q]) for q in dico_qrels)
lim_affichage = projet_tfidf.res_recherche_init

for queryID in parse_queries.keys():
    donnees_perti_requete = dico_qrels[queryID]
    ids_perti_attendus = []
    for el in donnees_perti_requete : 
        ids_perti_attendus.append(el[0])

    query_text = parse_queries[queryID]['text']
    
    print("\n" + "="*100)
    print(f"Query : {query_text}")
    print("="*100)
    
    vecteur_requete_test = projet_tfidf.traitement_requete(query_text)
    res_init_test = projet_tfidf.scores_simi(vecteur_requete_test, n = max_qrels)

    for doc_id,score in res_init_test[:lim_affichage]:
        titre = doc_film[doc_id]["title"]
        print(f"  - {titre} (Score : {score:.4f})")

    vecteur_augmente = projet_tfidf.pseudo_relevance_feedback(projet_tfidf.tf_idf, vecteur_requete_test, res_init_test, alpha=0.7, k = 10)
    print("----------------------PRF-------------------------")
    res_prf_test = projet_tfidf.scores_simi(vecteur_augmente, n = max_qrels)
    
    for doc_id,score in res_prf_test[:lim_affichage]:
        titre = doc_film[doc_id]["title"]
        print(f"  - {titre} (Score : {score:.4f})")
    

    ids_films_retrouves_prf = [filmID for filmID, _ in res_prf_test]
    
    rappel_courant = eval_rappel(ids_films_retrouves_prf, ids_perti_attendus)
    ap_courant = eval_AP(ids_films_retrouves_prf, ids_perti_attendus)
    ndcg_courant = eval_nDCG(ids_films_retrouves_prf, donnees_perti_requete)

    rappel_scores.append(rappel_courant)
    ap_scores.append(ap_courant)
    ndcg_scores.append(ap_courant)

print("Avg. Recall: ", np.mean(rappel_scores))
print("MAP: ", np.mean(ap_scores))
print("Avg. nDCG: ", np.mean(ndcg_scores))