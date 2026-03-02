# Padarunak.by

Сайт-вишлист: подборки товаров на главной и личный список желаний (добавление вручную).

## Стек

- **Фронт:** Vue 3, Vue Router, Pinia, SCSS → [frontend/README.md](frontend/README.md)
- **Бэк:** Python, Flask, PostgreSQL → [backend/README.md](backend/README.md)
- **Запуск:** локально или в Docker → [DOCKER.md](DOCKER.md)

## Структура репозитория

```
├── frontend/     # Vue SPA (подробнее — frontend/README.md)
├── backend/      # Flask API (подробнее — backend/README.md)
├── docker-compose.yml
└── DOCKER.md     # Запуск в Docker
```

## Быстрый старт

| Действие | Команда |
|----------|---------|
| **Всё в Docker (одной командой)** | `make up` или `docker compose up --build` → фронт 8080, API 3001 |
| Фронт (локально) | `cd frontend && npm install && npm run dev` → http://localhost:8080 |
| Бэк (локально) | `cd backend && pip install -r requirements.txt && python app.py` → http://localhost:3001 |

Остановка: `make down` или `docker compose down`.  
Детали — в README соответствующих папок и в [DOCKER.md](DOCKER.md).
