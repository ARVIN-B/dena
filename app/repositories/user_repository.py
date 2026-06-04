import pandas as pd

USERS_FILE = "data/users.csv"


def get_users():
    return pd.read_csv(
        USERS_FILE,
        encoding="utf-8-sig",
    )


def save_users(users):
    users.to_csv(
        USERS_FILE,
        index=False,
        encoding="utf-8-sig",
    )
