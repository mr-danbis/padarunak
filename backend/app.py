"""Точка входа: Flask, маршруты, init_db, запуск."""

import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from config import get_db_config, SECRET_KEY, FRONTEND_URL
from database import init_db
from routes import register_routes

load_dotenv()

app = Flask(__name__)
app.secret_key = SECRET_KEY
CORS(app, origins=[FRONTEND_URL], supports_credentials=True)

register_routes(app)


if __name__ == "__main__":
    use_retry = os.environ.get("POSTGRES_HOST") == "postgres"
    init_db(use_retry=use_retry)

    port = int(os.environ.get("PORT", 3001))
    cfg = get_db_config()
    db_label = cfg.get("dbname", "DATABASE_URL") if isinstance(cfg, dict) else "url"

    print(f"Сервер: http://localhost:{port}")
    print(f"API вишлиста: http://localhost:{port}/api/wishlist")
    print(f"БД: PostgreSQL ({db_label})")

    app.run(host="0.0.0.0", port=port, debug=True)
