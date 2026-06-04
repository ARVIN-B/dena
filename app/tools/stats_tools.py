from app.filters.task_filters import filter_tasks
from app.filters.user_filters import filter_users
from app.filters.task_user_filter import filter_task_users

from app.tools.constants import DataSource


FILTERS = {
    DataSource.TASKS: filter_tasks,
    DataSource.USERS: filter_users,
    DataSource.TASK_USERS: filter_task_users,
}


def count(
    source=DataSource.TASK_USERS,
    **filters
):

    if isinstance(source, str):
        source = DataSource(source)

    if source not in FILTERS:
        raise ValueError(
            f"Unsupported source: {source}"
        )

    data = FILTERS[source](
        **filters
    )

    return len(data)