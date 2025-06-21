from dotenv import load_dotenv
import os
from typing import Optional

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


class LLMModel():
    def __init__(self, model: str,
                 temperature: float = 0,
                 max_tokens: Optional[int] = None,
                 max_retries: int = 5):
        """_summary_

        Args:
            model (str): _description_
            temperature (float, optional): _description_. Defaults to 0.
            max_tokens (int, optional): _description_. Defaults to None.
            max_retries (int, optional): _description_. Defaults to 5.
        """

        self.model = model
        self.temperature = float(temperature)
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self.api_key = os.getenv("GOOGLE_API_KEY")

    def __call__(self):
        return ChatGoogleGenerativeAI(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            max_retries=self.max_retries,
            google_api_key=self.api_key
        )
