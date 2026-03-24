import pandas as pd
import numpy as np
import math
print("Load Moteur :")
import Projet_TAL_json

# pas besoin de parser les queries
print("Etape 1 : ")
df = pd.read_json("Dataset_Projet_TAL/collection_test/queries.json", encoding="utf-8")
parse_queries = df.set_index('query_id').to_dict(orient='index')
doc_film = Projet_TAL_json.docs
# Chargement des données

def load_qrels(file_path):
    qrels_data = {}

    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            queryID, docID, pertinence = line.strip().split(',')
            queryID = int(queryID)
            docID = int(docID)
            pertinence = float(pertinence)
            if queryID not in qrels_data:
                qrels_data[queryID] = []
            qrels_data[queryID].append((int(docID), pertinence))
    return qrels_data

qrels_file_path = "Dataset_Projet_TAL/collection_test/qrels.csv"
qrels_data = load_qrels(qrels_file_path)

print("Etape 2 :")

def eval_rappel(liste_film_recuperer, liste_des_documents_pertinent): 
    nb_film_trouver = 0
    for docID in liste_film_recuperer : 
        if docID in liste_des_documents_pertinent : 
            nb_film_trouver += 1 
    rappel = nb_film_trouver / len(liste_des_documents_pertinent)
    return rappel


def eval_AP(liste_film_recuperer, liste_doc_pertinent):
    if len(liste_doc_pertinent) == 0 : 
        return 0.0

    relevant_set = set(liste_doc_pertinent)
    nb_pertinents_trouves = 0
    somme = 0.0

    for k, docid in enumerate(liste_film_recuperer,start=1):
        if docid in relevant_set : 
            nb_pertinents_trouves += 1 
            precision_at_k = nb_pertinents_trouves / k 
            somme += precision_at_k
    
    ap = somme / len(relevant_set)
    return ap


def compute_DCG(relscores):
    dgc = 0
    for i, rel in enumerate(relscores):
        num = 2**rel -1 
        den = math.log2(i+2)
        dgc += num / den
    return dgc

def eval_nDCG(liste_film_recuperer, liste_paires):
    liste_relscores = []
    for docID in liste_film_recuperer:
        founded = False
        for doc, tagdl_score in liste_paires : 
            if docID == doc:
                relscores = int(round(tagdl_score * 4))
                liste_relscores.append(relscores)
                founded = True
                break
        if not founded : 
            liste_relscores.append(0)
    
    DCG = compute_DCG(liste_relscores)

    toute_les_notes = [int(round(score *4)) for _,score in liste_paires]
    note_triees = sorted(toute_les_notes, reverse=True)
    liste_ideal = note_triees[:len(liste_film_recuperer)]
    IDCG = compute_DCG(liste_ideal)

    if IDCG == 0:
        return 0.0 

    nDCG = DCG / IDCG 
    return nDCG


def pseudo_relevance_feedback_cours(tfidf_matrice,vecteur_requete,top_results, k = 5, nb_mot  = 10):
    top_k_ids = [docID for docID, _ in top_results[:k]]
    
    somme_vecteur = np.zeros(len(vecteur_requete))
    for docID in top_k_ids :
        somme_vecteur += np.array(tfidf_matrice[docID])
    
    meilleurs_indices = np.argsort(somme_vecteur)[-nb_mot:]
    
    nouvelle_requete = list(vecteur_requete)
    for idx in meilleurs_indices: 
        nouvelle_requete[idx] += (somme_vecteur[idx]/k)
    
    return nouvelle_requete
def pseudo_relevance_feedback(tfidf_matrice,vecteur_requete,top_results,documents_pertinents, alpha=1.0, beta = 0.75,gamma=0.15,k = 5):

    top_k_id = [docID for docID, score in top_results[:k]]
    vrai_pertinets_id = [docID for docID in top_k_id if docID in documents_pertinents]
    no_pertinent_id = [docID for docID in top_k_id if docID not in documents_pertinents]
    if len(vrai_pertinets_id) == 0:
        return vecteur_requete

    revelant_vectors = [np.array(tfidf_matrice[idx]) for idx in vrai_pertinets_id]
    moyenne_pertinent = np.mean(revelant_vectors,axis=0)
    
    if len(no_pertinent_id) > 0 :
        non_relevant_vectors = [np.array(tfidf_matrice[idx]) for idx in no_pertinent_id]
        moyenne_non_pertinent = np.mean(non_relevant_vectors,axis=0)
    else : 
        moyenne_non_pertinent = np.zeros(len(np.array(vecteur_requete)))
   
    augmented_query_vecteur = (np.array(vecteur_requete) * alpha) + (beta * moyenne_pertinent) - (gamma * moyenne_non_pertinent)

    return augmented_query_vecteur.tolist()

ap_scores = []
rappel_scores = []
ndcg_scores = []

for queryID in parse_queries.keys():
    qliste = qrels_data[queryID]
    qrels_ui = []
    for el in qliste : 
        qrels_ui.append(el[0])

    vecteur_requete = Projet_TAL_json.traitement_requete(parse_queries[queryID]['text'])
    vecteur_init = Projet_TAL_json.scores_simi(vecteur_requete, n = 1000)
    print("--------------------------------------")
    for doc_id,score in vecteur_init[:5]:
        titre = doc_film[doc_id]["title"]
        print(f"{titre} (Score de similarité : {score})")

    vecteur_augmente = pseudo_relevance_feedback(Projet_TAL_json.tf_idf, vecteur_requete, vecteur_init, qrels_ui, alpha = 1.0, beta = 0.6, k = 15)
    print("----------------------PRF-------------------------")
    query_ui = Projet_TAL_json.scores_simi(vecteur_augmente, n = 1000)
    
    for doc_id,score in query_ui[:5]:
        titre = doc_film[doc_id]["title"]
        print(f"{titre} (Score de similarité : {score})")
    
    print("--------------------------------------")
    print()
    print()
    query_ui_ids = [filmID for filmID, _ in query_ui]
    
    recall = eval_rappel(query_ui_ids, qrels_ui)
    ap = eval_AP(query_ui_ids, qrels_ui)
    ndcg = eval_nDCG(query_ui_ids, qliste)

    rappel_scores.append(recall)
    ap_scores.append(ap)
    ndcg_scores.append(ndcg)

print("Avg. Recall: ", np.mean(rappel_scores))
print("MAP: ", np.mean(ap_scores))
print("Avg. nDCG: ", np.mean(ndcg_scores))