def test_analytics_overview(client, seeded_team_and_project):
    headers = seeded_team_and_project["headers"]
    project_id = seeded_team_and_project["project_id"]

    client.post(
        f"/api/v1/projects/{project_id}/tasks",
        headers=headers,
        json={"title": "Analytics task", "status": "todo"},
    )

    response = client.get("/api/v1/analytics/overview", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_projects"] >= 1
    assert data["total_tasks"] >= 1
    assert "todo" in data["tasks_by_status"]


def test_feature_flags_endpoint(client):
    response = client.get("/api/v1/feature-flags")
    assert response.status_code == 200
    assert "flags" in response.json()
    assert response.json()["flags"]["analytics_dashboard"] is True


def test_my_teams_endpoint(client, seeded_team_and_project):
    headers = seeded_team_and_project["headers"]
    response = client.get("/api/v1/me/teams", headers=headers)
    assert response.status_code == 200
    teams = response.json()
    assert len(teams) >= 1
    assert teams[0]["role"] == "owner"