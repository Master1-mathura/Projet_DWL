import pytest
from app import app
from db import init_db, Base, engine

@pytest.fixture
def client():
    app.config["TESTING"] = True
    init_db()
    return app.test_client()


def test_create_then_login(client):
    compte = {
        "username" : "Testeur1",
        "password" : "123456"
    }
    
    creation = client.post("/compte",json=compte)

    assert creation.status_code == 201

    connexion = client.post("/connexion",json=compte)

    assert connexion.status_code == 200
    assert connexion.json["data"]["username"] == "Testeur1"


def test_creer_compte_doublon(client):
    compte = {
        "username" : "Testeur1",
        "password" : "415263"
    }

    response = client.post("/compte",json=compte)
    assert response.status_code == 409
    assert response.json["error"] == "This username already exists, choose another one."

def test_add_movies_watchlist(client):
    data = {
        "imdbID" : "tt0295297",
        "user_id" : 1,
        "title" : "Harry Potter : Chamber of Secrets",
        "poster": "poster.jpg",
        "background": "bg.jpg",
        "etat" : "En Attente"
    }
    
    ajout = client.post("/watchlist",json=data)
    assert ajout.status_code == 201
    assert ajout.json == "The movie has been added to your watchlist successfully !"

    get_watchlist = client.get("/watchlist/1")
    assert get_watchlist.status_code == 200
    assert get_watchlist.json[0]["film_name"] == "Harry Potter : Chamber of Secrets"


def test_change_state(client):
    
    data = {
        "etat" : "Abandon"
    }
    update = client.put("/watchlist/1/tt0295297",json=data)
    assert update.status_code == 200
    assert update.json["etat"] == "Abandon"

def test_change_state_failled(client):
    data = {
        "etat" : "Abandon"
    }
    update_failed = client.put("/watchlist/1/IMDBInconnu",json=data)
    assert update_failed.status_code == 404
    assert update_failed.json["error"] == "Film non trouvé dans votre watchlist."

def test_delete_movie(client):

    delete = client.delete("/watchlist/1/tt0295297")
    assert delete.status_code == 200
    assert delete.json["message"] == "Deleted successfully"