# app/agent/parameter_resolver.py

from datetime import datetime

from app.agent.tool_schemas import (
    TOOL_SCHEMAS,
    TOOL_METADATA,
)

from app.tools.constants import (
    DataSource,
    AggregateMetric,
    SortOrder,
)


STATUS_MAP = {
    "باز": "Open",
    "درحال انجام": "In Progress",
    "در حال انجام": "In Progress",
    "انجام شده": "Done",
    "بسته": "Done",
    "در انتظار بررسی": "Review",
    "بررسی": "Review",
}

PRIORITY_MAP = {
    "کم": "Low",
    "متوسط": "Medium",
    "زیاد": "High",
    "بالا": "High",
    "بحرانی": "Critical",
    "فوری": "Critical",
}

SOURCE_MAP = {
    "task": DataSource.TASKS,
    "tasks": DataSource.TASKS,
    "تسک": DataSource.TASKS,
    "تسکها": DataSource.TASKS,
    "تسک‌ها": DataSource.TASKS,

    "user": DataSource.USERS,
    "users": DataSource.USERS,
    "کاربر": DataSource.USERS,
    "کاربران": DataSource.USERS,

    "task_user": DataSource.TASK_USERS,
    "task_users": DataSource.TASK_USERS,
    "joined": DataSource.TASK_USERS,
}

METRIC_MAP = {
    "count": AggregateMetric.COUNT,
    "تعداد": AggregateMetric.COUNT,

    "avg": AggregateMetric.AVG,
    "average": AggregateMetric.AVG,
    "میانگین": AggregateMetric.AVG,

    "min": AggregateMetric.MIN,
    "کمترین": AggregateMetric.MIN,
    "حداقل": AggregateMetric.MIN,

    "max": AggregateMetric.MAX,
    "بیشترین": AggregateMetric.MAX,
    "حداکثر": AggregateMetric.MAX,

    "sum": AggregateMetric.SUM,
    "مجموع": AggregateMetric.SUM,
}

SORT_MAP = {
    "asc": SortOrder.ASC,
    "صعودی": SortOrder.ASC,

    "desc": SortOrder.DESC,
    "نزولی": SortOrder.DESC,
}


class ParameterResolver:

    @staticmethod
    def resolve(
        tool_name,
        params,
    ):

        schema = TOOL_SCHEMAS.get(
            tool_name
        )

        if not schema:

            return {
                "valid": False,
                "params": {},
                "missing_required": [],
                "clarification_needed": False,
                "clarification_question": "",
                "error": f"Unknown tool: {tool_name}",
            }

        resolved_params = {}

        for key, value in params.items():

            resolved_params[key] = (
                ParameterResolver
                ._normalize_value(
                    key,
                    value,
                )
            )

        missing_required = []

        for field in schema["required"]:

            if field not in resolved_params:
                missing_required.append(
                    field
                )

            elif resolved_params[field] in [
                None,
                "",
            ]:
                missing_required.append(
                    field
                )

        clarification_needed = (
            len(missing_required) > 0
        )

        clarification_question = ""

        if clarification_needed:

            clarification_question = (
                ParameterResolver
                ._build_clarification_question(
                    missing_required
                )
            )

        validation_error = (
            ParameterResolver
            ._validate_metadata(
                tool_name,
                resolved_params,
            )
        )

        if validation_error:

            return {
                "valid": False,
                "params": resolved_params,
                "missing_required": [],
                "clarification_needed": False,
                "clarification_question": "",
                "error": validation_error,
            }

        return {
            "valid": not clarification_needed,
            "params": resolved_params,
            "missing_required": missing_required,
            "clarification_needed": clarification_needed,
            "clarification_question": clarification_question,
            "error": "",
        }

    @staticmethod
    def _normalize_value(
        key,
        value,
    ):

        if value is None:
            return None

        if key == "status":

            if value in STATUS_MAP:
                return STATUS_MAP[value]

            return value

        if key == "priority":

            if value in PRIORITY_MAP:
                return PRIORITY_MAP[value]

            return value

        if key == "source":

            if isinstance(
                value,
                DataSource,
            ):
                return value

            return SOURCE_MAP.get(
                value,
                value,
            )

        if key == "metric":

            if isinstance(
                value,
                AggregateMetric,
            ):
                return value

            return METRIC_MAP.get(
                value,
                value,
            )

        if key == "sort":

            if isinstance(
                value,
                SortOrder,
            ):
                return value

            return SORT_MAP.get(
                value,
                value,
            )

        if (
            "time" in key
            and isinstance(value, str)
        ):

            return (
                ParameterResolver
                ._normalize_date(
                    value
                )
            )

        return value

    @staticmethod
    def _normalize_date(
        value,
    ):

        formats = [
            "%Y/%m/%d",
            "%Y-%m-%d",
            "%Y/%m/%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
        ]

        for fmt in formats:

            try:
                return datetime.strptime(
                    value,
                    fmt,
                )
            except Exception:
                pass

        return value

    @staticmethod
    def _validate_metadata(
        tool_name,
        params,
    ):

        metadata = TOOL_METADATA.get(
            tool_name
        )

        if not metadata:
            return None

        if (
            "allowed_sources"
            in metadata
            and "source" in params
        ):

            if (
                params["source"]
                not in metadata[
                    "allowed_sources"
                ]
            ):
                return (
                    f"Invalid source: "
                    f"{params['source']}"
                )

        if (
            "allowed_metrics"
            in metadata
            and "metric" in params
        ):

            if (
                params["metric"]
                not in metadata[
                    "allowed_metrics"
                ]
            ):
                return (
                    f"Invalid metric: "
                    f"{params['metric']}"
                )

        return None

    @staticmethod
    def _build_clarification_question(
        missing_fields,
    ):

        labels = {
            "title": "عنوان",
            "description": "توضیحات",
            "assignee_id": "مسئول تسک",
            "fullname": "نام کاربر",
            "department": "دپارتمان",
            "updates": "مقادیر بروزرسانی",
            "metric": "نوع تحلیل",
            "source": "منبع داده",
        }

        translated = []

        for field in missing_fields:

            translated.append(
                labels.get(
                    field,
                    field,
                )
            )

        return (
            "لطفا موارد زیر را مشخص کنید: "
            + " ، ".join(translated)
        )