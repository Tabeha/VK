# posts-etl/app/extract.py
import os
import sys
import logging
import time
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter, Retry
import psycopg2
from urllib.parse import urlparse

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("extract")

API_URL = os.environ.get("API_URL", "https://jsonplaceholder.typicode.com/posts")
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/posts_db")
RETRY_TOTAL = int(os.environ.get("HTTP_RETRY_TOTAL", "5"))
RETRY_BACKOFF = float(os.environ.get("HTTP_RETRY_BACKOFF", "0.5"))

def get_session():
    s = requests.Session()
    retries = Retry(total=RETRY_TOTAL,
                    backoff_factor=RETRY_BACKOFF,
                    status_forcelist=[500,502,503,504],
                    allowed_methods=["GET","POST"])
    s.mount("https://", HTTPAdapter(max_retries=retries))
    s.mount("http://", HTTPAdapter(max_retries=retries))
    return s

def fetch_posts():
    session = get_session()
    logger.info("Fetching posts from %s", API_URL)
    r = session.get(API_URL, timeout=10)
    r.raise_for_status()
    return r.json()

def connect_db():
    logger.debug("Connecting to DB: %s", DATABASE_URL)
    return psycopg2.connect(DATABASE_URL)

def ensure_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS raw_users_by_posts (
            post_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            title TEXT,
            body TEXT,
            fetched_at TIMESTAMPTZ DEFAULT now()
        );
        """)
        conn.commit()

def upsert_posts(conn, posts):
    inserted = 0
    with conn.cursor() as cur:
        for p in posts:
            cur.execute("""
                INSERT INTO raw_users_by_posts (post_id, user_id, title, body, fetched_at)
                VALUES (%s, %s, %s, %s, now())
                ON CONFLICT (post_id) DO UPDATE
                  SET user_id = EXCLUDED.user_id,
                      title = EXCLUDED.title,
                      body = EXCLUDED.body,
                      fetched_at = now()
            """, (p.get("id"), p.get("userId"), p.get("title"), p.get("body")))
            inserted += 1
        conn.commit()
    return inserted

def main():
    start = datetime.utcnow()
    try:
        posts = fetch_posts()
    except Exception as e:
        logger.exception("Failed to fetch posts: %s", e)
        sys.exit(1)

    try:
        conn = connect_db()
    except Exception as e:
        logger.exception("Failed to connect to DB: %s", e)
        sys.exit(2)

    try:
        ensure_table(conn)
        count = upsert_posts(conn, posts)
        logger.info("Upserted %d posts into raw_users_by_posts", count)
    except Exception as e:
        logger.exception("DB error: %s", e)
        sys.exit(3)
    finally:
        conn.close()
    duration = (datetime.utcnow() - start).total_seconds()
    logger.info("Extract finished in %.2fs", duration)

if __name__ == "__main__":
    main()
