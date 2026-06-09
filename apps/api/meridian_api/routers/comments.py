from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends
from psycopg2.extensions import connection

from meridian_api.auth import get_current_user
from meridian_api.database import get_db
from meridian_api.policies import require_task_access
from meridian_api.schemas import CommentCreate, CommentResponse

router = APIRouter(tags=["comments"])


@router.get("/tasks/{task_id}/comments", response_model=list[CommentResponse])
def list_comments(
    task_id: UUID,
    db: Annotated[connection, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    require_task_access(db, current_user["id"], task_id, "viewer")

    with db.cursor() as cur:
        cur.execute(
            """
            SELECT c.id, c.task_id, c.author_id, u.name AS author_name,
                   c.body, c.created_at, c.updated_at
            FROM comments c
            JOIN users u ON u.id = c.author_id
            WHERE c.task_id = %s
            ORDER BY c.created_at ASC
            """,
            (str(task_id),),
        )
        rows = cur.fetchall()
    return [CommentResponse(**row) for row in rows]


@router.post("/tasks/{task_id}/comments", response_model=CommentResponse, status_code=201)
def create_comment(
    task_id: UUID,
    body: CommentCreate,
    db: Annotated[connection, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    require_task_access(db, current_user["id"], task_id, "member")

    comment_id = uuid4()
    with db.cursor() as cur:
        cur.execute(
            """
            INSERT INTO comments (id, task_id, author_id, body)
            VALUES (%s, %s, %s, %s)
            RETURNING id, task_id, author_id, body, created_at, updated_at
            """,
            (str(comment_id), str(task_id), str(current_user["id"]), body.body),
        )
        row = cur.fetchone()

    return CommentResponse(**row, author_name=current_user["name"])