from pydantic import BaseModel
from typing import Dict


class AgentContractUpdate(BaseModel):
    agent_name: str
    contract: Dict
    session_id: str
