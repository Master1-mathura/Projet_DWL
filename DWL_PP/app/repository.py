from db import get_session,init_db
from orm import User, Watchlist, UserSettings

def get_all(user_id):
    session = get_session()
    try:
        watchlist = session.query(Watchlist).filter(Watchlist.user_id == user_id).all()
        result = []
        for item in watchlist:
            result.append(
                {"imdb_id" : item.imdb_id,
                 "user_id" : item.user_id,
                 "film_name" : item.film_name,
                 "poster" : item.poster,
                 "background" : item.background,
                 "etat" : item.etat
                 }
            )
        return result
    finally:
        session.close()

def add_movies(data):
    session = get_session()
    try:
        movie = Watchlist(
            imdb_id = data["imdbID"],
            user_id = data["user_id"],
            film_name = data["title"],
            poster = data["poster"],
            background = data["background"],
            etat = "En Attente"
        )
        session.add(movie)
        session.commit()
        return "The movie has been added to your watchlist successfully !"
    finally:
        session.close()

def delete_movie(imdbID,userID):
    session = get_session()
    try:
        movie = session.query(Watchlist).filter((Watchlist.imdb_id == imdbID) & (Watchlist.user_id == userID)).first()
        if movie:
            session.delete(movie)
            session.commit()
            return 1
    finally:
        session.close()

def update_movie_state(imdbID,nvEtat,userID):
    session = get_session()
    try:
        movie = session.query(Watchlist).filter((Watchlist.imdb_id == imdbID) & (Watchlist.user_id == userID)).first()
        if movie:
            movie.etat = nvEtat
            session.commit()
            return 1
    finally:
        session.close()

def creation_user(data):
    session = get_session()
    try:
        user = session.query(User).filter(User.username == data["username"]).first()
        if user :
            return -1

        new_user = User(username=data["username"],mdp = data["password"])
        default_settings = UserSettings()
        new_user.settings = default_settings

        session.add(new_user)
        session.commit()
        return 0
    except Exception as e:
        session.rollback()
        return -2
    finally:
        session.close()
def connexion(data):
    session = get_session()
    try:
        user = session.query(User).filter((User.username == data["username"]) & (User.mdp == data["password"])).first()
        if user:
            return {"id" : user.id, "username" : user.username}
        return None
    finally:
        session.close()

def delete_user(identifiant):
    session = get_session()
    try:
        user = session.query(User).filter(User.id == identifiant).first()
        if not user:
            return 0
        session.delete(user)
        session.commit()
        return 1
    finally:
        session.close()


def update_user(identifiant,data):
    session = get_session()
    try:
        user = session.query(User).filter(User.id == identifiant).first()
        if not user or len(data) == 0:
            return 0 #ID non trouvé ou pas de data envoyer
        if "username" in data:
            existe = session.query(User).filter((User.username == data["username"]) & (User.id != identifiant)).first()
            if existe:
                return -1 #Username deja pris
            if user.username == data["username"]:
                return -3 #Username identique ) l'acutelle

        if "old_mdp" in data and "mdp" in data:
            if data["old_mdp"] != "":
                if data["old_mdp"] != user.mdp:
                    return -2 #Ancien mot de passe incorrect
                data.pop("old_mdp")
        update = False
        for key,value in data.items():
            if key == "id" or value == "":
                continue
            if key == "username" and value == "":
                value = user.username
            setattr(user,key,value)
            update = True
        if not update :
            return 0
        session.commit()
        return 1
    finally:
        session.close()

def update_user_settings(user_id, data):
    session = get_session()
    try:
        user_settings = session.query(UserSettings).filter(UserSettings.user_id == user_id).first()
        if not user_settings:
            return 0
        if "theme" in data:
            user_settings.theme = data["theme"]
        if "blur_effect" in data:
            user_settings.blur_effect = data["blur_effect"]
        session.commit()
        return 1
    finally:
        session.close()

def get_user_settings(user_id):
    session = get_session()
    try:
        user_settings = session.query(UserSettings).filter(UserSettings.user_id == user_id).first()
        if not user_settings:
            return None
        return {"theme": user_settings.theme, "blur_effect": user_settings.blur_effect}
    finally:
        session.close()