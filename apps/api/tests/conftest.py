import os
import uuid

import bcrypt
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "postgresql://meridian:meridian@localhost:5432/meridian")
os.environ.setdefault("JWT_SECRET", "test-secret")

from meridian_api.main import app  # noqa: E402
from meridian_api.database import get_connection  # noqa: E402


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_user(client):
    email = f"test-{uuid.uuid4().hex[:8]}@example.com"
    response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "name": "Test User", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    return {
        "email": email,
        "token": data["access_token"],
        "user": data["user"],
        "headers": {"Authorization": f"Bearer {data['access_token']}"},
    }


@pytest.fixture
def seeded_team_and_project(test_user):
    conn = get_connection()
    team_id = str(uuid.uuid4())
    project_id = str(uuid.uuid4())
    user_id = str(test_user["user"]["id"])

    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO teams (id, name, slug) VALUES (%s, %s, %s)",
            (team_id, "Test Team", f"test-team-{uuid.uuid4().hex[:6]}"),
        )
        cur.execute(
            "INSERT INTO team_members (id, team_id, user_id, role) VALUES (%s, %s, %s, %s)",
            (str(uuid.uuid4()), team_id, user_id, "owner"),
        )
        cur.execute(
            """
            INSERT INTO projects (id, team_id, name, description, created_by)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (project_id, team_id, "Test Project", "A test project", user_id),
        )
    conn.commit()
    conn.close()

    return {"team_id": team_id, "project_id": project_id, **test_user}