from flask import Flask, jsonify, request
#Créer l'application
app = Flask(__name__)

#Definir les routes
@app.route('/')
def home():
    return "WELCOME TO DON'T WATCHLIST"


@app.route('/search',methods=['GET'])
def searchMovie():
    new_student = request.get_json()
    
    return jsonify(new_student),201
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=4000,debug=True)