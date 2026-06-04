from app.filters.task_user_filter import filter_task_users

def search_tasks(**filters):

    tasks = filter_task_users(**filters)

    return tasks.to_dict(
        orient="records"
    )