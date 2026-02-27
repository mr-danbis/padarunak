def get_by_google_id(conn, google_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE google_id = %s", (google_id,))
    row = cur.fetchone()
    cur.close()
    return row


def create(conn, google_id, email, name, picture_url):
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO users (google_id, email, name, picture_url)
           VALUES (%s, %s, %s, %s)
           RETURNING *""",
        (google_id, email, name or "", picture_url or ""),
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    return row


def update_profile(conn, user_id, name, picture_url):
    """Обновляет имя и картинку пользователя (при повторном входе из Google)."""
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET name = %s, picture_url = %s WHERE id = %s",
        (name or "", picture_url or "", user_id),
    )
    conn.commit()
    cur.close()
