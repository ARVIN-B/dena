from langgraph.graph import (
    StateGraph,
    END,
)

from app.agent.state import (
    AgentState,
)

from app.agent.nodes import (
    planner_node,
    tool_executor_node,
    clarification_node,
    reflection_node,
    memory_node,
    response_node,
    error_node,
)

from app.agent.router import (
    route_after_planner,
    route_after_clarification,
    route_after_tool_executor,
    route_after_reflection,
    route_after_memory,
    route_after_response,
    route_after_error,
)


def build_graph():

    workflow = StateGraph(
        AgentState
    )

    workflow.add_node(
        "planner",
        planner_node,
    )

    workflow.add_node(
        "tool_executor",
        tool_executor_node,
    )

    workflow.add_node(
        "clarification",
        clarification_node,
    )

    workflow.add_node(
        "reflection",
        reflection_node,
    )

    workflow.add_node(
        "memory",
        memory_node,
    )

    workflow.add_node(
        "response",
        response_node,
    )

    workflow.add_node(
        "error",
        error_node,
    )

    workflow.set_entry_point(
        "planner"
    )

    workflow.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "tool_executor": "tool_executor",
            "clarification": "clarification",
            "error": "error",
        },
    )

    workflow.add_conditional_edges(
        "tool_executor",
        route_after_tool_executor,
        {
            "reflection": "reflection",
            "error": "error",
        },
    )

    workflow.add_conditional_edges(
        "reflection",
        route_after_reflection,
        {
            "tool_executor": "tool_executor",
            "clarification": "clarification",
            "memory": "memory",
            "error": "error",
        },
    )

    workflow.add_conditional_edges(
        "memory",
        route_after_memory,
        {
            "response": "response",
            "error": "error",
        },
    )

    workflow.add_conditional_edges(
        "clarification",
        route_after_clarification,
        {
            "__end__": END,
        },
    )

    workflow.add_conditional_edges(
        "response",
        route_after_response,
        {
            "__end__": END,
        },
    )

    workflow.add_conditional_edges(
        "error",
        route_after_error,
        {
            "__end__": END,
        },
    )

    return workflow.compile()