from collections.abc import Generator
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row

DB_URL = "postgresql://postgres:postgres@localhost:5432/airline_db"


@contextmanager
def get_db_connection() -> Generator[psycopg.Connection, None, None]:
    """Контекстний менеджер для безпечного підключення та авто-коміту транзакцій."""
    conn = psycopg.connect(DB_URL, row_factory=dict_row)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()