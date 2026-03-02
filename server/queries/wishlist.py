def wishlist_claim_orphans(conn, user_id):
    """Привязывает записи с user_id = NULL к текущему пользователю (старые данные до введения авторизации)."""
    cur = conn.cursor()
    cur.execute("UPDATE wishlist_items SET user_id = %s WHERE user_id IS NULL", (user_id,))
    conn.commit()
    cur.close()


def wishlist_list(conn, user_id):
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM wishlist_items WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,),
    )
    rows = cur.fetchall()
    cur.close()
    return rows


def wishlist_create(conn, user_id, name, image_url, link, price):
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO wishlist_items (user_id, name, image_url, link, price)
           VALUES (%s, %s, %s, %s, %s)
           RETURNING *""",
        (user_id, name, image_url, link, price),
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    return row


def wishlist_delete(conn, user_id, item_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM wishlist_items WHERE id = %s AND user_id = %s", (item_id, user_id))
    deleted = cur.rowcount
    conn.commit()
    cur.close()
    return deleted
