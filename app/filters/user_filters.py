from app.repositories.user_repository import (
    get_users
)


def filter_users(
    user_id=None,
    fullname=None,
    department=None,
):

    users = get_users()
    
    if user_id:
        if isinstance(
            user_id,
            (list, tuple, set)
        ):
            users = users[
                users["id"].isin(user_id)
            ]
        else:
            users = users[
                users["id"] == user_id
            ]

    if fullname:
        users = users[
            users["fullname"].str.contains(
                fullname,
                case=False,
                na=False,
            )
        ]

    if department:
        users = users[
            users["department"] == department
        ]

    return users