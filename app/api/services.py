import json
import asyncio
from datetime import datetime
from typing import Dict, AsyncGenerator
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver


from llm.utils.user_input import add_watermark, remove_watermark
from llm.graph.graph_builder import graph_builder

active_sessions: Dict[str, Dict] = {}


async def generate_contract_stream(domain, schedule, schema_path, session_id) -> AsyncGenerator[bytes, None]:
    contract_details = {
        "domain": domain,
        "schema_file_path": schema_path,
        "owner": {"name": "Gaurav Bole", "email": "gauravbole2@gmail.com"},
        "schema_path": schema_path,
        "schedule": schedule,
        "refresh_method": "incremental",
        "approved_by": "gauravbole2@gmail.com"
    }

    initial_message = {"messages": [HumanMessage(content=f"Initial user details: {json.dumps(contract_details)}")]}
    config = {"configurable": {"thread_id": {"thread_id": session_id}}}

    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)

    state = graph.invoke(initial_message, config=config)
    active_sessions[session_id] = {"graph": graph, "state": state, "config": config}

    while True:

        if "__interrupt__" in state:
            current_agent = state.get("current_agent", "Unknown")
            contract = state.get("contract", {})
            contract = add_watermark(contract, current_agent)

            yield json.dumps({
                "type": "agent",
                "agent_name": current_agent,
                "contract": contract,
                "session_id": session_id
            }).encode() + b"\n"
            break
        else:
            final_contract = state.get("contract", {})
            yield json.dumps({
                "type": "final",
                "final_contract": final_contract
            }).encode() + b"\n"
            break


async def resume_graph(session_id: str, updated_contract: dict):
    session = active_sessions.get(session_id)
    if not session:
        return JSONResponse(status_code=400, content={"error": "Invalid session"})

    graph = session["graph"]
    config = session["config"]
    cleaned_input = remove_watermark(updated_contract)
    new_state = graph.invoke(Command(resume=json.dumps(cleaned_input)), config=config)
    session["state"] = new_state

    if "__interrupt__" in new_state:
        agent = new_state.get("current_agent", "Unknown")
        contract = add_watermark(new_state.get("contract", {}), agent)

        return JSONResponse(content={
            "type": "agent",
            "agent_name": agent,
            "contract": contract,
            "session_id": session_id
        })
    else:
        final_contract = new_state.get("contract", {})
        return JSONResponse(content={
            "type": "final",
            "final_contract": final_contract
        })
