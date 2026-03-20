import pandas as pd
import Projet_TAL_json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# pas besoin de parser les queries

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
            pertinence = float(pertinence)
            if queryID not in qrels_data:
                qrels_data[queryID] = []
            qrels_data[queryID].append((int(docID), pertinence))
    return qrels_data

qrels_file_path = "Dataset_Projet_TAL/collection_test/qrels.csv"
qrels_data = load_qrels(qrels_file_path)


query_ex = "Are there any intense scenes with dark, claustrophobic atmospheres?"

resultats = Projet_TAL_json.search(query_ex)
print("Top Movie DNW : ")
for i,(doc_id, score) in enumerate(resultats,1) :
    print("N° :" , i , "  ", doc_film[doc_id]["title"])
    print(f"    Score : {score}")