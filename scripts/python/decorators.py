"""装饰器集合"""

import contextlib
import warnings
import asyncio
from functools import wraps

  # Warning的提示过滤掉
class IgnoreWarnings:
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        with contextlib.suppress(IndexError, ValueError):
            with warnings.catch_warnings(record=True):
                for _category in [
                    Warning,
                    SyntaxWarning,
                    RuntimeWarning,
                    FutureWarning,
                    DeprecationWarning,
                    PendingDeprecationWarning,
                ]:
                    warnings.filterwarnings(action="ignore", category=_category)
                return self.function(*args, **kwargs)


def timeout_decorator(seconds):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(
                    asyncio.get_event_loop().run_in_executor(None, func, *args, **kwargs),
                    timeout=seconds
                )
            except asyncio.TimeoutError:
                raise Exception(f"Function timeout after {seconds} seconds")
        return wrapper
    return decorator
