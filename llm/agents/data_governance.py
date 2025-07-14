from llm.agents.base import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from llm.models.agent_state import AgentState
from llm.models.data_governance import DataGovernance
from langgraph.types import Command
from datetime import datetime

class DataGovernanceAgent(BaseAgent):

    def __init__(self):
        super().__init__(agent_name="data_governance",
                         prompt_file="data_governance.j2",
                         structured_output_model=DataGovernance
                         )

    def run(self, state: AgentState) -> AgentState:
        current_messages = state["messages"]
        source_schemas = state.get("source_schemas", {})
        initial_user_details = state.get("initial_user_details", {})
        prompt = self.build_prompt({
            "source_schemas": source_schemas,
            "initial_user_details": initial_user_details,
            "domain": initial_user_details.get("domain", "general"),
            "current_date": datetime.now().strftime("%Y-%m-%d"),
        })
        result = self.call_llm([SystemMessage(prompt), current_messages[0]])
        updated_contract_dict = result.model_dump()
        contract = state.get("contract", {})
        final_message = AIMessage(
            content=f"data_governance_agent complete for data product: {updated_contract_dict}")
        state["messages"] = [final_message]
        final_metadata_contract = {**contract, **updated_contract_dict}

        return {"messages": [final_message],
                "contract": final_metadata_contract}
