from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.funnel_settings import FunnelSettings
from src.schemas.funnel_settings import FunnelSettingsCreate, FunnelSettingsUpdate


class FunnelSettingsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, funnel_settings_id: int) -> FunnelSettings | None:
        return await self.session.get(FunnelSettings, funnel_settings_id)

    async def get_by_owner_id(self, owner_id: int) -> FunnelSettings | None:
        result = await self.session.execute(
            select(FunnelSettings).where(FunnelSettings.owner_id == owner_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data: FunnelSettingsCreate) -> FunnelSettings:
        funnel_settings = FunnelSettings(**data.model_dump())
        self.session.add(funnel_settings)
        await self.session.flush()
        return funnel_settings

    async def update(
        self, funnel_settings: FunnelSettings, data: FunnelSettingsUpdate
    ) -> FunnelSettings:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(funnel_settings, field, value)
        await self.session.flush()
        return funnel_settings

    async def delete(self, funnel_settings: FunnelSettings) -> None:
        await self.session.delete(funnel_settings)
        await self.session.flush()
