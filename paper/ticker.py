"""The markets desk: repository activity, quoted like stock.

The price is commits in the last fortnight. The change is that against the
fortnight before. A repo you ignored for two weeks prints a red triangle, which
is the entire point — a quote you cannot lose on is not a quote.

Network at build time is a liability: no wifi, a rate limit, or GitHub having a
bad morning must not break the paper. So every fetch is cached to disk, the
cache is used when it is fresh, and a failed fetch falls back to whatever the
cache last held. If there is nothing at all, the strip simply does not print.
"""

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import date, timedelta

from .config import ROOT, SITE

CACHE = ROOT / ".cache" / "ticker.json"
CACHE_TTL_HOURS = 6
PERIOD = 14                      # one issue. the fortnight is the trading session.
API = "https://api.github.com"


@dataclass
class Quote:
    symbol: str
    repo: str
    last: int                    # commits this session
    chg: int                     # against the session before

    @property
    def arrow(self) -> str:
        return "\u25b2" if self.chg > 0 else "\u25bc" if self.chg < 0 else "\u25ac"

    @property
    def direction(self) -> str:
        return "up" if self.chg > 0 else "down" if self.chg < 0 else "flat"


def _get(url: str):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "basement-gazette",
    })
    # Optional: 60 requests/hour anonymous, 5000 with a token. Two per repo.
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)


def _commits(repo: str, since: date, until: date) -> int:
    url = (f"{API}/repos/{repo}/commits"
           f"?since={since.isoformat()}T00:00:00Z"
           f"&until={until.isoformat()}T00:00:00Z&per_page=100")
    return len(_get(url))


def _fetch(today: date) -> list[dict]:
    quotes = []
    for entry in SITE["repos"]:
        last = _commits(entry["repo"], today - timedelta(days=PERIOD), today)
        prev = _commits(entry["repo"],
                        today - timedelta(days=PERIOD * 2),
                        today - timedelta(days=PERIOD))
        quotes.append({
            "symbol": entry["symbol"], "repo": entry["repo"],
            "last": last, "chg": last - prev,
        })
    return quotes


def _cache_age_hours() -> float:
    if not CACHE.exists():
        return float("inf")
    fetched = json.loads(CACHE.read_text()).get("fetched", 0)
    return (date.today().toordinal() * 24) - fetched


def load_ticker(today: date | None = None) -> list[Quote]:
    """Quotes for the front page. Never raises — a dead API prints no strip."""
    today = today or date.today()
    if not SITE.get("repos"):
        return []

    cached = json.loads(CACHE.read_text()) if CACHE.exists() else None
    if cached and _cache_age_hours() < CACHE_TTL_HOURS:
        return [Quote(**q) for q in cached["quotes"]]

    try:
        quotes = _fetch(today)
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(
            {"fetched": date.today().toordinal() * 24, "quotes": quotes}, indent=2))
        return [Quote(**q) for q in quotes]
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
        if cached:
            print(f"  markets: {e} — printing the cached session")
            return [Quote(**q) for q in cached["quotes"]]
        print(f"  markets: {e} — no quotes, the strip will not print")
        return []