import json
import re
import logging

from app.agent.state import AgentState
from app.agent.parameter_resolver import ParameterResolver

from app.agent.tool_registry import TOOLS
from app.agent.tool_schemas import (
    TOOL_SCHEMAS,
    TOOL_METADATA,
)

from app.agent.llm.llm import ask_llm


logger = logging.getLogger(__name__)


def _normalize_text(
    value,
):

    if not value:
        return ""

    return str(
        value
    ).strip()


def _extract_previous_filters(
    memory_context,
):

    filters = {}

    if not isinstance(
        memory_context,
        list,
    ):
        return filters

    for memory_item in reversed(
        memory_context
    ):

        plan = memory_item.get(
            "plan",
            []
        )

        if not isinstance(
            plan,
            list,
        ):
            continue

        for step in plan:

            params = step.get(
                "params",
                {}
            )

            if not isinstance(
                params,
                dict,
            ):
                continue

            for key in [
                "user_name",
                "fullname",
                "status",
                "priority",
                "department",
            ]:

                value = params.get(
                    key
                )

                if value not in [
                    None,
                    "",
                ]:
                    filters[key] = value

        if filters:
            break

    return filters


def _build_count_plan(
    query,
    memory_context,
):

    normalized_query = query.strip()
    lowered_query = normalized_query.lower()

    if not re.search(
        r"(چند|تعداد)",
        normalized_query,
    ):
        return None

    params = {
        "source": "tasks",
    }

    previous_filters = _extract_previous_filters(
        memory_context
    )

    for key in [
        "user_name",
        "fullname",
        "status",
        "priority",
        "department",
    ]:

        value = previous_filters.get(
            key
        )

        if value not in [
            None,
            "",
        ]:
            params[key] = value

    if re.search(
        r"(^|\s)باز(\s|$)",
        normalized_query,
    ):
        params["status"] = "Open"

    if re.search(
        r"(^|\s)بسته(\s|$)",
        normalized_query,
    ):
        params["status"] = "Done"

    if (
        "حیاتی" in normalized_query
        or "critical" in lowered_query
    ):
        params["priority"] = "Critical"

    if (
        "بالا" in normalized_query
        or "high" in lowered_query
    ) and params.get("priority") is None:
        params["priority"] = "High"

    name_match = re.match(
        r"^(?P<name>.+?)\s+چند(?:تا| تا)?",
        normalized_query,
    )

    if name_match:
        candidate_name = _normalize_text(
            name_match.group("name")
        )

        if candidate_name and candidate_name not in [
            "چند",
            "حالا",
            "الان",
            "میشه",
            "لطفا",
        ]:
            params["user_name"] = candidate_name

    if not any(
        key in params
        for key in [
            "user_name",
            "fullname",
            "status",
            "priority",
            "department",
        ]
    ):
        return None

    return [
        {
            "tool": "count",
            "params": params,
        }
    ]


