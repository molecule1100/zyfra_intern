1. Клонировать репозиторий
```
git clone https://github.com/molecule1100/zyfra_intern.git
cd zyfra_intern
```

2. Создать .env файл

Содержимое файла .env
```
SECRET_KEY = secret_key
POSTGRES_DB = db_name
POSTGRES_USER = user
POSTGRES_PASSWORD = password
POSTGRES_HOST = host
POSTGRES_PORT = port
```

3. Запустить проект через docker-compose

```
docker-compose up --build
```

Проект разворачивается в двух контейнерах через docker-compose:

- zyfra — контейнер с Django приложением
- db — контейнер с PostgreSQL