# FastAPI Advertisement API

Это простое REST API приложение для управления объявлениями, построенное на FastAPI и PostgreSQL.

## Функциональность

- Создание объявлений
- Получение объявлений по ID
- Обновление объявлений
- Удаление объявлений
- Поиск объявлений с фильтрами

## Технологии

- FastAPI
- SQLAlchemy (асинхронный режим)
- PostgreSQL
- Docker
- Docker Compose

## Требования

- Docker
- Docker Compose

## Установка и запуск

1. Клонируйте репозиторий:
   
```bash
git clone https://github.com/zvezda1207/Fast-api-homework1.git
cd fast-api-homework
```

2. Создайте файл .env на основе .env.example и настройте переменные окружения (при необходимости):


```bash
cp .env.example .env
```

3. Запустите приложение с помощью Docker Compose:

```bash
docker-compose up -d --build
```

Приложение будет доступно по адресу: http://localhost:8000

Документация API (Swagger): http://localhost:8000/docs

## Использование API

### Создание объявления

```bash
curl -X POST "http://localhost:8000/api/v1/adv" \
-H "Content-Type: application/json" \
-d '{"title": "Название", "description": "Описание", "price": 100, "author": "Автор"}'
```

### Получение объявления по ID

```bash
curl "http://localhost:8000/api/v1/adv/1"
```
### Обновление объявления

```bash
curl -X PATCH "http://localhost:8000/api/v1/adv/1" \
-H "Content-Type: application/json" \
-d '{"title": "Новое название"}'
```

### Удаление объявления

```bash
curl -X DELETE "http://localhost:8000/api/v1/adv/1"
```
### Поиск объявлений
```bash
curl "http://localhost:8000/api/v1/adv?title=Название&author=Автор&price_from=50&price_to=150"
```

## Остановка приложения

```bash
docker-compose down
```
Для полной очистки данных (включая базу данных):

```bash
docker-compose down -v
```
## Примечания

При первом запуске автоматически создаются таблицы в базе данных.

Для работы приложения необходимо, чтобы был запущен Docker Desktop (или Docker Engine на Linux).

Все изменения в базе данных сохраняются между перезапусками контейнеров, если не используется флаг -v при остановке