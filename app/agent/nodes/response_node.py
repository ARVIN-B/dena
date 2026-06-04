import json

from app.agent.state import AgentState


STATUS_LABELS = {
    "Open": "باز",
    "In Progress": "در حال انجام",
    "Done": "بسته",
    "Review": "در حال بررسی",
}

PRIORITY_LABELS = {
    "Low": "کم‌اهمیت",
    "Medium": "متوسط",
    "High": "مهم",
    "Critical": "حیاتی",
}


def _format_scalar_result(
    value,
):

    if isinstance(
        value,
        bool,
    ):
        return "بله" if value else "خیر"

    if isinstance(
        value,
        (int, float),
    ):
        if isinstance(
            value,
            float,
        ):
            value = round(
                value,
                2,
            )

        return str(
            value
        )

    return str(
        value
    )


def _summarize_record(
    record,
):

    if not isinstance(
        record,
        dict,
    ):
        return _format_scalar_result(
            record
        )

    preferred_keys = [
        "fullname",
        "title",
        "status",
        "priority",
        "department",
        "id",
    ]

    parts = []

    for key in preferred_keys:

        value = record.get(
            key
        )

        if value not in [
            None,
            "",
        ]:
            parts.append(
                f"{key}={_format_scalar_result(value)}"
            )

    if parts:
        return "، ".join(
            parts
        )

    return json.dumps(
        record,
        ensure_ascii=False,
        default=str,
    )


def _describe_count_scope(
    params,
):

    parts = []

    user_name = params.get(
        "user_name"
    ) or params.get(
        "fullname"
    )

    if user_name not in [
        None,
        "",
    ]:
        parts.append(
            str(
                user_name
            )
        )

    status = STATUS_LABELS.get(
        params.get("status"),
        params.get("status"),
    )

    if status not in [
        None,
        "",
    ]:
        parts.append(
            str(status)
        )

    priority = PRIORITY_LABELS.get(
        params.get("priority"),
        params.get("priority"),
    )

    if priority not in [
        None,
        "",
    ]:
        parts.append(
            str(priority)
        )

    department = params.get(
        "department"
    )

    if department not in [
        None,
        "",
    ]:
        parts.append(
            f"دپارتمان {department}"
        )

    return "، ".join(
        parts
    )


def _build_answer(
    user_query,
    tool_results,
    plan=None,
):

    if not tool_results:
        return "نتیجه‌ای برای نمایش وجود ندارد."

    successful_results = [
        result
        for result in tool_results
        if result.get(
            "success"
        )
    ]

    failed_results = [
        result
        for result in tool_results
        if not result.get(
            "success"
        )
    ]

    if not successful_results:

        errors = [
            str(
                result.get(
                    "error",
                    "Unknown Error",
                )
            )
            for result in failed_results
        ]

        return (
            "خطا در اجرای درخواست:\n"
            + "\n".join(
                errors
            )
        )

    if len(successful_results) == 1:

        result = successful_results[0].get(
            "result"
        )
        tool_name = successful_results[0].get(
            "tool"
        )

        if isinstance(
            result,
            (int, float),
        ):

            if tool_name == "count" and isinstance(
                plan,
                list,
            ):

                for step in plan:

                    if step.get("tool") != "count":
                        continue

                    scope = _describe_count_scope(
                        step.get(
                            "params",
                            {},
                        )
                    )

                    if scope:
                        return (
                            f"تعداد تسک‌های {scope} { _format_scalar_result(result) } مورد است."
                        )

            return (
                f"نتیجه درخواست شما { _format_scalar_result(result) } است."
            )

        if isinstance(
            result,
            list,
        ):

            if not result:
                return "موردی پیدا نشد."

            lines = [
                "نتایج یافت‌شده:"
            ]

            for index, item in enumerate(
                result[:5],
                start=1,
            ):
                lines.append(
                    f"{index}. {_summarize_record(item)}"
                )

            if len(result) > 5:
                lines.append(
                    f"و {len(result) - 5} مورد دیگر."
                )

            return "\n".join(
                lines
            )

        if isinstance(
            result,
            dict,
        ):
            return (
                "نتیجه عملیات:\n"
                + _summarize_record(
                    result
                )
            )

        return (
            "نتیجه درخواست:\n"
            + _format_scalar_result(
                result
            )
        )

    lines = [
        "نتایج اجرای ابزارها:"
    ]

    for result in successful_results:

        tool_name = result.get(
            "tool",
            "tool",
        )
        value = result.get(
            "result"
        )

        if isinstance(
            value,
            list,
        ):
            lines.append(
                f"- {tool_name}: {len(value)} مورد"
            )
        else:
            lines.append(
                f"- {tool_name}: {_format_scalar_result(value)}"
            )

    return "\n".join(
        lines
    )


async def response_node(
    state: AgentState,
) -> AgentState:

    try:

        tool_results = state.get(
            "tool_results",
            [],
        )

        state["final_answer"] = _build_answer(
            state.get("user_query", ""),
            tool_results,
            state.get("plan"),
        )

        return state

    except Exception as e:

        state["error"] = str(
            e
        )

        return state
