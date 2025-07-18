from llm.agents.base import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from llm.models.agent_state import AgentState
from llm.utils.contract_downloader import download_contract_in_yaml, save_markdown_tool


class DataContractGeneratorAgent(BaseAgent):

    def __init__(self):
        super().__init__(agent_name="data_contract_generator_agent",
                         prompt_file="data_contract.j2"
                         )

    def run(self, state: AgentState) -> AgentState:
        contract = state.get("contract", {})
        domain = state.get("initial_user_details", {}). get("domain", "default_domain")
        prompt = self.build_prompt({
            "contract": state.get("contract", {}),
        })
        result = self.call_llm([SystemMessage(prompt), HumanMessage(
            content="generate markdown content of contract")])

        yaml_contract_generator = download_contract_in_yaml(domain, contract)
        print("yaml_contract_generator", yaml_contract_generator)
        if yaml_contract_generator.get("status") != "success":
            raise Exception(f"Failed to download contract in YAML: {yaml_contract_generator.get('error', 'Unknown error')}")
    
        markdown_contract_generator = save_markdown_tool(domain, result.content)
        if markdown_contract_generator.get("status") != "success":
            raise Exception(f"Failed to save markdown contract: {markdown_contract_generator.get('error', 'Unknown error')}")

        final_message = [
            AIMessage(content=f"yaml and markdown files downloaded")]

        return {"messages": final_message}
