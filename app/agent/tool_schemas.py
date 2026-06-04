TOOL_SCHEMAS = {

    "count": {
        "description": "Count records from a source using filters",
        "required": [
            "source"
        ],
        "optional": [
            "status",
            "priority",
            "user_id",
            "user_name",
            "fullname",
            "department",
            "title",
            "description",
            "create_time_from",
            "create_time_to",
            "due_time_from",
            "due_time_to",
        ],
    },

    "search": {
        "description": "Search records from a source using filters",
        "required": [
            "source"
        ],
        "optional": [
            "status",
            "priority",
            "user_id",
            "user_name",
            "fullname",
            "department",
            "title",
            "description",
            "create_time_from",
            "create_time_to",
            "due_time_from",
            "due_time_to",
        ],
    },

    "aggregate": {
        "description": "Aggregate records from a source",
        "required": [
            "source",
            "metric",
        ],
        "optional": [
            "field",
            "group_by",
            "sort",
            "top_n",

            "status",
            "priority",

            "user_id",
            "user_name",
            "fullname",
            "department",

            "title",
            "description",

            "create_time_from",
            "create_time_to",

            "due_time_from",
            "due_time_to",
        ],
    },

    "create_task": {
        "description": "Create new task",
        "required": [
            "title",
            "description",
            "assignee_id",
        ],
        "optional": [
            "priority",
            "status",
            "due_time",
        ],
    },

    "update_task": {
        "description": "Update tasks by filters",
        "required": [
            "updates"
        ],
        "optional": [
            "status",
            "priority",

            "user_id",
            "user_name",
            "department",

            "title",
            "description",

            "create_time_from",
            "create_time_to",

            "due_time_from",
            "due_time_to",
        ],
    },

    "delete_task": {
        "description": "Delete tasks by filters",
        "required": [],
        "optional": [
            "status",
            "priority",

            "user_id",
            "user_name",
            "department",

            "title",
            "description",

            "create_time_from",
            "create_time_to",

            "due_time_from",
            "due_time_to",
        ],
    },

    "create_user": {
        "description": "Create new user",
        "required": [
            "fullname",
            "department",
        ],
        "optional": [],
    },

    "update_user": {
        "description": "Update users by filters",
        "required": [
            "updates"
        ],
        "optional": [

            "user_id",
            "fullname",
            "department",

            "status",
            "priority",

            "title",
            "description",

            "create_time_from",
            "create_time_to",

            "due_time_from",
            "due_time_to",
        ],
    },

    "delete_user": {
        "description": "Delete users by filters",
        "required": [],
        "optional": [

            "user_id",
            "fullname",
            "department",

            "status",
            "priority",

            "title",
            "description",

            "create_time_from",
            "create_time_to",

            "due_time_from",
            "due_time_to",
        ],
    },
}

TOOL_METADATA = {

    "count": {
        "allowed_sources": [
            DataSource.TASKS,
            DataSource.USERS,
            DataSource.TASK_USERS,
        ]
    },

    "aggregate": {
        "allowed_sources": [
            DataSource.TASKS,
            DataSource.USERS,
            DataSource.TASK_USERS,
        ],

        "allowed_metrics": [
            AggregateMetric.COUNT,
            AggregateMetric.AVG,
            AggregateMetric.MIN,
            AggregateMetric.MAX,
            AggregateMetric.SUM,
        ]
    }
}