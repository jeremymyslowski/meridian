"""Canonical user service for the Meridian API.

NOTE: qa-fixtures/naming-traps/ contains decoy files with similar names.
When editing user lookup logic, THIS is the production file.
"""

from uuid import UUID

from psycopg2.extensions import connection

from meridian_api.errors import APIError


def get_user_by_id(db: connection, user_id: UUID) -> dict:
    with db.cursor() as cur:
        cur.execute(
            "SELECT id, email, name, created_at FROM users WHERE id = %s",
            (str(user_id),),
        )
        row = cur.fetchone()
    if not row:
        raise APIError("USER_NOT_FOUND", "User not found", 404)
    return dict(row)


def get_user_by_email(db: connection, email: str) -> dict | None:
    with db.cursor() as cur:
        cur.execute(
            "SELECT id, email, name, created_at FROM users WHERE email = %s",
            (email,),
        )
        row = cur.fetchone()
    return dict(row) if row else None