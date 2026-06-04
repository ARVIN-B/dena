from app.services.task_command_service import (
    insert_task,
    update_tasks,
    delete_tasks,
)
from app.filters.user_filters import (
    filter_users,
)

from app.services.user_command_service import (
    insert_user,
    update_users,
    delete_users,
)


# =========================
# Task Actions
# =========================

def create_task(
    title,
    description,
    assignee_id=None,
    assignee_name=None,
    priority="Medium",
    status="Open",
    due_time=None,
):

    if assignee_id is None and assignee_name:

        matched_users = filter_users(
            fullname=assignee_name,
        )

        if matched_users.empty:
            raise ValueError(
                f"No user found for assignee_name: {assignee_name}"
            )

        if len(matched_users) > 1:
            raise ValueError(
                f"Multiple users matched assignee_name: {assignee_name}"
            )

        assignee_id = int(
            matched_users.iloc[0]["id"]
        )

    if assignee_id is None:
        raise ValueError(
            "assignee_id or assignee_name is required"
        )

    return insert_task(
        title=title,
        description=description,
        assignee_id=assignee_id,
        priority=priority,
        status=status,
        due_time=due_time,
    )


def update_task(
    updates,
    **filters
):

    return update_tasks(
        updates=updates,
        **filters
    )


def delete_task(
    **filters
):

    return delete_tasks(
        **filters
    )


# =========================
# User Actions
# =========================

def create_user(
    fullname,
    department,
):

    return insert_user(
        fullname=fullname,
        department=department,
    )


def update_user(
    updates,
    **filters
):

    return update_users(
        updates=updates,
        **filters
    )


def delete_user(
    **filters
):

    return delete_users(
        **filters
    )
