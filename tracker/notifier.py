import smtplib
from email.message import EmailMessage

from tracker.config import settings


def send_price_alert(to_email: str, product_name: str, current_price: float, target_price: float, url: str) -> None:
    message = EmailMessage()
    message["Subject"] = f"Цена снизилась: {product_name}"
    message["From"] = settings.smtp_from
    message["To"] = to_email
    message.set_content(_build_body(product_name, current_price, target_price, url))
    _send(message)


def _build_body(product_name: str, current_price: float, target_price: float, url: str) -> str:
    return (
        f"Товар «{product_name}» подешевел.\n\n"
        f"Текущая цена: {current_price:.2f}\n"
        f"Целевая цена: {target_price:.2f}\n\n"
        f"Ссылка: {url}\n"
    )


def _send(message: EmailMessage) -> None:
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        if settings.smtp_user:
            server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(message)
