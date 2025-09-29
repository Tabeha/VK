# tests/test_utils.py
from etl.app.utils import aggregate_posts

def test_aggregate_simple():
    posts = [
        {"userId": 1, "id": 1},
        {"userId": 2, "id": 2},
        {"userId": 1, "id": 3},
        {"user_id": 2, "id": 4},
        {"userId": "3", "id": 5},
        {"userId": "3", "id": 6},
    ]
    res = aggregate_posts(posts)
    assert (1,2) in res
    assert any(u==3 and cnt==2 for u, cnt in res)
    assert any(u==2 and cnt==2 for u, cnt in res)
