"""Конфигурация из env (подключение к БД, auth)."""

import os


def get_db_config():
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


SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")
API_URL = os.environ.get("API_URL", "http://localhost:3001")
