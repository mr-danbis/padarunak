# Фронтенд (Vue 3)

SPA Padarunak.by: главная с подборками и личный вишлист.

## Стек

Vue 3, Vue Router, Pinia, Vue CLI, SCSS.

## Структура

| Папка / файл | Назначение |
|--------------|------------|
| `src/views/` | Страницы: Home, Wishlist, Account |
| `src/components/` | Компоненты (common, wishlist, home) |
| `src/api/` | Запросы к API (auth, wishlist, home) |
| `src/stores/` | Pinia: authStore, wishlistStore |
| `src/composables/` | useWishlist, useWishlistForm |
| `src/router/` | Роутер |
| `src/assets/` | Стили (SCSS), общие ресурсы |
| `public/` | Статика, index.html |

## Установка

```bash
npm install
```

## Запуск (режим разработки)

```bash
npm run dev
```

Приложение: http://localhost:8080  

Запросы к `/api` проксируются на бэкенд (по умолчанию http://localhost:3001). Переменная `VUE_APP_*` или настройка proxy в `vue.config.js` (для Docker задаётся `API_PROXY_TARGET`).

## Сборка

```bash
npm run build
```

Результат в каталоге `dist/`.

## Линт

```bash
npm run lint
```

## Зависимость от бэкенда

Для входа и вишлиста нужен запущенный API. Подробнее — [../backend/README.md](../backend/README.md).
