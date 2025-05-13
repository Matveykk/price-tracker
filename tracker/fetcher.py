import random
import time

import requests

from tracker.config import settings

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36",
]


class FetchError(Exception):
    pass


def fetch_html(url: str) -> str:
    last_error = None
    for attempt in range(settings.max_retries):
        try:
            response = requests.get(
                url,
                headers=_build_headers(),
                timeout=settings.request_timeout,
            )
            if response.status_code in (403, 429):
                raise FetchError(f"blocked with status {response.status_code}")
            response.raise_for_status()
            return response.text
        except (requests.RequestException, FetchError) as exc:
            last_error = exc
            _backoff(attempt)
    raise FetchError(f"failed to fetch {url}: {last_error}")


def _build_headers() -> dict:
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
    }


def _backoff(attempt: int) -> None:
    delay = (2 ** attempt) + random.uniform(0, 1)
    time.sleep(delay)
