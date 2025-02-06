import logging
from typing import List, Optional

from google.cloud import aiplatform
from google.oauth2 import service_account
from .base import BaseProvider

logger = logging.getLogger(__name__)


def _load_model(model_name: str):
    """
    Internal method to load a PaLM text model from Vertex AI by name.
    """
    try:
        # Vertex AI has specialized classes for PaLM text & chat; we'll assume text model here.
        text_model = aiplatform.TextGenerationModel.from_pretrained(model_name)
        return text_model
    except Exception as e:
        logger.error(f"Failed to load Vertex AI model '{model_name}': {e}")
        return None


class GoogleProvider(BaseProvider):
    """
    A Vertex AI provider for Google PaLM text models.
    It supports:
      - Initializing Vertex AI with your project/location/credentials
      - Listing available text models (subset)
      - Generating text with a known model (e.g. 'text-bison@001')
    You'll need to install the CLI: https://cloud.google.com/sdk/docs/install-sdk
    """

    def __init__(
        self,
        project_id: str,
        location: str = "us-central1",
        model_name: str = "text-bison@001",
        temperature: float = 0.7,
        max_output_tokens: int = 256,
        top_p: float = 0.95,
        top_k: int = 40,
    ):
        """
        :param project_id: GCP project to use for Vertex AI.
        :param location: GCP region (e.g. 'us-central1').
        :param model_name: The Vertex AI PaLM model ID (e.g., "text-bison@001").
        :param api_key: Optional path to service account key file or other credential object.
        :param temperature: Default temperature for generation (can be overridden in generate()).
        :param max_output_tokens: Default max tokens for generation (override in generate()).
        :param top_p: Default nucleus sampling hyperparam (0.0-1.0).
        :param top_k: Default top-k sampling.
        """
        self.project_id = project_id
        self.location = location


        # Defaults for generation
        self.default_temperature = temperature
        self.default_max_output_tokens = max_output_tokens
        self.default_top_p = top_p
        self.default_top_k = top_k

        # Initialize Vertex AI
        logger.info("Initializing Vertex AI...")
        aiplatform.init(
            project=self.project_id,
            location=self.location,
        )
        logger.info(f"Initialized Vertex AI in project='{project_id}', location='{location}'.")

    def list_models(self, search_filter: Optional[str] = None) -> List[str]:
        """
        Example method: returns a small set of matching models from Vertex AI.
        NOTE: Listing all models in Vertex is possible, but to filter for PaLM:
          aiplatform.Model.list(filter="supported_prediction_types=vertex_ai.generation")
        This is approximate. Adjust the filter if needed.
        """
        try:
            logger.info("Listing Vertex AI models (filtering for text generation).")
            if search_filter is None:
                # Filter for generative text models in Vertex AI
                search_filter = "labels.aiplatform.googleapis.com/model_type=generative,text"
            models = aiplatform.Model.list(
                filter=search_filter,
                order_by="create_time desc",
            )
            model_names = [m.name for m in models]  # 'm.name' is the resource name, e.g. "projects/xxx/locations/xxx/models/xxxx"
            logger.info(f"Found {len(model_names)} model(s) in Vertex AI with filter='{search_filter}'.")
            return model_names
        except Exception as e:
            logger.error(f"Could not list models from Vertex AI: {e}")
            return []

    def set_model(self, model_name: str):
        """
        Switch to a different PaLM model in Vertex AI.
        """
        logger.info(f"Switching to model '{model_name}'...")
        self.model_name = model_name
        self.model = _load_model(model_name)
        if self.model:
            logger.info(f"Model switched to '{model_name}'.")
        else:
            logger.error(f"Failed to switch to model '{model_name}'.")

    def generate(
            self,
            prompt: str,
            temperature: Optional[float] = None,
            max_output_tokens: Optional[int] = None,
            top_p: Optional[float] = None,
            top_k: Optional[int] = None,
    ) -> str:
        """
        Generates text with the currently loaded Vertex AI PaLM model.

        :param prompt: The user prompt or context.
        :param temperature: Controls randomness (default from constructor if None).
        :param max_output_tokens: Maximum tokens to generate beyond the prompt (default if None).
        :param top_p: Nucleus sampling hyperparam.
        :param top_k: Top-k sampling limit.
        :return: Generated text string or empty if error/none.
        """
        if not self.model:
            logger.error("No model is set. Call set_model(model_name) first.")
            return ""

        # Use defaults from constructor if param is None
        temperature = temperature if temperature is not None else self.default_temperature
        max_output_tokens = max_output_tokens if max_output_tokens is not None else self.default_max_output_tokens
        top_p = top_p if top_p is not None else self.default_top_p
        top_k = top_k if top_k is not None else self.default_top_k

        try:
            logger.info(
                f"Generating text with model='{self.model_name}', "
                f"temperature={temperature}, max_output_tokens={max_output_tokens}, top_p={top_p}, top_k={top_k}."
            )
            response = self.model.predict(
                prompt=prompt,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                top_p=top_p,
                top_k=top_k,
            )
            if hasattr(response, "text"):
                # The new SDK returns a PredictResponse with .text
                generated_text = response.text
            else:
                # or sometimes returns a raw string in older versions
                generated_text = str(response)

            logger.info(f"Vertex AI generated text of length {len(generated_text)}.")
            return generated_text
        except Exception as e:
            logger.error(f"Error during Vertex AI text generation: {e}")
            return ""
