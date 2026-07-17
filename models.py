"""
models.py — датаклассы, описывающие структуру таблиц БД
(public.user, public.post, public.feed_action).

Датаклассы (@dataclass) автоматически создают конструктор и __repr__,
что удобно для отладки и наглядного вывода объектов.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """Пользователь соцсети (таблица public.user)."""
    id: int
    gender: int          # 0 — мужчина, 1 — женщина
    age: int
    country: str
    city: str
    exp_group: int       # экспериментальная группа для A/B-тестов
    os: str
    source: str


@dataclass
class Post:
    """Пост/контент (таблица public.post)."""
    id: int
    text: str
    topic: Optional[str] = None   # тема может быть не задана


@dataclass
class Feed:
    """Действие пользователя с постом (таблица public.feed_action)."""
    user_id: int
    post_id: int
    user: User           # вложенный объект пользователя
    post: Post           # вложенный объект поста
    action: str          # 'like' или 'view'
    time: datetime
