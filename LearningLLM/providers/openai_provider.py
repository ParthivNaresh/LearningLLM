import logging
from typing import List

import openai

from .base import BaseProvider

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseProvider):
    """
    Concrete implementation for OpenAI LLMs.
    """

    def __init__(self, api_key: str, model_name: str = "gpt-3.5-turbo"):
        super().__init__(api_key=api_key, model_name=model_name)
        openai.api_key = api_key

    def list_models(self) -> List[str]:
        """
        Example: Return a known subset, or fetch dynamically via openai.Model.list().
        """
        try:
            models_data = openai.Model.list()
            return [m.id for m in models_data["data"]]
        except Exception:
            return ["gpt-3.5-turbo"]  # Fallback

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Uses OpenAI's ChatCompletion for generation.
        """
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 150),
        )
        return response["choices"][0]["message"]["content"].strip()
