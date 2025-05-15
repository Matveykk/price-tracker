import pytest

from tracker import parser


def test_extract_price_from_itemprop():
    html = '<div itemprop="price" content="1299.00">1299 руб</div>'
    assert parser.extract_price(html) == 1299.0


def test_extract_price_from_class():
    html = '<span class="price">2 499,90 ₽</span>'
    assert parser.extract_price(html) == 2499.90


def test_extract_price_from_meta():
    html = '<meta property="product:price:amount" content="799.50">'
    assert parser.extract_price(html) == 799.50


def test_extract_price_thousands_separator():
    html = '<div class="price">1,234.56</div>'
    assert parser.extract_price(html) == 1234.56


def test_missing_price_raises():
    with pytest.raises(parser.PriceNotFoundError):
        parser.extract_price("<html><body>no price here</body></html>")


def test_extract_title():
    html = "<html><head><title>Товар — магазин</title></head></html>"
    assert parser.extract_title(html) == "Товар — магазин"
