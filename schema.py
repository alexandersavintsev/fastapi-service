"""
schema.py — Pydantic-модели ответов API (UserGet, PostGet, FeedGet).

Pydantic автоматически валидирует данные и сериализует их в JSON.
model_config = ConfigDict(from_attributes=True) позволяет создавать модель
напрямую из объекта с атрибутами (например, из датакласса или строки БД).
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserGet(BaseModel):
    """Данные пользователя для ответа API."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    gender: int
    age: int
    country: str
    city: str
    exp_group: int
    os: str
    source: str


class PostGet(BaseModel):
    """Данные поста для ответа API."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    topic: Optional[str] = None


class FeedGet(BaseModel):
    """Данные действия пользователя с постом для ответа API."""
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    post_id: int
    user: UserGet          # вложенный объект пользователя
    post: PostGet          # вложенный объект поста
    action: str
    time: datetime
