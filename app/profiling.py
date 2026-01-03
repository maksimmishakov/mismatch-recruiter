import time
import functools
from typing import Any, Callable

def profile_endpoint(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        print(f"[PROFILE] {func.__name__} took {elapsed:.3f}s")
        return result
    return wrapper
