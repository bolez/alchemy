from langchain_core.tools import tool
from llm.tools.tool_registry import AGENT_TOOL_REGISTRY


def register_tool(agent_name: str):
    def wrapper(func):
        decorated = tool(func)
        AGENT_TOOL_REGISTRY.setdefault(agent_name, []).append(decorated)
        return decorated
    return wrapper
