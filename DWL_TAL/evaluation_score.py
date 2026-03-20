import pandas as pd
import Projet_TAL_json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# pas besoin de parser les queries

df = pd.read_json("Dataset_Projet_TAL/collection_test/queries.json", encoding="utf-8")
parse_queries = df.set_index('query_id').to_dict(orient='index')

# Chargement des données

def load_qrels(file_path):
    qrels_data = {}

    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            queryID, docID, pertinence = line.strip().split(',')
            pertinence = float(pertinence)
            if queryID not in qrels_data:
                qrels_data[queryID] = []
            qrels_data[queryID].append((int(docID), pertinence))
    return qrels_data

qrels_file_path = "Dataset_Projet_TAL/collection_test/qrels.csv"
qrels_data = load_qrels(qrels_file_path)

# for queryID, docID in qrels_data.items():
#     print(f"Query ID : {queryID}")
#     for id, pertinence in docID:
#         print(f" Doc ID : {id}, Pertinence: {pertinence}")

liste_doc_id = list(Projet_TAL_json.docs.keys())
liste_textes = []
for doc_id in liste_doc_id :
    liste_textes.append(Projet_TAL_json.docs[doc_id]["text"])

# Vectorisation de tout le corpus
vectorizer = TfidfVectorizer(stop_words='english')
tf_idf_matrice = vectorizer.fit_transform(liste_textes)

def query_documents(vectorizer, tf_idf_matrice, query_texte):
    vecteur_query = vectorizer.transform([query_texte])
    similarities = cosine_similarity(vecteur_query, tf_idf_matrice).flatten()

    top_n = 5
    top_indices = similarities.argsort()[-top_n:][::-1]

    resultats = []
    for id in top_indices:
        doc_id = liste_doc_id[id]
        score = similarities[id]
        resultats.append((doc_id, score))
    print(resultats)
    return resultats

query_ex = "Are there any intense scenes with dark, claustrophobic atmospheres?"
resultats = query_documents(vectorizer, tf_idf_matrice,query_ex)
for (doc_id, score) in resultats :
    print(Projet_TAL_json.docs[doc_id]["title"])
    print(f"    Score : {score}")