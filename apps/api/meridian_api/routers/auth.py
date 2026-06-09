from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends
from psycopg2.extensions import connection

from meridian_api.auth import authenticate_user, create_access_token, hash_password
from meridian_api.database import get_db
from meridian_api.errors import APIError
from meridian_api.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(body: RegisterRequest, db: Annotated[connection, Depends(get_db)]):
    with db.cursor() as cur:
        cur.execute("SELECT id FROM users WHERE email = %s", (body.email,))
        if cur.fetchone():
            raise APIError("EMAIL_EXISTS", "Email already registered", 409)

        user_id = uuid4()
        cur.execute(
            """
            INSERT INTO users (id, email, name, password_hash)
            VALUES (%s, %s, %s, %s)
            RETURNING id, email, name, created_at
            """,
            (str(user_id), body.email, body.name, hash_password(body.password)),
        )
        user = cur.fetchone()

    token = create_access_token(user["id"], user["email"])
    return TokenResponse(access_token=token, user=UserResponse(**user))


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Annotated[connection, Depends(get_db)]):
    user = authenticate_user(db, body.email, body.password)
    if not user:
        raise APIError("INVALID_CREDENTIALS", "Invalid email or password", 401)

    token = create_access_token(user["id"], user["email"])
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            created_at=user["created_at"],
        ),
    )