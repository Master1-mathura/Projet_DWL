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

@app.route('/search',methods=['GET'])
def searchMovie():
    # ----- AJOUT POUR PP :
    # on récupère la query envoyée par le PHP
    user_query = request.args.get('q', '')

    if not user_query:
        return jsonify({"results": []}), 200

    # stockage de score pour donner la couleur de l'étiquette
    resultats = search_moteur.rechercher(user_query)

    resultats_finaux = []
    for film in resultats:
        score = film['score']
        if score > 0.6:
            film['color'] = '#9b2c3b'
        elif score > 0.3:
            film['color'] = '#b87322'
        else:
            film['color'] = '#2e7d52'
        resultats_finaux.append(film)
    return jsonify(resultats_finaux), 200 #on envoie au php


@app.route('/movies/<string:imdbID>',methods=['GET'])
def get_metadata(imdbID):
    url = f"https://api.themoviedb.org/3/find/{imdbID}?api_key={TMDB_KEY}&external_source=imdb_id"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "TMDB error"}), 502
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


@app.route('/watchlist', methods=['GET'])
def getWatchlist():
    watchlist = repository.get_all()
    return jsonify(watchlist),200

@app.route('/watchlist',methods=['POST'])
def ajout_watchlist():
    data = request.get_json()
    output = repository.add_movies(data)
    return jsonify(output),201

@app.route('/watchlist/<string:imdbID>',methods=['DELETE'])
def deleteMovie(imdbID):
    movie = repository.get_movie_by_id(imdbID)
    if not movie:
        return jsonify({"Movie not found in watchlist."})
    repository.delete_movie(imdbID)
    return jsonify(movie), 200

@app.route('/watchlist/<string:imdbID>', methods=['PUT'])
def updateMovie(imdbID):
    data = request.get_json()
    nv_etat = data.get('etat')
    if not nv_etat:
        return jsonify({"No given tag."}), 400
    movie = repository.get_movie_by_id(imdbID)
    if not movie:
        return jsonify({"No movies found."}), 404
    repository.update_movie_state(imdbID, nv_etat)
    return jsonify({"erreur": "Updated successfully", "etat": nv_etat}), 200

@app.route('/compte', methods=['POST'])
def creation_user():
    data = request.get_json()
    output = repository.creation_user(data)
    if output == -1:
        return jsonify({"error" : "Ce nom utilisateur existe déja, veuillez choisir autre"}),409
    return jsonify({"message" : "Votre compte a été creer"}), 201

@app.route('/connexion',methods=['POST'])
def connexion():
    data = request.get_json()
    output = repository.connexion(data)
    if output is None:
        return jsonify({"error" : "Identifiant ou Mot de passe Incorrect"}),401
    return jsonify({"message" : "Connecter ...", "data" : output}),200

@app.route('/compte/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    output = repository.update_user(id,data)
    if output == 0:
        return jsonify({"error" : "ID non trouvée"}),404
    elif output == -1 :
        return jsonify({"error" : "Le Username existe déjà, veuillez choisir un autre"}),409
    elif output == -2:
        return jsonify({"error" : "L'ancien mot de passe est incorrect."}), 403
    elif output == -3:
        return jsonify({"error" : "Nom d'utilisateut identique à l'actuelle"}),400

    return jsonify({"message" : "Modification effectué"}),200
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=4000,debug=False)