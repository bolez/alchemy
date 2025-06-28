from langchain_core.messages import ToolMessage
from typing import Dict, Any
import json


class ToolNode:
    def __init__(self, tools: Dict[str, Any]):
        """_summary_

        Args:
            tools (Dict[str, Any]): tools dictionary where keys are tool names 
            and values are callable functions.
        """
        self.tools = tools

    def __call__(self, state: dict) -> dict:
        messages = state["messages"]
        last_msg = messages[-1]
        outputs = []

        for tool_call in getattr(last_msg, "tool_calls", []):
            tool_name = tool_call["name"]
            args = tool_call["args"]
            if tool_name not in self.tools:
                raise ValueError(f"Tool '{tool_name}' not found.")

            result = self.tools[tool_name](args)

            outputs.append(
                ToolMessage(
                    content=json.dumps(result),
                    name=tool_name,
                    tool_call_id=tool_call["id"]
                )
            )

        return {"messages": outputs}
