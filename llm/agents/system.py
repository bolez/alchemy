

from agents.base import Agent
from pydantic import BaseModel
from agents.base import BaseAgent
# from prompts import SystemPrompt

from tools.tool_registry import AGENT_TOOL_REGISTRY

class SystemAgent(BaseAgent):
    
    def __init__(self, model: str):
        super().__init__(model=model,
                         agent_name="system",
                         prompt_file="request_processing.j2",
                         tools=AGENT_TOOL_REGISTRY.get("system", {})
        )

    def run(self, state: dict) -> dict:
        state["current_agent"] = self.agent_name
        state["agent_status"] = {
            agent: {"revised": False, "reviewed": False}
            for agent in state.get("agents", [])
        }
        state["progress"] = {
            agent: "pending" for agent in state.get("agents", [])
        }
        prompt = self.build_prompt({
            "available_tools": ", ".join(self.tools.keys())
        })
        current_messages = state["messages"]
        result = self.call_llm(prompt)
        state["messages"] = current_messages + [result]
        return state
