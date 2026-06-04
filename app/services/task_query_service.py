from app.repositories.task_repository import get_tasks
from app.repositories.user_repository import get_users


def get_tasks_with_users():

    tasks = get_tasks()
    users = get_users()

    return tasks.merge(
        users,
        left_on="assignee_id",
        right_on="id",
        how="left",
        suffixes=("", "_user")
    )