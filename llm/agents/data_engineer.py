from llm.agents.base import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from llm.models.agent_state import AgentState
from llm.models.data_engineer import DataProductSchema
from langgraph.types import Command


class DataEngineer(BaseAgent):

    def __init__(self, model: str):
        super().__init__(model=model,
                         agent_name="data_engineer",
                         prompt_file="data_engineer.j2",
                         structured_output_model=DataProductSchema
                         )

    def run(self, state: AgentState) -> AgentState:
        # source_schemas, initial_user_details

        current_messages = state["messages"]
        source_schemas = state.get("source_schemas", {})
        initial_user_details = state.get("initial_user_details", {})
        prompt = self.build_prompt({
            "source_schemas": source_schemas,
            "initial_user_details": initial_user_details
        })
        result = self.call_llm([SystemMessage(prompt), current_messages[0]])
        updated_contract_dict = result.model_dump()
        contract = state.get("contract", {})
        final_schema_contract = {**contract, **updated_contract_dict}
        final_message = AIMessage(
            content=f"Schema generation complete for data product: {updated_contract_dict}")
        return {**state,
                **{"messages": [final_message],
                   "contract": final_schema_contract}}
