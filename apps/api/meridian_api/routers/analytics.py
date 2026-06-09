from typing import Annotated

from fastapi import APIRouter, Depends
from psycopg2.extensions import connection

from meridian_api.auth import get_current_user
from meridian_api.database import get_db
from meridian_api.feature_flags import load_feature_flags
from meridian_api.errors import APIError
from meridian_api.schemas import AnalyticsOverview

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview", response_model=AnalyticsOverview)
def analytics_overview(
    db: Annotated[connection, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    flags = load_feature_flags()
    if not flags.get("analytics_dashboard", False):
        raise APIError("FEATURE_DISABLED", "Analytics dashboard is disabled", 403)

    user_id = str(current_user["id"])

    with db.cursor() as cur:
        cur.execute(
            """
            SELECT COUNT(DISTINCT p.id) AS total_projects
            FROM projects p
            JOIN team_members tm ON tm.team_id = p.team_id
            WHERE tm.user_id = %s AND p.status = 'active'
            """,
            (user_id,),
        )
        total_projects = cur.fetchone()["total_projects"]

        cur.execute(
            """
            SELECT COUNT(t.id) AS total_tasks
            FROM tasks t
            JOIN projects p ON p.id = t.project_id
            JOIN team_members tm ON tm.team_id = p.team_id
            WHERE tm.user_id = %s
            """,
            (user_id,),
        )
        total_tasks = cur.fetchone()["total_tasks"]

        cur.execute(
            """
            SELECT t.status, COUNT(*) AS count
            FROM tasks t
            JOIN projects p ON p.id = t.project_id
            JOIN team_members tm ON tm.team_id = p.team_id
            WHERE tm.user_id = %s
            GROUP BY t.status
            """,
            (user_id,),
        )
        tasks_by_status = {row["status"]: row["count"] for row in cur.fetchall()}

        cur.execute(
            """
            SELECT COUNT(c.id) AS total_comments
            FROM comments c
            JOIN tasks t ON t.id = c.task_id
            JOIN projects p ON p.id = t.project_id
            JOIN team_members tm ON tm.team_id = p.team_id
            WHERE tm.user_id = %s
            """,
            (user_id,),
        )
        total_comments = cur.fetchone()["total_comments"]

        cur.execute(
            "SELECT COUNT(*) AS total_teams FROM team_members WHERE user_id = %s",
            (user_id,),
        )
        total_teams = cur.fetchone()["total_teams"]

    return AnalyticsOverview(
        total_projects=total_projects,
        total_tasks=total_tasks,
        tasks_by_status=tasks_by_status,
        total_comments=total_comments,
        total_teams=total_teams,
    )