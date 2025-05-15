# Price Tracker

Трекер цен на товары с email-уведомлениями при снижении цены до целевой.

## Возможности

- Парсинг цен с интернет-магазинов (BeautifulSoup, несколько стратегий поиска цены)
- Проверка по расписанию через APScheduler
- Хранение истории цен в БД (SQLAlchemy)
- Email-оповещение по SMTP при достижении целевой цены
- Устойчивость к сбоям сети: повторные попытки с экспоненциальной задержкой, ротация User-Agent против антибот-защиты

## Стек

Python, BeautifulSoup, SQLAlchemy, APScheduler, SMTP.

## Установка

```bash
pip install -r requirements.txt
cp .env.example .env
```

## Использование

Добавить товар для отслеживания:

```bash
python -m tracker.cli --name "Наушники" --url "https://shop.example/item/123" \
  --target 4990 --email you@example.com
```

Запустить фоновую проверку по расписанию:

```bash
python -m tracker.scheduler
```

## Тесты

```bash
pytest
```
