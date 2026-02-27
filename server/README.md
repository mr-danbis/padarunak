# Бэкенд (Python + Flask)

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
- `GET /api/wishlist` — список товаров вишлиста
- `POST /api/wishlist` — добавить товар (body: name, imageUrl, link, price)
- `DELETE /api/wishlist/:id` — удалить товар

БД: **PostgreSQL**. Таблицы: `wishlist_items`, `home_categories`, `home_products`. При первом запуске таблицы создаются и подборки главной заполняются начальными данными.

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

Локально (PostgreSQL уже установлен и запущен):

```bash
cd server
export POSTGRES_USER=postgres POSTGRES_PASSWORD=postgres POSTGRES_DB=wishlist
python app.py
```

В DBeaver/TablePlus подключайтесь к той же базе (хост/порт/пользователь/база), что указаны в переменных окружения.
