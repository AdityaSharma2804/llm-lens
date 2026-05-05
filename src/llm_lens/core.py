import time
import functools


def track(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            elapsed = (time.perf_counter() - start) * 1000
            print(f"[{func.__name__}] OK — {elapsed:.2f}ms")
            return result
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            print(f"[{func.__name__}] ERROR — {elapsed:.2f}ms — {e}")
            raise
    return wrapper
