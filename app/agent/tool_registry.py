from app.tools.stats_tools import *
from app.tools.search_tools import *
from app.tools.analytics_tools import *
from app.tools.action_tools import *


TOOLS = {
    # stats
    "count": count,

    # search
    "search": search,

    # analytics
    "aggregate": aggregate,

    # task actions
    "create_task": create_task,
    "update_task": update_task,
    "delete_task": delete_task,

    # user actions
    "create_user": create_user,
    "update_user": update_user,
    "delete_user": delete_user,
}