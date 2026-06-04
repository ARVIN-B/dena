from app.repositories.user_repository import get_users
from app.repositories.task_repository import get_tasks

from app.filters.task_user_filter import filter_task_users


def count_tasks(**filters):

    tasks = filter_task_users(**filters)
    return len(tasks)