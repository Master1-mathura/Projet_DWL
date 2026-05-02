import pytest
from app import app
#Le mock doit simuler ce que renvoie VRAIMENT repository.add_movies
#add_movie prend 'data' en paramètre, donc notre mock aussi

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_search_empty(client):
    response = client.get("/search")
    assert response.status_code == 200
    assert response.json == []

def test_search_query(client, monkeypatch):
    def fake_search(query):
        return [
            {"title": "Spider-Man", "score": 0.8}
        ]
    monkeypatch.setattr("app.search_moteur.rechercher", fake_search)
    response = client.get("/search?q=spiders")
    assert response.status_code == 200
    assert response.json[0]['color'] == '#9b2c3b'

####################
# WATHCLIST
####################

def test_get_watchlist_success(client,monkeypatch):
    def fake_get_all(user_id):
        return [
            {
                "imdbID": "tt0295297",
                "user_id": 1,
                "title": "Harry Potter : Chamber of Secrets",
                "poster": "poster.jpg",
                "background": "bg.jpg"
            }
        ]
    monkeypatch.setattr("app.repository.get_all",fake_get_all)
    response = client.get("/watchlist/1")
    assert response.status_code == 200
    assert response.json[0]["title"] == "Harry Potter : Chamber of Secrets"


def test_add_watchlist_success(client,monkeypatch):
    def fake_add_movies(data):
        return "The movie has been added to your watchlist successfully !"
    monkeypatch.setattr("app.repository.add_movies",fake_add_movies)

    data = {
        "imdbID": "tt0295297",
        "user_id": 1,
        "title": "Harry Potter : Chamber of Secrets",
        "poster": "poster.jpg",
        "background": "bg.jpg"
    }

    response = client.post("/watchlist",json=data)

    assert response.status_code == 201
    assert response.json == "The movie has been added to your watchlist successfully !"

def test_delete_watchlist_success(client,monkeypatch):
    def fake_delete_movie(imdbID,userID):
        return 1
    monkeypatch.setattr("app.repository.delete_movie",fake_delete_movie)

    response = client.delete("/watchlist/1/tt0295297")

    assert response.status_code == 200
    assert response.json["message"] == "Deleted successfully"

def test_delete_watchlist_not_found(client,monkeypatch):
    def fake_delete_movie(imdbID,userID):
        return None
    monkeypatch.setattr("app.repository.delete_movie",fake_delete_movie)

    response = client.delete("/watchlist/1/FilmInconnu")

    assert response.status_code == 404
    assert response.json["error"] == "Movie not found in watchlist."


def test_update_watchlist_success(client,monkeypatch):
    def fake_update_movie(imdbID,nvEtat,userID):
        return 1

    monkeypatch.setattr("app.repository.update_movie_state",fake_update_movie)
    data = {"etat" : "Survécu"}
    response = client.put("/watchlist/1/tt0295297",json=data)

    assert response.status_code == 200
    assert response.json["message"] == "Mis à jour avec succès"
    assert response.json["etat"] == "Survécu"

def test_update_watchlist_missing_data(client):
    data = {}
    response = client.put("/watchlist/1/tt0295297",json=data)
    assert response.status_code == 400
    assert response.json["error"] == "Données manquantes."

def test_update_watchlist_not_found(client,monkeypatch):
    def fake_update_fail(imdbID, nvEtat, userID):
        return None
    monkeypatch.setattr("app.repository.update_movie_state",fake_update_fail)
    data = {"etat" : "Survécu"}
    response = client.put("/watchlist/1/tt0295297",json=data)

    assert response.status_code == 404
    assert response.json["error"] == "Film non trouvé dans votre watchlist."


####################
# COMPTE
####################

def test_creation_user_success(client,monkeypatch):
    def fake_success_creation(data):
        return 0

    monkeypatch.setattr("app.repository.creation_user",fake_success_creation)

    data = {"username" : "Test", "password" : "Test123456"}
    response = client.post("/compte",json=data)

    assert response.status_code == 201
    assert response.json["message"] == "Account created"

