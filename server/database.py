"""Подключение к PostgreSQL и создание таблиц при старте."""

import time as _time

import psycopg2
from psycopg2.extras import RealDictCursor

from config import get_db_config


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


def connect_with_retry(max_attempts=30, delay=1):
    for attempt in range(max_attempts):
        try:
            return get_db()
        except psycopg2.OperationalError:
            if attempt == max_attempts - 1:
                raise
            print(f"[db] Ожидание PostgreSQL... ({attempt + 1}/{max_attempts})")
            _time.sleep(delay)
    return get_db()


def init_db(use_retry=False):
    conn = connect_with_retry() if use_retry else get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            google_id TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            name TEXT NOT NULL DEFAULT '',
            picture_url TEXT NOT NULL DEFAULT '',
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS wishlist_items (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL DEFAULT '',
            image_url TEXT NOT NULL DEFAULT '',
            link TEXT NOT NULL DEFAULT '',
            price TEXT NOT NULL DEFAULT '',
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)
    cur.execute("""
        ALTER TABLE wishlist_items ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS home_categories (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS home_products (
            id SERIAL PRIMARY KEY,
            category_id INTEGER NOT NULL REFERENCES home_categories(id),
            name TEXT NOT NULL DEFAULT '',
            price TEXT NOT NULL DEFAULT '',
            link TEXT NOT NULL DEFAULT '',
            image_url TEXT NOT NULL DEFAULT ''
        )
    """)
    conn.commit()

    cur.close()
    conn.close()
