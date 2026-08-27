from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.enums import MessageType
from src.keyboards.buyer import get_offer_keyboard
from src.models.funnel_settings import FunnelSettings
from src.models.scheduled_messages import ScheduledMessage
from src.repositories.funnel_settings_repository import FunnelSettingsRepository
from src.repositories.scheduled_message_repository import ScheduledMessageRepository
from src.repositories.user_repository import UserRepository
from src.schemas.scheduled_messages import ScheduledMessageCreate
from src.schemas.users import UserUpdate

CASE_DELAY = timedelta(hours=24)
OFFER_DELAY = timedelta(hours=48)

FUNNEL_STEP_BY_MESSAGE_TYPE = {
    MessageType.CASE: 2,
    MessageType.OFFER: 3,
}


class SchedulingService:
    def __init__(
        self,
        session: AsyncSession,
        bot: Bot,
        scheduled_message_repository: ScheduledMessageRepository,
        funnel_settings_repository: FunnelSettingsRepository,
        user_repository: UserRepository,
    ):
        self.session = session
        self.bot = bot
        self.scheduled_message_repository = scheduled_message_repository
        self.funnel_settings_repository = funnel_settings_repository
        self.user_repository = user_repository

    async def schedule_messages_for_user(self, user_id: int) -> None:
        now = datetime.utcnow()
        await self.scheduled_message_repository.create(
            ScheduledMessageCreate(user_id=user_id, message_type=MessageType.CASE, send_at=now + CASE_DELAY)
        )
        await self.scheduled_message_repository.create(
            ScheduledMessageCreate(user_id=user_id, message_type=MessageType.OFFER, send_at=now + OFFER_DELAY)
        )
        await self.session.commit()

    async def send_pending_messages(self) -> None:
        now = datetime.utcnow()
        pending = await self.scheduled_message_repository.get_pending(now)
        if not pending:
            return

        funnel_settings = await self.funnel_settings_repository.get_by_owner_id(settings.owner_id)

        for message in pending:
            text = self._build_text(message.message_type, funnel_settings)
            reply_markup = get_offer_keyboard() if message.message_type == MessageType.OFFER else None
            try:
                await self.bot.send_message(chat_id=message.user_id, text=text, reply_markup=reply_markup)
            except TelegramAPIError:
                continue
            await self.scheduled_message_repository.mark_as_sent(message)
            await self._advance_funnel_step(message)
            await self.session.commit()

    async def _advance_funnel_step(self, message: ScheduledMessage) -> None:
        target_step = FUNNEL_STEP_BY_MESSAGE_TYPE[message.message_type]
        user = await self.user_repository.get_by_id(message.user_id)
        if user is not None and user.funnel_step < target_step:
            await self.user_repository.update(user, UserUpdate(funnel_step=target_step))

    def _build_text(self, message_type: MessageType, funnel_settings: FunnelSettings) -> str:
        if message_type == MessageType.CASE:
            return funnel_settings.warm_up_text
        return f"{funnel_settings.offer_text}\n\nЦена: {funnel_settings.offer_price}"