def test_creation_user_already_exists(client,monkeypatch):
    def fake_failed_creation(data):
        return -1

    monkeypatch.setattr("app.repository.creation_user",fake_failed_creation)
    data = {"username" : "Test", "password" : "Test123456"}
    response = client.post("/compte",json=data)
    assert response.status_code == 409
    assert response.json["error"] == "This username already exists, choose another one."

def test_connexion_success(client,monkeypatch):
    def fake_success_connexion(data):
        return {"id" : "1", "username" : "Test"}

    monkeypatch.setattr("app.repository.connexion",fake_success_connexion)
    data = {"username" : "Test", "password" : "Test123456"}

    response = client.post("/connexion",json=data)

    assert response.status_code == 200
    assert response.json["message"] == "Connecting ..."
    assert response.json["data"]["id"] == "1"

def test_connexion_incorrect(client,monkeypatch):
    def fake_failed_connexion(data):
        return None

    monkeypatch.setattr("app.repository.connexion",fake_failed_connexion)
    data = {"username" : "Test", "password" : "Test123456"}

    response = client.post("/connexion",json=data)
    assert response.status_code == 401
    assert response.json["error"] == "Incorrect Username or Password."


################
# GESTION PROFIL
#################

def test_update_user_success(client,monkeypatch):
    def fake_update_success(identifiant,data):
        return 1
    monkeypatch.setattr("app.repository.update_user",fake_update_success)
    data = {
        "username" : "Testeur",
        "old_mdp" : "Test123456",
        "mdp" : "Testing"
    }
    response = client.put("/compte/1",json=data)
    assert response.status_code == 200
    assert response.json["message"] == "Changed successfully."

def test_update_user_id_not_found(client,monkeypatch):
    def fake_update_id_not_found(identifiant,data):
        return 0
    monkeypatch.setattr("app.repository.update_user",fake_update_id_not_found)
    data = {
        "username" : "Testeur",
        "old_mdp" : "Test123456",
        "mdp" : "Testing"
    }
    response = client.put("/compte/1",json=data)
    assert response.status_code == 404
    assert response.json["error"] == "ID not found"


def test_update_username_taken(client,monkeypatch):
    def fake_update_username_taken(identifiant,data):
        return -1
    monkeypatch.setattr("app.repository.update_user",fake_update_username_taken)
    data = {
        "username" : "Testeur",
        "old_mdp" : "Test123456",
        "mdp" : "Testing"
    }
    response = client.put("/compte/1",json=data)
    assert response.status_code == 409
    assert response.json["error"] == "This username already exists, choose another one."

def test_update_user_wrong_old_password(client,monkeypatch):
    def fake_update_wrong_oldmdp(identifiant,data):
        return -2
    monkeypatch.setattr("app.repository.update_user",fake_update_wrong_oldmdp)
    data = {
        "username" : "Testeur",
        "old_mdp" : "Test123456",
        "mdp" : "Testing"
    }
    response = client.put("/compte/1",json=data)
    assert response.status_code == 403
    assert response.json["error"] == "The old password is incorrect."

def test_update_user_identical_username(client,monkeypatch):
    def fake_update_identical_username(identifiant,data):
        return -3
    monkeypatch.setattr("app.repository.update_user",fake_update_identical_username)
    data = {
        "username" : "Testeur",
        "old_mdp" : "Test123456",
        "mdp" : "Testing"
    }
    response = client.put("/compte/1",json=data)
    assert response.status_code == 400
    assert response.json["error"] == "Username identical to the current one, choose another one."

def test_delete_user_success(client,monkeypatch):
    def fake_delete_success(identifiant):
        return 1
    monkeypatch.setattr("app.repository.delete_user",fake_delete_success)
    response = client.delete("/compte/1")
    assert response.status_code == 200
    assert response.json["message"] == "Account Deleted"

def test_delete_user_failure(client,monkeypatch):
    def fake_delete_failure(identifiant):
        return 0
    monkeypatch.setattr("app.repository.delete_user",fake_delete_failure)
    response = client.delete("/compte/1")
    assert response.status_code == 400
    assert response.json["error"] == "Deletion Error"