from flask import Flask, jsonify, request
import repository

#Créer l'application
app = Flask(__name__)

#Definir les routes
@app.route('/')
def home():
    return "WELCOME TO DON'T WATCHLIST"


@app.route('/search',methods=['POST'])
def searchMovie():

    new_student = request.get_json()
    data_sql = repository.add_data(new_student)
    return jsonify(data_sql),201


@app.route('/total_watchlist', methods=['GET'])
def getWatchlist():
    watchlist = repository.get_all()
    return jsonify(watchlist),200

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=4000,debug=True)