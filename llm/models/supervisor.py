from typing import Literal, TypedDict
from llm.config.loader import load_config
config = load_config()
SUPERVISOR_AGENTS = config["supervisor"]


class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""
    next: Literal[*SUPERVISOR_AGENTS, "FINISH"]
    resone: str
