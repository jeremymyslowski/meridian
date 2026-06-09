from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends
from psycopg2.extensions import connection

from meridian_api.auth import get_current_user
from meridian_api.database import get_db
from meridian_api.errors import APIError
from meridian_api.schemas import CommentCreate, CommentResponse

router = APIRouter(tags=["comments"])


def _user_can_access_task(db: connection, task_id: UUID, user_id: UUID) -> bool:
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT 1 FROM tasks t
            JOIN projects p ON p.id = t.project_id
            JOIN team_members tm ON tm.team_id = p.team_id
            WHERE t.id = %s AND tm.user_id = %s
            """,
            (str(task_id), str(user_id)),
        )
        return cur.fetchone() is not None


@router.get("/tasks/{task_id}/comments", response_model=list[CommentResponse])
def list_comments(
    task_id: UUID,
    db: Annotated[connection, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if not _user_can_access_task(db, task_id, current_user["id"]):
        raise APIError("NOT_FOUND", "Task not found", 404)

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
    if not _user_can_access_task(db, task_id, current_user["id"]):
        raise APIError("NOT_FOUND", "Task not found", 404)

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