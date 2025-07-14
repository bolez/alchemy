from llm.agents.base import BaseAgent
from langchain_core.messages import SystemMessage, AIMessage
from llm.models.agent_state import AgentState
from llm.models.data_steward import SemanticMetadata


class DataStewardAgent(BaseAgent):
    """
    Agent responsible for generating and refining data product schemas.
    It uses LLM to process the initial user request and generate a structured schema.
    """

    def __init__(self):
        super().__init__(agent_name="data_steward_agent",
                         prompt_file="data_steward.j2",
                         structured_output_model=SemanticMetadata
                         )

    def merge_columns_by_name(self, contract_column: list, data_steward_agent_column: list) -> list:
        # Build lookup from data_steward_agent_column
        steward_lookup = {col["column_name"]                          : col for col in data_steward_agent_column}

        merged = []
        for col in contract_column:
            col_name = col.get("column_name")
            if col_name in steward_lookup:
                merged.append({**col, **steward_lookup[col_name]})
            else:
                merged.append(col)

        extra = [
            col for col in data_steward_agent_column
            if col["column_name"] not in {c["column_name"] for c in contract_column}
        ]
        merged.extend(extra)

        return merged

    def run(self, state: AgentState) -> AgentState:
        """
        Runs the data steward agent to generate a schema based on the provided state.
        It retrieves source schemas and initial user details from the state,
        builds a prompt, and calls the LLM to generate the schema.
        """
        current_messages = state.get("messages", [])[0]
        source_schemas = state.get("source_schemas", {})
        contract = state.get("contract", {})

        prompt = self.build_prompt({
            "source_schemas": source_schemas,
            "contract": contract
        })

        response = self.call_llm([SystemMessage(prompt), current_messages])
        result = response.model_dump() if hasattr(response, 'model_dump') else response
        # updated_contract_dict = data_contract_obj.model_dump()
        contract_column = contract.get("properties", [])
        data_steward_agent_column = result.get("columns", [])
        m = self.merge_columns_by_name(
            contract_column, data_steward_agent_column)
        contract['properties'] = m
        s_contract = {k: v for k, v in result.items() if k != 'columns'}

        final_message = AIMessage(
            content=f"data_steward_agent completed  data contract completed: {result}")

        state["messages"] = [final_message]
        # state["progress"]["data_steward_agent"] = "completed"
        # updated_state = self.update_agent_state(state, is_completed=True)

        return {
            # **state, 
        **{"messages": [final_message], "contract": {**contract, **s_contract}}
                # **updated_state
                }
        # print("Final contract after data steward agent:", contract)
        # return {"contract": {**contract, **s_contract}, "messages": [final_message]}
