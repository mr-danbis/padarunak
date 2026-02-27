def home_get_collections(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM home_categories ORDER BY id")
    categories = cur.fetchall()
    result = []
    for cat in categories:
        cur.execute(
            """SELECT id, name, price, link, image_url
               FROM home_products WHERE category_id = %s ORDER BY id""",
            (cat["id"],),
        )
        products = cur.fetchall()
        result.append({
            "id": cat["id"],
            "name": cat["name"],
            "products": list(products),
        })
    cur.close()
    return result
