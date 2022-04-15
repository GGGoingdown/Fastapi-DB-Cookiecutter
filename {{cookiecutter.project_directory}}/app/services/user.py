from typing import Iterable, Optional

# Application
from app import repositories
from app.models import User
from app.schemas import UserSchema


class UserService:
    __slots__ = ("_user_repo", "_user_role_repo", "_user_cache")

    def __init__(
        self,
        user_repo: repositories.UserRepo,
        user_role_repo: repositories.UserRoleRepo,
        user_cache: repositories.UserCache,
    ) -> None:
        self._user_repo = user_repo
        self._user_role_repo = user_role_repo
        self._user_cache = user_cache

    async def get_all_users(
        self, *, offset: int = 0, limit: int = 100
    ) -> Iterable[User]:
        users = await self._user_repo.get_all(offset=offset, limit=limit)
        return users

    async def get_user_with_roles(
        self, user_id: int
    ) -> Optional[UserSchema.UserInfoRoles]:
        user = await self._user_repo.get_by_id_with_role(id=user_id)
        return UserSchema.UserInfoRoles.from_orm(user) if user else None

    async def get_roles_by_user_id(self, user_id: int) -> Iterable[str]:
        roles = await self._user_role_repo.get_by_user_id(user_id)
        return [role.value for role in roles]

    async def save_user_in_cache(self, user_id: int) -> bool:
        return await self._user_cache.save(user_id)

    async def user_exists_in_cache(self, user_id: int) -> bool:
        res = await self._user_cache.get(user_id)
        return True if res else False

    async def remove_user_in_cache(self, user_id: int) -> bool:
        res = await self._user_cache.delete(user_id)
        return True if res else False
