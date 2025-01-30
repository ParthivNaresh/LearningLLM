import logging
import os
from datetime import datetime

import pytest


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    """
    A session-level fixture that sets up logging for all tests.
    It runs once before any tests start.
    """
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Time-stamped log file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = os.path.join(log_dir, f"test_session_{timestamp}.log")

    # Set up root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logging.info(f"Pytest logging configured. Writing logs to: {log_file_path}")

    yield

    logging.info("End of Pytest session. Shutting down logging.")
