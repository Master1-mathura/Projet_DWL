import pandas as pd
import time
import math
import numpy as np
from nltk.corpus import stopwords
from nltk import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity

# ******************************************************************************** #
# ************************ Étape 1 : Prétraitement du texte ************************ #
# ******************************************************************************** #

def parsing_script(script):
    # Extraction uniquement du texte compris entre les balises <scene_description>
    script = script.replace("<", " <").replace(">", "> ")
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
        if balise_scene:
            scene_description.append(mot)
    return " ".join(scene_description)

# Chargement des données
temps_total = time.time()
df = pd.read_json("Dataset_Projet_TAL/collection_test/corpus.json", encoding="utf-8")
df['text'] = df['text'].apply(parsing_script)

docs = df.set_index('doc_id').to_dict(orient='index')

# ******************************************************************************** #
# ******************** Étape 2 : Création de l'index inversé ********************* #
# ******************************************************************************** #

tokenizer = RegexpTokenizer(r"\w+")
stopwords_set = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
lemme = {}
postings = {}

start_posting = time.time()

for filmID, data in docs.items():
    script = data["text"]
    tokens = tokenizer.tokenize(script)  
    for mot in tokens:
        token_lower = mot.lower()
        if token_lower not in stopwords_set:
            if token_lower not in lemme:
                lemme[token_lower] = lemmatizer.lemmatize(token_lower)
            t = lemme[token_lower]

            if t not in postings:
                postings[t] = {}
            postings[t][filmID] = postings[t].get(filmID, 0) + 1

end_posting = time.time()

# ******************************************************************************** #
# ********************** Étape 3 : Calcul des scores TF-IDF ********************** #
# ******************************************************************************** #

start = time.time()
N = len(docs)

idf_score = {terme: math.log(N / len(postings[terme])) + 1 for terme in postings}
liste_terme = list(postings.keys())
terme_index = {term: i for i, term in enumerate(liste_terme)}

n_liste_terme = len(liste_terme)
tf_idf = {filmID: [0.0] * n_liste_terme for filmID in docs}

log10 = math.log10
for i, terme in enumerate(postings):
    score_idf = idf_score[terme]
    for filmID, tf in postings[terme].items():
        tf_idf[filmID][i] = (1 + log10(tf)) * score_idf

end = time.time()

# ******************************************************************************** #
# ********************** Étape 4 : Traitement de la requête ********************** #
# ******************************************************************************** #

def traitement_requete(query):
    tokens = tokenizer.tokenize(query)
    queryterms = []
    for mot in tokens:
        mot_lower = mot.lower()
        if mot_lower not in stopwords_set:
            lemme_mot = lemmatizer.lemmatize(mot_lower)
            queryterms.append(lemme_mot)

    vecteur_query = [0.0] * len(liste_terme)
    liste_terme_set = set(liste_terme)
    for mot in queryterms:
        if mot in liste_terme_set:
            index = terme_index[mot]
            tf = queryterms.count(mot)
            vecteur_query[index] = (1 + log10(tf)) * idf_score[mot]
    return vecteur_query

# ******************************************************************************** #
# ****************** Étape 5 : Calcul des scores de similarité ******************* #
# ******************************************************************************** #

def scores_simi(vecteur_query, n=5):
    vect_query_arr = np.array(vecteur_query).reshape(1, -1)

    score_similarite = {}
    for filmID, vecteur in tf_idf.items():
        vecteur_film_arr = np.array(vecteur).reshape(1, -1)
        cos = cosine_similarity(vect_query_arr, vecteur_film_arr)[0][0]
        score_similarite[filmID] = cos

    pires_n_films = sorted(score_similarite.items(), key=lambda x: x[1], reverse=True)[:n]
    return pires_n_films

# ******************************************************************************** #
# ****************** Étape 6 : Pseudo-Relevance Feedback (PRF) ******************* #
# ******************************************************************************** #

def pseudo_relevance_feedback(tfidf_matrice, vecteur_requete, top_results, alpha=0.7, k=10):
    pseudo_pertinents_id = [docID for docID, _ in top_results[:k]]
    if len(pseudo_pertinents_id) == 0:
        return vecteur_requete

    revelant_vectors = [np.array(tfidf_matrice[idx]) for idx in pseudo_pertinents_id]
    moyenne_pertinent = np.mean(revelant_vectors, axis=0)

    augmented_query_vecteur = np.array(vecteur_requete) + alpha * moyenne_pertinent
    return augmented_query_vecteur.tolist()

# ******************************************************************************** #
# ************************ Étape 7 : Exécution principale ************************ #
# ******************************************************************************** #

texte_requete_utilisateur = input("What are you afraid of ? ")
res_recherche_init = 5

vect_requete = traitement_requete(texte_requete_utilisateur)
top_res = scores_simi(vect_requete)

vect_prf = pseudo_relevance_feedback(tf_idf, vect_requete, top_res)
res_finaux = scores_simi(vect_prf)

print(f"Here are the top {res_recherche_init} movies that you should avoid : \n")
for id, score in res_finaux[:res_recherche_init]:
    print(f"Movie : {docs[id]['title']} (Score : {score})\n")

temps_total_end = time.time()
print(f"Temps d'exécution total du programme : {temps_total_end - temps_total}")