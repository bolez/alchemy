from llm.agents.base import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from llm.models.agent_state import AgentState
from llm.models.data_quality import ValidationRule
from langgraph.types import Command
from llm.utils.data_quality_rules import rule_refrences


class DataQualityAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="data_quality_agent",
                         prompt_file="data_quality.j2",
                         structured_output_model=ValidationRule
                         )
                         
    def run(self, state: AgentState) -> Command:
        current_messages = state["messages"]
        source_schemas = state.get("source_schemas", {})
        initial_user_details = state.get("initial_user_details", {})
        contract = state.get("contract", {})

        prompt = self.build_prompt({
            "rule_refrences": rule_refrences,
            "contract": initial_user_details,
            "source_schemas": source_schemas
        })
        
        result = self.call_llm([SystemMessage(prompt), current_messages[0]])
        updated_contract_dict = result.model_dump()
        final_schema_contract = {**contract, **updated_contract_dict}
        final_message = AIMessage(
            content=f"data Quality generation complete for data product: {updated_contract_dict}")
        state["messages"] = [final_message]
        final_schema_contract = {**state.get("contract", {}), **updated_contract_dict}
        return {"messages": [final_message],
                "contract": final_schema_contract}

