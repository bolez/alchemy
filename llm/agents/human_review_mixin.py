from langgraph.types import interrupt
from typing import Dict, Any


class HumanReviewMixin:
    def human_review(self, state: Dict[str, Any]) -> Dict[str, Any]:
        agent = state.get("current_agent", "unknown")
        contract = state.get("contract", {})

        result = interrupt({
            "task": f"Please review the output from `{agent}`",
            "contract": contract,
        })

        if result == "yes":
            final_contract = contract
        else:
            final_contract = eval(result) if isinstance(result, str) else result

        state.setdefault("agent_status", {}).setdefault(agent, {})
        state["agent_status"][agent]["reviewed"] = True
        state["agent_status"][agent]["revised"] = result != "yes"

        state["contract"] = final_contract
        return state
