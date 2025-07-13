# llm/core_nodes.py
from llm.agents.system import SystemAgent
from llm.agents.supervisor import Supervisor
from llm.agents.user_request_formating_agent import RequestFromating
from llm.tools.tool_node import ToolNode
from llm.tools.tool_registry import AGENT_TOOL_REGISTRY
from typing import Dict, Type
from llm.agents.data_engineer import DataEngineer
from llm.agents.data_steward import DataStewardAgent
from llm.agents.data_quality import DataQualityAgent
from llm.agents.data_governance import DataGovernanceAgent
from llm.agents.contract_generator import DataContractGeneratorAgent
from llm.agents.dbt_test_case_generator import DbtTestCaseGeneratorAgent
from llm.agents.human_review_mixin import human_editing



def get_syatem_tool_node():
    return ToolNode({tool.name: tool for tool in AGENT_TOOL_REGISTRY.get("system", [])})


CORE_NODE_REGISTRY = {
    "SystemAgent": lambda model: SystemAgent(model=model),
    "Supervisor": lambda model: Supervisor(model=model),
    "RequestFromating": lambda model: RequestFromating(model=model),
    "ToolNode": lambda model: get_syatem_tool_node(),
}



AGENT_CLASS_REGISTRY: Dict[str, Type] = {
    "data_engineer": DataEngineer,
    "data_steward_agent": DataStewardAgent,
    "data_quality_agent": DataQualityAgent,
    "data_governance_agent": DataGovernanceAgent,
    "data_contract_generator_agent": DataContractGeneratorAgent,
    'dbt_test_case_generator_agent': DbtTestCaseGeneratorAgent,

}

FUNCTION_NODE_REGISTRY = {
    "human_editing": human_editing
}