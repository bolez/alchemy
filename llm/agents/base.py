
import os
from abc import ABC, abstractmethod
from typing import Optional, Type, Dict, Callable, Any
<<<<<<< HEAD
from llm.config.llm import LLMModel
=======
from config.llm import LLMModel
>>>>>>> cda17236d56e216f3d9a1106824aba1a3291ac6c
from pydantic import BaseModel
from jinja2 import Environment, FileSystemLoader, Template
from langchain_core.messages import AIMessage

<<<<<<< HEAD
from llm.config.loader import load_config
=======
from config.loader import load_config
>>>>>>> cda17236d56e216f3d9a1106824aba1a3291ac6c

config = load_config()
llm_config = config["llm"]


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
        llm_builder = model if isinstance(model, LLMModel) else LLMModel(**llm_config)
        self.llm = llm_builder()
        self.agent_name = agent_name
        self.prompt_file = prompt_file
        self.prompt_text = prompt_text
        self.tools = tools or {}
        self.structured_output_model = structured_output_model
        self.jinja_env = Environment(
            loader=FileSystemLoader(searchpath=os.path.join(os.getcwd(), "llm/prompts")),
            autoescape=True,
        )

    def call_llm(self, prompt: str):
        try:
            if self.structured_output_model:
                structured_llm = self.llm.with_structured_output(
                    self.structured_output_model
                )
                return structured_llm.invoke(prompt)
            return self.llm.invoke(prompt)

        except Exception as e:
            raise RuntimeError(f"LLM error in agent `{self.agent_name}`: {str(e)}")

    def build_prompt(self, context: Dict[str, Any]) -> str:
        try:
            if self.prompt_text:
                template = Template(self.prompt_text)
                return template.render(**context)
            elif self.prompt_file:
                template = self.jinja_env.get_template(self.prompt_file)
                return template.render(**context)
            else:
                raise ValueError("Neither prompt_text nor prompt_file provided for agent.")
        except Exception as e:
            raise RuntimeError(f"[{self.agent_name}] Prompt rendering failed: {str(e)}")

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
        try:
            return self.run(state)
        except Exception as e:
            state["messages"] = [
                AIMessage(content=f"{self.agent_name} failed: {str(e)}")
            ]
            state["errors"] = state.get("errors", [])
            return state





