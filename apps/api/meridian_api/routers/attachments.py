from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends
from psycopg2.extensions import connection

from meridian_api.auth import get_current_user
from meridian_api.database import get_db
from meridian_api.errors import APIError
from meridian_api.feature_flags import load_feature_flags
from meridian_api.policies import require_task_access
from meridian_api.schemas import AttachmentCreate, AttachmentResponse

router = APIRouter(tags=["attachments"])

S3_STUB_BASE = "https://s3.stub.meridian.test/uploads"


@router.get("/tasks/{task_id}/attachments", response_model=list[AttachmentResponse])
def list_attachments(
    task_id: UUID,
    db: Annotated[connection, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if not load_feature_flags().get("file_attachments", False):
        raise APIError("FEATURE_DISABLED", "File attachments are disabled", 403)

    require_task_access(db, current_user["id"], task_id, "viewer")

    with db.cursor() as cur:
        cur.execute(
            """
            SELECT id, task_id, filename, content_type, size_bytes, s3_url, uploaded_by, created_at
            FROM attachments WHERE task_id = %s ORDER BY created_at DESC
            """,
            (str(task_id),),
        )
        rows = cur.fetchall()
    return [AttachmentResponse(**row) for row in rows]


@router.post("/tasks/{task_id}/attachments", response_model=AttachmentResponse, status_code=201)
def create_attachment(
    task_id: UUID,
    body: AttachmentCreate,
    db: Annotated[connection, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if not load_feature_flags().get("file_attachments", False):
        raise APIError("FEATURE_DISABLED", "File attachments are disabled", 403)

    require_task_access(db, current_user["id"], task_id, "member")

    attachment_id = uuid4()
    s3_key = f"tasks/{task_id}/{attachment_id}/{body.filename}"
    s3_url = f"{S3_STUB_BASE}/{s3_key}"

    with db.cursor() as cur:
        cur.execute(
            """
            INSERT INTO attachments (id, task_id, filename, content_type, size_bytes, s3_key, s3_url, uploaded_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, task_id, filename, content_type, size_bytes, s3_url, uploaded_by, created_at
            """,
            (
                str(attachment_id),
                str(task_id),
                body.filename,
                body.content_type,
                body.size_bytes,
                s3_key,
                s3_url,
                str(current_user["id"]),
            ),
        )
        row = cur.fetchone()
    return AttachmentResponse(**row)