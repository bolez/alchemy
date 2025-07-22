from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse, JSONResponse
from app.api.schemas import AgentContractUpdate
from app.api.services import generate_contract_stream, resume_graph

router = APIRouter()
from datetime import datetime

def create_session_id() -> str:
    return datetime.utcnow().isoformat()


@router.post("/generate")
async def generate_contract(
    domain: str = Form(...),
    schedule: str = Form(...),
    yaml_file: UploadFile = File(...)
):
    session_id = create_session_id()
    content = await yaml_file.read()
    schema_path = f"/tmp/{session_id}.yml"
    with open(schema_path, "wb") as f:
        f.write(content)
    return StreamingResponse(generate_contract_stream(domain, schedule, schema_path, session_id),
                             media_type="application/json")


@router.post("/update-agent-contract")
async def update_agent_contract(update: AgentContractUpdate):
    return await resume_graph(update.session_id, update.contract)
