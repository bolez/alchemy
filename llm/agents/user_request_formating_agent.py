
from llm.agents.base import BaseAgent
from llm.models.system import UserRequest
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from llm.models.agent_state import AgentState


class RequestFromating(BaseAgent):
    def __init__(self, model: str):

        super().__init__(model=model,
                         agent_name="request_formating",
                         prompt_file="request_formating.j2",
                         structured_output_model=UserRequest
                         )

    def run(self, state: AgentState) -> AgentState:
        # print("#" * 20, "request", "#" * 20)
        current_messages = state.get("messages", [])[0]
        source_schemas = state.get("source_schemas", {})
        initial_message = current_messages.content if state.get(
            "messages") else ""

        prompt = self.build_prompt({
            "source_schemas": source_schemas,
            "initial_message": initial_message,
        })
        response = self.call_llm([HumanMessage(prompt)])
        result = response.model_dump() if isinstance(
            response, UserRequest) else response
        state["messages"] = [AIMessage(
            content=f"request_proccessing_agent executed successfully start Preparing data contract using available agents using state: {state}")]
        print("Result from request_formating agent:", result, type(result))
        return { "messages":  [AIMessage(
            content=f"request_proccessing_agent executed successfully start Preparing data contract using available agents using state: {state}")],
                    "schema_file_path": result["schema_file_path"],
                    "initial_user_details": result["initial_user_details"],
                    "source_schemas": result["source_schemas"]
                }
