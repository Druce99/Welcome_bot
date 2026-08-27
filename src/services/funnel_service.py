from sqlalchemy.ext.asyncio import AsyncSession

from src.models.funnel_settings import FunnelSettings
from src.repositories.funnel_settings_repository import FunnelSettingsRepository
from src.schemas.funnel_settings import FunnelSettingsCreate, FunnelSettingsUpdate


class FunnelService:
    def __init__(self, session: AsyncSession, funnel_settings_repository: FunnelSettingsRepository):
        self.session = session
        self.funnel_settings_repository = funnel_settings_repository

    async def get_by_owner(self, owner_id: int) -> FunnelSettings | None:
        return await self.funnel_settings_repository.get_by_owner_id(owner_id)

    async def create(self, data: FunnelSettingsCreate) -> FunnelSettings:
        funnel_settings = await self.funnel_settings_repository.create(data)
        await self.session.commit()
        return funnel_settings

    async def update(self, funnel_settings: FunnelSettings, data: FunnelSettingsUpdate) -> FunnelSettings:
        funnel_settings = await self.funnel_settings_repository.update(funnel_settings, data)
        await self.session.commit()
        return funnel_settings
