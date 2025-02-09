import logging
import time
from functools import wraps
from pathlib import Path

logger = logging.getLogger("CustomLogger")
logger.setLevel(logging.DEBUG)

info_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(message)s")

error_formatter = logging.Formatter("%(asctime)s - %(filename)s - ERROR: %(message)s")

info_handler = logging.FileHandler(Path(__file__).parent.parent / "logs/info.log")
info_handler.setFormatter(info_formatter)
info_handler.setLevel(logging.INFO)
info_handler.addFilter(lambda record: record.levelno == logging.INFO)

error_handler = logging.FileHandler(Path(__file__).parent.parent / "logs/error.log")
error_handler.setFormatter(error_formatter)
error_handler.setLevel(logging.ERROR)
error_handler.addFilter(lambda record: record.levelno == logging.ERROR)


logger.addHandler(info_handler)
logger.addHandler(error_handler)


def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            logger.info(
                f"Function: {func.__name__} Timetaken: {end_time-start_time:.4f} seconds",
                stacklevel=3,
            )

            return result
        except Exception:
            None

    return wrapper
