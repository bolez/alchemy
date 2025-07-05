
from langsmith import trace
from dotenv import load_dotenv
import os
from abc import ABC, abstractmethod
from typing import Optional, Type, Dict, Callable, Any, Union, List
from llm.config.llm import LLMModel
from pydantic import BaseModel
from jinja2 import Environment, FileSystemLoader, Template
from langchain_core.messages import AIMessage, BaseMessage
from llm.models.agent_state import AgentState
from llm.config.loader import load_config
import json
from langgraph.types import Command
config = load_config()
llm_config = config["llm"]
AGENT_LIST = config["agents"]

load_dotenv()



class BaseAgent(ABC):
    def __init__(
        self,
        model: LLMModel,
        prompt_file: Optional[str] = None,
        prompt_text: Optional[str] = None,
        agent_name: Optional[str] = "",
        structured_output_model: Optional[Type[BaseModel]] = None,
        tools: Optional[Dict[str, Callable]] = None,
    ):
        llm_builder = model if isinstance(
            model, LLMModel) else LLMModel(**llm_config)
        self.llm = llm_builder()
        self.agent_name = agent_name
        self.prompt_file = prompt_file
        self.prompt_text = prompt_text
        self.tools = tools or {}
        self.structured_output_model = structured_output_model
        self.jinja_env = Environment(
            loader=FileSystemLoader(
                searchpath=os.path.join(os.getcwd(), "llm/prompts")),
            autoescape=True,
        )

        self.jinja_env.globals["json"] = json

    def prepare_agent_state(self, state: AgentState) -> AgentState:
        """
        Prepares and returns a new AgentState with updated tracking info:
        - Sets current_agent
        - Initializes agent_status and progress for each agent in the workflow
        """
        print("---->", state)
        agent_status = dict(state.get("agent_status", {}))
        progress = dict(state.get("progress", {}))
        print(",,,,,")
        agents = AGENT_LIST
        print(agents)
        for agent in agents:
            agent_status.setdefault(
                agent, {"revised": False, "reviewed": False})
            progress.setdefault(agent, "pending")

        return {
            "current_agent": self.agent_name,
            "agent_status": agent_status,
            "progress": progress,
        }

    

    def call_llm(self, messages: Union[str, List[BaseMessage]], use_tools: bool = False) -> AIMessage:
        model = self.llm
        if use_tools and self.tools:
            model = model.bind_tools(list(self.tools.values()))

        try:
            if self.structured_output_model:
                structured_llm = model.with_structured_output(
                    self.structured_output_model
                )

                return structured_llm.invoke(messages)
            return model.invoke(messages)

        except Exception as e:
            raise RuntimeError(
                f"LLM error in agent `{self.agent_name}`: {str(e)}")

    def build_prompt(self, context: Dict[str, Any]) -> str:
        try:
            if self.prompt_text:
                template = Template(self.prompt_text)
                return template.render(**context)
            elif self.prompt_file:
                template = self.jinja_env.get_template(self.prompt_file)
                return template.render(**context)
            else:
                raise ValueError(
                    "Neither prompt_text nor prompt_file provided for agent.")
        except Exception as e:
            raise RuntimeError(
                f"[{self.agent_name}] Prompt rendering failed: {str(e)}")

    @abstractmethod
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the agent with the provided state.
        
        Args:
            state (Dict[str, Any]): The current state of the agent.
        
        Returns:
            Dict[str, Any]: The updated state after running the agent.
        """
        pass

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        agent = self.agent_name

        try:
            with trace(
                    name=f"{self.agent_name}_agent_run",
                    metadata={
                        "agent": self.agent_name,
                        "state_keys": list(state.keys())
                    }):
                result = self.run(state)
                if isinstance(result, Command):
                    return result

                # Post-processing
                result["progress"][agent] = "completed"
                result["agent_status"].setdefault(agent, {})
                result["agent_status"][agent].setdefault("revised", False)
                result["agent_status"][agent].setdefault("reviewed", False)

                return result

        except Exception as e:
            # state["messages"] = [
            #     AIMessage(content=f"{self.agent_name} failed: {str(e)}")
            # ]
            # state["errors"] = state.get("errors", [])
            # return state
            state["progress"][agent] = "failed"
            state["messages"] = [AIMessage(content=f"{agent} failed: {str(e)}")]
            state.setdefault("errors", []).append(str(e))
            return state

