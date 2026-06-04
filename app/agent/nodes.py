from app.agent.state import AgentState
from app.tools.stats_tools import count_open_tasks


def planner_node(state: AgentState):
    query = state["user_query"]
    if "باز" in query:
        return {
            "selected_tool": "count_open_tasks"
        }
    return {
        "final_answer": "متوجه سؤال نشدم."
    }


def tool_node(state: AgentState):
    tool = state["selected_tool"]
    if tool == "count_open_tasks":
        result = count_open_tasks()
        return {
            "tool_result": result
        }
    return {}


def response_node(state: AgentState):
    if state.get("final_answer"):
        return {
            "final_answer": state["final_answer"]
        }
    return {
        "final_answer": f"تعداد تسک‌های باز: {state['tool_result']}"
    }