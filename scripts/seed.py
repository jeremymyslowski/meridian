#!/usr/bin/env python3
"""Seed the Meridian database with realistic test data."""

import os
import sys
import uuid
from datetime import datetime, timezone

import bcrypt
import psycopg2
from psycopg2.extras import execute_values

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://meridian:meridian@localhost:5432/meridian"
)

PASSWORD = "password123"


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def main() -> None:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] > 0:
        print("Database already seeded. Skipping.")
        conn.close()
        return

    now = datetime.now(timezone.utc)
    password_hash = hash_password(PASSWORD)

    users = [
        (str(uuid.uuid4()), f"user{i}@example.com", f"User {i}", password_hash, now, now)
        for i in range(1, 11)
    ]
    execute_values(
        cur,
        "INSERT INTO users (id, email, name, password_hash, created_at, updated_at) VALUES %s",
        users,
    )

    teams = [
        (str(uuid.uuid4()), "Engineering", "engineering", now, now),
        (str(uuid.uuid4()), "Design", "design", now, now),
        (str(uuid.uuid4()), "Product", "product", now, now),
    ]
    execute_values(
        cur,
        "INSERT INTO teams (id, name, slug, created_at, updated_at) VALUES %s",
        teams,
    )

    memberships = []
    roles = ["owner", "member", "member", "viewer", "member"]
    for team_idx, team in enumerate(teams):
        for user_idx in range(2):
            user = users[(team_idx * 2 + user_idx) % len(users)]
            role = roles[user_idx]
            memberships.append(
                (str(uuid.uuid4()), team[0], user[0], role, now)
            )
    # Add a few cross-team memberships
    memberships.append((str(uuid.uuid4()), teams[0][0], users[5][0], "member", now))
    memberships.append((str(uuid.uuid4()), teams[1][0], users[6][0], "viewer", now))

    execute_values(
        cur,
        "INSERT INTO team_members (id, team_id, user_id, role, created_at) VALUES %s",
        memberships,
    )

    projects = []
    project_names = [
        ("Platform Rewrite", "Modernize core infrastructure"),
        ("Mobile App v2", "Next generation mobile experience"),
        ("Analytics Dashboard", "Real-time team metrics"),
        ("API Gateway", "Unified API entry point"),
        ("Onboarding Flow", "Improve new user experience"),
    ]
    for i, (name, desc) in enumerate(project_names):
        team = teams[i % len(teams)]
        creator = users[i % len(users)]
        projects.append(
            (str(uuid.uuid4()), team[0], name, desc, "active", creator[0], now, now)
        )

    execute_values(
        cur,
        "INSERT INTO projects (id, team_id, name, description, status, created_by, created_at, updated_at) VALUES %s",
        projects,
    )

    tasks = []
    statuses = ["todo", "in_progress", "done"]
    for i in range(50):
        project = projects[i % len(projects)]
        creator = users[i % len(users)]
        assignee = users[(i + 3) % len(users)]
        tasks.append(
            (
                str(uuid.uuid4()),
                project[0],
                f"Task {i + 1}: {project[2]} work item",
                f"Description for task {i + 1}",
                statuses[i % 3],
                assignee[0],
                creator[0],
                i % 10,
                now,
                now,
            )
        )

    execute_values(
        cur,
        "INSERT INTO tasks (id, project_id, title, description, status, assignee_id, created_by, position, created_at, updated_at) VALUES %s",
        tasks,
    )

    comments = []
    for i, task in enumerate(tasks[:20]):
        author = users[i % len(users)]
        comments.append(
            (
                str(uuid.uuid4()),
                task[0],
                author[0],
                f"Comment on {task[2]} — looks good, let's ship it.",
                now,
                now,
            )
        )

    execute_values(
        cur,
        "INSERT INTO comments (id, task_id, author_id, body, created_at, updated_at) VALUES %s",
        comments,
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Seed complete!")
    print(f"  Users: {len(users)} (password: {PASSWORD})")
    print(f"  Teams: {len(teams)}")
    print(f"  Projects: {len(projects)}")
    print(f"  Tasks: {len(tasks)}")
    print(f"  Comments: {len(comments)}")
    print("\nLogin as: user1@example.com / password123")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Seed failed: {e}", file=sys.stderr)
        sys.exit(1)