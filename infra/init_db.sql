
CREATE TABLE IF NOT EXISTS raw_users_by_posts (
    post_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title TEXT,
    body TEXT,
    fetched_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS top_users_by_posts (
    user_id INTEGER PRIMARY KEY,
    posts_cnt INTEGER NOT NULL,
    calculated_at TIMESTAMPTZ NOT NULL
);
