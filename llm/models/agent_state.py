
from typing import Dict, List, Optional, Sequence
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
import operator


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    contract: dict = {}
    schema_file_path: str = ""
    initial_user_details: dict = {}
    source_schemas: dict = {}
    current_agent: str = ""
    progress: Dict[str, bool] = {}
    agent_status: Dict[str, Dict[str, bool]] = {}
    errors: Optional[List[str]] = []
    finished: bool = False
    contract_document: Dict[str, str] = {}