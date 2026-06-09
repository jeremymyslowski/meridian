import json
from uuid import UUID, uuid4

from psycopg2.extensions import connection


def queue_webhook_event(
    db: connection,
    team_id: UUID,
    event_type: str,
    payload: dict,
) -> None:
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT id, events FROM webhooks
            WHERE team_id = %s AND active = TRUE
            """,
            (str(team_id),),
        )
        webhooks = cur.fetchall()

        for webhook in webhooks:
            if event_type not in webhook["events"]:
                continue
            cur.execute(
                """
                INSERT INTO webhook_events (id, webhook_id, event_type, payload)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    str(uuid4()),
                    str(webhook["id"]),
                    event_type,
                    json.dumps(payload),
                ),
            )