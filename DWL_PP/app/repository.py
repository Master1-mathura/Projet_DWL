from db import get_session,init_db
from orm import User, Watchlist, UserSettings,Badges
from werkzeug.security import generate_password_hash, check_password_hash

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
        hashed_password = generate_password_hash(data["password"])
        new_user = User(username=data["username"],mdp=hashed_password)
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
        user = session.query(User).filter((User.username == data["username"])).first()

        if user and check_password_hash(user.mdp, data["password"]):
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
                if not check_password_hash(user.mdp, data["old_mdp"]):
                    return -2 #Ancien mot de passe incorrect

                data["mdp"] = generate_password_hash(data["mdp"])

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
def init_default_badges():
    session = get_session()
    try:
        badge_par_defaut = [
            {"name": "Cadreur de Watchlist", "description": "You added 10 movies to your watchlist!", "valeur": 10, "type": "watchlist"},
            {"name": "Architecte de Seance", "description": "You added 20 movies to your watchlist!", "valeur": 20, "type": "watchlist"},
            {"name": "Directeur de Collection", "description": "You added 30 movies to your watchlist!", "valeur": 30, "type": "watchlist"},
            {"name": "Œil d'Acier", "description": "You survived 5 movies!", "valeur": 5, "type": "survie"},
            {"name": "Le Cri du Silence", "description": "You abandoned 10 movies!", "valeur": 10, "type": "abandon"},
        ]
        for badge in badge_par_defaut:
            exist = session.query(Badges).filter(Badges.badge_name == badge["name"]).first()
            if not exist:
                new_badge = Badges(badge_name=badge["name"], badge_description=badge["description"], valeur=badge["valeur"], type=badge["type"])
                session.add(new_badge)
        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()

def save_user_badge(user_id,badge_name):
    session = get_session()
    try:
        badge = session.query(Badges).filter(Badges.badge_name == badge_name).first()
        if not badge:
            return -1
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return 0
        user.badges.append(badge)
        session.commit()
        return 1
    except Exception as e:
        session.rollback()
        return -2
    finally:
        session.close()

def get_user_badges(user_id):
    session = get_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        badges = user.badges
        result = []
        for badge in badges:
            result.append(badge.badge_name)
        return result
    finally:
        session.close()

def get_all_badges():
    session = get_session()
    try:
        badges = session.query(Badges).all()
        result = []
        for badge in badges:
            result.append({
                "name" : badge.badge_name,
                "description" : badge.badge_description,
                "valeur" : badge.valeur,
                "type" : badge.type
            })
        return result
    finally:
        session.close()