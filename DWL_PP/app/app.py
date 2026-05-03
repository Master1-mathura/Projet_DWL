import traceback
import requests
import time
import os
import repository
import search_moteur
from flasgger import Swagger
from flask import Flask, jsonify, request
from db import init_db
from sqlalchemy.exc import OperationalError, DatabaseError

app = Flask(__name__)
swagger = Swagger(app)

TMDB_KEY = "b78f8df42770d71ac2d434fc023adf18"

if os.getenv("TESTING") != "1":
    search_moteur.init_model()
    max_retries = 10
    for i in range(max_retries):
        try:
            init_db()
            repository.init_default_badges()
            print("Connexion à la base de données réussie !")
            break 
        except (OperationalError, DatabaseError) as e:
            print(f"Base de données non prête, tentative {i+1}/{max_retries} dans 3 secondes...")
            time.sleep(3)
    else:
        print("Erreur critique : Impossible de se connecter à la base de données après plusieurs tentatives.")

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
    """
    Rechercher un film
    ---
    parameters:
      - name: q
        in: query
        type: string
        required: true
        description: Terme de recherche
    responses:
      200:
        description: Liste de films avec score et couleur
    """
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
    """
    Métadonnées d'un film via TMDB
    ---
    parameters:
      - name: imdbID
        in: path
        type: string
        required: true
        description: ID IMDb (ex tt0111161)
    responses:
      200:
        description: Titre, synopsis, poster, background, score
      404:
        description: Film introuvable
      502:
        description: Erreur côté TMDB
    """
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
    """
    Récupérer la watchlist d'un utilisateur
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Liste des films dans la watchlist
    """
    if not user_id:
        return jsonify({"error" : "user_id manquant"}), 400
    watchlist = repository.get_all(user_id)
    return jsonify(watchlist),200

@app.route('/watchlist',methods=['POST'])
def ajout_watchlist():
    """
    Ajouter un film à la watchlist
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            user_id:
              type: integer
            imdbID:
              type: string
            etat:
              type: string
    responses:
      201:
        description: Film ajouté avec succès
    """
    data = request.get_json()
    output = repository.add_movies(data)
    return jsonify(output),201

@app.route('/watchlist/<int:user_id>/<string:imdbID>', methods=['DELETE'])
def deleteMovie(user_id,imdbID):
    """
    Supprimer un film de la watchlist
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
      - name: imdbID
        in: path
        type: string
        required: true
    responses:
      200:
        description: Supprimé avec succès
      404:
        description: Film introuvable dans la watchlist
    """
    success = repository.delete_movie(imdbID, user_id)
    if not success:
        return jsonify({"error": "Movie not found in watchlist."}), 404
    return jsonify({"message": "Deleted successfully"}), 200

@app.route('/watchlist/<int:user_id>/<string:imdbID>', methods=['PUT'])
def updateMovie(user_id,imdbID):
    """
    Mettre à jour l'état d'un film
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
      - name: imdbID
        in: path
        type: string
        required: true
      - name: body
        in: body
        required: true
        schema:
          properties:
            etat:
              type: string
    responses:
      200:
        description: État mis à jour
      400:
        description: Données manquantes
      404:
        description: Film introuvable dans la watchlist
    """
    data = request.get_json(silent=True) or {}
    nv_etat = data.get('etat')
    if not nv_etat or not user_id:
        return jsonify({"error": "Données manquantes."}), 400
    success = repository.update_movie_state(imdbID, nv_etat, user_id)
    if not success:
        return jsonify({"error": "Film non trouvé dans votre watchlist."}), 404
    return jsonify({"message": "Mis à jour avec succès", "etat": nv_etat}), 200

@app.route('/compte', methods=['POST'])
def creation_user():
    """
    Créer un compte
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      201:
        description: Compte créé
      409:
        description: Nom d'utilisateur déjà pris
    """
    data = request.get_json()
    output = repository.creation_user(data)
    if output == -1:
        return jsonify({"error" : "This username already exists, choose another one."}),409
    return jsonify({"message" : "Account created"}), 201

