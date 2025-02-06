import importlib
import logging
from typing import List, Tuple

from .constants import PROVIDER_MAP

logger = logging.getLogger(__name__)


def load_chat_provider(provider_key: str):
    cleaned_provider_key = provider_key.lower().strip()
    module_name, class_name = PROVIDER_MAP[cleaned_provider_key]
    try:
        mod = importlib.import_module(module_name)
        return getattr(mod, class_name)
    except ModuleNotFoundError as module_error:
        logger.error(module_error)
        return None


def fetch_models(provider: str, api_key: str) -> Tuple[str, dict]:
    """Fetch available models for a given provider."""
    try:
        if provider == "anthropic":
            url = "https://api.anthropic.com/v1/models"
            headers = {"x-api-key": api_key}
        elif provider == "openai":
            url = "https://api.openai.com/v1/models"
            headers = {"Authorization": f"Bearer {api_key}"}
        elif provider == "groq":
            url = "https://api.groq.com/openai/v1/models"
            headers = {"Authorization": f"Bearer {api_key}"}
        elif provider == "cohere":
            url = "https://api.cohere.com/v1/models"
            headers = {"Authorization": f"Bearer {api_key}"}
        elif provider == "fireworks":
            url = "https://api.fireworks.ai/inference/v1/models"
            headers = {"Authorization": f"Bearer {api_key}"}
        elif provider == "together":
            url = "https://api.together.ai/v1/models"
            headers = {"Authorization": f"Bearer {api_key}"}
        elif provider == "nvidia":
            url = "https://api.nvidia.com/v1/models"
            headers = {"Authorization": f"Bearer {api_key}"}
        elif provider == "mistral":
            url = "https://api.mistral.ai/v1/models"
            headers = {"Authorization": f"Bearer {api_key}"}
        elif provider == "aws":
            url = "https://bedrock-runtime.us-east-1.amazonaws.com/models"
            headers = {"Authorization": f"Bearer {api_key}"}
        elif provider == "azure":
            return ["Azure OpenAI models depend on configured deployments"]
        elif provider == "google":
            url = "https://generativelanguage.googleapis.com/v1beta/models"
            headers = {"Authorization": f"Bearer {api_key}"}
        elif provider == "huggingface":
            url = "https://huggingface.co/api/models"
            headers = {"Authorization": f"Bearer {api_key}"}
        elif provider == "vertex":
            return ["Use Google VertexAI Console to list models"]
        elif provider == "ollama":
            url = "http://localhost:11434/api/tags"
            headers = {}
        elif provider == "databricks":
            url = "https://YOUR-DATABRICKS-WORKSPACE/api/2.0/serving-endpoints"
            headers = {"Authorization": f"Bearer {api_key}"}
        elif provider == "upstage":
            url = "https://api.upstage.ai/v1/models"
            headers = {"Authorization": f"Bearer {api_key}"}
        elif provider == "ibm":
            url = "https://watsonx.ai/api/v1/models"
            headers = {"Authorization": f"Bearer {api_key}"}
        elif provider == "xai":
            url = "https://api.x.ai/v1/models"
            headers = {"Authorization": f"Bearer {api_key}"}
        else:
            return [f"Provider {provider} not supported"]
        return url, headers
    except Exception as e:
        return [f"Error: {str(e)}"]