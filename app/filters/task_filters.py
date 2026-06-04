# from app.services.task_query_service import get_tasks_with_users


# def filter_tasks(
#     status=None,
#     priority=None,
#     user_id=None,
#     user_name=None,
#     department=None,
#     title=None,
#     description=None,
#     create_time_from=None,
#     create_time_to=None,

#     due_time_from=None,
#     due_time_to=None,
# ):
    
#     tasks["create_time"] = pd.to_datetime(
#         tasks["create_time"]
#     )

#     tasks["due_time"] = pd.to_datetime(
#         tasks["due_time"]
#     )




#     tasks = get_tasks_with_users()

#     if status:
#         tasks = tasks[tasks["status"] == status]

#     if priority:
#         tasks = tasks[tasks["priority"] == priority]

#     if user_id:
#         tasks = tasks[tasks["assignee_id"] == user_id]

#     if user_name:
#         tasks = tasks[tasks["fullname"] == user_name]

#     if department:
#         tasks = tasks[tasks["department"] == department]

#     if title:
#         tasks = tasks[
#             tasks["title"].str.contains(
#                 title,
#                 case=False,
#                 na=False
#             )
#         ]
        
#     if description:
#         tasks = tasks[
#             tasks["description"].str.contains(
#                 description,
#                 case=False,
#                 na=False
#             )
#         ]
        
#     if create_time_from:
#         tasks = tasks[
#             tasks["create_time"] >= create_time_from
#         ]
        
#     if create_time_to:
#         tasks = tasks[
#             tasks["create_time"] <= create_time_to
#         ]
        
#     if due_time_from:
#         tasks = tasks[
#             tasks["due_time"] >= due_time_from
#         ]
        
#     if due_time_to:
#         tasks = tasks[
#             tasks["due_time"] <= due_time_to
#         ]
        

#     return tasks




import pandas as pd
from app.services.task_query_service import (
    get_tasks_with_users
)


def filter_tasks(
    status=None,
    priority=None,
    user_id=None,
    user_name=None,
    department=None,
    title=None,
    description=None,
    create_time_from=None,
    create_time_to=None,
    due_time_from=None,
    due_time_to=None,
):

    tasks = get_tasks_with_users()
    tasks["create_time"] = pd.to_datetime(
        tasks["create_time"]
    )
    tasks["due_time"] = pd.to_datetime(
        tasks["due_time"]
    )
    if status:
        tasks = tasks[
            tasks["status"] == status
        ]

    if priority:
        tasks = tasks[
            tasks["priority"] == priority
        ]

    if user_id:
        if isinstance(
            user_id,
            (list, tuple, set)
        ):
            tasks = tasks[
                tasks["assignee_id"].isin(
                    user_id
                )
            ]
        else:
            tasks = tasks[
                tasks["assignee_id"] == user_id
            ]

    if user_name:
        tasks = tasks[
            tasks["fullname"].str.contains(
                user_name,
                case=False,
                na=False,
            )
        ]

    if department:
        tasks = tasks[
            tasks["department"] == department
        ]

    if title:
        tasks = tasks[
            tasks["title"].str.contains(
                title,
                case=False,
                na=False,
            )
        ]

    if description:
        tasks = tasks[
            tasks["description"].str.contains(
                description,
                case=False,
                na=False,
            )
        ]

    if create_time_from:
        tasks = tasks[
            tasks["create_time"] >= pd.to_datetime(
                create_time_from
            )
        ]

    if create_time_to:
        tasks = tasks[
            tasks["create_time"] <= pd.to_datetime(
                create_time_to
            )
        ]

    if due_time_from:
        tasks = tasks[
            tasks["due_time"] >= pd.to_datetime(
                due_time_from
            )
        ]

    if due_time_to:
        tasks = tasks[
            tasks["due_time"] <= pd.to_datetime(
                due_time_to
            )
        ]

    return tasks