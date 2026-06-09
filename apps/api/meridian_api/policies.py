from enum import IntEnum
from uuid import UUID

from psycopg2.extensions import connection

from meridian_api.errors import APIError

ROLE_HIERARCHY = {"viewer": 1, "member": 2, "owner": 3}


class Permission(IntEnum):
    READ = 1
    WRITE = 2
    ADMIN = 3


def get_user_team_role(db: connection, user_id: UUID, team_id: UUID) -> str | None:
    with db.cursor() as cur:
        cur.execute(
            "SELECT role FROM team_members WHERE user_id = %s AND team_id = %s",
            (str(user_id), str(team_id)),
        )
        row = cur.fetchone()
    return row["role"] if row else None


def get_project_team_id(db: connection, project_id: UUID) -> UUID | None:
    with db.cursor() as cur:
        cur.execute("SELECT team_id FROM projects WHERE id = %s", (str(project_id),))
        row = cur.fetchone()
    return row["team_id"] if row else None


def get_task_project_team(db: connection, task_id: UUID) -> tuple[UUID, UUID] | None:
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT t.project_id, p.team_id
            FROM tasks t
            JOIN projects p ON p.id = t.project_id
            WHERE t.id = %s
            """,
            (str(task_id),),
        )
        row = cur.fetchone()
    if not row:
        return None
    return row["project_id"], row["team_id"]


def require_team_role(
    db: connection,
    user_id: UUID,
    team_id: UUID,
    min_role: str = "viewer",
) -> str:
    role = get_user_team_role(db, user_id, team_id)
    if not role:
        raise APIError("NOT_FOUND", "Resource not found", 404)
    if ROLE_HIERARCHY[role] < ROLE_HIERARCHY[min_role]:
        raise APIError("FORBIDDEN", f"Requires {min_role} role or higher", 403)
    return role


def require_project_access(
    db: connection,
    user_id: UUID,
    project_id: UUID,
    min_role: str = "viewer",
) -> str:
    team_id = get_project_team_id(db, project_id)
    if not team_id:
        raise APIError("NOT_FOUND", "Project not found", 404)
    return require_team_role(db, user_id, team_id, min_role)


def require_task_access(
    db: connection,
    user_id: UUID,
    task_id: UUID,
    min_role: str = "viewer",
) -> str:
    ids = get_task_project_team(db, task_id)
    if not ids:
        raise APIError("NOT_FOUND", "Task not found", 404)
    _, team_id = ids
    return require_team_role(db, user_id, team_id, min_role)


def can_write(role: str) -> bool:
    return ROLE_HIERARCHY[role] >= ROLE_HIERARCHY["member"]


def can_admin(role: str) -> bool:
    return ROLE_HIERARCHY[role] >= ROLE_HIERARCHY["owner"]