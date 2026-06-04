from enum import Enum


class AggregateMetric(str, Enum):

    COUNT = "count"
    AVG = "avg"
    MIN = "min"
    MAX = "max"
    SUM = "sum"


class DataSource(str, Enum):

    TASKS = "tasks"
    USERS = "users"
    TASK_USERS = "task_users"


class TaskStatus(str, Enum):

    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    REVIEW = "Review"
    DONE = "Done"


class TaskPriority(str, Enum):

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class SortOrder(str, Enum):

    ASC = "asc"
    DESC = "desc"