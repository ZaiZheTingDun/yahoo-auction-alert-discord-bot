import os
import logging


def log(logs: str) -> None:
    if os.getenv("SHOW_LOG", "true") == "true":
        logging.info(logs)


def error(logs: str) -> None:
    if os.getenv("SHOW_LOG", "true") == "true":
        logging.error(logs)
