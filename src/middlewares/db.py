from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.core.database import get_async_db
from src.repositories.funnel_settings_repository import FunnelSettingsRepository
from src.repositories.lead_repository import LeadRepository
from src.repositories.scheduled_message_repository import ScheduledMessageRepository
from src.repositories.user_repository import UserRepository
from src.services.funnel_service import FunnelService
from src.services.lead_service import LeadService
from src.services.scheduling_service import SchedulingService
from src.services.stats_service import StatsService
from src.services.user_service import UserService


class DbSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async for session in get_async_db():
            bot = data["bot"]
            user_repository = UserRepository(session)

            data["session"] = session
            data["user_service"] = UserService(session, user_repository)
            data["funnel_service"] = FunnelService(session, FunnelSettingsRepository(session))
            data["lead_service"] = LeadService(session, bot, LeadRepository(session), user_repository)
            data["scheduling_service"] = SchedulingService(
                session,
                bot,
                ScheduledMessageRepository(session),
                FunnelSettingsRepository(session),
                user_repository,
            )
            data["stats_service"] = StatsService(session, user_repository)

            return await handler(event, data)
