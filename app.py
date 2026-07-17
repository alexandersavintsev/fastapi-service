"""
app.py — FastAPI-сервис (baseline рекомендательной системы).

Эндпоинты:
    GET /user/{id}                — данные пользователя
    GET /post/{id}                — данные поста
    GET /user/{id}/feed?limit=N   — действия пользователя
    GET /post/{id}/feed?limit=N   — действия по посту
    GET /post/recommendations/    — top-N популярных постов (одинаково для всех)
"""
from typing import List

from fastapi import FastAPI, HTTPException, Depends

from database import postgres_connection
from schema import UserGet, PostGet, FeedGet
from helpers import get_user, get_post, get_feed, get_recommended_feed

app = FastAPI()


def get_conn():
    """Создаёт соединение с БД на время запроса и закрывает его после."""
    conn = postgres_connection()
    try:
        yield conn
    finally:
        conn.close()


@app.get("/user/{id}", response_model=UserGet)
def handle_get_user(id: int, conn=Depends(get_conn)) -> UserGet:
    """Информация о пользователе по ID (404, если не найден)."""
    user = get_user(conn, id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@app.get("/post/{id}", response_model=PostGet)
def handle_get_post(id: int, conn=Depends(get_conn)) -> PostGet:
    """Информация о посте по ID (404, если не найден)."""
    post = get_post(conn, id)
    if post is None:
        raise HTTPException(status_code=404, detail="post not found")
    return post


@app.get("/user/{id}/feed", response_model=List[FeedGet])
def handle_get_user_feed(id: int, limit: int = 10, conn=Depends(get_conn)) -> List[FeedGet]:
    """Действия пользователя (свежие первыми)."""
    return get_feed(conn, user_id=id, limit=limit)


@app.get("/post/{id}/feed", response_model=List[FeedGet])
def handle_get_post_feed(id: int, limit: int = 10, conn=Depends(get_conn)) -> List[FeedGet]:
    """Действия пользователей с заданным постом (свежие первыми)."""
    return get_feed(conn, post_id=id, limit=limit)


@app.get("/post/recommendations/", response_model=List[PostGet])
def recommended_posts(id: int, limit: int = 10, conn=Depends(get_conn)) -> List[PostGet]:
    """Baseline-рекомендации: топ-N постов по числу лайков."""
    return get_recommended_feed(conn, id, limit)
