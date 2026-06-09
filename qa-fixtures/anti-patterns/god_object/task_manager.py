"""God object anti-pattern fixture."""

from dataclasses import dataclass, field


@dataclass
class TaskManager:
    tasks: list[dict] = field(default_factory=list)
    users: list[dict] = field(default_factory=list)
    notifications: list[dict] = field(default_factory=list)
    webhooks: list[dict] = field(default_factory=list)

    def create_task(self, title: str, project_id: str) -> dict:
        task = {"id": f"task-{len(self.tasks)}", "title": title, "project_id": project_id}
        self.tasks.append(task)
        return task

    def assign_task(self, task_id: str, user_id: str) -> None:
        for task in self.tasks:
            if task["id"] == task_id:
                task["assignee_id"] = user_id
                self._notify_assignee(user_id, task_id)
                self._fire_webhook("task.assigned", task)
                return

    def _notify_assignee(self, user_id: str, task_id: str) -> None:
        self.notifications.append({"user_id": user_id, "task_id": task_id})

    def _fire_webhook(self, event: str, payload: dict) -> None:
        for hook in self.webhooks:
            self.webhooks.append({"url": hook.get("url"), "event": event, "payload": payload})

    def list_tasks_by_project(self, project_id: str) -> list[dict]:
        return [t for t in self.tasks if t.get("project_id") == project_id]

    def add_user(self, email: str, name: str) -> dict:
        user = {"id": f"user-{len(self.users)}", "email": email, "name": name}
        self.users.append(user)
        return user

    def export_tasks_csv(self) -> str:
        rows = ["id,title,project_id"]
        for task in self.tasks:
            rows.append(f"{task['id']},{task['title']},{task['project_id']}")
        return "\n".join(rows)