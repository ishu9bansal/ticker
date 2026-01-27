
import functools
import time
from typing import Any, Callable, Self

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


class KeyValCache:
    def __init__(self):
        self._cache: dict[str, str] = {}

    def get(self, key: str) -> str | None:
        return self._cache.get(key)

    def set(self, key: str, value: str) -> None:
        self._cache[key] = value
        
    def has(self, key: str) -> bool:
        return key in self._cache

    @classmethod
    def singleton(cls) -> Self:
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance


def cached(cache: KeyValCache = KeyValCache.singleton()):
    """Simple caching decorator for instance methods with a single str argument."""
    
    def cached_inner(func: Callable[[Any, str], str | None]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if cache.has(args[1]):
                return cache.get(args[1])
            result = func(*args, **kwargs)
            if result is not None:
                cache.set(args[1], result)
            return result
        return wrapper
    return cached_inner
