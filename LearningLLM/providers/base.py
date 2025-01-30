from abc import ABC, abstractmethod
from typing import List, Optional


class BaseProvider(ABC):
    """
    Abstract base class for LLM providers.
    Each provider must implement methods to list models and generate text.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key
        self.model_name = model_name

    @abstractmethod
    def list_models(self) -> List[str]:
        """
        Return a list of available model names for this provider.
        """
        pass

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text from a prompt using the current model.
        """
        pass

    def set_model(self, model_name: str) -> None:
        """
        Optionally switch to a different model supported by this provider.
        """
        self.model_name = model_name
