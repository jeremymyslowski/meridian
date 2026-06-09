from typing import Annotated

from fastapi import APIRouter, Depends
from psycopg2.extensions import connection

from meridian_api.auth import get_current_user
from meridian_api.database import get_db
from meridian_api.schemas import TeamMembershipResponse

router = APIRouter(prefix="/me", tags=["teams"])


@router.get("/teams", response_model=list[TeamMembershipResponse])
def list_my_teams(
    db: Annotated[connection, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT tm.team_id, t.name AS team_name, t.slug AS team_slug, tm.role
            FROM team_members tm
            JOIN teams t ON t.id = tm.team_id
            WHERE tm.user_id = %s
            ORDER BY t.name ASC
            """,
            (str(current_user["id"]),),
        )
        rows = cur.fetchall()
    return [TeamMembershipResponse(**row) for row in rows]