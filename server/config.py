"""Конфигурация из env (подключение к БД)."""

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
