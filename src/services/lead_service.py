from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from sqlalchemy.ext.asyncio import AsyncSession

from src.keyboards.owner import get_contact_buyer_keyboard
from src.models.leads import Lead
from src.repositories.lead_repository import LeadRepository
from src.repositories.user_repository import UserRepository
from src.schemas.leads import LeadCreate
from src.schemas.users import UserUpdate

SUBSCRIBED_STATUSES = {"creator", "administrator", "member"}
PURCHASE_FUNNEL_STEP = 4


class LeadService:
    def __init__(
        self,
        session: AsyncSession,
        bot: Bot,
        lead_repository: LeadRepository,
        user_repository: UserRepository,
    ):
        self.session = session
        self.bot = bot
        self.lead_repository = lead_repository
        self.user_repository = user_repository

    async def check_subscription(self, channel_username: str, user_id: int) -> bool | None:
        try:
            member = await self.bot.get_chat_member(chat_id=channel_username, user_id=user_id)
        except TelegramBadRequest:
            return None
        return member.status in SUBSCRIBED_STATUSES

    async def list_leads(self, owner_id: int) -> list[Lead]:
        return await self.lead_repository.list_by_owner(owner_id)

    async def create_lead(self, owner_id: int, buyer_id: int, buyer_username: str | None, buyer_contact: str) -> Lead | None:
        existing = await self.lead_repository.get_by_owner_and_buyer(owner_id=owner_id, buyer_id=buyer_id)
        if existing is not None:
            return None

        lead = await self.lead_repository.create(
            LeadCreate(
                owner_id=owner_id,
                buyer_id=buyer_id,
                buyer_username=buyer_username,
                buyer_contact=buyer_contact,
            )
        )

        buyer = await self.user_repository.get_by_id(buyer_id)
        if buyer is not None and buyer.funnel_step < PURCHASE_FUNNEL_STEP:
            await self.user_repository.update(buyer, UserUpdate(funnel_step=PURCHASE_FUNNEL_STEP))

        await self.session.commit()
        await self._notify_owner(lead)
        return lead

    async def _notify_owner(self, lead: Lead) -> None:
        text = (
            "🔥 Новый лид!\n"
            f"Покупатель: @{lead.buyer_username}\n"
            f"Контакт: {lead.buyer_contact}"
        )
        await self.bot.send_message(
            chat_id=lead.owner_id,
            text=text,
            reply_markup=get_contact_buyer_keyboard(lead.buyer_username),
        )