import time
import sqlite3
import functools
import json
from pathlib import Path

DB_PATH = Path.home() / ".llm_lens" / "calls.db"
CONFIG_PATH = Path.home() / ".llm_lens" / "config.json"

def _get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def _init_db():
    conn = _get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS calls (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            func          TEXT    NOT NULL,
            latency_ms    REAL    NOT NULL,
            status        TEXT    NOT NULL,
            error         TEXT,
            timestamp     TEXT    NOT NULL DEFAULT (datetime('now')),
            input_tokens  INTEGER,
            output_tokens INTEGER,
            cost_usd      REAL,
            model         TEXT
        )
    """)
    conn.commit()
    conn.close()

_init_db()

def _insert_record(func, latency_ms, status, error,
                   input_tokens=None, output_tokens=None,
                   cost_usd=None, model=None):
    conn = _get_connection()
    conn.execute(
        """INSERT INTO calls
           (func, latency_ms, status, error, input_tokens, output_tokens, cost_usd, model)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (func, latency_ms, status, error, input_tokens, output_tokens, cost_usd, model)
    )
    conn.commit()
    conn.close()

def track(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            elapsed = round((time.perf_counter() - start) * 1000, 2)
            _insert_record(func.__name__, elapsed, "ok", None)
            return result
        except Exception as e:
            elapsed = round((time.perf_counter() - start) * 1000, 2)
            _insert_record(func.__name__, elapsed, "error", str(e))
            raise
    return wrapper

def get_records():
    conn = _get_connection()
    rows = conn.execute("SELECT * FROM calls ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_stats():
    conn = _get_connection()
    row = conn.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) as errors,
            ROUND(AVG(latency_ms), 2) as avg_latency,
            ROUND(SUM(cost_usd), 6) as total_cost
        FROM calls
    """).fetchone()
    conn.close()
    return dict(row)

def get_config():
    if not CONFIG_PATH.exists():
        return {}
    with open(CONFIG_PATH) as f:
        return json.load(f)

def set_config(key, value):
    config = get_config()
    config[key] = value
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

def check_cost_alert():
    config = get_config()
    threshold = config.get("cost_alert_usd")
    if threshold is None:
        return None
    conn = _get_connection()
    row = conn.execute("SELECT SUM(cost_usd) as total FROM calls").fetchone()
    conn.close()
    total = row["total"] or 0.0
    if total >= threshold:
        return {"threshold": threshold, "total": round(total, 6)}
    return None
