import pandas as pd

USERS_FILE = "data/users.csv"


def get_users():
    return pd.read_csv(USERS_FILE)


def save_users(users):
    users.to_csv(
        USERS_FILE,
        index=False
    )