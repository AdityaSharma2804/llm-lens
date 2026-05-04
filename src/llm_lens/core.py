import time
import functools
from dataclasses import dataclass, field
from contextlib import contextmanager
from datetime import datetime, timezone


@dataclass
class CallRecord:
    func_name: str
    latency_ms: float
    status: str          # "ok" or "error"
    error: str | None
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


# In-memory store — abhi ke liye simple list
_records: list[CallRecord] = []


def track(func):
    """Decorator: wraps any function, logs latency and status."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            elapsed = (time.perf_counter() - start) * 1000
            record = CallRecord(
                func_name=func.__name__,
                latency_ms=round(elapsed, 2),
                status="ok",
                error=None,
            )
            _records.append(record)
            return result
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            record = CallRecord(
                func_name=func.__name__,
                latency_ms=round(elapsed, 2),
                status="error",
                error=str(e),
            )
            _records.append(record)
            raise
    return wrapper


def get_records() -> list[CallRecord]:
    """Returns all tracked call records."""
    return list(_records)


@contextmanager
def track_latency(label: str):
    """Context manager for manually timing a block."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = (time.perf_counter() - start) * 1000
        print(f"[{label}] {elapsed:.2f}ms")
        