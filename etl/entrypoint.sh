#!/usr/bin/env bash
set -euo pipefail

TEMPLATE="/opt/etl/crontab.template"
CRON_DEST="/etc/cron.d/posts_etl"
LOGDIR="/var/log"

# Ensure log files
mkdir -p /var/log
touch /var/log/extract.log /var/log/transform.log
chmod 644 /var/log/extract.log /var/log/transform.log

# Create env file for cron
cat > /opt/etl/env.sh <<'ENVSH'
export API_URL="${API_URL:-https://jsonplaceholder.typicode.com/posts}"
export DATABASE_URL="${DATABASE_URL:-postgresql://postgres:postgres@db:5432/posts_db}"
export LOG_LEVEL="${LOG_LEVEL:-INFO}"
ENVSH
chmod +x /opt/etl/env.sh

envsubst < "$TEMPLATE" > "$CRON_DEST"
chmod 0644 "$CRON_DEST"
cat "$CRON_DEST"

cron -f
