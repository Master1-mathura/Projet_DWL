import pandas as pd
import time
import math
import numpy as np
from nltk.corpus import stopwords
from nltk import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import wordnet as wn 
from nltk.corpus import brown
from nltk.tag import UnigramTagger

# ******************************************************************************** #
# ************************ Étape 1 : Prétraitement du texte ************************* #
# ******************************************************************************** #

# Nettoyage du script pour n'avoir que l'essentiel
def parsing_script(script,dico):
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
            mot_lower = mot.lower()
            if mot_lower in dico.keys() : 
                mot = mot_lower + " " + dico[mot_lower]
            scene_description.append(mot) 
    return " ".join(scene_description)

def theme_dico(liste_theme):
    mot_a_theme = {}
    for theme in liste_theme : 
        theme_lower = theme.lower()
        mot_virtuel = f"THEME_{theme.upper()}"
        mot_a_theme[theme_lower] = mot_virtuel
        
        synset = wn.synsets(theme)[0]
        for hypo in synset.hyponyms():
            for lemma in hypo.lemmas():
                theme_mot = lemma.name().lower().replace("_"," ").replace("-", " ")
                mot_a_theme[theme_mot.lower()] = mot_virtuel
    return mot_a_theme 

# Chargement des données
temps_total = time.time()
df = pd.read_json("Dataset_Projet_TAL/collection_test/corpus.json", encoding="utf-8")
liste_theme = ["violence","arachnid","snake","blood","insect","monster"]
mot_a_theme = theme_dico(liste_theme)
df['text'] = df['text'].apply(lambda x: parsing_script(x,mot_a_theme))

docs = df.set_index('doc_id').to_dict(orient='index')

# ******************************************************************************** #
# ******************** Étape 2 : Création de l'index inversé ********************* #
# ******************************************************************************** #
tokenizer = RegexpTokenizer(r"\w+")
start_posting = time.time()
stopwords_set = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
# Pour optimiser en évitant de re-lemmatiser plusieurs fois un même mot
lemme = {}
postings = {}
tagger = UnigramTagger(brown.tagged_sents())

for filmID, data in docs.items():
    script = data["text"]
    tokens = script.split()
    
    liste_postag = tagger.tag(tokens)
    for mot, tag in liste_postag:
        if mot.startswith("THEME_"):
            t = mot
        elif tag not in ('NNP', 'NNPS','MD',None) :
            token_lower = mot.lower() 
            if token_lower not in stopwords_set:
                if token_lower  not in lemme : 
                    lemme[token_lower] = lemmatizer.lemmatize(token_lower)
                t = lemme[token_lower]
            else : 
                continue
        else :
            continue
        # Remplissage de l'index inversé
        if t not in postings :
            postings[t] = {}
        if filmID not in postings[t]:
            postings[t][filmID] = 1
        else : 
            postings[t][filmID] +=1
end_posting = time.time()

# ******************************************************************************** #
# ********************** Étape 3 : Calcul des scores TF-IDF ********************** #
# ******************************************************************************** #

start = time.time()
N = len(docs)
# Calcul de l'IDF pour chaque terme du vocabulaire 
idf_score = {terme : math.log((N) / len(postings[terme])) + 1 for terme in postings}
# Création d'une liste des mots, elle doit être fixe pour comparer les vecteurs
liste_terme = list(postings.keys())

# Initialisation des vecteurs TF*IDF
n_liste_terme = len(liste_terme)
tf_idf = {filmID : [0.0] * n_liste_terme for filmID in docs}

# Remplissage des vecteurs TF*IDF
log10 = math.log10
for i,terme in enumerate(postings):
    score_idf = idf_score[terme]
    for filmID,tf in postings[terme].items():
        tf_idf[filmID][i] = (1 + log10(tf)) * score_idf
end = time.time()

# ******************************************************************************** #
# ********************** Étape 4 : Traitement de la requête ********************** #
# ******************************************************************************** #

def traitement_requete(query, dico_theme = mot_a_theme):
    tokens = tokenizer.tokenize(query)
    queryterms = []
    for mot in tokens:
        mot_lower = mot.lower()

        if mot_lower not in stopwords_set:
            lemme_mot = lemmatizer.lemmatize(mot_lower)
            queryterms.append(lemme_mot)    

        if mot_lower in dico_theme.keys():
            queryterms.append(dico_theme[mot_lower])
            lemme_mot = lemmatizer.lemmatize(mot_lower)
            queryterms.append(lemme_mot)

    vecteur_query = [0.0] * len(liste_terme)
    terme_index = {term : i for i,term in enumerate(liste_terme)}
    for mot in queryterms : 
        if mot in postings : 
            index = terme_index[mot]
            tf = queryterms.count(mot)
            vecteur_query[index] = (1 + log10(tf)) * idf_score[mot]
    return vecteur_query

# ******************************************************************************** #
# ****************** Étape 5 : Calcul des scores de similarité ******************* #
# ******************************************************************************** #

def scores_simi(vecteur_query, n = 5):  
    vect_query_arr = np.array(vecteur_query).reshape(1,-1)

    score_similarite = {}
    for filmID, vecteur in tf_idf.items() :
        vecteur_film_arr = np.array(vecteur).reshape(1,-1)
        # Similarité cosinus
        cos = cosine_similarity(vect_query_arr,vecteur_film_arr)[0][0]
        score_similarite[filmID] = cos

    # Tri pour avoir les 5 meilleurs scores -> les films à éviter à toçut prix
    pires_n_films = sorted(score_similarite.items(), key=lambda x: x[1], reverse = True)[:n]

    liste_scores_films_trie = []

    for (filmID, score) in pires_n_films:
        liste_scores_films_trie.append((filmID, score))
    return liste_scores_films_trie


def pseudo_relevance_feedback(tfidf_matrice,vecteur_requete,top_results, alpha=0.7, k = 10):

    pseudo_pertinents_id = [docID for docID,_ in top_results[:k]]
    if len(pseudo_pertinents_id) == 0:
        return vecteur_requete

    revelant_vectors = [np.array(tfidf_matrice[idx]) for idx in pseudo_pertinents_id]
    moyenne_pertinent = np.mean(revelant_vectors,axis=0)

   
    augmented_query_vecteur = np.array(vecteur_requete) + alpha * moyenne_pertinent

    return augmented_query_vecteur.tolist()


texte_requete_utilisateur = input("What are you afraid of ? ")
res_recherche_init  = 5

vect_requete = traitement_requete(texte_requete_utilisateur)
top_res = scores_simi(vect_requete)

vect_prf = pseudo_relevance_feedback(tf_idf,vect_requete,top_res)
res_finaux = scores_simi(vect_prf)

print(f"Here are the top {res_recherche_init} movies that you should avoid : \n")
for id,score in res_finaux[:res_recherche_init]:
    print(f"Movie : {docs[id]['title']} (Score : {score})\n")
temps_total_end = time.time()
print(f"Temps d'exécution total du programme : {temps_total_end - temps_total}")
