from llm.agents.base import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from llm.models.agent_state import AgentState
from llm.models.supervisor import Router, SUPERVISOR_AGENTS
from langgraph.types import Command
from langgraph.graph import START, END


class Supervisor(BaseAgent):
    """
    Supervisor agent that oversees the execution of tasks and manages other agents.
    It can assign tasks, monitor progress, and ensure that the overall objectives are met.
    """

    def __init__(self, model: str):
        super().__init__(model=model,
                         agent_name="supervisor",
                         prompt_file="request_processing.j2",
                         structured_output_model=Router
                         )

    def run(self, state: AgentState) -> AgentState:

        current_messages = state["messages"][-1]
        domain = state.get("initial_user_details", {}).get("domain", "general")
        agents = ", ".join(SUPERVISOR_AGENTS)

        prompt = self.build_prompt({
            "domain": domain,
            "agents": agents
        })
        current_messages = state.get("messages", [])[0]
        current_messages = state["messages"]

        result = self.call_llm([SystemMessage(prompt), *current_messages])
        next_agent = result["next"]
        resone = result["resone"]

        if next_agent == "FINISH":
            state["finished"] = True
            return Command(goto=END)
            
        return Command(
            update={**state,
                    "messages": [HumanMessage(content=f"Routing to {next_agent} for further processing. Reason: {resone}")]},
            goto=next_agent)

    def assign_task(self, agent, task):
        """Assign a task to a specific agent."""
        agent.receive_task(task)
        self.assigned_agents.append(agent)

    def monitor_progress(self):
        """Monitor the progress of assigned agents."""
        for agent in self.assigned_agents:
            print(f"Agent {agent.name} is working on: {agent.current_task}")
