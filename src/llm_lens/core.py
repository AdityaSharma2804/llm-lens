import time
import functools

_records = []

def track(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            elapsed = (time.perf_counter() - start) * 1000
            _records.append({
                "func": func.__name__,
                "latency_ms": round(elapsed, 2),
                "status": "ok",
                "error": None
            })
            return result
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            _records.append({
                "func": func.__name__,
                "latency_ms": round(elapsed, 2),
                "status": "error",
                "error": str(e)
            })
            raise
    return wrapper       

def get_records():
    return list(_records)
