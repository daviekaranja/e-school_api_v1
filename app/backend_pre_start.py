import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN)
)
def init() -> None:
    try:
        logger.info("   checking database")
        db = SessionLocal()
        # Try and create session to check if the DB is awake
        db.execute("SELECT 1")
        logger.info("   database up and running successfully")
    except Exception as e:
        logger.error(e)
        logger.warning(f"   oops database error{e}")
        raise e


def main() -> None:
    logger.info('   Initializing service')
    init()
    logger.info("   service initialized successfully")


if __name__ == "__main__":
    main()
