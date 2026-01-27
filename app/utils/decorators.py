
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
        self._cache: dict[str, Any] = {}

    def get(self, key: str) -> Any:
        return self._cache.get(key)

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = value
        
    def has(self, key: str) -> bool:
        return key in self._cache

    @classmethod
    def singleton(cls) -> Self:
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

CACHE_CONTAINERS: dict[str, KeyValCache] = {}
def cache_container(name: str) -> KeyValCache:
    if name not in CACHE_CONTAINERS:
        CACHE_CONTAINERS[name] = KeyValCache()
    return CACHE_CONTAINERS[name]

def cached(cache_key: str):
    """Simple caching decorator for instance methods with a single str argument."""
    cache = cache_container(cache_key)
    def cached_inner(func: Callable[[Any, str], Any]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if cache.has(args[1]):
                print(f"[CACHE] Hit for key {args[1]} in cache {cache_key}" )
                return cache.get(args[1])
            print(f"[CACHE] Miss for key {args[1]} in cache {cache_key}" )
            result = func(*args, **kwargs)
            if result is not None:
                cache.set(args[1], result)
            return result
        return wrapper
    return cached_inner
