from db import get_connection

def get_all():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, film_name, watched FROM watchlist")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def add_data(data):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "INSERT INTO watchlist (film_name,watched) VALUES (%s,%s)"
    valeurs = (data['query'], False)

    cursor.execute(sql,valeurs)
    conn.commit()

    cursor.close()
    conn.close()

    return "Test ok"