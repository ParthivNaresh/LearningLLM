import logging
from typing import List, Optional

import torch
from huggingface_hub import list_models, login
from openai import api_key
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)

from .base import BaseProvider

logger = logging.getLogger(__name__)


class HuggingFaceProvider(BaseProvider):
    """
    Minimal Hugging Face provider for listing, selecting, and generating with different models.
    Uses raw model/tokenizer calls (no pipeline).
    """

    def __init__(
        self,
        device: Optional[str] = None,
        local_files_only: bool = False,
        cache_dir: Optional[str] = None,
    ):
        """
        :param device: Device identifier (e.g., "cpu", "cuda", "cuda:0"). If None, defaults to "cuda" if available.
        :param local_files_only: If True, use local cached files and do not fetch from Hugging Face Hub.
        :param cache_dir: Custom cache directory where models are stored locally.
        """
        super().__init__(api_key=api_key, model_name=None)
        self.tokenizer = None
        self.local_files_only = local_files_only
        self.cache_dir = cache_dir

        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        if self.api_key and not self.local_files_only:
            try:
                login(token=self.api_key)
                logger.info("Logged in to Hugging Face Hub with provided token.")
            except Exception as e:
                logger.error(f"Could not log in with provided token: {e}")

    def list_models(
        self, search_query: Optional[str] = None, limit: int = 10
    ) -> List[str]:
        """
        Returns a list of popular or relevant models on Hugging Face Hub.
        By default, it just returns some top results. You can refine via filters if desired.

        :param search_query: Optional keyword to filter models (e.g. "gpt2", "bert").
        :param limit: Max number of model IDs to return.
        :return: A list of model IDs.
        """
        try:
            logger.info("Retrieving list of public Hugging Face models...")
            models_info = list_models(
                search=search_query, limit=10, token=self.api_key
            )
            model_ids = [m.modelId for m in models_info]
            logger.info(f"{len(model_ids)} models returned.")
            return model_ids
        except Exception as e:
            logger.error(f"Could not retrieve models from Hugging Face Hub: {e}")
            return []

    def set_model(self, model_name: str):
        """
        Loads the specified model and tokenizer from the Hugging Face Hub.
        Moves them to the requested device (CPU/GPU).

        :param model_name: The model identifier on the Hub (e.g. "gpt2") or a local path to model files.
        """
        try:
            logger.info(
                f"Loading model '{model_name}' on device '{self.device}', "
                f"local_files_only={self.local_files_only}, cache_dir={self.cache_dir}"
            )
            self.model_name = model_name
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                use_auth_token=self.api_key,
                local_files_only=self.local_files_only,
                cache_dir=self.cache_dir,
            )
            logger.info(f"Loaded tokenizer {self.tokenizer}")
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=True,
                use_auth_token=self.api_key,
                local_files_only=self.local_files_only,
                cache_dir=self.cache_dir,
            )
            self.model.to(self.device)
            logger.info(f"Successfully loaded {model_name} on {self.device}.")
        except Exception as e:
            logger.error(f"Failed to load model '{model_name}': {e}")
            self.model = None
            self.tokenizer = None

    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 256,
        temperature: float = 0.7,
        do_sample: bool = True,
        top_k: Optional[int] = None,
        top_p: Optional[float] = 0.95,
        repetition_penalty: Optional[float] = 1.5,
        num_return_sequences: int = 1,
    ) -> str:
        """
        Generates text from a given prompt. Minimal arguments for simplicity.

        :param prompt: The user prompt or query.
        :param max_new_tokens: Max tokens to generate (beyond the prompt length).
        :param temperature: Controls randomness in generation (higher -> more random).
        :param do_sample: If True, uses sampling. Otherwise, uses greedy decoding.
        :param top_k: Top-k filtering for sampling (higher -> more diverse).
        :param top_p: Nucleus sampling hyperparameter (fraction of tokens to consider).
        :param repetition_penalty: Penalty for repeated tokens (1.0 means no penalty).
        :param num_return_sequences: Number of distinct generated sequences to return.
        :return: Generated string.
        """
        if not self.model or not self.tokenizer:
            logger.error("No model/tokenizer is set. Call set_model(model_name) first.")
            return ""

        try:
            input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(
                self.device
            )
            prompt_tokens = input_ids.shape[1]
            logger.info(
                f"Generating text for prompt of length {prompt_tokens} tokens with model {self.model_name}."
            )

            output_ids = self.model.generate(
                input_ids,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=do_sample,
                top_k=top_k,
                top_p=top_p,
                repetition_penalty=repetition_penalty,
                num_return_sequences=num_return_sequences,
            )

            generated_texts = []
            for seq_num, seq_ids in enumerate(output_ids, start=1):
                new_tokens = seq_ids[prompt_tokens:]
                gen_text = self.tokenizer.decode(new_tokens, skip_special_tokens=True)
                generated_texts.append(gen_text)
                logger.debug(f"Sequence {seq_num}/{num_return_sequences} generated.")

            logger.info(
                f"Generated {num_return_sequences} sequence(s) from {self.model_name}."
            )
            return " ".join(generated_texts)
        except Exception as e:
            logger.error(f"Error during text generation: {e}")
            return ""

    def count_tokens(self, text: str) -> int:
        """
        Returns the approximate number of tokens in the provided text
        (requires a loaded tokenizer).

        :param text: Any string to tokenize.
        :return: Number of tokens.
        """
        if not self.tokenizer:
            logger.warning("No tokenizer available. Call set_model(model_name) first.")
            return 0
        tokens = self.tokenizer(text, return_tensors="pt").input_ids[0]
        return len(tokens)
