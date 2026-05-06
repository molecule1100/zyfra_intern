# Zyfra Intern — Учёт спецтехники и запчастей

Django-приложение для учёта спецтехники и запасных частей с ролевой моделью доступа.

## Стек

| Технология | Версия |
|---|---|
| Python | 3.13 |
| Django | 5.2.4 |
| PostgreSQL | 17 |
| gunicorn | 23.0.0 |
| nginx | alpine |
| Docker Compose | v2 |
| Bootstrap | 5.3 |
| sorl-thumbnail | 12.11.0 |

## Структура проекта

```
zyfra_intern/
├── intern_project/   # настройки, urls, wsgi
├── vehicle/          # модели и views техники
├── spare_part/       # модели и views запчастей, management-команды
├── reports/          # дашборд статистики
├── templates/        # общие шаблоны (логин)
├── nginx/            # конфиг nginx
├── logs/             # логи приложения
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Запуск локально

1. Клонировать репозиторий:
```bash
git clone https://github.com/molecule1100/zyfra_intern.git
cd zyfra_intern
```

2. Создать файл `.env` на основе `.env-example`:
```bash
cp .env-example .env
```

Пример содержимого `.env`:
```
SECRET_KEY=your-secret-key-here
POSTGRES_DB=zyfra_db
POSTGRES_USER=zyfra_user
POSTGRES_PASSWORD=zyfra_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

3. Запустить проект:
```bash
docker-compose up --build
```

Приложение будет доступно на http://localhost (порт 80, через nginx).

## Демо-данные

После запуска выполнить:
```bash
docker-compose exec zyfra python manage.py seed_demo
```

## Тестовые пользователи

После `seed_demo` в системе будут созданы:

| Логин | Пароль | Роль |
|---|---|---|
| admin | demo12345 | Администратор (полный доступ) |
| storekeeper1 | demo12345 | Кладовщик (управление запчастями) |
| mechanic1 | demo12345 | Механик (управление техникой, установка запчастей) |

## Роли и права

- **Администраторы** — полный доступ ко всему, включая дашборд
- **Механики** — CRUD техники и типов техники, просмотр запчастей, установка/снятие запчастей, дашборд
- **Кладовщики** — CRUD запчастей, типов запчастей, атрибутов; техника только на просмотр

## Тесты

```bash
docker-compose exec zyfra python manage.py test
```

Или локально (если установлены зависимости):
```bash
python manage.py test
```

## Создать суперпользователя вручную

```bash
docker-compose exec zyfra python manage.py createsuperuser
```

## Развёртывание на VPS

1. Установить Docker и Docker Compose:
```bash
curl -fsSL https://get.docker.com | sh
```

2. Клонировать репозиторий и настроить `.env`:
```bash
git clone https://github.com/molecule1100/zyfra_intern.git
cd zyfra_intern
cp .env-example .env
nano .env  # заполнить все значения, DEBUG=False, ALLOWED_HOSTS=ваш_домен
```

3. Запустить:
```bash
docker-compose up -d --build
```

4. Наполнить демо-данными:
```bash
docker-compose exec zyfra python manage.py seed_demo
```

5. Для домена — настроить nginx на хосте или использовать встроенный контейнер nginx. Добавить SSL через certbot:
```bash
docker-compose exec nginx certbot --nginx -d your-domain.com
```

6. Бэкап БД — см. `BACKUP.md`.
