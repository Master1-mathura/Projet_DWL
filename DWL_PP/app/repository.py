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