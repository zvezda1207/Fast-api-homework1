# FastAPI Advertisement API

Это REST API приложение для управления объявлениями с системой авторизации и управления пользователями, построенное на FastAPI и PostgreSQL.

## Функциональность

### Управление пользователями
- Создание пользователей
- Авторизация (получение токена)
- Получение информации о пользователе
- Обновление данных пользователя
- Удаление пользователя

### Управление объявлениями
- Создание объявлений
- Получение объявлений по ID
- Обновление объявлений
- Удаление объявлений
- Поиск объявлений с фильтрами

### Система авторизации
- JWT-подобные токены с 48-часовым сроком действия
- Роли пользователей: `user` и `admin`
- Права доступа на основе ролей

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

### Управление пользователями

#### Создание пользователя
```bash
curl -X POST "http://localhost:8000/api/v1/user" \
-H "Content-Type: application/json" \
-d '{"name": "username", "password": "password"}'
```

#### Авторизация (получение токена)
```bash
curl -X POST "http://localhost:8000/api/v1/user/login" \
-H "Content-Type: application/json" \
-d '{"name": "username", "password": "password"}'
```

#### Получение информации о пользователе
```bash
curl "http://localhost:8000/api/v1/user/1" \
-H "x-token: YOUR_TOKEN_HERE"
```

#### Обновление данных пользователя
```bash
curl -X PATCH "http://localhost:8000/api/v1/user/1" \
-H "Content-Type: application/json" \
-H "x-token: YOUR_TOKEN_HERE" \
-d '{"name": "new_username", "password": "new_password"}'
```

#### Удаление пользователя
```bash
curl -X DELETE "http://localhost:8000/api/v1/user/1" \
-H "x-token: YOUR_TOKEN_HERE"
```

### Управление объявлениями

#### Создание объявления
```bash
curl -X POST "http://localhost:8000/api/v1/adv" \
-H "Content-Type: application/json" \
-H "x-token: YOUR_TOKEN_HERE" \
-d '{"title": "Название", "description": "Описание", "price": 100, "author": "Автор"}'
```

#### Получение объявления по ID
```bash
curl "http://localhost:8000/api/v1/adv/1" \
-H "x-token: YOUR_TOKEN_HERE"
```

#### Обновление объявления
```bash
curl -X PATCH "http://localhost:8000/api/v1/adv/1" \
-H "Content-Type: application/json" \
-H "x-token: YOUR_TOKEN_HERE" \
-d '{"title": "Новое название"}'
```

#### Удаление объявления
```bash
curl -X DELETE "http://localhost:8000/api/v1/adv/1" \
-H "x-token: YOUR_TOKEN_HERE"
```

#### Поиск объявлений
```bash
curl "http://localhost:8000/api/v1/adv?title=Название&author=Автор&price_from=50&price_to=150"
```

## Система прав доступа

### Неавторизованные пользователи
- Создание пользователя (`POST /api/v1/user`)
- Получение пользователя по ID (`GET /api/v1/user/{user_id}`)
- Получение объявления по ID (`GET /api/v1/adv/{adv_id}`)
- Поиск объявлений (`GET /api/v1/adv`)

### Авторизованные пользователи (роль `user`)
- Все права неавторизованных пользователей
- Обновление своих данных (`PATCH /api/v1/user/{user_id}`)
- Удаление себя (`DELETE /api/v1/user/{user_id}`)
- Создание объявлений (`POST /api/v1/adv`)
- Обновление своих объявлений (`PATCH /api/v1/adv/{adv_id}`)
- Удаление своих объявлений (`DELETE /api/v1/adv/{adv_id}`)

### Администраторы (роль `admin`)
- Любые действия с любыми сущностями

### Ошибки авторизации
- `401 Unauthorized` - неверный токен или учетные данные
- `403 Forbidden` - недостаточно прав для выполнения операции

## Остановка приложения

```bash
docker-compose down
```
Для полной очистки данных (включая базу данных):

```bash
docker-compose down -v
```
## Пример использования

1. Создайте пользователя:
```bash
curl -X POST "http://localhost:8000/api/v1/user" \
-H "Content-Type: application/json" \
-d '{"name": "admin", "password": "password123"}'
```

2. Получите токен:
```bash
curl -X POST "http://localhost:8000/api/v1/user/login" \
-H "Content-Type: application/json" \
-d '{"name": "admin", "password": "password123"}'
```

3. Создайте объявление с токеном:
```bash
curl -X POST "http://localhost:8000/api/v1/adv" \
-H "Content-Type: application/json" \
-H "x-token: YOUR_TOKEN_FROM_STEP_2" \
-d '{"title": "Продам телефон", "description": "iPhone в хорошем состоянии", "price": 50000, "author": "Продавец"}'
```

## Примечания

- При первом запуске автоматически создаются таблицы в базе данных
- Пароли хранятся в хешированном виде (bcrypt)
- Токены действительны в течение 48 часов
- Для работы приложения необходимо, чтобы был запущен Docker Desktop (или Docker Engine на Linux)
- Все изменения в базе данных сохраняются между перезапусками контейнеров, если не используется флаг -v при остановке
- Для создания администратора установите роль `admin` при создании пользователя через PATCH запрос