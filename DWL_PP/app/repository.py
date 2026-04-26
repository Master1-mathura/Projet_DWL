from db import get_connection

def get_all(user_id):
    conn = None
    cursor = None
    try :
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM watchlist WHERE user_id = %s"
        cursor.execute(sql,(user_id,))
        return cursor.fetchall()
    finally :
        if cursor:
            cursor.close()
        if conn and conn.is_connected() :
            conn.close()


def add_movies(data):
    conn = None
    cursor = None
    try :
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "INSERT INTO watchlist (imdb_id, user_id, film_name, poster, background, etat) VALUES (%s, %s, %s, %s, %s, %s)"
        valeurs = (data['imdbID'], data['user_id'], data['title'], data['poster'], data["background"], "En Attente")
        
        cursor.execute(sql,valeurs)
        conn.commit()
        return "The movie has been added to your watchlist successfully !"
    finally :
        if cursor:
            cursor.close()
        if conn and conn.is_connected() :
            conn.close()

def get_movie_by_id(imdbID):
    conn = None
    cursor = None
    try :
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM watchlist WHERE imdb_id = %s", (imdbID,))
        return cursor.fetchone()
    finally :
        if cursor:
            cursor.close()
        if conn and conn.is_connected() :
            conn.close()


def delete_movie(imdbID, user_id):
    conn = None
    cursor = None
    try :
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM watchlist WHERE imdb_id = %s AND user_id = %s", (imdbID, user_id))
        conn.commit()
        return cursor.rowcount > 0
    finally :
        if cursor:
            cursor.close()
        if conn and conn.is_connected() :
            conn.close()

def update_movie_state(imdbID, nv_etat, user_id):
    conn = None
    cursor = None
    try :
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE watchlist SET etat = %s WHERE imdb_id = %s AND user_id = %s", (nv_etat, imdbID, user_id))
        conn.commit()
        return cursor.rowcount > 0
    finally :
        if cursor:
            cursor.close()
        if conn and conn.is_connected() :
            conn.close()

def creation_user(data):
    conn = None
    cursor = None
    try :
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM users WHERE username = %s", (data["username"],))
        verification = cursor.fetchone()
        if verification is not None:
            return -1

        sql = "INSERT INTO users (username,mdp) VALUES (%s,%s)"
        valeur = (data['username'],data['password'])
        cursor.execute(sql,valeur)
        conn.commit()
        return 1
    finally :
        if cursor:
            cursor.close()
        if conn and conn.is_connected() :
            conn.close()


def connexion(data):
    conn = None
    cursor = None
    try :
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, username FROM users WHERE username = %s AND mdp = %s", (data["username"],data["password"]))
        verification = cursor.fetchone()
        if verification is None:
            cursor.close()
            conn.close()
            return None
        return verification
    finally :
        if cursor:
            cursor.close()
        if conn and conn.is_connected() :
            conn.close()

def delete_user(id):
    conn = None
    cursor = None
    try :
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (id,))
        existe = cursor.fetchone()
        
        if existe is None :
            cursor.close()
            conn.close()
            return 0

        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query,(id,))
        conn.commit()
        return 1
    finally :
        if cursor:
            cursor.close()
        if conn and conn.is_connected() :
            conn.close()

def update_user(identifiant,data):
    conn = None
    cursor = None
    try :
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (identifiant,))
        existe = cursor.fetchone()

        if existe is None or len(data) == 0:
            return 0

        cursor.execute("SELECT id FROM users WHERE username = %s and id != %s", (data["username"],data["id"]))
        verification = cursor.fetchone()
        if verification is not None:
            return -1

        cursor.execute("SELECT id FROM users WHERE username = %s and id = %s", (data["username"],data["id"]))
        verification = cursor.fetchone()
        if verification is not None:
            return -3

        if "old_mdp" in data and "mdp" in data:
            if data["old_mdp"] != "":
                if data["old_mdp"] != existe["mdp"]:
                    return -2
                data.pop("old_mdp")

        champs = []
        valeur = []
        for key, values in data.items():
            if key == "id" or values == "":
                continue
            champs.append(f"{key} = %s")
            valeur.append(values)

        if len(champs) == 0:
            return 0

        set_clause = ', '.join(champs)
        query = f"UPDATE users SET {set_clause} WHERE id = %s"
        valeur.append(identifiant)
        valeur = tuple(valeur)

        cursor.execute(query,valeur)
        conn.commit()

        return 1
    finally :
        if cursor:
            cursor.close()
        if conn and conn.is_connected() :
            conn.close()