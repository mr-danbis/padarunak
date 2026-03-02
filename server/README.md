# Бэкенд (Python + Flask)

## Структура проекта

Код разнесён по модулям: конфиг, БД, запросы, сервисы, маршруты.

| Файл / папка | Назначение |
|--------------|------------|
| `app.py` | Точка входа: создание Flask, CORS, регистрация маршрутов, запуск сервера |
| `config.py` | Конфигурация из env (подключение к PostgreSQL: `get_db_config`) |
| `database.py` | Подключение к БД (`get_db`, `connect_with_retry`) и инициализация схемы (`init_db`) |
| `serializers.py` | Преобразование строк БД в формат API: `row_to_item`, `row_to_product` |
| `queries/` | Запросы к таблицам (без Flask): `wishlist` (список, создание, удаление), `home` (подборки) |
| `services/` | Бизнес-логика: `link_preview` — подгрузка превью товара по URL (парсинг страницы) |
| `routes/` | HTTP-эндпоинты: `home`, `wishlist`, `link_preview` — регистрируются в `app` через blueprints |

Зависимости между слоями: `routes` → `queries`, `database`, `serializers`, `services`; `queries` и `services` используют только `config`/`database` или стандартные библиотеки.

## Установка

```bash
cd server
pip install -r requirements.txt
```

Рекомендуется использовать виртуальное окружение:

```bash
cd server
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

Из корня проекта:

```bash
npm run server
```

Или из папки server:

```bash
cd server
python app.py
```

Сервер: http://localhost:3001  
API вишлиста: http://localhost:3001/api/wishlist

## API

- `GET /api/home` — подборки для главной (категории с товарами)
- `GET /api/wishlist` — список товаров вишлиста (требуется вход)
- `POST /api/wishlist` — добавить товар (требуется вход)
- `DELETE /api/wishlist/:id` — удалить товар (требуется вход)
- `GET /api/link-preview?url=...` — превью товара по ссылке (публичный)
- `GET /api/auth/login` — редирект на Google OAuth (вход только Gmail)
- `GET /api/auth/callback` — callback после входа через Google
- `GET /api/auth/me` — текущий пользователь (сессия) или 401
- `GET /api/auth/logout` — выход и редирект на фронт

БД: **PostgreSQL**. Таблицы: `users`, `wishlist_items`, `home_categories`, `home_products`. Вишлист привязан к пользователю (`user_id`). При первом запуске создаются только пустые таблицы — показывается только то, что есть в БД (данные добавляются вручную или миграциями).

### Подключение к PostgreSQL

Задайте переменные окружения (или одну `DATABASE_URL`):

| Переменная | По умолчанию | Описание |
|------------|--------------|----------|
| `POSTGRES_HOST` | localhost | Хост |
| `POSTGRES_PORT` | 5432 | Порт |
| `POSTGRES_USER` | postgres | Пользователь |
| `POSTGRES_PASSWORD` | postgres | Пароль |
| `POSTGRES_DB` | wishlist | Имя базы |

Либо одна строка: `DATABASE_URL=postgresql://user:password@host:5432/dbname`

### Авторизация (только Gmail)

Вход через Google OAuth. Нужны переменные:

| Переменная | Описание |
|------------|----------|
| `SECRET_KEY` | Секрет для сессий Flask |
| `GOOGLE_CLIENT_ID` | Client ID из Google Cloud Console (OAuth 2.0) |
| `GOOGLE_CLIENT_SECRET` | Client Secret |
| `FRONTEND_URL` | URL фронта (например http://localhost:5173) — для CORS и редиректа после входа |
| `API_URL` | URL этого API (например http://localhost:3001) — для redirect_uri в OAuth |

В Google Cloud Console: создать OAuth 2.0 Client (тип «Веб-приложение»), в «Authorized redirect URIs» указать `{API_URL}/api/auth/callback`. Разрешены только аккаунты @gmail.com / @googlemail.com.

Локально (PostgreSQL уже установлен и запущен):

```bash
cd server
export POSTGRES_USER=postgres POSTGRES_PASSWORD=postgres POSTGRES_DB=wishlist
python app.py
```

В DBeaver/TablePlus подключайтесь к той же базе (хост/порт/пользователь/база), что указаны в переменных окружения.
