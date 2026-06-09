import psycopg2
from psycopg2.extras import RealDictCursor

from meridian_api.config import settings


def get_connection():
    return psycopg2.connect(settings.database_url, cursor_factory=RealDictCursor)


def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()