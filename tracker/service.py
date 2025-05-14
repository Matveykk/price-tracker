import logging

from sqlalchemy.orm import Session

from tracker import notifier, parser
from tracker.fetcher import FetchError, fetch_html
from tracker.models import PriceHistory, Product

logger = logging.getLogger(__name__)


def add_product(db: Session, name: str, url: str, target_price: float, notify_email: str) -> Product:
    product = Product(name=name, url=url, target_price=target_price, notify_email=notify_email)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def check_product(db: Session, product: Product) -> float | None:
    try:
        html = fetch_html(product.url)
        price = parser.extract_price(html)
    except (FetchError, parser.PriceNotFoundError) as exc:
        logger.warning("check failed for %s: %s", product.url, exc)
        return None

    db.add(PriceHistory(product_id=product.id, price=price))
    product.last_price = price

    if price <= product.target_price and not product.notified:
        _notify(product, price)
        product.notified = 1
    elif price > product.target_price:
        product.notified = 0

    db.commit()
    return price


def check_all(db: Session) -> int:
    products = db.query(Product).all()
    checked = 0
    for product in products:
        if check_product(db, product) is not None:
            checked += 1
    return checked


def _notify(product: Product, price: float) -> None:
    try:
        notifier.send_price_alert(
            to_email=product.notify_email,
            product_name=product.name,
            current_price=price,
            target_price=product.target_price,
            url=product.url,
        )
        logger.info("alert sent to %s for %s", product.notify_email, product.name)
    except Exception as exc:
        logger.error("failed to send alert: %s", exc)
