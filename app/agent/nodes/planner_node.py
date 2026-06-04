import json

from app.agent.state import AgentState
from app.agent.parameter_resolver import ParameterResolver

from app.agent.tool_registry import TOOLS
from app.agent.tool_schemas import (
    TOOL_SCHEMAS,
    TOOL_METADATA,
)

from app.agent.llm.llm import ask_llm


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

Output format:

[
    {{
        "tool": "count",
        "params": {{
            "source": "task_users",
            "status": "Open"
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

        raw_plan = json.loads(
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