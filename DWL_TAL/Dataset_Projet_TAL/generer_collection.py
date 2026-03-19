import pandas as pd
import os
from datasets import load_dataset
if not os.path.exists("collection_test"):
    os.makedirs("collection_test") 

def nettoyer_IMDB_ID(id):
    id = str(id)
    #pd.isna : Méthode panda qui permet d'identifier les données manquantes NaN ou None
    if id == "" or pd.isna(id):
        return ""
    id = id.replace("tt","").lstrip("0") #On supprime les tt et tout les 0 devant l'ID
    return id


ds = load_dataset("rohitsaxena/MovieSum")
#Un DataFrame est une structure de données en tableau comme sur Excel ou un tableau SQL
#En DataFrame c'est plus simple de manipuler les données
MovieSum = pd.DataFrame(ds["train"]) #On récupere les données "train" avec le DataFrame de panda 

#On va charger les fichiers de TAG-Genome 

#On des fichier JSON en format JSON Lines, donc on met lines=True car chaque ligne est un objet JSON séparé 
#Les fonctions pd.read_x() lis les données et les transforme en DataFrame
metadata = pd.read_json("raw/metadata_updated.json",lines = True)
tags = pd.read_json("raw/tags.json",lines = True)
scores = pd.read_csv("scores/tagdl.csv")

clean_imdb = []
#On nettoie chaque IMDB de MovieSum
for id in MovieSum["imdb_id"]:
    new_id = nettoyer_IMDB_ID(id)
    clean_imdb.append(new_id)

MovieSum["imdb_nettoyer"] = clean_imdb

# La ligne ci-dessous permet de faire la meme chose mais plus rapidement :
#df_moviesum['imdb_nettoyer'] = df_moviesum['imdb_id'].apply(nettoyer_IMDB_ID)
# Fait exactement la même chose que la boucle, mais plus rapidement et en une ligne

#On verifie l'existance de la colonne imdbID dans le DataFrame metadata
if "imdbId" in metadata.columns:
    colonne_imdb_meta = "imdbId"
else : # Selon la version de Tag Genome, la colonne peut s'appeler 'imdbId' ou 'imdb_id'
    colonne_imdb_meta = "imdb_id"

#On peut faire avec une boucle comme pour MovieSum mais déja qu'avec 1800 films, c'est long alors pour plus de 80k films 
metadata["imdb_nettoyer"] = metadata[colonne_imdb_meta].apply(nettoyer_IMDB_ID)



####################################
#       1.CREATION DU CORPUS
#####################################

#On verifie l'existance de la colonne item_id dnas la metadata
#On a besoin des id film données par TagGenome pour le score, tags...
if "item_id" in metadata.columns:
    id_colonne = "item_id"
else:
    id_colonne = "id"

#La liste de ce qu'on veut fusionner : 
moviesum_colonne_fusion = ["movie_name","script","imdb_nettoyer"]
metadata_colonne_fusion = [id_colonne,"imdb_nettoyer"] 

#On fusionne les deux Datarames sur la colonne imdb_nettoyer
corpus = pd.merge(MovieSum[moviesum_colonne_fusion], metadata[metadata_colonne_fusion],on="imdb_nettoyer")

#On renomme les colonnes (pour avoir un formmat standard IR) 
#Pas obligé 
corpus = corpus.rename(columns={id_colonne: 'doc_id', 'movie_name': 'title','script': 'text' })

#On supprime les doublons de films
corpus = corpus.drop_duplicates(subset=["doc_id"])

#On garde que les 3 colonnes finales
corpus = corpus[['doc_id','title','text']]

#On sauvegarde notre corpus sous format csv et json 
#orient = "records" : Chaque ligne devient un objet JSON ([{"doc_id" : ... , "title" : ..., "text" : ...}])
#force_ascii = False : Garde les caracrères accentués corrects
corpus.to_json("collection_test/corpus.json",orient="records",force_ascii=False,indent=2)
# index = False : Sert a ne pas mettre des numeros de ligne dans le CSV
# corpus.to_csv("collection_test/corpus.csv",index=False,encoding="utf-8")


####################################
#       2.QUERIES 
#####################################

#Dictionnaire des thèmes sensibles et phrase qu'on a choisit : 

requetes = {
    "blood": "Are there any movies with extremely bloody and graphic violence?",
    "clowns": "I have a phobia of clowns, which films should I be careful about?",
    "torture": "Are there any scenes involving physical or psychological torture?",
    "ghosts": "I want to avoid scenes with ghosts or supernatural hauntings, what should I filter?",
    "cannibalism": "Does this film depict scenes of cannibalism or eating human flesh?",
    "murder": "Are there disturbing sequences showing detailed murder or serial killers?",
    "gore": "Is there a lot of gore and body horror in this movie's script?",
    "suicide": "Does the script contain depictions of suicide or self-harm?",
    "monsters": "Are there any jump scares involving monsters or creepy creatures?",
    "death": "I am sensitive to themes of death and dying, is this movie safe for me?",
    "dark": "Are there any intense scenes with dark, claustrophobic atmospheres?"
}

#Comme avant on recuperer les colonnes à utiliser 
if "tag" in tags.columns : 
    tag_colonne = "tag"
else :
    tag_colonne = "text"

if "id" in tags.columns:
    id_tag_colonne = "id"
else : 
    id_tag_colonne = "tag_id"
#Filtrer les tags présents dans notre dictionnaire

#On transforme les tag en miniscules pour comparer facilement
#tags[tag_colonne] : C'est de type Series contenant les tags, c'est pourquoi on convertit en str
tag_lower = tags[tag_colonne].str.lower()
tags_a_garder = tag_lower.isin(requetes.keys())
#On peut faire sous forme de boucle mais c'st trop long

selectionner = tags[tags_a_garder].copy()

#On ajoute la requete correspondant au tag
selectionner['text_human'] = selectionner[tag_colonne].str.lower().map(requetes)

queries = selectionner.rename(columns={id_tag_colonne :"query_id", "text_human" : "text"})

#Je selectionne juste query_id et text parce qu'on veut pas le tag dans queries.json
queries[["query_id","text"]].to_json("collection_test/queries.json",orient="records",indent=2)


####################################
#       3.QRELS
#####################################

#On commence par fusionner les scores avec les requetes sélectionnées
#On utilise la colonne "tag" dans le DataFrame scores et le nom du tag dans selectionner
qrels = pd.merge(scores,selectionner[[id_tag_colonne,tag_colonne]],left_on='tag',right_on=tag_colonne)

#On recupere les films dans notre corpus
doc_ids = corpus['doc_id'].unique()
#On filtre pour garder uniquement les films présent dans le corpus
qrels = qrels[qrels["item_id"].isin(doc_ids)]

qrels = qrels.rename(columns={id_colonne : "doc_id", id_tag_colonne : "query_id"})
qrels[['query_id','doc_id','score']].to_csv("collection_test/qrels.csv",index=False)

print("-" * 30)
print(f"🎬 Corpus : {len(corpus)} films (Scripts complets)")
print(f"📌 Queries : {len(queries)} requêtes humaines")
print(f"📈 Qrels : {len(qrels)} jugements de pertinence")