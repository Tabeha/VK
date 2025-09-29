FROM postgres:15

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       cron python3 python3-venv python3-dev build-essential libpq-dev gettext-base procps \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir requests psycopg2-binary

ENV PATH="/opt/venv/bin:$PATH"

COPY app /opt/app
COPY infra/init_db.sql /docker-entrypoint-initdb.d/01-init_db.sql
COPY crontab.template /opt/crontab.template
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh /opt/app/*.py

EXPOSE 5432

ENTRYPOINT ["/opt/entrypoint.sh"]
