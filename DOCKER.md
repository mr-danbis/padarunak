# Запуск в Docker

## Контейнеры

| Сервис    | Описание              | Порт  |
|-----------|------------------------|-------|
| **frontend** | Vue (dev-сервер)     | 8080  |
| **backend**  | Flask API             | 3001  |
| **postgres** | PostgreSQL 16         | 5432  |

## Команды

```bash
# Собрать и запустить все сервисы
docker compose up --build

# В фоне
docker compose up -d --build
```

Фронт: http://localhost:8080  
API: http://localhost:3001  
PostgreSQL: localhost:5432 (логин/пароль/база: postgres/postgres/wishlist)

Остановка: `docker compose down`  
С удалением данных БД: `docker compose down -v`

## Только один сервис

```bash
docker compose up -d postgres
docker compose up --build backend
docker compose up --build frontend
```

Данные PostgreSQL хранятся в Docker-volume `postgres_data`. Подключиться к БД из хоста: `psql -h localhost -U postgres -d wishlist` (пароль: postgres).
