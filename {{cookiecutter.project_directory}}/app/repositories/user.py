import aioredis
from loguru import logger
from typing import Iterable, Optional

# Application
from app.repositories import BaseRepository
from app.models import User, Role
from app.constants import RoleEnum
from app.utils import get_utc_now, dt_to_string


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=User)

    async def get_by_mail(self, email: str) -> Optional[User]:
        return await self.get(email=email)

    async def get_by_id_with_role(self, id: int) -> Optional[User]:
        return await self.get(id=id, prefetch=("roles",))

    async def get_by_id(
        self,
        id: int,
    ) -> Optional[User]:

        return await self.get(id=id)


class UserRoleRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=Role)

    async def get_by_user_id(self, user_id: int) -> Iterable[RoleEnum]:
        roles = await self.model.filter(users__id=user_id).values_list(
            "name", flat=True
        )
        return roles


class UserCache:
    __slots__ = ("_redis_client", "_expired_seconds")

    def __init__(self, redis_client: aioredis, expired_time_min: int) -> None:
        self._redis_client = redis_client
        self._expired_seconds = expired_time_min * 60

    async def save(self, user_id: int) -> bool:
        now = get_utc_now()
        res = await self._redis_client.setex(
            user_id, self._expired_seconds, dt_to_string(now)
        )
        logger.debug(f"[UserCache]::Save: {res}")
        return res

    async def get(self, user_id: int) -> Optional[str]:
        res = await self._redis_client.get(user_id)
        logger.debug(f"[UserCache]::Get: {res}")
        return res

    async def delete(self, user_id: int) -> int:
        res = await self._redis_client.delete(user_id)
        logger.debug(f"[UserCache]::Delete: {res}")
        return res
