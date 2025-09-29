# web/app.py
import os
import psycopg2
from flask import Flask, request, jsonify, Response,redirect

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@db:5432/posts_db")


def get_top_users(limit: int = 100):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT user_id, posts_cnt, calculated_at FROM top_users_by_posts ORDER BY posts_cnt DESC, user_id ASC LIMIT %s", (limit,))
            rows = cur.fetchall()
            return [{"user_id": r[0], "posts_cnt": r[1], "calculated_at": r[2].isoformat()} for r in rows]

@app.get("/top")
def top():
    fmt = request.args.get("format", "").lower()
    limit = int(request.args.get("limit", 100))
    rows = get_top_users(limit)
    if fmt == "json" or request.headers.get("Accept","").startswith("application/json"):
        return jsonify(rows)
    html = ["<html><head><meta charset='utf-8'><title>Top users by posts</title></head><body>"]
    html.append("<h2>Top users by posts</h2>")
    html.append("<table border='1' cellpadding='6'><tr><th>user_id</th><th>posts_cnt</th><th>calculated_at</th></tr>")
    for r in rows:
        html.append(f"<tr><td>{r['user_id']}</td><td>{r['posts_cnt']}</td><td>{r['calculated_at']}</td></tr>")
    html.append("</table></body></html>")
    return Response("\n".join(html), mimetype="text/html")

@app.get("/")
def root():
    return redirect("/top")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

