# etl/app/utils.py
from collections import Counter
from typing import Iterable, Mapping

def aggregate_posts(posts: Iterable[Mapping]) -> list[tuple[int,int]]:
    """
    Получает iterable постов (каждый — mapping с ключом 'userId' или 'user_id')
    Возвращает список (user_id, posts_cnt) отсортированных по убыванию cnt.
    """
    c = Counter()
    for p in posts:
        if 'userId' in p:
            uid = p['userId']
        elif 'user_id' in p:
            uid = p['user_id']
        else:
            continue
        try:
            uid_int = int(uid)
        except Exception:
            continue
        c[uid_int] += 1
    return sorted(((u, cnt) for u, cnt in c.items()), key=lambda x: (-x[1], x[0]))
