from llm.agents.system import SystemAgent
from llm.models.agent_state import AgentState
import json
from datetime import datetime
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, ToolMessage
from llm.tools.tool_registry import AGENT_TOOL_REGISTRY
from llm.tools.tool_node import ToolNode
from llm.tools import load_all_tools
from llm.agents.user_request_formating_agent import RequestFromating
from langgraph.checkpoint.memory import MemorySaver
from llm.agents.supervisor import Supervisor
from llm.agents.data_engineer import DataEngineer
from llm.agents.data_steward import DataStewardAgent
from llm.agents.data_quality import DataQualityAgent
from llm.agents.data_governance import DataGovernanceAgent
from llm.agents.contract_generator import DataContractGeneratorAgent
from llm.agents.human_review_mixin import human_editing
from llm.agents.dbt_test_case_generator import DbtTestCaseGeneratorAgent
from langgraph.types import Command
from llm.utils.user_input import add_watermark, remove_watermark, get_user_input_via_editor
load_all_tools()


system_agent = SystemAgent()
system_tools = AGENT_TOOL_REGISTRY.get("system", [])
tools_by_name = {tool.name: tool for tool in system_tools}

superviser_agent = Supervisor()  
request_fromating_agent = RequestFromating()
graph_builder = StateGraph(AgentState)

graph_builder.add_node("system_agent", system_agent)
graph_builder.add_node("superviser_agent", superviser_agent)
graph_builder.add_node("request_formatting", request_fromating_agent)
graph_builder.add_node("tools", ToolNode(tools_by_name))
graph_builder.add_node("data_engineer", DataEngineer())
graph_builder.add_node("data_steward_agent", DataStewardAgent())
graph_builder.add_node("data_quality_agent", DataQualityAgent())
graph_builder.add_node("data_governance_agent", DataGovernanceAgent())
graph_builder.add_node("data_contract_generator_agent", DataContractGeneratorAgent())
graph_builder.add_node("dbt_test_case_generator_agent", DbtTestCaseGeneratorAgent())
graph_builder.add_node("human_editing", human_editing)

def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "respond"
    else:
        return "continue"   


graph_builder.add_edge(START, "system_agent")
graph_builder.add_edge("tools", "system_agent")

graph_builder.add_conditional_edges(
    "system_agent",
    should_continue,
    {
        "continue": "tools",
        "respond": "request_formatting",
    },
)
graph_builder.add_edge("request_formatting", "superviser_agent")
graph_builder.add_edge("data_engineer", "human_editing")
graph_builder.add_edge("data_steward_agent", "human_editing")
graph_builder.add_edge("data_quality_agent", "human_editing")
graph_builder.add_edge("data_governance_agent", "human_editing")
graph_builder.add_edge("data_contract_generator_agent", "superviser_agent")
graph_builder.add_edge("dbt_test_case_generator_agent", "superviser_agent")
graph_builder.add_edge("human_editing", "superviser_agent")  
graph_builder.add_edge("superviser_agent", END)

ROUTABLE_AGENTS = [
    "data_engineer",
    "data_steward_agent",
    "data_quality_agent",
    "data_governance_agent",
    "data_contract_generator_agent",
    "dbt_test_case_generator_agent",
    "FINISH"
]

graph_builder.add_conditional_edges(
    "superviser_agent",
    lambda state: state.get("next_agent", "FINISH"),
    {
        agent: agent for agent in ROUTABLE_AGENTS if agent != "FINISH"
    } | {"FINISH": END}
)

new_contract_path = r"/Users/gauravbole/Documents/workspace/alchemy/formatted_orders.yml"


def create_contract(owner, schema_path, domain, schedule, refresh_method):
    contract_details = {
        "domain": domain,
        "schema_file_path": schema_path,
        "owner": {
            "name": owner,
            "email": "gauravbole2@gmail.com"
        },
        "schema_path": schema_path,
        "schedule": schedule,
        "refresh_method": refresh_method,
        "approved_by": "gauravbole2@gmail.com"
    }
    
    initial_message_content = f"""
    Intial user details :{json.dumps(contract_details, indent=2)}
    read yaml file and create data contract
    """
    initial_message = {"messages": [HumanMessage(content=initial_message_content)]}
    config = {"configurable": {"thread_id": {"thread_id": str(datetime.now())}}}
    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)
    result = graph.invoke(initial_message, config=config)
    while "__interrupt__" in result:
        print("\n Workflow paused for human input...\n")
        contract = result.get("contract", {})
        currnt_agent = result.get("current_agent", "Unknown Agent")

        contract = add_watermark(contract, currnt_agent)

        try:
            initial_text = json.dumps(contract, indent=2)
        except Exception:
            initial_text = str(contract)

        user_input_raw = get_user_input_via_editor(initial_text)

        try:
            user_input_dict = json.loads(user_input_raw)
        except json.JSONDecodeError as e:
            print("Failed to parse JSON:", e)
            raise

        cleaned_input = remove_watermark(user_input_dict)

        result = graph.invoke(Command(resume=json.dumps(cleaned_input)), config=config)


