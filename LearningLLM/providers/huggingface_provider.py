import logging
from typing import List, Optional

import torch
from huggingface_hub import list_models, login
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)

from .base import BaseProvider

logger = logging.getLogger("my_app_logger")


class HuggingFaceProvider(BaseProvider):
    """
    Minimal Hugging Face provider for listing, selecting, and generating with different models.
    Uses raw model/tokenizer calls (no pipeline).
    """

    def __init__(
        self,
        hf_token: Optional[str] = "",
        device: Optional[str] = None,
    ):
        """
        :param hf_token: Optional token for private models on Hugging Face Hub.
        :param device: Device identifier (e.g., "cpu", "cuda", "cuda:0"). If None, defaults to "cuda" if available.
        """
        super().__init__(model_name=None)
        self.hf_token = hf_token
        self.model = None
        self.tokenizer = None

        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        if self.hf_token:
            try:
                login(token=self.hf_token)
                logger.info("Logged in to Hugging Face Hub with provided token.")
            except Exception as e:
                logger.error(f"Could not log in with provided token: {e}")

    def list_models(self) -> List[str]:
        """
        Returns a list of popular or relevant models on Hugging Face Hub.
        By default, it just returns some top results. You can refine via filters if desired.
        """
        try:
            logger.info("Retrieving list of public Hugging Face models...")
            models = list_models(limit=10, token=self.hf_token)
            model_ids = [model.modelId for model in models]
            logger.info(f"{len(model_ids)} models returned.")
            return model_ids
        except Exception as e:
            logger.error(f"Could not retrieve models from Hugging Face Hub: {e}")
            return []

    def set_model(self, model_name: str):
        """
        Loads the specified model and tokenizer from the Hugging Face Hub.
        Moves them to the requested device (CPU/GPU).
        """
        try:
            logger.info(f"Loading model '{model_name}' on device '{self.device}'...")
            self.model_name = model_name
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name, use_auth_token=self.hf_token
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name, use_auth_token=self.hf_token
            )
            self.model.to(self.device)
            logger.info(f"Successfully loaded {model_name}.")
        except Exception as e:
            logger.error(f"Failed to load model '{model_name}': {e}")
            self.model = None
            self.tokenizer = None

    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 50,
        temperature: float = 0.7,
        do_sample: bool = True,
    ) -> str:
        """
        Generates text from a given prompt. Minimal arguments for simplicity.

        :param prompt: The user prompt or query.
        :param max_new_tokens: Max tokens to generate (beyond the prompt length).
        :param temperature: Controls randomness in generation (higher -> more random).
        :param do_sample: If True, uses sampling. Otherwise, uses greedy decoding.
        :return: Generated string (may include prompt + completion).
        """
        if not self.model:
            logger.error("No model is set. Call set_model(model_name) first.")
            return ""

        if not self.tokenizer:
            logger.error("No tokenizer is set. Call set_model(model_name) first.")
            return ""

        try:
            input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(
                self.device
            )
            output_ids = self.model.generate(
                input_ids,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=do_sample,
            )
            generated_text = self.tokenizer.decode(
                output_ids[0], skip_special_tokens=True
            )
            logger.info(f"Generated response from {self.model_name}.")
            return generated_text
        except Exception as e:
            logger.error(f"Error during text generation: {e}")
            return ""
