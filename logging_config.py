import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    logger = logging.getLogger("my_framework")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)

    file_handler = RotatingFileHandler("framework.log", maxBytes=1000000, backupCount=3)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logging()
