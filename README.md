# Posts ETL (JSONPlaceholder) — простая ETL-сборка в Docker

Коротко: контейнер поднимает PostgreSQL и cron, два скрипта (`extract` и `transform`) выполняются по расписанию и формируют витрину "топ пользователей по числу постов".

## Что в репозитории
- `Dockerfile` — образ на базе `postgres:15` + python + cron
- `app/extract.py` — получает посты из API и сохраняет в `raw_users_by_posts` (upsert по `post_id`)
- `app/transform.py` — агрегирует из `raw_users_by_posts` в `top_users_by_posts` (upsert по `user_id`)
- `infra/init_db.sql` — создание таблиц (выполняется при инициализации БД)
- `crontab.template` — шаблон cron расписания (подменяется `envsubst`)
- `entrypoint.sh` — запускает postgres, применяет crontab и запускает cron
- `run.sh` — optional: сборка и запуск контейнера одной командой

## Как запустить (одной командой)
В терминале ввести следующие команды и все вроде должно быть ок
chmod +x run.sh
./run.sh
