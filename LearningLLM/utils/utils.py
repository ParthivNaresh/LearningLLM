import importlib
import logging

from utils.constants import PROVIDER_MAP

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
