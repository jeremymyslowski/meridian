from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends
from psycopg2.extensions import connection

from meridian_api.auth import get_current_user
from meridian_api.database import get_db
from meridian_api.errors import APIError
from meridian_api.feature_flags import load_feature_flags
from meridian_api.policies import require_team_role
from meridian_api.schemas import WebhookCreate, WebhookResponse

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.get("", response_model=list[WebhookResponse])
def list_webhooks(
    db: Annotated[connection, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if not load_feature_flags().get("webhook_integrations", False):
        raise APIError("FEATURE_DISABLED", "Webhook integrations are disabled", 403)

    with db.cursor() as cur:
        cur.execute(
            """
            SELECT w.id, w.team_id, w.url, w.events, w.active, w.created_at
            FROM webhooks w
            JOIN team_members tm ON tm.team_id = w.team_id
            WHERE tm.user_id = %s AND tm.role = 'owner'
            ORDER BY w.created_at DESC
            """,
            (str(current_user["id"]),),
        )
        rows = cur.fetchall()
    return [WebhookResponse(**row) for row in rows]


@router.post("", response_model=WebhookResponse, status_code=201)
def create_webhook(
    body: WebhookCreate,
    db: Annotated[connection, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if not load_feature_flags().get("webhook_integrations", False):
        raise APIError("FEATURE_DISABLED", "Webhook integrations are disabled", 403)

    require_team_role(db, current_user["id"], body.team_id, "owner")

    webhook_id = uuid4()
    with db.cursor() as cur:
        cur.execute(
            """
            INSERT INTO webhooks (id, team_id, url, events, created_by)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, team_id, url, events, active, created_at
            """,
            (str(webhook_id), str(body.team_id), body.url, body.events, str(current_user["id"])),
        )
        row = cur.fetchone()
    return WebhookResponse(**row)