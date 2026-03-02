# Запуск всего проекта (фронт + бэк + postgres)
up:
	docker compose up --build

# В фоне
up-d:
	docker compose up -d --build

# Остановка
down:
	docker compose down

.PHONY: up up-d down
