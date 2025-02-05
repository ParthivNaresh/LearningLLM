import logging
from typing import List, Optional

from openai import OpenAI
from .base import BaseProvider

logger = logging.getLogger(__name__)

try:
    import tiktoken
except ImportError:
    tiktoken = None


class OpenAIProvider(BaseProvider):
    """
    A more comprehensive OpenAI LLM provider that allows:
     - Listing and switching models (via set_model).
     - Advanced generation parameters (temperature, top_p, presence_penalty, frequency_penalty, etc.).
     - Counting tokens in a prompt (requires tiktoken).
    """

    def __init__(
        self,
        api_key: str,
        model_name: str = "gpt-3.5-turbo",
        organization: Optional[str] = None
    ):
        """
        :param api_key: Your OpenAI API key.
        :param model_name: Default model name (e.g. 'gpt-3.5-turbo').
        :param organization: Optional organization ID if you belong to multiple OpenAI orgs.
        """
        super().__init__(api_key=api_key, model_name=model_name)
        self.client = OpenAI(
            api_key=api_key,
        )
        if organization:
            self.client.organization = organization

        logger.info(f"Initialized OpenAIProvider with model='{model_name}'.")

    def list_models(self) -> List[str]:
        """
        Returns a list of available model IDs, based on openai.Model.list().
        """
        try:
            logger.info("Fetching list of OpenAI models...")
            response = self.client.models.list()
            model_names = [m.id for m in response.data]
            logger.info(f"Retrieved {len(model_names)} models from OpenAI.")
            return model_names
        except Exception as e:
            logger.error(f"Failed to list OpenAI models: {e}")
            return [self.model_name]  # fallback

    def set_model(self, model_name: str):
        """
        Switch to a different OpenAI model (e.g., 'gpt-4', 'text-davinci-003', etc.).
        """
        self.model_name = model_name
        logger.info(f"Switched OpenAI model to '{model_name}'.")

    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 150,
        top_p: float = 1.0,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        n: int = 1,
        system_prompt: Optional[str] = None,
    ) -> str:
        """
        Generates text using OpenAI's ChatCompletion endpoint (for GPT-3.5, GPT-4, etc.)

        :param prompt: The user prompt or query.
        :param temperature: Controls randomness (0.0 -> deterministic, higher -> more random).
        :param max_tokens: Maximum number of tokens in the generated completion.
        :param top_p: Nucleus sampling. 1.0 means no nucleus clipping.
        :param presence_penalty: Penalizes new tokens based on whether they appear in the text so far.
        :param frequency_penalty: Penalizes new tokens based on frequency in the text so far.
        :param n: Number of chat completion choices to generate.
        :param system_prompt: Optional system instruction to guide model behavior. If provided, it's sent as a separate system message.
        :return: The text of the first generated completion (or empty string on error).
        """
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            logger.info(
                f"Sending prompt to OpenAI model='{self.model_name}', "
                f"temperature={temperature}, top_p={top_p}, presence_penalty={presence_penalty}, "
                f"frequency_penalty={frequency_penalty}, max_tokens={max_tokens}, n={n}."
            )

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                n=n
            )

            choice = response["choices"][0]
            text = choice["message"]["content"].strip()
            logger.info(f"Received completion of length {len(text)} chars.")
            return text
        except Exception as e:
            logger.error(f"OpenAI generation error: {e}")
            return ""

    def count_tokens(self, text: str, model_name: Optional[str] = None) -> int:
        """
        Estimates the number of tokens in the given text, using tiktoken if installed.
        If no model_name is given, use self.model_name.

        :param text: The text to tokenize.
        :param model_name: Optionally override the model (e.g. "gpt-3.5-turbo").
        :return: Estimated token count, or 0 if tiktoken is unavailable or fails.
        """
        if not tiktoken:
            logger.warning("tiktoken is not installed. Cannot count tokens accurately.")
            return 0

        model = model_name or self.model_name
        logger.debug(f"Counting tokens for model='{model}'.")

        try:
            # e.g. using tiktoken.get_encoding("cl100k_base") for GPT-3.5
            encoding = None
            try:
                encoding = tiktoken.encoding_for_model(model)
            except KeyError:
                # fallback for unknown models
                logger.debug(f"No specific tiktoken encoding found for '{model}', using default.")
                encoding = tiktoken.get_encoding("cl100k_base")

            tokens = encoding.encode(text)
            return len(tokens)
        except Exception as e:
            logger.error(f"Token counting failed: {e}")
            return 0
