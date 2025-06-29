

# from base import Agent
from pydantic import BaseModel
from llm.agents.base import BaseAgent
# from prompts import SystemPrompt

from langchain_core.messages import SystemMessage, AIMessage, BaseMessage, ToolMessage
from llm.models.agent_state import AgentState

from llm.tools.tool_registry import AGENT_TOOL_REGISTRY
import json
from typing import Dict, Any



class SystemAgent(BaseAgent):

    def __init__(self, model: str):
        tools_list = AGENT_TOOL_REGISTRY.get("system", [])
        tools_dict = {tool.name: tool for tool in tools_list}

        super().__init__(model=model,
                         agent_name="system",
                         prompt_file="request_processing.j2",

                         tools=tools_dict

                         )

    def process_tool_calls(self, state: AgentState, tool_response: BaseMessage) -> AgentState:
        last_tool_message = next(
            (msg for msg in reversed(
                state["messages"]) if isinstance(msg, ToolMessage)),
            None
        )
        tool_output_dict = {}
        if last_tool_message:
            print("^^^^"*100)

            try:
                tool_output = last_tool_message.content
                tool_output_dict = json.loads(tool_output)
                if isinstance(tool_output_dict, dict) and "error" in tool_output_dict:
                    error_msg = f"Tool Error: {tool_output_dict['error']}"
                    return {
                        **state,
                        "messages": [AIMessage(content=error_msg)]
                    }

            except json.JSONDecodeError:
                return {
                    **state,
                    "messages": [AIMessage(content="Error parsing tool output.")]
                }
        other_state = self.prepare_agent_state(state)
        return {
            **state,
            **other_state,
            "messages": [tool_response],
            "source_schemas": tool_output_dict
        }


    def run(self, state: AgentState) -> AgentState:
        print("this is a stete", state)
        tool_names = list(self.tools.keys())


        prompt = self.build_prompt({
            "available_tools": ", ".join(tool_names)
        })
        current_messages = state.get("messages", [])[0]
        current_messages = state["messages"]

        result = self.call_llm([SystemMessage(prompt), *current_messages],
                               use_tools=True)
        d = self.process_tool_calls(state, result)
        print("result", state)
        print("state messages", state["messages"])
        return d

