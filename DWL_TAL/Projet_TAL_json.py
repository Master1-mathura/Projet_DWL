import pandas as pd
import time
import math
import numpy as np
import string
from nltk.corpus import stopwords
from nltk import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import wordnet as wn 
from nltk.corpus import brown
from nltk.tag import UnigramTagger
print("IMPORT")
# ******************************************************************************** #
# ************************ Étape 0 : Nettoyage préalable ************************* #
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
            mot_sans_punct = ''.join(c for c in mot if c not in string.punctuation)
            for key,value in dico.items():
                if mot_sans_punct in value : 
                    mot = f"{mot_sans_punct} {key}"
                    break 
            scene_description.append(mot) 
    return " ".join(scene_description)

def theme_dico(liste_theme):
    mot_a_theme = {}
    for theme in liste_theme : 
        mot_virtuel = f"THEME_{theme.upper()}"
        mot_a_theme[mot_virtuel] = [theme]
        
        synset = wn.synsets(theme)[0]
        for hypo in synset.hyponyms():
            for lemma in hypo.lemmas():
                theme_mot = lemma.name().lower().replace("_"," ").replace("-", " ")
                if theme_mot not in mot_a_theme[mot_virtuel]:
                    mot_a_theme[mot_virtuel].append(theme_mot)
    return mot_a_theme 

# Chargement des données
temps_total = time.time()
df = pd.read_json("Dataset_Projet_TAL/collection_test/corpus.json", encoding="utf-8")
liste_theme = ["violence","arachnid","snake","blood","insect","monster"]
mot_a_theme = theme_dico(liste_theme)
df['text'] = df['text'].apply(lambda x: parsing_script(x,mot_a_theme))

docs = df.set_index('doc_id').to_dict(orient='index')

print("Doc créee !")
# ******************************************************************************** #
# ******************** Étape 1 : Création de l'index inversé ********************* #
# ******************************************************************************** #
tokenizer = RegexpTokenizer(r"\w+")
start_posting = time.time()
stopwords_set = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
# Pour optimiser en évitant de re-lemmatiser plusieurs fois un même mot
lemme = {}
postings = {}
tagger = UnigramTagger(brown.tagged_sents())

print("Debut postings")
# tag_map = {'J': wn.ADJ, 'V': wn.VERB, 'R': wn.ADV}
for filmID, data in docs.items():
    script = data["text"]
    tokens = script.split()
    
    liste_postag = tagger.tag(tokens)
    for mot, tag in liste_postag:
        if mot.startswith("THEME_"):
            t = mot
        #NNP : Nom Propres Singulier
        #NNPS : Nom Propres Pluriel
        #MD : Modal
        #NN-TL : Nom singulier en debut de phrase
        elif tag not in ('NNP', 'NNPS','MD','NN-TL') :
            token_lower = mot.lower() 
            if token_lower not in stopwords_set:
                if token_lower  not in lemme : 
                    # wn_tag = tag_map.get(tag[0].upper(), wn.NOUN) 
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
print("Fin postings, donc posting crée ")
# ******************************************************************************** #
# ********************** Étape 2 : Calcul des scores TF-IDF ********************** #
# ******************************************************************************** #
print("TF-IDF")
start = time.time()
N = len(docs)

tf_idf = {}

# Calcul de l'IDF pour chaque terme du vocabulaire 
idf_score = {terme : math.log((N) / len(postings[terme])) + 1 for terme in postings}
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
            tf_idf[filmID][i] = (1 + math.log10(tf)) * score_idf
end = time.time()
print("TF-IDF Done")

# ******************************************************************************** #
# ********************** Étape 3 : Traitement de la requête ********************** #
# ******************************************************************************** #
#Attention mettre le dico en param
#Par default, c'est n = 5 et dico_theme = mot_a_theme, peut-etre faire la meme pour le parsing
def traitement_requete(query, dico_theme = mot_a_theme):
    tokens = tokenizer.tokenize(query)
    tags = tagger.tag(tokens)
    queryterms = []
    for mot,_ in tags:
        mot_lower = mot.lower()
        found_theme = False
        for thm_virt, hyponyms in dico_theme.items():
            if mot_lower in hyponyms:
                queryterms.append(thm_virt)
                queryterms.append(mot_lower)
                found_theme = True
                break
        if not found_theme:
            if mot_lower not in stopwords_set:
                lemme_mot = lemmatizer.lemmatize(mot_lower)
                queryterms.append(lemme_mot)          
        
    #print("Nouvelle requete : ", queryterms)
    # Création du vecteur de la requête
    vecteur_query = [0.0] * len(liste_terme)
    terme_index = {term : i for i,term in enumerate(liste_terme)}
    for mot in queryterms : 
        if mot in postings : 
            index = terme_index[mot]
            tf = queryterms.count(mot)
            vecteur_query[index]  = (1 + math.log10(tf)) * idf_score[mot]
    return vecteur_query
# ******************************************************************************** #
# ****************** Étape 4 : Calcul des scores de similarité ******************* #
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

    res = []

    # print("Vous devriez éviter le(s) film(s) : ")
    for (filmID, score) in pires_n_films:
        res.append((filmID, score))
    return res

query = input("Enter query : ")
result = scores_simi(traitement_requete(query))
for doc_id,score in result:
    titre = docs[doc_id]["title"]
    print(f"{titre} (Score de similarité : {score})")
print(f"Temps d'exécution du tf-idf: {end - start}")
print(f"Temps d'exécution des postings: {end_posting - start_posting}")
temps_total_end = time.time()
print(f"Temps d'exécution total du programme : {temps_total_end - temps_total}")