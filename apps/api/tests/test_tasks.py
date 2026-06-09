def test_create_and_list_tasks(client, seeded_team_and_project):
    headers = seeded_team_and_project["headers"]
    project_id = seeded_team_and_project["project_id"]

    create = client.post(
        f"/api/v1/projects/{project_id}/tasks",
        headers=headers,
        json={"title": "Implement auth", "status": "todo"},
    )
    assert create.status_code == 201
    task_id = create.json()["id"]

    listing = client.get(f"/api/v1/projects/{project_id}/tasks", headers=headers)
    assert listing.status_code == 200
    assert any(t["id"] == task_id for t in listing.json())


def test_update_task_status(client, seeded_team_and_project):
    headers = seeded_team_and_project["headers"]
    project_id = seeded_team_and_project["project_id"]

    create = client.post(
        f"/api/v1/projects/{project_id}/tasks",
        headers=headers,
        json={"title": "Review PR", "status": "todo"},
    )
    task_id = create.json()["id"]

    update = client.patch(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
        json={"status": "in_progress"},
    )
    assert update.status_code == 200
    assert update.json()["status"] == "in_progress"