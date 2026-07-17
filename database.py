"""
database.py — подключение к базе данных PostgreSQL через psycopg2.

Параметры подключения берутся из переменных окружения, а как fallback
используется публичный read-only доступ к учебной базе Karpov Courses
(логин/пароль опубликованы в задании курса — это не секрет, разрешено
только чтение учебных данных).
"""
import os

import psycopg2


def postgres_connection():
    """Устанавливает и возвращает соединение с PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("PG_HOST", "postgres.lab.karpov.courses"),
            port=int(os.getenv("PG_PORT", "6432")),
            database=os.getenv("PG_DATABASE", "startml"),
            user=os.getenv("PG_USER", "robot-startml-ro"),
            password=os.getenv("PG_PASSWORD", "pheiph0hahj1Vaif"),
        )
    except Exception as e:
        print("❌ Ошибка при подключении к базе данных.")
        raise e
    conn.autocommit = True
    return conn
