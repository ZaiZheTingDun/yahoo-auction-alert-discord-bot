import os
from logging import info


def log(logs: str) -> None:
    if os.getenv("SHOW_LOG", "true") == "true":
        info(logs)
