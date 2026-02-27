import os
import time
import random

from dotenv import load_dotenv

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify
from flask_cors import CORS

load_dotenv()  # загружает .env из текущей директории (server/)

app = Flask(__name__)
CORS(app)


def get_db_config():
    """Конфиг подключения: DATABASE_URL или отдельные переменные POSTGRES_*."""
    url = os.environ.get("DATABASE_URL")
    if url:
        return url
    return {
        "host": os.environ.get("POSTGRES_HOST", "localhost"),
        "port": os.environ.get("POSTGRES_PORT", "5432"),
        "user": os.environ.get("POSTGRES_USER", "postgres"),
        "password": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "dbname": os.environ.get("POSTGRES_DB", "wishlist"),
    }


def get_db():
    config = get_db_config()
    if isinstance(config, str):
        return psycopg2.connect(config, cursor_factory=RealDictCursor)
    return psycopg2.connect(
        host=config["host"],
        port=config["port"],
        user=config["user"],
        password=config["password"],
        dbname=config["dbname"],
        cursor_factory=RealDictCursor,
    )


def _connect_with_retry(max_attempts=30, delay=1):
    """Подключение с повторами (для старта вместе с Docker)."""
    import time as _time
    for attempt in range(max_attempts):
        try:
            return get_db()
        except psycopg2.OperationalError as e:
            if attempt == max_attempts - 1:
                raise
            print(f"[db] Ожидание PostgreSQL... ({attempt + 1}/{max_attempts})")
            _time.sleep(delay)
    return get_db()


def init_db(use_retry=False):
    conn = (_connect_with_retry() if use_retry else get_db())
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS wishlist_items (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL DEFAULT '',
            image_url TEXT NOT NULL DEFAULT '',
            link TEXT NOT NULL DEFAULT '',
            price TEXT NOT NULL DEFAULT '',
            created_at TIMESTAMPTZ NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS home_categories (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            sort_order INTEGER NOT NULL DEFAULT 0
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS home_products (
            id SERIAL PRIMARY KEY,
            category_id INTEGER NOT NULL REFERENCES home_categories(id),
            name TEXT NOT NULL DEFAULT '',
            price TEXT NOT NULL DEFAULT '',
            link TEXT NOT NULL DEFAULT '',
            image_url TEXT NOT NULL DEFAULT '',
            sort_order INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()

    # Seed home collections if empty
    cur.execute("SELECT COUNT(*) FROM home_categories")
    if cur.fetchone()["count"] == 0:
        cur.execute(
            "INSERT INTO home_categories (name, sort_order) VALUES (%s, %s), (%s, %s), (%s, %s)",
            ("Подарки для мужчин", 1, "Подарки для женщин", 2, "Подарки для детей", 3),
        )
        conn.commit()
        cur.execute("SELECT id FROM home_categories ORDER BY sort_order")
        cat_ids = [r["id"] for r in cur.fetchall()]
        seed_products = [
            (cat_ids[0], "Часы наручные классические", "от 120 р.", "#", "https://loremflickr.com/300/300/watch", 1),
            (cat_ids[0], "Набор для бритья", "от 45 р.", "#", "https://loremflickr.com/300/300/shaving,razor", 2),
            (cat_ids[0], "Портмоне кожаное", "от 89 р.", "#", "https://loremflickr.com/300/300/wallet,leather", 3),
            (cat_ids[0], "Термокружка", "от 35 р.", "#", "https://loremflickr.com/300/300/thermos,mug", 4),
            (cat_ids[1], "Букет цветов", "от 55 р.", "#", "https://loremflickr.com/300/300/flowers,bouquet", 1),
            (cat_ids[1], "Парфюмерный набор", "от 95 р.", "#", "https://loremflickr.com/300/300/perfume", 2),
            (cat_ids[1], "Шарф шёлковый", "от 42 р.", "#", "https://loremflickr.com/300/300/scarf,silk", 3),
            (cat_ids[1], "Сертификат в спа", "от 80 р.", "#", "https://loremflickr.com/300/300/spa,gift", 4),
            (cat_ids[2], "Конструктор", "от 38 р.", "#", "https://loremflickr.com/300/300/lego,constructor", 1),
            (cat_ids[2], "Набор для творчества", "от 25 р.", "#", "https://loremflickr.com/300/300/art,craft", 2),
            (cat_ids[2], "Книга с иллюстрациями", "от 22 р.", "#", "https://loremflickr.com/300/300/book,children", 3),
            (cat_ids[2], "Игрушка мягкая", "от 30 р.", "#", "https://loremflickr.com/300/300/teddy,plush", 4),
        ]
        for row in seed_products:
            cur.execute(
                """INSERT INTO home_products (category_id, name, price, link, image_url, sort_order)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                row,
            )
        conn.commit()
    cur.close()
    conn.close()


def row_to_item(row):
    created = row["created_at"]
    if hasattr(created, "isoformat"):
        created = created.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return {
        "id": row["id"],
        "name": row["name"],
        "imageUrl": row["image_url"],
        "link": row["link"],
        "price": row["price"],
        "createdAt": created,
    }


def generate_id():
    return f"{int(time.time() * 1000):x}{random.randint(0, 0xFFFFFF):x}"


def row_to_product(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "price": row["price"],
        "link": row["link"],
        "imageUrl": row["image_url"],
    }


@app.route("/api/home", methods=["GET"])
def home_collections():
    """Подборки для главной: категории с товарами."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM home_categories ORDER BY sort_order")
    categories = cur.fetchall()
    result = []
    for cat in categories:
        cur.execute(
            """SELECT id, name, price, link, image_url
               FROM home_products WHERE category_id = %s ORDER BY sort_order""",
            (cat["id"],),
        )
        products = cur.fetchall()
        result.append({
            "id": cat["id"],
            "name": cat["name"],
            "products": [row_to_product(p) for p in products],
        })
    cur.close()
    conn.close()
    return jsonify({"collections": result})


@app.route("/api/wishlist", methods=["GET"])
def list_wishlist():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM wishlist_items ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    data = [row_to_item(row) for row in rows]
    db_info = get_db_config()
    db_name = db_info.get("dbname", "DATABASE_URL") if isinstance(db_info, dict) else "url"
    print(f"[wishlist] DB: {db_name}, rows: {len(data)}")
    resp = jsonify(data)
    resp.headers["X-Wishlist-Count"] = str(len(data))
    return resp


@app.route("/api/wishlist", methods=["POST"])
def create_item():
    data = request.get_json() or {}
    name = data.get("name", "")
    image_url = data.get("imageUrl", "")
    link = data.get("link", "")
    price = data.get("price", "")
    item_id = generate_id()
    created_at = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())

    conn = get_db()
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
    conn.close()

    return jsonify(row_to_item(row)), 201


@app.route("/api/wishlist/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM wishlist_items WHERE id = %s", (item_id,))
    deleted = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    if deleted == 0:
        return jsonify(error="Not found"), 404
    return "", 204


if __name__ == "__main__":
    use_retry = os.environ.get("POSTGRES_HOST") == "postgres"  # Docker
    init_db(use_retry=use_retry)
    port = int(os.environ.get("PORT", 3001))
    cfg = get_db_config()
    db_label = cfg.get("dbname", "DATABASE_URL") if isinstance(cfg, dict) else "url"
    print(f"Сервер: http://localhost:{port}")
    print(f"API вишлиста: http://localhost:{port}/api/wishlist")
    print(f"БД: PostgreSQL ({db_label})")
    app.run(host="0.0.0.0", port=port, debug=True)
