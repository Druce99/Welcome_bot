from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user_repository import UserRepository


@dataclass
class FunnelStats:
    subscribers: int
    case_views: int
    offer_views: int
    purchases: int

    @property
    def conversion_rate(self) -> float:
        if self.subscribers == 0:
            return 0.0
        return self.purchases / self.subscribers * 100


class StatsService:
    def __init__(self, session: AsyncSession, user_repository: UserRepository):
        self.session = session
        self.user_repository = user_repository

    async def get_funnel_stats(self) -> FunnelStats:
        return FunnelStats(
            subscribers=await self.user_repository.count_by_min_funnel_step(1),
            case_views=await self.user_repository.count_by_min_funnel_step(2),
            offer_views=await self.user_repository.count_by_min_funnel_step(3),
            purchases=await self.user_repository.count_by_min_funnel_step(4),
        )
