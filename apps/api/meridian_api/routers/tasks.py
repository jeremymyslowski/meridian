from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends
from psycopg2.extensions import connection

from meridian_api.auth import get_current_user
from meridian_api.database import get_db
from meridian_api.errors import APIError
from meridian_api.schemas import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(tags=["tasks"])


def _get_task_with_access(db: connection, task_id: UUID, user_id: UUID) -> dict | None:
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT t.id, t.project_id, t.title, t.description, t.status,
                   t.assignee_id, t.created_by, t.position, t.created_at, t.updated_at
            FROM tasks t
            JOIN projects p ON p.id = t.project_id
            JOIN team_members tm ON tm.team_id = p.team_id
            WHERE t.id = %s AND tm.user_id = %s
            """,
            (str(task_id), str(user_id)),
        )
        return cur.fetchone()


def _queue_assignment_event(
    db: connection, task_id: UUID, assignee_id: UUID, assigned_by: UUID
) -> None:
    with db.cursor() as cur:
        cur.execute(
            """
            INSERT INTO task_assignment_events (id, task_id, assignee_id, assigned_by)
            VALUES (%s, %s, %s, %s)
            """,
            (str(uuid4()), str(task_id), str(assignee_id), str(assigned_by)),
        )


@router.get("/projects/{project_id}/tasks", response_model=list[TaskResponse])
def list_tasks(
    project_id: UUID,
    db: Annotated[connection, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT t.id, t.project_id, t.title, t.description, t.status,
                   t.assignee_id, t.created_by, t.position, t.created_at, t.updated_at
            FROM tasks t
            JOIN projects p ON p.id = t.project_id
            JOIN team_members tm ON tm.team_id = p.team_id
            WHERE t.project_id = %s AND tm.user_id = %s
            ORDER BY t.position ASC, t.created_at ASC
            """,
            (str(project_id), str(current_user["id"])),
        )
        rows = cur.fetchall()
    return [TaskResponse(**row) for row in rows]


@router.post("/projects/{project_id}/tasks", response_model=TaskResponse, status_code=201)
def create_task(
    project_id: UUID,
    body: TaskCreate,
    db: Annotated[connection, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT p.id FROM projects p
            JOIN team_members tm ON tm.team_id = p.team_id
            WHERE p.id = %s AND tm.user_id = %s
            """,
            (str(project_id), str(current_user["id"])),
        )
        if not cur.fetchone():
            raise APIError("NOT_FOUND", "Project not found", 404)

        task_id = uuid4()
        cur.execute(
            """
            INSERT INTO tasks (id, project_id, title, description, status, assignee_id, created_by, position)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, project_id, title, description, status, assignee_id,
                      created_by, position, created_at, updated_at
            """,
            (
                str(task_id),
                str(project_id),
                body.title,
                body.description,
                body.status,
                str(body.assignee_id) if body.assignee_id else None,
                str(current_user["id"]),
                body.position,
            ),
        )
        row = cur.fetchone()

    if body.assignee_id:
        _queue_assignment_event(db, task_id, body.assignee_id, current_user["id"])

    return TaskResponse(**row)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: UUID,
    db: Annotated[connection, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    row = _get_task_with_access(db, task_id, current_user["id"])
    if not row:
        raise APIError("NOT_FOUND", "Task not found", 404)
    return TaskResponse(**row)


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: UUID,
    body: TaskUpdate,
    db: Annotated[connection, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    existing = _get_task_with_access(db, task_id, current_user["id"])
    if not existing:
        raise APIError("NOT_FOUND", "Task not found", 404)

    updates = body.model_dump(exclude_unset=True)
    if not updates:
        return TaskResponse(**existing)

    set_clauses = []
    values = []
    for field, value in updates.items():
        set_clauses.append(f"{field} = %s")
        values.append(str(value) if field == "assignee_id" and value else value)

    values.append(str(task_id))

    with db.cursor() as cur:
        cur.execute(
            f"""
            UPDATE tasks SET {", ".join(set_clauses)}, updated_at = NOW()
            WHERE id = %s
            RETURNING id, project_id, title, description, status, assignee_id,
                      created_by, position, created_at, updated_at
            """,
            values,
        )
        row = cur.fetchone()

    if "assignee_id" in updates and updates["assignee_id"]:
        _queue_assignment_event(
            db, task_id, updates["assignee_id"], current_user["id"]
        )

    return TaskResponse(**row)