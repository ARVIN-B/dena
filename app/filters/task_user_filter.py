import pandas as pd
from app.services.task_query_service import (
    get_tasks_with_users
)


def filter_task_users(
    
    # task filters
    status=None,
    priority=None,
    title=None,
    description=None,
    create_time_from=None,
    create_time_to=None,
    due_time_from=None,
    due_time_to=None,

    # user filters
    user_id=None,
    user_name=None,
    department=None,
):

    data = get_tasks_with_users()
    data["create_time"] = pd.to_datetime(
        data["create_time"]
    )
    data["due_time"] = pd.to_datetime(
        data["due_time"]
    )

    if status:
        data = data[
            data["status"] == status
        ]

    if priority:
        data = data[
            data["priority"] == priority
        ]

    if title:
        data = data[
            data["title"].str.contains(
                title,
                case=False,
                na=False,
            )
        ]

    if description:
        data = data[
            data["description"].str.contains(
                description,
                case=False,
                na=False,
            )
        ]

    if create_time_from:
        data = data[
            data["create_time"] >= pd.to_datetime(
                create_time_from
            )
        ]

    if create_time_to:
        data = data[
            data["create_time"] <= pd.to_datetime(
                create_time_to
            )
        ]

    if due_time_from:
        data = data[
            data["due_time"] >= pd.to_datetime(
                due_time_from
            )
        ]

    if due_time_to:
        data = data[
            data["due_time"] <= pd.to_datetime(
                due_time_to
            )
        ]

    if user_id:
        if isinstance(
            user_id,
            (list, tuple, set)
        ):
            data = data[
                data["assignee_id"].isin(
                    user_id
                )
            ]
        else:
            data = data[
                data["assignee_id"] == user_id
            ]

    if user_name:
        data = data[
            data["fullname"].str.contains(
                user_name,
                case=False,
                na=False,
            )
        ]

    if department:
        data = data[
            data["department"] == department
        ]

    return data