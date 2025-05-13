import re

from bs4 import BeautifulSoup


class PriceNotFoundError(Exception):
    pass


PRICE_SELECTORS = [
    {"attrs": {"itemprop": "price"}},
    {"class_": "price"},
    {"class_": "product-price"},
    {"attrs": {"data-price": True}},
]


def extract_price(html: str) -> float:
    soup = BeautifulSoup(html, "lxml")

    for selector in PRICE_SELECTORS:
        node = soup.find(**selector)
        if node is None:
            continue
        raw = node.get("content") or node.get("data-price") or node.get_text()
        price = _parse_number(raw)
        if price is not None:
            return price

    meta = soup.find("meta", attrs={"property": "product:price:amount"})
    if meta and meta.get("content"):
        price = _parse_number(meta["content"])
        if price is not None:
            return price

    raise PriceNotFoundError("price element not found on page")


def extract_title(html: str) -> str | None:
    soup = BeautifulSoup(html, "lxml")
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return None


def _parse_number(raw: str) -> float | None:
    if raw is None:
        return None
    cleaned = re.sub(r"[^\d,.\s]", "", str(raw)).strip()
    cleaned = cleaned.replace(" ", "").replace("\u00a0", "")
    if "," in cleaned and "." in cleaned:
        cleaned = cleaned.replace(",", "")
    elif "," in cleaned:
        cleaned = cleaned.replace(",", ".")
    match = re.search(r"\d+(?:\.\d+)?", cleaned)
    if not match:
        return None
    try:
        return float(match.group())
    except ValueError:
        return None
