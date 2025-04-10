# Tron Service

Микросервис на FastAPI, который:
- Принимает **Tron-адрес** (POST `/tron`),
- Получает у Tron-сети информацию о балансе, bandwidth и energy,
- Сохраняет запрос в **PostgreSQL**,
- Позволяет получить историю запросов (GET `/tron`) с пагинацией.

---

## Запуск через Docker

### 1. Подготовка

1. Убедитесь, что у вас установлен [Docker](https://docs.docker.com/engine/install/) и [docker-compose](https://docs.docker.com/compose/install/).
2. (Опционально) Отредактируйте `docker-compose.yml`, если нужно.

### 2. Запуск

В корне проекта выполните:

```bash
docker-compose up --build
```

- Команда соберёт Docker-образ для приложения (используя `Dockerfile`).
- Запустит два контейнера: `db` (PostgreSQL) и `app` (FastAPI).
- Внутри контейнера `app` автоматически будут выполнены миграции Alembic (создание таблиц).

После сборки вы увидите логи, что Uvicorn запущен:

```text
app         | INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

Значит, приложение доступно по адресу:

[http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)

---

## Локальный запуск (без Docker)

Если хотите поднять проект на своей машине (предположим, у вас уже есть установленный PostgreSQL), следуйте шагам:

### 1. Создайте файл `.env`

В корне проекта есть пример `**.env.example**`. Скопируйте его в `.env`:

```bash
cp .env.example .env
```

И отредактируйте при необходимости (логин/пароль к БД, хост, порт и т.д.):

```bash
# Пример настроек для БД
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tron_db

# Для получения реальных данных из mainnet Tron
TRON_NODE_URL=https://api.trongrid.io
```


### 2. Установка зависимостей

Убедитесь, что у вас есть Python 3.11 (или совместимая версия). Далее:

```bash
python -m venv venv
source venv/bin/activate  # (Linux/Mac)
# Или на Windows: .\venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Миграции Alembic

Примените миграции, чтобы создать таблицы в вашей локальной БД:

```bash
alembic upgrade head
```

### 4. Запуск сервера

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Приложение будет доступно по адресу:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---
Ниже упрощённый раздел про локальное тестирование, **с учётом** того, что по ТЗ нужно всего **2 теста** (юнит и интеграционный), и мы запускаем их **по очереди**.

---

## Тестирование локально

### 1. Запуск юнит-теста (запись в БД)
```bash
python -m pytest tests/test_db.py --maxfail=1 --disable-warnings -v
```
- Проверяет, что функция создания записи в БД работает корректно.
- `--maxfail=1` прерывает на первой ошибке.
- `--disable-warnings` убирает ворнинги.
- `-v` показывает детальный вывод.

### 2. Запуск интеграционного теста (эндпоинт)
```bash
python -m pytest tests/test_api.py --maxfail=1 --disable-warnings -v
```
- Проверяет /tron эндпоинт, имитируя запрос в реальное приложение через ASGITransport(app=app).

---

#### Файл `.env.test`
В `tests/conftest.py` загружается переменный окружения из `.env.test`, убедитесь, что он содержит корректные данные для тестовой Tron-ноды:

```bash
TRON_NODE_URL=https://nile.trongrid.io
```
