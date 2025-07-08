from llm.agents.base import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from llm.models.agent_state import AgentState
from llm.models.supervisor import Router, SUPERVISOR_AGENTS
from langgraph.types import Command
from langgraph.graph import START, END
from typing import Literal

from llm.models.supervisor import SUPERVISOR_AGENTS
AgentLiteral = Literal["data_engineer", "data_steward_agent", "FINISH"]


class Supervisor(BaseAgent):
    """
    Supervisor agent that oversees the execution of tasks and manages other agents.
    It can assign tasks, monitor progress, and ensure that the overall objectives are met.
    """

    def __init__(self, model: str):
        super().__init__(model=model,
                         agent_name="supervisor",
                         prompt_file="supervisor.j2",
                         structured_output_model=Router
                         )

    def run(self, state: AgentState) -> Command[Literal["data_engineer", "data_steward_agent", "FINISH"]]:
        print("#" * 20, "Supervisor Agent Run", "#" * 20,
              "current state:", state.get("initial_user_details", "N/A"))
        current_messages = state["messages"][-1]
        domain = state.get("initial_user_details", {}).get("domain", "general")
        agents = ", ".join(SUPERVISOR_AGENTS + ["FINISH"])

        prompt = self.build_prompt({
            "domain": domain,
            "agents": agents,
            "progress": state.get("progress", {}),
            "current_agent": state.get("current_agent", {}),
        })
        current_messages = state.get("messages", [])[0]
        current_messages = state["messages"]

        result = self.call_llm([SystemMessage(prompt), *current_messages])

        next_agent = result["next"]
        resone = result["resone"]

        if next_agent == "FINISH":
            # state["finished"] = True
            return Command(goto=END)

        return Command(
            update={**state,
                    "messages": [HumanMessage(content=f"Routing to {next_agent} for further processing. Reason: {resone}")]},
            goto=next_agent)
