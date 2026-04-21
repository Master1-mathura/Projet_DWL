import requests
from flask import Flask, jsonify, request
import repository
import search_moteur

app = Flask(__name__)
TMDB_KEY = "b78f8df42770d71ac2d434fc023adf18"
search_moteur.init_model()

@app.route('/')
def home():
    return "WELCOME TO DON'T WATCHLIST"

@app.route('/search',methods=['POST'])
def searchMovie():
    # ----- AJOUT POUR PP :
    # on récupère la query envoyée par le PHP
    data = request.get_json()
    user_query = data.get('query', '')
    if not user_query:
        return jsonify([]), 200
    
    # stockage de score pour donner la couleur de l'étiquette
    resultats = search_moteur.rechercher(user_query)

    resultats_finaux = []
    for film in resultats:
        score = film['score']        
        if score > 0.6:
            film['color'] = 'red'
        elif score > 0.3:
            film['color'] = 'orange'
        else:
            film['color'] = 'green'
        resultats_finaux.append(film)
    return jsonify(resultats_finaux), 200 #on envoie au php

@app.route('/total_watchlist', methods=['GET'])
def getWatchlist():
    watchlist = repository.get_all()
    return jsonify(watchlist),200
@app.route('/get_metadata',methods=['POST'])
def get_metadata():
    data = request.get_json()
    imdbID = data.get('film_ID')

    url = f"https://api.themoviedb.org/3/find/{imdbID}?api_key={TMDB_KEY}&external_source=imdb_id"
    response = requests.get(url)
    tmbd_data = response.json()

    if tmbd_data.get('movie_results'):
        movie_info = tmbd_data['movie_results'][0]

        data = {"id" : imdbID,
                "title" : movie_info.get('title'),
                "synposis" : movie_info.get('overview'),
                "poster" : f"https://image.tmdb.org/t/p/w500{movie_info.get('poster_path')}",
                "background" : f"https://image.tmdb.org/t/p/original{movie_info.get('backdrop_path')}",
                "score" : movie_info.get('vote_average')
                }
        return jsonify(data),200
    return jsonify({"erreur" : "Movie not found"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=4000,debug=False)