"""Central path and connection settings.

Every script in this repo used to hardcode an absolute path from whichever
machine happened to run it, so nothing worked on a second machine. Paths and
credentials now come from the environment, with local defaults.

    export RAG_DATA_DIR=/path/to/data     # defaults to ./data
    export PG_HOST=... PG_DB=... PG_USER=... PG_PASSWORD=...
"""
import os
from pathlib import Path

DATA_DIR = Path(os.getenv("RAG_DATA_DIR", Path(__file__).parent / "data")).expanduser()
NEWS_DIR = DATA_DIR / "news"
STOCKS_DIR = DATA_DIR / "stocks"

for _d in (DATA_DIR, NEWS_DIR, STOCKS_DIR):
    _d.mkdir(parents=True, exist_ok=True)


def news(name: str) -> str:
    """Absolute path to a file in the news data directory."""
    return str(NEWS_DIR / name)


def stocks(name: str) -> str:
    """Absolute path to a file in the stock data directory."""
    return str(STOCKS_DIR / name)


PG = {
    "host": os.getenv("PG_HOST", "localhost"),
    "port": os.getenv("PG_PORT", "5432"),
    "dbname": os.getenv("PG_DB", "rag"),
    "user": os.getenv("PG_USER", "postgres"),
    "password": os.getenv("PG_PASSWORD", ""),
}
