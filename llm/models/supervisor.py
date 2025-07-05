from typing import Literal, TypedDict
SUPERVISOR_AGENTS = []


class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""
    next: Literal[*SUPERVISOR_AGENTS, "FINISH"]
    resone: str
