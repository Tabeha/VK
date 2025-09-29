# Posts ETL (JSONPlaceholder) — простая ETL-сборка в Docker

Коротко: проект поднимает PostgreSQL и ETL (cron), два скрипта `extract` и `transform` выполняются по расписанию и формируют витрину **топ пользователей по числу постов**. Дополнительно есть лёгкий веб-сервис с endpoint `/top`.

## Что в репозитории
- `docker-compose.yml` — стек с сервисами `db`, `etl`, `web`
- `etl/Dockerfile` — образ для ETL (python + cron)
- `etl/app/extract.py` — получает посты из API и сохраняет в `raw_users_by_posts` (upsert по `post_id`)
- `etl/app/transform.py` — агрегирует из `raw_users_by_posts` в `top_users_by_posts` (upsert по `user_id`)
- `etl/app/utils.py` — вспомогательные функции
- `etl/crontab.template` — шаблон cron-расписания
- `etl/entrypoint.sh` — запускает cron и подставляет переменные окружения
- `web/Dockerfile` — образ веб-сервиса (Flask)
- `web/app.py` — сервис с endpoint `/top` (HTML / JSON)
- `infra/init_db.sql` — создание таблиц (выполняется при инициализации БД)
- `run.sh` — опциональный скрипт для сборки и запуска
- `tests/` — unit-тесты (pytest)

## Как запустить
- Установить Docker и Docker Compose v2
- Выполнить команду:
  ```bash
  docker compose up -d --build
