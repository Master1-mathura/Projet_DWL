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
colonne_imdb_meta = "imdbId"

#On peut faire avec une boucle comme pour MovieSum mais déja qu'avec 1800 films, c'est long alors pour plus de 80k films 
metadata["imdb_nettoyer"] = metadata[colonne_imdb_meta].apply(nettoyer_IMDB_ID)



####################################
#       1.CREATION DU CORPUS
#####################################

#On verifie l'existance de la colonne item_id dnas la metadata
#On a besoin des id film données par TagGenome pour le score, tags...
if "item_id" in metadata.columns:
    id_colonne = "item_id"


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
corpus.to_sql("collection_test/corpus.json",orient="records",force_ascii=False,indent=2)

print("-" * 30)
print(f"🎬 Corpus : {len(corpus)} films (Scripts complets)")