from llm.agents.base import BaseAgent
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from llm.models.agent_state import AgentState
from llm.models.dbt_tests import AllColumnsTest
from llm.utils.data_quality_rules import rule_refrences
from llm.utils.download_dbt_test_case import download_dbt_yaml

class DbtTestCaseGeneratorAgent(BaseAgent):
    """
    Agent responsible for generating dbt test cases.
    It uses LLM to process the initial user request and generate a structured schema.
    """

    def __init__(self, model: str):
        super().__init__(model=model,
                         agent_name="dbt_test_case_generator_agent",
                         prompt_file="dbt_test_case_generator.j2",
                         structured_output_model=AllColumnsTest
                         )

    def run(self, state: AgentState) -> AgentState:

        # current_messages = state.get("messages", [])[0]
        source_schemas = state.get("source_schemas", {})
        contract = state.get("contract", {})

        prompt = self.build_prompt({
            "rule_refrences": rule_refrences,
            "contract": contract,
            "source_schemas": source_schemas
        })

        result = self.call_llm([SystemMessage(prompt), HumanMessage(
            content="generate dbt test cases for the provided schema")])
        updated_contract_dict = result.model_dump()
        
        download_dbt_yaml(updated_contract_dict)
        # final_schema_contract = {**contract, **updated_contract_dict}
        final_message = AIMessage(
            content=f"DBT test cases generated: {updated_contract_dict}")
        state["messages"] = [final_message]
        # final_schema_contract = {**state.get("contract", {}), **updated_contract_dict}
        return {"messages": [final_message]}