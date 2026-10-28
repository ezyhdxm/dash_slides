"""A stand-in for a tick database (kdb+, TimescaleDB, QuestDB, ClickHouse, ...).

A background thread plays the market feed: it writes a tick every 50-300 ms into an in-memory SQLite table.
ticks_since(ts) is the query a real app would send to its own database.
"""
import random
import sqlite3
import threading
import time

_db = sqlite3.connect(":memory:", check_same_thread=False)
_db.execute("CREATE TABLE ticks (ts REAL, price REAL)")
_lock = threading.Lock()


def _feed():
    price = 100.0
    while True:
        price += random.gauss(0, 0.05)
        with _lock:
            _db.execute("INSERT INTO ticks VALUES (?, ?)", (time.time(), round(price, 3)))
        time.sleep(random.uniform(0.05, 0.3))


threading.Thread(target=_feed, daemon=True).start()


def ticks_since(ts):
    """Every tick newer than ts (seconds since 1970), oldest first: [(ts, price), ...]."""
    with _lock:
        return _db.execute("SELECT ts, price FROM ticks WHERE ts > ? ORDER BY ts", (ts,)).fetchall()
