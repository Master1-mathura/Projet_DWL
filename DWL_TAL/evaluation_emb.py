import pandas as pd
import numpy as np
import math
import torch
print("Load Moteur :")
import projet_emb
from sentence_transformers import util

# pas besoin de parser les queries
print("Etape 1 : ")
df = pd.read_json("Dataset_Projet_TAL/collection_test/queries.json", encoding="utf-8")
parse_queries = df.set_index('query_id').to_dict(orient='index')
doc_film = projet_emb.docs
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


def pseudo_relevance_feedback(query_vector, top_results, doc_embeddings, doc_ids, alpha = 0.7, k =10):
    doc_id_to_idx = {id : i for i, id in enumerate(doc_ids)}

    pseudo_pertinents_id = [docID for docID, score in top_results[:k]]

    if len(pseudo_pertinents_id) == 0:
        return query_vector

    relevant_vectors = []
    for docID in pseudo_pertinents_id:
        idx = doc_id_to_idx[docID]
        doc_chunk = doc_embeddings[idx]

        # alignement matériel (mac/windows)
        doc_chunk = doc_chunk.to(query_vector.device)
        
        doc_mean_vector = torch.mean(doc_chunk,dim=0)
        relevant_vectors.append(doc_mean_vector)

    moyenne_pertinent = torch.mean(torch.stack(relevant_vectors), dim = 0)
    
    augmented_query_vector = query_vector + alpha * moyenne_pertinent

    return augmented_query_vector


ap_scores = []
rappel_scores = []
ndcg_scores = []
max_qrels = max(len(qrels_data[q]) for q in qrels_data)
nb_film_envoyer_a_user = projet_emb.nb_films_envoyer_a_user
for queryID in parse_queries.keys():
    qliste = qrels_data[queryID]
    qrels_ui = []
    for el in qliste : 
        qrels_ui.append(el[0])

    vecteur_requete = projet_emb.traitement_requete(parse_queries[queryID]['text'])
    query_ui_init = projet_emb.scores_simi(vecteur_requete, n = max_qrels)

    for doc_id, score in query_ui_init[:nb_film_envoyer_a_user]:
        titre = doc_film[doc_id]["title"]
        print(f"  - {titre} (Score : {score:.4f})")

    vecteur_augmente = pseudo_relevance_feedback(vecteur_requete,query_ui_init,projet_emb.doc_embedding,projet_emb.doc_ids,alpha=0.7,k=10)
    print("----------------------PRF-------------------------")
    query_ui_prf = projet_emb.scores_simi(vecteur_augmente, n = max_qrels)

    for doc_id, score in query_ui_prf[:nb_film_envoyer_a_user]:
        titre = doc_film[doc_id]["title"]
        print(f"  - {titre} (Score : {score:.4f})")
    
    query_ui_ids = [filmID for filmID, _ in query_ui_prf]
    
    recall = eval_rappel(query_ui_ids, qrels_ui)
    ap = eval_AP(query_ui_ids, qrels_ui)
    ndcg = eval_nDCG(query_ui_ids, qliste)

    rappel_scores.append(recall)
    ap_scores.append(ap)
    ndcg_scores.append(ndcg)

print("Avg. Recall: ", np.mean(rappel_scores))
print("MAP: ", np.mean(ap_scores))
print("Avg. nDCG: ", np.mean(ndcg_scores))