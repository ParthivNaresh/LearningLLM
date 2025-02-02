import importlib
import logging
import os
from datetime import datetime

from utils.constants import PROVIDER_MAP


def setup_app_logger(name="my_app_logger", log_dir="logs", level=logging.INFO):
    """
    Sets up and returns a named logger with a single file and console handler.
    """
    logger = logging.getLogger(name)
    # If the logger is already configured, just return it
    if logger.handlers:
        return logger

    logger.setLevel(level)

    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"{name}_{timestamp}.log")

    formatter = logging.Formatter(
        "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(level)
    logger.addHandler(ch)

    fh = logging.FileHandler(log_file)
    fh.setFormatter(formatter)
    fh.setLevel(level)
    logger.addHandler(fh)

    logger.info(f"Logging to {log_file} (level={logging.getLevelName(level)})")

    return logger


def load_chat_provider(provider_key: str):
    cleaned_provider_key = provider_key.lower().strip()
    module_name, class_name = PROVIDER_MAP[cleaned_provider_key]
    mod = importlib.import_module(module_name)
    return getattr(mod, class_name)
