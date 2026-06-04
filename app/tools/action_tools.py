from app.services.task_command_service import (
    insert_task,
    update_tasks,
    delete_tasks,
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
    assignee_id,
    priority="Medium",
    status="Open",
    due_time=None,
):

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