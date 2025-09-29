#!/usr/bin/env bash
set -euo pipefail



TEMPLATE="/opt/crontab.template"
CRON_DEST="/etc/cron.d/posts_etl"
LOGDIR="/var/log"
export PGHOST=localhost

echo "[entrypoint] launching postgres in background..."
/usr/local/bin/docker-entrypoint.sh postgres &

echo "[entrypoint] waiting for postgres to be ready..."
RETRIES=30
until pg_isready -q || [ $RETRIES -le 0 ]; do
  echo "[entrypoint] waiting for pg... retries left: $RETRIES"
  sleep 1
  RETRIES=$((RETRIES-1))
done

if [ $RETRIES -le 0 ]; then
  echo "[entrypoint] Postgres did not become available, exiting." >&2
  exit 1
fi

echo "[entrypoint] Postgres ready."

touch /var/log/extract.log /var/log/transform.log
chmod 644 /var/log/extract.log /var/log/transform.log

cat > /opt/env.sh <<'ENVSH'
export API_URL="${API_URL:-https://jsonplaceholder.typicode.com/posts}"
export DATABASE_URL="${DATABASE_URL:-postgresql://postgres:postgres@localhost:5432/posts_db}"
export LOG_LEVEL="${LOG_LEVEL:-INFO}"
ENVSH
chmod +x /opt/env.sh

echo "[entrypoint] rendering crontab from template..."
envsubst < "$TEMPLATE" > "$CRON_DEST"
chmod 0644 "$CRON_DEST"
ls -l "$CRON_DEST"
cat "$CRON_DEST"

echo "[entrypoint] starting cron (foreground)..."
cron -f
