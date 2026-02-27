# Padarunak.by

Сайт-вишлист: подборки товаров на главной и личный список желаний (добавление вручную).

## Стек

- **Фронт:** Vue 3, Vue Router, Pinia, SCSS
- **Бэк:** Python, Flask, SQLite
- **Запуск:** локально или в Docker

## Структура

```
├── src/                 # Vue-приложение
│   ├── views/           # Страницы (Home, Wishlist)
│   ├── components/      # Компоненты
│   ├── api/             # Запросы к API
│   ├── stores/          # Pinia
│   └── composables/
├── server/              # Flask API и БД
│   ├── app.py
│   ├── data/            # SQLite (wishlist.db)
│   └── requirements.txt
├── docker-compose.yml
└── DOCKER.md            # Запуск в Docker
```

## Разработка (локально)

### 1. Фронт

```bash
npm install
npm run dev
```

Приложение: http://localhost:8080

### 2. Бэкенд

```bash
npm run server
```

Либо из папки `server`: создать venv, установить зависимости, запустить `python app.py`.  
API: http://localhost:3001  
Подробнее — [server/README.md](server/README.md).

### 3. Линт

```bash
npm run lint
```

## Сборка

```bash
npm run build
```

Статика в каталоге `dist/`.

## Docker

Запуск фронта и бэка в контейнерах:

```bash
docker compose up --build
```

Фронт: http://localhost:8080, API: http://localhost:3001  
Подробнее — [DOCKER.md](DOCKER.md).

## API (кратко)

- `GET /api/home` — подборки для главной
- `GET /api/wishlist` — список вишлиста
- `POST /api/wishlist` — добавить товар
- `DELETE /api/wishlist/:id` — удалить товар

Полное описание — в [server/README.md](server/README.md).
