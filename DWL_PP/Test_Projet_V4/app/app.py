from flask import Flask, jsonify, request
import repository
import search_moteur

app = Flask(__name__)
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

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=4000,debug=False)