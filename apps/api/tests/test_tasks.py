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
    data = listing.json()
    assert "items" in data
    assert "meta" in data
    assert any(t["id"] == task_id for t in data["items"])


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


def test_task_pagination_and_filter(client, seeded_team_and_project):
    headers = seeded_team_and_project["headers"]
    project_id = seeded_team_and_project["project_id"]

    for i in range(5):
        client.post(
            f"/api/v1/projects/{project_id}/tasks",
            headers=headers,
            json={"title": f"Paginated task {i}", "status": "todo" if i % 2 == 0 else "done"},
        )

    page1 = client.get(
        f"/api/v1/projects/{project_id}/tasks?page=1&page_size=2",
        headers=headers,
    )
    assert page1.status_code == 200
    data = page1.json()
    assert len(data["items"]) == 2
    assert data["meta"]["page"] == 1
    assert data["meta"]["total"] >= 5

    filtered = client.get(
        f"/api/v1/projects/{project_id}/tasks?status=done",
        headers=headers,
    )
    assert filtered.status_code == 200
    assert all(t["status"] == "done" for t in filtered.json()["items"])