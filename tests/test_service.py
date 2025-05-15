from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tracker.database import Base
from tracker.models import PriceHistory, Product
from tracker import service


def _session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def test_add_product():
    db = _session()
    product = service.add_product(db, "Товар", "http://shop.test/item", 100.0, "u@test.io")
    assert product.id is not None
    assert product.target_price == 100.0


def test_check_product_sends_alert_below_target():
    db = _session()
    product = service.add_product(db, "Товар", "http://shop.test/item", 100.0, "u@test.io")
    html = '<div class="price">90.00</div>'
    with patch("tracker.service.fetch_html", return_value=html), \
         patch("tracker.service.notifier.send_price_alert") as send:
        price = service.check_product(db, product)
    assert price == 90.0
    assert product.notified == 1
    send.assert_called_once()
    assert db.query(PriceHistory).count() == 1


def test_check_product_no_alert_above_target():
    db = _session()
    product = service.add_product(db, "Товар", "http://shop.test/item", 100.0, "u@test.io")
    html = '<div class="price">150.00</div>'
    with patch("tracker.service.fetch_html", return_value=html), \
         patch("tracker.service.notifier.send_price_alert") as send:
        service.check_product(db, product)
    assert product.notified == 0
    send.assert_not_called()


def test_check_product_handles_fetch_failure():
    db = _session()
    product = service.add_product(db, "Товар", "http://shop.test/item", 100.0, "u@test.io")
    with patch("tracker.service.fetch_html", side_effect=service.FetchError("blocked")):
        assert service.check_product(db, product) is None
