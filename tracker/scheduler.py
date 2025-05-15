import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from tracker.config import settings
from tracker.database import SessionLocal, init_db
from tracker.service import check_all

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def run_check():
    db = SessionLocal()
    try:
        count = check_all(db)
        logger.info("checked %s products", count)
    finally:
        db.close()


def main():
    init_db()
    scheduler = BlockingScheduler()
    scheduler.add_job(run_check, "interval", minutes=settings.check_interval_minutes, next_run_time=None)
    logger.info("scheduler started, interval=%s min", settings.check_interval_minutes)
    run_check()
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("scheduler stopped")


if __name__ == "__main__":
    main()
