import pandas as pd
import time
import math
import numpy as np
from nltk.corpus import stopwords
from nltk import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#------------A VERIFIER---------------------
# Voici comment on stocke dans le film_csv : 
# { 
#     5816 : { 
#         "title" : "Harry Potter and the chamber of secret",
#         "scenes" : wide helicopter shot. privet drive. camera cranes down, down, over the rooftops 
#             harry pages through a scrapbook, stops on a moving photo...
#     }
# }
# 


def parsing_script(script):
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
            scene_description.append(mot.lower()) 
    return " ".join(scene_description)

df = pd.read_json("Dataset_Projet_TAL/collection_test/corpus.json", encoding="utf-8")
df['text'] = df['text'].apply(parsing_script)

docs = df.set_index('doc_id').to_dict(orient='index')

start_posting = time.time()
postings = {}
stopwords = set(stopwords.words("english"))
tokenizer = RegexpTokenizer(r"\w+")
lemmatizer = WordNetLemmatizer()
for filmID, data in docs.items():
    script = data["text"]
    tokens=tokenizer.tokenize(script)
    for t in tokens : 
        if t not in stopwords:
            t = lemmatizer.lemmatize(t)
            if t not in postings :
                postings[t] = {}
            if filmID not in postings[t]:
                postings[t][filmID] = 1
            else : 
                postings[t][filmID] +=1

end_posting = time.time()



start = time.time()
N = len(docs)
#Optimisation possible : 
#   Au lieu de passer de panda à dico, on reste sur pandas
#   Et donc on pourra utiliser TfidfVectorizer() sur une colonne où on aura enlever les stopwords , fait les lemmatisation 

tf_idf = {}
idf_score = {terme : math.log(N / len(postings[terme])) for terme in postings}
liste_terme = list(postings.keys())
for filmID in docs : 
    tf_idf[filmID] = [0.0] * len(liste_terme)

for i,terme in enumerate(postings):
    score_idf = idf_score[terme]
    for filmID,tf in postings[terme].items():
        if filmID in tf_idf  : 
            tf_idf[filmID][i] = tf * score_idf

end = time.time()

query = "I am afraid of spider"
tokens = tokenizer.tokenize(query.lower())
queryterms = [lemmatizer.lemmatize(t) for t in tokens if t not in stopwords]

vecteur_query = [0.0] * len(liste_terme)
for mot in queryterms : 
    if mot in postings : 
        index = liste_terme.index(mot)
        tf = queryterms.count(mot)
        vecteur_query[index] = tf * idf_score[mot]

vect_query_arr = np.array(vecteur_query).reshape(1,-1)
maximum = -2
not_watch = None
for filmID, vecteur in tf_idf.items() : 
    vecteur_film_arr = np.array(vecteur).reshape(1,-1)
    cos = cosine_similarity(vect_query_arr,vecteur_film_arr)[0][0]
    if(cos > maximum):
        maximum = cos
        not_watch = filmID 

print("LE FILM A EVITER : ", docs[not_watch]["title"])
print("SCORE DE SIMILARITE :", maximum)

print(f"Execution temps tf-idf: {end - start}")
print(f"Execution temps postings: {end_posting - start_posting}")
