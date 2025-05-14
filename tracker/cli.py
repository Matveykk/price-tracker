import argparse

from tracker.database import SessionLocal, init_db
from tracker.service import add_product


def main():
    parser = argparse.ArgumentParser(description="Управление отслеживаемыми товарами")
    parser.add_argument("--name", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--target", type=float, required=True)
    parser.add_argument("--email", required=True)
    args = parser.parse_args()

    init_db()
    db = SessionLocal()
    try:
        product = add_product(db, args.name, args.url, args.target, args.email)
        print(f"added product #{product.id}: {product.name}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
