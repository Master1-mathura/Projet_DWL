import pandas as pd
import time
import math
import numpy as np
from nltk.corpus import stopwords
from nltk import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity

# ******************************************************************************** #
# ************************ Étape 0 : Nettoyage préalable ************************* #
# ******************************************************************************** #

# Nettoyage du script pour n'avoir que l'essentiel
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

# Chargement des données
temps_total = time.time()
df = pd.read_json("Dataset_Projet_TAL/collection_test/corpus.json", encoding="utf-8")
df['text'] = df['text'].apply(parsing_script)

docs = df.set_index('doc_id').to_dict(orient='index')

# ******************************************************************************** #
# ******************** Étape 1 : Création de l'index inversé ********************* #
# ******************************************************************************** #

start_posting = time.time()
postings = {}
stopwords = set(stopwords.words("english"))
tokenizer = RegexpTokenizer(r"\w+")
lemmatizer = WordNetLemmatizer()
# Pour optimiser en évitant de re-lemmatiser plusieurs fois un même mot
lemme = {}

for filmID, data in docs.items():
    script = data["text"]
    tokens=tokenizer.tokenize(script)
    for token in tokens :

        # Lemmatisation
        if token not in stopwords:
            if token not in lemme : 
                lemme[token] = lemmatizer.lemmatize(token)
            t = lemme[token]

            # Remplissage de l'index inversé
            if t not in postings :
                postings[t] = {}
            if filmID not in postings[t]:
                postings[t][filmID] = 1
            else : 
                postings[t][filmID] +=1
end_posting = time.time()


# ******************************************************************************** #
# ********************** Étape 2 : Calcul des scores TF-IDF ********************** #
# ******************************************************************************** #

start = time.time()
N = len(docs)

tf_idf = {}

# Calcul de l'IDF pour chaque terme du vocabulaire 
idf_score = {terme : math.log(N / len(postings[terme])) for terme in postings}
# Création d'une liste des mots, elle doit être fixe pour comparer les vecteurs
liste_terme = list(postings.keys())

# Initialisation des vecteurs TF*IDF
for filmID in docs :
    tf_idf[filmID] = [0.0] * len(liste_terme)

# Remplissage des vecteurs TF*IDF
for i,terme in enumerate(postings):
    score_idf = idf_score[terme]
    for filmID,tf in postings[terme].items():
        if filmID in tf_idf  : 
            tf_idf[filmID][i] = tf * score_idf
end = time.time()

# ******************************************************************************** #
# ********************** Étape 3 : Traitement de la requête ********************** #
# ******************************************************************************** #
def search(query):
    # query = input("Enter your query : ")
    tokens = tokenizer.tokenize(query.lower())
    queryterms = [lemmatizer.lemmatize(t) for t in tokens if t not in stopwords]

    # Création du vecteur de la requête
    vecteur_query = [0.0] * len(liste_terme)
    for mot in queryterms : 
        if mot in postings : 
            index = liste_terme.index(mot)
            tf = queryterms.count(mot)
            vecteur_query[index] = tf * idf_score[mot]

# ******************************************************************************** #
# ****************** Étape 4 : Calcul des scores de similarité ******************* #
# ******************************************************************************** #
            
    vect_query_arr = np.array(vecteur_query).reshape(1,-1)

    score_similarite = {}
    for filmID, vecteur in tf_idf.items() :
        vecteur_film_arr = np.array(vecteur).reshape(1,-1)
        # Similarité cosinus
        cos = cosine_similarity(vect_query_arr,vecteur_film_arr)[0][0]
        score_similarite[filmID] = cos

    # Tri pour avoir les 5 meilleurs scores -> les films à éviter à toçut prix
    pires_5_films = sorted(score_similarite.items(), key=lambda x: x[1], reverse = True)[:5]

    res = []

    # print("Vous devriez éviter le(s) film(s) : ")
    for (filmID, score) in pires_5_films:
        res.append((filmID, score))
        # titre = docs[filmID]["title"]
        # print(f"{rang}. {titre} (Score de similarité : {score})")
    return res

query = input("Enter query : ")
result = search(query)
for doc_id,score in result:
    titre = docs[doc_id]["title"]
    print(f"{titre} (Score de similarité : {score})")
# Temps d'exécution
# print(f"Temps d'exécution du tf-idf: {end - start}")
# print(f"Temps d'exécution des postings: {end_posting - start_posting}")
# temps_total_end = time.time()
# print(f"Temps d'exécution total du programme : {temps_total_end - temps_total}")