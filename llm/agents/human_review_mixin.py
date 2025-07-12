from langgraph.types import interrupt
from typing import Dict, Any
from langchain_core.messages import AIMessage

from langgraph.types import interrupt
from llm.models.agent_state import AgentState

import json

def human_editing(state: AgentState):
    """
    This function is a placeholder for human editing of the generated object.
    """
    contract = state.get("contract", {})
    currnt_agent = state.get("current_agent", "")
    # formatted_contract = json.dumps(contract, indent=2)

    print("\n" + "#" * 30 + " CONTRACT PREVIEW " + currnt_agent + "#" * 30)
    print(contract)
    print("#" * 76 + "\n")

 
    contract = state.get("contract", {})
    print("#" * 20, "Human Editing", "#" * 20)
    result = interrupt(
        {
            "task": f"""Please review the generated response from currnt_agent: `{currnt_agent}` and make any necessary changes.
            """,
            "Contract":  f"{contract}",
        }

    )
    print("#" * 20, "Human Editing", "#" * 20)

    progress_dict = {"progress": state.get("progress", {})}
    

    if result == 'yes':
        print("Human editing result: UserRequest object approved without changes.")
        state["agent_status"][currnt_agent]["revised"] = True
        state["agent_status"][currnt_agent]["reviewed"] = True
        final_response = state.get("contract", {})
        state["messages"] = [AIMessage(content=f"{currnt_agent} executed successfully and agent `{progress_dict}`, and contarcat genarated till now is {final_response}")]

    else:
     
        final_response = json.loads(result)
        state["agent_status"][currnt_agent]["revised"] = True
        state["agent_status"][currnt_agent]["reviewed"] = True
        state_data = {key: value for key, value in state.items() if key != "messages"}
        state["messages"] = [AIMessage(content=f"{currnt_agent} executed successfully and agent `{progress_dict}`, and contarcat genarated till now is {final_response}")]
        print(f"State after human editing: {final_response}")
    return {**state, **{"contract": final_response}}

