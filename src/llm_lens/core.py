import time
import functools


def track(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"[{func.__name__}] took {elapsed:.2f}ms")
        return result
    return wrapper