@app.route('/connexion',methods=['POST'])
def connexion():
    """
    Se connecter
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Connexion réussie
      401:
        description: Identifiants incorrects
    """
    data = request.get_json()
    output = repository.connexion(data)
    if output is None:
        return jsonify({"error" : "Incorrect Username or Password."}),401
    return jsonify({"message" : "Connecting ...", "data" : output}),200

@app.route('/compte/<int:id>', methods=['PUT'])
def update_user(id):
    """
    Modifier un compte
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          properties:
            username:
              type: string
            old_password:
              type: string
            new_password:
              type: string
    responses:
      200:
        description: Modifié avec succès
      400:
        description: Nom identique au précédent
      403:
        description: Ancien mot de passe incorrect
      404:
        description: ID introuvable
      409:
        description: Nom d'utilisateur déjà pris
    """
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
    """
    Supprimer un compte
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Compte supprimé
      400:
        description: Erreur de suppression
    """
    output = repository.delete_user(id)
    if output == 0:
        return jsonify({"error" : "Deletion Error"}),400
    return jsonify({"message" : "Account Deleted"}),200

@app.route('/usersettings/<int:user_id>', methods=['PUT'])
def update_user_settings(user_id):
    """
    Mettre à jour les paramètres d'un utilisateur
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          properties:
            theme:
              type: string
            langue:
              type: string
    responses:
      200:
        description: Paramètres mis à jour
      404:
        description: Utilisateur introuvable
    """
    data = request.get_json()
    output = repository.update_user_settings(user_id, data)
    if output == 0:
        return jsonify({"error": "User not found."}), 404
    return jsonify({"message": "Settings updated successfully."}), 200

@app.route('/usersettings/<int:user_id>', methods=['GET'])
def get_user_settings(user_id):
    """
    Récupérer les paramètres d'un utilisateur
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Paramètres de l'utilisateur
      404:
        description: Utilisateur introuvable
    """
    output = repository.get_user_settings(user_id)
    if output is None:
        return jsonify({"error": "User not found."}), 404
    return jsonify(output), 200

@app.route('/userbadges/<int:user_id>', methods=['POST'])
def save_user_badge(user_id):
    """
    Attribuer un badge à un utilisateur
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          properties:
            badgeName:
              type: string
    responses:
      200:
        description: Badge attribué
      400:
        description: Nom du badge manquant
      404:
        description: Utilisateur introuvable
      409:
        description: Badge introuvable
      500:
        description: Erreur lors de l'enregistrement
    """
    data = request.get_json()
    badge_name = data.get('badgeName')
    if not badge_name:
        return jsonify({"error": "Badge Name is required."}), 400
    output = repository.save_user_badge(user_id, badge_name)
    if output == -1:
        return jsonify({"error": "Badge not found."}), 409
    elif output == 0:
        return jsonify({"error": "User not found."}), 404
    elif output == -2:
        return jsonify({"error": "An error occurred while saving the badge."}), 500
    return jsonify({"message": "Badge saved successfully.","data" : output}), 200

@app.route('/userbadges/<int:user_id>', methods=['GET'])
def get_user_badges(user_id):
    """
    Badges d'un utilisateur
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Liste des badges de l'utilisateur
      404:
        description: Utilisateur introuvable
    """
    output = repository.get_user_badges(user_id)
    if output is None:
        return jsonify({"error": "User not found."}), 404
    return jsonify(output), 200

@app.route("/badges", methods = ['GET'])
def get_all_badges():
    """
    Lister tous les badges disponibles
    ---
    responses:
      200:
        description: Liste de tous les badges
      404:
        description: Aucun badge trouvé
    """
    output = repository.get_all_badges()
    if output is None:
        return jsonify({"error": "No badges found."}), 404
    return jsonify(output), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=4000,debug=False)