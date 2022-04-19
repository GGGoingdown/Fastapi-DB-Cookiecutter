from tortoise import Tortoise, run_async
from tenacity import retry, stop_after_attempt, wait_fixed
from loguru import logger

# Application
# try:
#     from app import db
# except ModuleNotFoundError:
#     #! For cookiecutter testing
#     import sys

#     sys.path.append("/app/Testing-Project")

from app import db

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(stop=stop_after_attempt(max_tries), wait=wait_fixed(wait_seconds))
async def connect():
    try:
        await db.db_startup()
        conn = Tortoise.get_connection("default")
        logger.info(f"Ping -> {await conn.execute_query('SELECT 1')}")

    except Exception as e:
        logger.error(e)
        raise e

    finally:
        await db.db_shutdown()


async def main():
    logger.info("--- Initial DB ---")
    await connect()
    logger.info("--- Initial DB successful ---")


if __name__ == "__main__":
    run_async(main())
