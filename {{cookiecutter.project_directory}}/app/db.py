import aioredis
from typing import Dict
from tortoise import Tortoise, connections

# from tortoise.contrib.fastapi import register_tortoise

# Configuration
from app.config import settings

db_model_list = ["app.models"]


def get_redis_url() -> str:
    url = f"redis://{settings.redis.username}:{settings.redis.password}@{settings.redis.host}:{settings.redis.port}/{settings.redis.backend_db}"
    return url


def get_pg_url() -> str:
    url = f"postgres://{settings.pg.username}:{settings.pg.password}@{settings.pg.host}:{settings.pg.port}/{settings.pg.db}"
    return url


def get_tortoise_config(db_url: str = None) -> Dict:
    config = {
        "connections": {"default": db_url if db_url else get_pg_url()},
        "apps": {
            "models": {
                "models": [*db_model_list, "aerich.models"],
                "default_connection": "default",
            },
        },
    }
    return config


TORTOISE_ORM = get_tortoise_config()


def redis_init() -> aioredis:
    connect_uri = get_redis_url()
    redis_client = aioredis.from_url(
        connect_uri,
        encoding="utf-8",
        decode_responses=True,
    )
    return redis_client


async def db_startup(config: Dict = TORTOISE_ORM):
    await Tortoise.init(config=config)


async def db_shutdown():
    await connections.close_all()
