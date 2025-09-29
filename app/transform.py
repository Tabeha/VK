import os
import sys
import logging
from datetime import datetime
import psycopg2

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("transform")

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/posts_db")

def connect_db():
    return psycopg2.connect(DATABASE_URL)

def ensure_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS top_users_by_posts (
            user_id INTEGER PRIMARY KEY,
            posts_cnt INTEGER NOT NULL,
            calculated_at TIMESTAMPTZ NOT NULL
        );
        """)
        conn.commit()

def aggregate_and_upsert(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT user_id, COUNT(*) AS cnt
            FROM raw_users_by_posts
            GROUP BY user_id
            ORDER BY cnt DESC
        """)
        rows = cur.fetchall()

        now = datetime.utcnow()
        for user_id, cnt in rows:
            cur.execute("""
                INSERT INTO top_users_by_posts (user_id, posts_cnt, calculated_at)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE
                  SET posts_cnt = EXCLUDED.posts_cnt,
                      calculated_at = EXCLUDED.calculated_at
            """, (user_id, cnt, now))
        conn.commit()
        return len(rows)

def main():
    try:
        conn = connect_db()
    except Exception as e:
        logger.exception("Failed to connect to DB: %s", e)
        sys.exit(1)

    try:
        ensure_table(conn)
        cnt = aggregate_and_upsert(conn)
        logger.info("Transformed and upserted %d users into top_users_by_posts", cnt)
    except Exception as e:
        logger.exception("Transform error: %s", e)
        sys.exit(2)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
