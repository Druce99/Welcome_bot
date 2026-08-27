from sqlalchemy.ext.asyncio import AsyncSession

from src.core.enums import UserRole
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.schemas.users import UserCreate, UserUpdate


class UserService:
    def __init__(self, session: AsyncSession, user_repository: UserRepository):
        self.session = session
        self.user_repository = user_repository

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.user_repository.get_by_id(user_id)

    async def get_or_create(self, user_id: int, username: str | None) -> User:
        user = await self.user_repository.get_by_id(user_id)
        if user is not None:
            return user
        user = await self.user_repository.create(UserCreate(id=user_id, username=username))
        await self.session.commit()
        return user

    async def advance_funnel_step(self, user: User, step: int) -> User:
        user = await self.user_repository.update(user, UserUpdate(funnel_step=step))
        await self.session.commit()
        return user

    async def set_role(self, user: User, role: UserRole) -> User:
        user = await self.user_repository.update(user, UserUpdate(role=role))
        await self.session.commit()
        return user
