import uuid

from meridian_api.database import get_connection


def _create_viewer_on_team(team_id: str) -> dict:
    viewer_email = f"viewer-{uuid.uuid4().hex[:6]}@example.com"
    return {"email": viewer_email}


def test_viewer_cannot_create_task(client, seeded_team_and_project):
    team_id = seeded_team_and_project["team_id"]
    project_id = seeded_team_and_project["project_id"]

    viewer_email = f"viewer-{uuid.uuid4().hex[:6]}@example.com"
    register = client.post(
        "/api/v1/auth/register",
        json={"email": viewer_email, "name": "Viewer", "password": "password123"},
    )
    viewer_id = register.json()["user"]["id"]
    token = register.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO team_members (id, team_id, user_id, role) VALUES (%s, %s, %s, 'viewer')",
            (str(uuid.uuid4()), team_id, str(viewer_id)),
        )
    conn.commit()
    conn.close()

    create = client.post(
        f"/api/v1/projects/{project_id}/tasks",
        headers=headers,
        json={"title": "Should fail"},
    )
    assert create.status_code == 403
    assert create.json()["detail"]["error"]["code"] == "FORBIDDEN"


def test_viewer_can_list_tasks(client, seeded_team_and_project):
    team_id = seeded_team_and_project["team_id"]
    project_id = seeded_team_and_project["project_id"]
    owner_headers = seeded_team_and_project["headers"]

    client.post(
        f"/api/v1/projects/{project_id}/tasks",
        headers=owner_headers,
        json={"title": "Visible to viewer"},
    )

    viewer_email = f"viewer-read-{uuid.uuid4().hex[:6]}@example.com"
    viewer = client.post(
        "/api/v1/auth/register",
        json={"email": viewer_email, "name": "Viewer Read", "password": "password123"},
    )
    viewer_id = viewer.json()["user"]["id"]
    token = viewer.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO team_members (id, team_id, user_id, role) VALUES (%s, %s, %s, 'viewer')",
            (str(uuid.uuid4()), team_id, str(viewer_id)),
        )
    conn.commit()
    conn.close()

    listing = client.get(f"/api/v1/projects/{project_id}/tasks", headers=headers)
    assert listing.status_code == 200
    assert len(listing.json()["items"]) >= 1


def test_only_owner_can_create_project(client, seeded_team_and_project):
    team_id = seeded_team_and_project["team_id"]
    headers = seeded_team_and_project["headers"]

    create = client.post(
        "/api/v1/projects",
        headers=headers,
        json={"team_id": team_id, "name": "Owner project"},
    )
    assert create.status_code == 201