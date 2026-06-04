import pandas as pd

TASKS_FILE = "data/tasks.csv"


def get_tasks():
    return pd.read_csv(TASKS_FILE)


def save_tasks(tasks):
    tasks.to_csv(
        TASKS_FILE,
        index=False
    )