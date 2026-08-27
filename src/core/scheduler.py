from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.core.database import async_session_maker
from src.repositories.funnel_settings_repository import FunnelSettingsRepository
from src.repositories.scheduled_message_repository import ScheduledMessageRepository
from src.repositories.user_repository import UserRepository
from src.services.scheduling_service import SchedulingService


async def send_pending_messages_job(bot: Bot) -> None:
    async with async_session_maker() as session:
        scheduling_service = SchedulingService(
            session,
            bot,
            ScheduledMessageRepository(session),
            FunnelSettingsRepository(session),
            UserRepository(session),
        )
        await scheduling_service.send_pending_messages()


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_pending_messages_job, trigger="interval", seconds=60, args=[bot])
    return scheduler
