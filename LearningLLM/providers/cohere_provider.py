from typing import List

import cohere

from .base import BaseProvider


class CohereProvider(BaseProvider):
    """
    Concrete implementation for Cohere LLMs.
    """

    def __init__(self, api_key: str, model_name: str = "command-nightly"):
        super().__init__(api_key="", model_name=model_name)
        self.client = cohere.Client(api_key)

    def list_models(self) -> List[str]:
        """
        Example subset or dynamically fetch from Cohere's model listings if available.
        """
        return self.client.models.list()

    def generate(self, prompt: str, **kwargs) -> str:
        response = self.client.generate(
            model=self.model_name,
            prompt=prompt,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 150),
        )
        return response.generations[0].text.strip()
