from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.leads import Lead
from src.schemas.leads import LeadCreate


class LeadRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, lead_id: int) -> Lead | None:
        return await self.session.get(Lead, lead_id)

    async def get_by_owner_and_buyer(self, owner_id: int, buyer_id: int) -> Lead | None:
        result = await self.session.execute(
            select(Lead).where(Lead.owner_id == owner_id, Lead.buyer_id == buyer_id)
        )
        return result.scalar_one_or_none()

    async def list_by_owner(self, owner_id: int) -> list[Lead]:
        result = await self.session.execute(
            select(Lead).where(Lead.owner_id == owner_id).order_by(Lead.created_at.desc())
        )
        return list(result.scalars().all())

    async def create(self, data: LeadCreate) -> Lead:
        lead = Lead(**data.model_dump())
        self.session.add(lead)
        await self.session.flush()
        return lead
