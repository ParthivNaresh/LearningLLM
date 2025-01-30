import logging

from utils import setup_app_logger


def main():
    app_logger = setup_app_logger(name="my_app_logger", level=logging.INFO)
    app_logger.info("Application started.")


if __name__ == "__main__":
    main()
