from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID

import bcrypt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from psycopg2.extensions import connection

from meridian_api.config import settings
from meridian_api.database import get_db
from meridian_api.errors import APIError

security = HTTPBearer()


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def create_access_token(user_id: UUID, email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": str(user_id), "email": email, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[connection, Depends(get_db)],
) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
        if not user_id:
            raise APIError("INVALID_TOKEN", "Invalid authentication token", 401)
    except JWTError as exc:
        raise APIError("INVALID_TOKEN", "Invalid authentication token", 401) from exc

    with db.cursor() as cur:
        cur.execute("SELECT id, email, name, created_at FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()

    if not user:
        raise APIError("USER_NOT_FOUND", "User not found", 401)

    return dict(user)


def authenticate_user(db: connection, email: str, password: str) -> dict | None:
    with db.cursor() as cur:
        cur.execute(
            "SELECT id, email, name, password_hash, created_at FROM users WHERE email = %s",
            (email,),
        )
        user = cur.fetchone()

    if not user or not verify_password(password, user["password_hash"]):
        return None

    return dict(user)