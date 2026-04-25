from db import get_connection

def get_all():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM watchlist")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def add_movies(data):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "INSERT INTO watchlist (id,film_name,poster,background,etat) VALUES (%s,%s,%s,%s,%s)"
    valeurs = (data['id'], data['title'],data['poster'],data["background"],"En Attente")

    cursor.execute(sql,valeurs)
    conn.commit()

    cursor.close()
    conn.close()

    return "Succès : Le film a été ajoute dans votre watchlist"


def get_movie_by_id(imdbID):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM watchlist WHERE id = %s", (imdbID,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


def delete_movie(imdbID):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM watchlist WHERE id = %s", (imdbID,))
    conn.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    conn.close()
    return rows_affected > 0

def update_movie_state(imdbID, nv_etat):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE watchlist SET etat = %s WHERE id = %s", (nv_etat, imdbID))
    conn.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    conn.close()
    return rows_affected > 0

def creation_user(data):
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
    cursor.close()
    conn.close()
    return 1

def connexion(data):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, username FROM users WHERE username = %s AND mdp = %s", (data["username"],data["password"]))
    verification = cursor.fetchone()
    if verification is None:
        cursor.close()
        conn.close()
        return None

    cursor.close()
    conn.close()
    return verification


def update_user(identifiant,data):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (identifiant,))
    existe = cursor.fetchone()

    if existe is None or len(data) == 0:
        cursor.close()
        conn.close()
        return 0

    cursor.execute("SELECT id FROM users WHERE username = %s and id != %s", (data["username"],data["id"]))
    verification = cursor.fetchone()
    if verification is not None:
        cursor.close()
        conn.close()
        return -1

    cursor.execute("SELECT id FROM users WHERE username = %s and id = %s", (data["username"],data["id"]))
    verification = cursor.fetchone()
    if verification is not None:
        cursor.close()
        conn.close()
        return -3

    if "old_mdp" in data and "mdp" in data:
        if data["old_mdp"] != "":
            if data["old_mdp"] != existe["mdp"]:
                cursor.close()
                conn.close()
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
        cursor.close()
        conn.close()
        return 0

    set_clause = ', '.join(champs)

    query = f"UPDATE users SET {set_clause} WHERE id = %s"
    valeur.append(identifiant)
    valeur = tuple(valeur)
    cursor.execute(query,valeur)
    conn.commit()

    cursor.close()
    conn.close()

    return 1