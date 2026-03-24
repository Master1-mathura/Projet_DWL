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
print("Début d'encodage des scripts")
doc_embedding = model.encode_document(doc_texts, convert_to_tensor=True) # 
print("Fin d'encodage des scripts")

# Traitement de la requête :
def traitement_requete(query):
    print("Début d'encodage des queries")
    query_embedding = model.encode_query(query, convert_to_tensor=True)
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