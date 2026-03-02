# Запуск всего проекта (фронт + бэк + postgres)
up:
	docker compose up --build

# В фоне
up-d:
	docker compose up -d --build

# Остановка
down:
	docker compose down

# Линт: фронт (ESLint)
lint-frontend:
	cd frontend && npm run lint

# Форматирование: фронт (Prettier)
format-frontend:
	cd frontend && npm run format

.PHONY: up up-d down lint-frontend format-frontend
