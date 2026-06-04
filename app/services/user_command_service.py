from app.repositories.user_repository import (
    get_users,
    save_users,
)
from app.repositories.task_repository import (
    get_tasks,
    save_tasks,
)
from app.filters.user_filters import (
    filter_users
)


def insert_user(
    fullname,
    department,
):
    users = get_users()
    new_id = 1

    if not users.empty:
        new_id = int(users["id"].max()) + 1

    new_user = {
        "id": new_id,
        "fullname": fullname,
        "department": department,
    }

    users.loc[len(users)] = new_user
    save_users(users)

    return new_user


def update_users(
    updates,
    **filters
):

    matched_users = filter_users(
        **filters
    )

    if matched_users.empty:
        return {
            "updated_count": 0,
            "updated_user_ids": [],
        }

    user_ids = matched_users[
        "id"
    ].tolist()
    users = get_users()
    tasks = get_tasks()
    old_new_id_map = {}

    if "id" in updates:
        new_id = updates["id"]
        
        if len(user_ids) != 1:
            raise ValueError(
                "Updating id requires exactly one user"
            )

        old_new_id_map[
            user_ids[0]
        ] = new_id

    mask = users["id"].isin(
        user_ids
    )

    for field, value in updates.items():

        if field not in users.columns:
            continue

        users.loc[
            mask,
            field
        ] = value

    for old_id, new_id in old_new_id_map.items():
        tasks.loc[
            tasks["assignee_id"] == old_id,
            "assignee_id"
        ] = new_id

    save_users(users)
    save_tasks(tasks)

    return {
        "updated_count": len(user_ids),
        "updated_user_ids": user_ids,
        "updates": updates,
    }


def delete_users(
    **filters
):

    matched_users = filter_users(
        **filters
    )
    if matched_users.empty:
        return {
            "deleted_count": 0,
            "deleted_user_ids": [],
        }

    user_ids = matched_users[
        "id"
    ].tolist()
    users = get_users()
    tasks = get_tasks()
    users = users[
        ~users["id"].isin(user_ids)
    ]
    tasks = tasks[
        ~tasks["assignee_id"].isin(
            user_ids
        )
    ]
    save_users(users)
    save_tasks(tasks)

    return {
        "deleted_count": len(user_ids),
        "deleted_user_ids": user_ids,
        "deleted_tasks": True,
    }