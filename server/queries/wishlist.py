def wishlist_list(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM wishlist_items ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    return rows


def wishlist_create(conn, item_id, name, image_url, link, price, created_at):
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO wishlist_items (id, name, image_url, link, price, created_at)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (item_id, name, image_url, link, price, created_at),
    )
    conn.commit()
    cur.execute("SELECT * FROM wishlist_items WHERE id = %s", (item_id,))
    row = cur.fetchone()
    cur.close()
    return row


def wishlist_delete(conn, item_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM wishlist_items WHERE id = %s", (item_id,))
    deleted = cur.rowcount
    conn.commit()
    cur.close()
    return deleted
