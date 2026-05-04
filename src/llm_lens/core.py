import time
import functools
from contextlib import contextmanager


def add(a, b):
    """Original test function — will remove later."""
    return a + b


@contextmanager
def track_latency(label: str):
    """Context manager that measures and prints elapsed time."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"[{label}] took {elapsed * 1000:.2f}ms")


def track(func):
    """Decorator that wraps any function and logs its latency."""
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
