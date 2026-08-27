import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from src.core.config import settings
from src.core.scheduler import setup_scheduler
from src.handlers.buyer_funnel import router as buyer_funnel_router
from src.handlers.owner_dashboard import router as owner_dashboard_router
from src.handlers.owner_menu import router as owner_menu_router
from src.handlers.owner_setup import router as owner_setup_router
from src.handlers.start import router as start_router
from src.middlewares.db import DbSessionMiddleware


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    storage = RedisStorage.from_url(settings.redis_url)
    dp = Dispatcher(storage=storage)

    dp.update.outer_middleware(DbSessionMiddleware())
    dp.include_router(owner_menu_router)
    dp.include_router(start_router)
    dp.include_router(buyer_funnel_router)
    dp.include_router(owner_setup_router)
    dp.include_router(owner_dashboard_router)

    scheduler = setup_scheduler(bot)
    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
