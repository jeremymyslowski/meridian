from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends
from psycopg2.extensions import connection

from meridian_api.auth import get_current_user
from meridian_api.database import get_db
from meridian_api.errors import APIError
from meridian_api.schemas import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["projects"])


def _user_can_access_team(db: connection, user_id: UUID, team_id: UUID) -> bool:
    with db.cursor() as cur:
        cur.execute(
            "SELECT 1 FROM team_members WHERE user_id = %s AND team_id = %s",
            (str(user_id), str(team_id)),
        )
        return cur.fetchone() is not None


@router.get("", response_model=list[ProjectResponse])
def list_projects(
    db: Annotated[connection, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT p.id, p.team_id, p.name, p.description, p.status,
                   p.created_by, p.created_at, p.updated_at
            FROM projects p
            JOIN team_members tm ON tm.team_id = p.team_id
            WHERE tm.user_id = %s AND p.status = 'active'
            ORDER BY p.updated_at DESC
            """,
            (str(current_user["id"]),),
        )
        rows = cur.fetchall()
    return [ProjectResponse(**row) for row in rows]


@router.post("", response_model=ProjectResponse, status_code=201)
def create_project(
    body: ProjectCreate,
    db: Annotated[connection, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if not _user_can_access_team(db, current_user["id"], body.team_id):
        raise APIError("FORBIDDEN", "You are not a member of this team", 403)

    project_id = uuid4()
    with db.cursor() as cur:
        cur.execute(
            """
            INSERT INTO projects (id, team_id, name, description, created_by)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, team_id, name, description, status, created_by, created_at, updated_at
            """,
            (str(project_id), str(body.team_id), body.name, body.description, str(current_user["id"])),
        )
        row = cur.fetchone()
    return ProjectResponse(**row)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: UUID,
    db: Annotated[connection, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT p.id, p.team_id, p.name, p.description, p.status,
                   p.created_by, p.created_at, p.updated_at
            FROM projects p
            JOIN team_members tm ON tm.team_id = p.team_id
            WHERE p.id = %s AND tm.user_id = %s
            """,
            (str(project_id), str(current_user["id"])),
        )
        row = cur.fetchone()

    if not row:
        raise APIError("NOT_FOUND", "Project not found", 404)

    return ProjectResponse(**row)