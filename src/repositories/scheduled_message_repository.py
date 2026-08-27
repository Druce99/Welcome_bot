from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.scheduled_messages import ScheduledMessage
from src.schemas.scheduled_messages import ScheduledMessageCreate


class ScheduledMessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, message_id: int) -> ScheduledMessage | None:
        return await self.session.get(ScheduledMessage, message_id)

    async def get_pending(self, now: datetime) -> list[ScheduledMessage]:
        result = await self.session.execute(
            select(ScheduledMessage).where(
                ScheduledMessage.is_sent.is_(False),
                ScheduledMessage.send_at <= now,
            )
        )
        return list(result.scalars().all())

    async def create(self, data: ScheduledMessageCreate) -> ScheduledMessage:
        scheduled_message = ScheduledMessage(**data.model_dump())
        self.session.add(scheduled_message)
        await self.session.flush()
        return scheduled_message

    async def mark_as_sent(self, scheduled_message: ScheduledMessage) -> ScheduledMessage:
        scheduled_message.is_sent = True
        await self.session.flush()
        return scheduled_message
