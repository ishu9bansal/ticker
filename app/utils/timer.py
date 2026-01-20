
import functools
import time

from fastapi.logger import logger

THRESHOLD_WARNING = 2  # 2 seconds
THRESHOLD_ERROR = 4  # 4 seconds
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()  # better for timing

        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            msg = f"[TIMER] {func.__qualname__} took {elapsed:.6f}s"
            if elapsed > THRESHOLD_ERROR:
                logger.error(msg)
            elif elapsed > THRESHOLD_WARNING:
                logger.warning(msg)

    return wrapper