def _parse_planner_response(
    llm_response: str,
):

    candidates = []

    stripped = (
        llm_response.strip()
    )

    candidates.append(
        stripped
    )

    fenced_match = re.search(
        r"```(?:json)?\s*(.*?)\s*```",
        stripped,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if fenced_match:
        candidates.insert(
            0,
            fenced_match.group(1).strip(),
        )

    for start, end in [
        ("[", "]"),
        ("{", "}"),
    ]:

        start_index = stripped.find(
            start
        )
        end_index = stripped.rfind(
            end
        )

        if (
            start_index != -1
            and end_index != -1
            and end_index > start_index
        ):

            candidates.append(
                stripped[start_index:end_index + 1].strip()
            )

    for candidate in candidates:

        try:
            parsed = json.loads(
                candidate
            )

            if isinstance(
                parsed,
                dict,
            ) and "plan" in parsed:
                return parsed["plan"]

            if isinstance(
                parsed,
                dict,
            ) and "tool" in parsed:
                return [parsed]

            return parsed

        except Exception:
            continue

    raise ValueError(
        "Planner must return valid JSON"
    )


PLANNER_SYSTEM_PROMPT = f"""
You are an AI Planner.

Your job is ONLY to convert user requests into execution plans.

Available tools:

{json.dumps(
    TOOL_SCHEMAS,
    ensure_ascii=False,
    indent=2
)}

Tool metadata:

{json.dumps(
    {
        k: str(v)
        for k, v in TOOL_METADATA.items()
    },
    ensure_ascii=False,
    indent=2
)}

Rules:

1. Return ONLY valid JSON.
2. Never explain.
3. Never answer the user.
4. Generate a list of tool calls.
5. Multi-step plans are allowed.
6. Use exact tool names.
7. Fill parameters when possible.
8. If information is missing, leave parameter empty.
9. For create_task, prefer assignee_name when user mentions a person by name.
10. Use memory context to resolve follow-up references like "now", "them", or "those tasks".

Output format:

[
    {{
        "tool": "count",
        "params": {{
            "source": "task_users",
            "status": "Open"
        }}
    }},
    {{
        "tool": "create_task",
        "params": {{
            "title": "پیگیری درخواست مشتری",
            "description": "بررسی مشکل و پاسخ به مشتری",
            "assignee_name": "علی صابری"
        }}
    }}
]
"""

async def planner_node(
    state: AgentState,
) -> AgentState:

    try:

        query = state["user_query"]

        memory_context = state.get(
            "memory_context",
            []
        )

        heuristic_plan = _build_count_plan(
            query,
            memory_context,
        )

        if heuristic_plan is not None:
            llm_response = json.dumps(
                heuristic_plan,
                ensure_ascii=False,
                indent=2,
            )
        else:
            planner_prompt = f"""
                Memory Context:

                {json.dumps(
                    memory_context[-5:],
                    ensure_ascii=False,
                    default=str,
                )}

                User Request:

                {query}

                Generate execution plan.
                """

            llm_response = await ask_llm(
                planner_prompt,
                system_message=PLANNER_SYSTEM_PROMPT,
            )
        
        logger.debug(
            "Planner LLM response: %s",
            llm_response,
        )

        raw_plan = _parse_planner_response(
            llm_response
        )

        if not isinstance(
            raw_plan,
            list
        ):
            raise ValueError(
                "Planner must return list"
            )

        validated_plan = []

        clarification_needed = False

        clarification_questions = []

        clarification_contexts = []

        for step in raw_plan:

            tool_name = step.get(
                "tool"
            )

            params = step.get(
                "params",
                {}
            )

            if tool_name not in TOOLS:

                raise ValueError(
                    f"Unknown tool: {tool_name}"
                )

            resolved = (
                ParameterResolver.resolve(
                    tool_name,
                    params,
                )
            )

            if resolved.get(
                "error"
            ):
                raise ValueError(
                    resolved["error"]
                )

            if resolved.get(
                "clarification_needed"
            ):

                clarification_needed = True

                clarification_questions.append(
                    resolved.get(
                        "clarification_question",
                        ""
                    )
                )

                clarification_contexts.append(
                    resolved.get(
                        "clarification_context",
                        {}
                    )
                )

            validated_plan.append(
                {
                    "tool": tool_name,
                    "params": resolved[
                        "params"
                    ],
                }
            )

        execution_history = state.get(
            "execution_history",
            []
        )

        execution_history.append(
            {
                "node": "planner",
                "query": query,
                "plan": validated_plan,
            }
        )

        metadata = state.get(
            "metadata",
            {}
        )

        metadata[
            "planner_raw_response"
        ] = llm_response

        state["metadata"] = metadata

        state[
            "execution_history"
        ] = execution_history

        state["plan"] = validated_plan

        state["current_step"] = 0

        state[
            "clarification_needed"
        ] = clarification_needed

        state[
            "clarification_question"
        ] = "\n".join(
            clarification_questions
        )

        state[
            "clarification_context"
        ] = {
            "items": clarification_contexts
        }

        return state

    except Exception as e:

        state["error"] = str(
            e
        )

        return state
