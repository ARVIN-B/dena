import pandas as pd

from app.repositories.task_repository import (
    get_tasks,
    save_tasks,
)

from app.filters.task_filters import (
    filter_tasks
)


def insert_task(
    title,
    description,
    assignee_id,
    priority="Medium",
    status="Open",
    due_time=None,
):

    tasks = get_tasks()
    new_id = 1

    if not tasks.empty:
        new_id = int(tasks["id"].max()) + 1

    new_task = {
        "id": new_id,
        "title": title,
        "description": description,
        "create_time": pd.Timestamp.now().strftime(
            "%Y/%m/%d"
        ),
        "status": status,
        "assignee_id": assignee_id,
        "priority": priority,
        "due_time": due_time,
    }

    tasks.loc[len(tasks)] = new_task
    save_tasks(tasks)

    return new_task


def update_tasks(
    updates,
    **filters
):

    matched_tasks = filter_tasks(
        **filters
    )

    if matched_tasks.empty:
        return {
            "updated_count": 0,
            "updated_task_ids": [],
        }

    task_ids = matched_tasks[
        "id"
    ].tolist()
    tasks = get_tasks()
    mask = tasks["id"].isin(
        task_ids
    )

    for field, value in updates.items():

        if field not in tasks.columns:
            continue

        tasks.loc[
            mask,
            field
        ] = value
    save_tasks(tasks)

    return {
        "updated_count": len(task_ids),
        "updated_task_ids": task_ids,
        "updates": updates,
    }


def delete_tasks(
    **filters
):
    matched_tasks = filter_tasks(
        **filters
    )

    if matched_tasks.empty:
        return {
            "deleted_count": 0,
            "deleted_task_ids": [],
        }

    task_ids = matched_tasks[
        "id"
    ].tolist()
    tasks = get_tasks()
    tasks = tasks[
        ~tasks["id"].isin(task_ids)
    ]
    save_tasks(tasks)

    return {
        "deleted_count": len(task_ids),
        "deleted_task_ids": task_ids,
    }