
from langchain.agents import tool
from tools.agent_tool_registry import AGENT_TOOL_REGISTRY


def register_tool(agent_name: str):
    def wrapper(func):
        decorated = tool(func)
        print(decorated)
        AGENT_TOOL_REGISTRY.setdefault(agent_name, []).append(decorated)
        return decorated
    return wrapper
