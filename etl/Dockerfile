# etl/Dockerfile
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       cron build-essential gcc libpq-dev gettext-base procps \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/etl

COPY etl/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY etl/app /opt/etl/app
COPY etl/crontab.template /opt/etl/crontab.template
COPY etl/entrypoint.sh /opt/etl/entrypoint.sh
RUN chmod +x /opt/etl/entrypoint.sh /opt/etl/app/*.py

ENTRYPOINT ["/opt/etl/entrypoint.sh"]
