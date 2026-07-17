"""
helpers.py — функции загрузки данных из БД.

Каждая функция получает соединение (conn) и возвращает объекты моделей
(User, Post, Feed). Строки из БД (DictCursor) распаковываются в конструкторы
классов через синтаксис **row.
"""
from typing import List, Optional

from psycopg2.extensions import connection
from psycopg2.extras import DictCursor

from models import User, Post, Feed


def get_user(conn: connection, user_id: int) -> Optional[User]:
    """Загружает пользователя по id. Возвращает User или None."""
    query = """
        SELECT id, gender, age, country, city, exp_group, os, source
        FROM public.user
        WHERE id = %s
    """
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute(query, (user_id,))
        row = cur.fetchone()
        return User(**row) if row else None


def get_post(conn: connection, post_id: int) -> Optional[Post]:
    """Загружает пост по id. Возвращает Post или None."""
    query = """
        SELECT id, text, topic
        FROM public.post
        WHERE id = %s
    """
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute(query, (post_id,))
        row = cur.fetchone()
        return Post(**row) if row else None


def get_feed(
    conn: connection, user_id: int = None, post_id: int = None, limit: int = 10
) -> List[Feed]:
    """
    Список действий с постами (свежие первыми), не более `limit` записей.
    Нужно указать хотя бы один фильтр: user_id или post_id.
    """
    if user_id is None and post_id is None:
        raise ValueError("Необходимо указать хотя бы user_id или post_id")

    query = """
        SELECT
            f.user_id, f.post_id, f.action, f.time,
            u.id AS u_id, u.gender, u.age, u.country,
            u.city, u.exp_group, u.os, u.source,
            p.id AS p_id, p.text, p.topic
        FROM public.feed_action AS f
        JOIN public.user AS u ON u.id = f.user_id
        JOIN public.post AS p ON p.id = f.post_id
    """
    conditions, params = [], []
    if user_id is not None:
        conditions.append("f.user_id = %s")
        params.append(user_id)
    if post_id is not None:
        conditions.append("f.post_id = %s")
        params.append(post_id)
    query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY f.time DESC LIMIT %s"
    params.append(limit)

    result: List[Feed] = []
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute(query, tuple(params))
        for row in cur.fetchall():
            user = User(
                id=row["u_id"], gender=row["gender"], age=row["age"],
                country=row["country"], city=row["city"],
                exp_group=row["exp_group"], os=row["os"], source=row["source"],
            )
            post = Post(id=row["p_id"], text=row["text"], topic=row["topic"])
            result.append(Feed(
                user_id=row["user_id"], post_id=row["post_id"],
                user=user, post=post, action=row["action"], time=row["time"],
            ))
    return result


def get_recommended_feed(conn: connection, id: int, limit: int) -> List[Post]:
    """
    Baseline-рекомендации: top-N постов по числу лайков.
    Одинаковы для всех пользователей (id пока не используется).
    """
    query = """
        SELECT p.id, p.text, p.topic
        FROM public.feed_action AS f
        JOIN public.post AS p ON p.id = f.post_id
        WHERE f.action = 'like'
        GROUP BY p.id, p.text, p.topic
        ORDER BY COUNT(*) DESC
        LIMIT %s
    """
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute(query, (limit,))
        rows = cur.fetchall()
        return [Post(**row) for row in rows]
