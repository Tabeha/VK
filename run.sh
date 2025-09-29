#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="posts-etl:latest"
CONTAINER_NAME="posts_etl"

docker build -t $IMAGE_NAME .

if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "Stopping and removing existing container ${CONTAINER_NAME}..."
  docker rm -f ${CONTAINER_NAME}
fi

docker run -d --name ${CONTAINER_NAME} \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=posts_db \
  -e POSTGRES_USER=postgres \
  -e API_URL="https://jsonplaceholder.typicode.com/posts" \
  -e EXTRACT_CRON="*/5 * * * *" \
  -e TRANSFORM_CRON="*/6 * * * *" \
  -e LOG_LEVEL="INFO" \
  -p 5432:5432 \
  $IMAGE_NAME

echo "Container started. To follow logs:"
echo "  docker logs -f ${CONTAINER_NAME}"
echo ""
echo "Sample query to check result (run on host, requires psql client):"
echo "  PGPASSWORD=postgres psql -h localhost -U postgres -d posts_db -c \"select * from top_users_by_posts order by posts_cnt desc limit 10;\""
