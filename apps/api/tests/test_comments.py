def test_create_and_list_comments(client, seeded_team_and_project):
    headers = seeded_team_and_project["headers"]
    project_id = seeded_team_and_project["project_id"]

    task = client.post(
        f"/api/v1/projects/{project_id}/tasks",
        headers=headers,
        json={"title": "Task with comments"},
    )
    task_id = task.json()["id"]

    comment = client.post(
        f"/api/v1/tasks/{task_id}/comments",
        headers=headers,
        json={"body": "Great progress on this!"},
    )
    assert comment.status_code == 201
    assert comment.json()["body"] == "Great progress on this!"

    listing = client.get(f"/api/v1/tasks/{task_id}/comments", headers=headers)
    assert listing.status_code == 200
    assert len(listing.json()) == 1