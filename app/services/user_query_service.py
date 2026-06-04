from app.repositories.user_repository import get_users
from app.repositories.task_repository import get_tasks


def get_users_with_tasks():

    users = get_users()
    tasks = get_tasks()

    return users.merge(
        tasks,
        left_on="id",
        right_on="assignee_id",
        how="left",
        suffixes=("", "_task")
    )