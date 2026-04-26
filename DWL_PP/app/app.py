import traceback
import requests
from flask import Flask, jsonify, request
import repository
import search_moteur

app = Flask(__name__)

TMDB_KEY = "b78f8df42770d71ac2d434fc023adf18"

search_moteur.init_model()

@app.errorhandler(Exception)
def handle_global_error(e):
    print(traceback.format_exc()) 
    return jsonify({
        "error": "Internal Error.",
        "details": str(e)
    }), 500

@app.route('/')
def home():
    return "WELCOME TO DON'T WATCHLIST"

@app.route('/search',methods=['GET'])
def searchMovie():
    user_query = request.args.get('q', '')

    if not user_query:
        return jsonify([]), 200
    
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
    return jsonify(resultats_finaux), 200


@app.route('/movies/<string:imdbID>',methods=['GET'])
def get_metadata(imdbID):
    url = f"https://api.themoviedb.org/3/find/{imdbID}?api_key={TMDB_KEY}&external_source=imdb_id"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "TMDB error"}), 502
    tmbd_data = response.json()

    if tmbd_data.get('movie_results'):
        movie_info = tmbd_data['movie_results'][0]
        
        data = {"imdbID" : imdbID, 
                "title" : movie_info.get('title'),
                "synposis" : movie_info.get('overview'),
                "poster" : f"https://image.tmdb.org/t/p/w500{movie_info.get('poster_path')}",
                "background" : f"https://image.tmdb.org/t/p/original{movie_info.get('backdrop_path')}",
                "score" : movie_info.get('vote_average')
                }
        return jsonify(data),200
    return jsonify({"error" : "Movie not found."}), 404

@app.route('/watchlist/<int:user_id>', methods=['GET'])
def getWatchlist(user_id):
    if not user_id:
         return jsonify({"error" : "user_id manquant"}), 400
    watchlist = repository.get_all(user_id)
    return jsonify(watchlist),200

@app.route('/watchlist',methods=['POST'])
def ajout_watchlist():
    data = request.get_json()
    output = repository.add_movies(data)
    return jsonify(output),201

@app.route('/watchlist/<string:imdbID>/<int:user_id>', methods=['DELETE'])
def deleteMovie(imdbID, user_id):
    success = repository.delete_movie(imdbID, user_id)
    if not success:
        return jsonify({"error": "Movie not found in watchlist."}), 404
    return jsonify({"message": "Deleted successfully"}), 200

@app.route('/watchlist/<string:imdbID>', methods=['PUT'])
def updateMovie(imdbID):
    data = request.get_json(silent=True) or {} 
    nv_etat = data.get('etat')
    user_id = data.get('user_id')
    if not nv_etat or not user_id:
        return jsonify({"error": "Données manquantes."}), 400 
    success = repository.update_movie_state(imdbID, nv_etat, user_id)
    if not success:
        return jsonify({"error": "Film non trouvé dans votre watchlist."}), 404 
    return jsonify({"message": "Mis à jour avec succès", "etat": nv_etat}), 200

@app.route('/compte', methods=['POST'])
def creation_user():
    data = request.get_json()
    output = repository.creation_user(data)
    if output == -1:
        return jsonify({"error" : "This username already exists, choose another one."}),409
    return jsonify({"message" : "Account created"}), 201

@app.route('/connexion',methods=['POST'])
def connexion():
    data = request.get_json()
    output = repository.connexion(data)
    if output is None:
        return jsonify({"error" : "Incorrect Username or Password."}),401
    return jsonify({"message" : "Connecting ...", "data" : output}),200

@app.route('/compte/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    output = repository.update_user(id,data)
    if output == 0:
        return jsonify({"error" : "ID not found"}),404
    elif output == -1 :
        return jsonify({"error" : "This username already exists, choose another one."}),409
    elif output == -2:
        return jsonify({"error" : "The old password is incorrect."}), 403
    elif output == -3:
        return jsonify({"error" : "Username identical to the current one, choose another one."}),400

    return jsonify({"message" : "Changed successfully."}),200

@app.route('/compte/<int:id>', methods=["DELETE"])
def delete_user(id):
    output = repository.delete_user(id)
    if output == 0:
        return jsonify({"error" : "Deletion Error"})
    return jsonify({"message" : "Account Deleted"})

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=4000,debug=False)