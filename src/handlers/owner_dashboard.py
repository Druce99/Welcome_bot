from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from src.core.config import settings
from src.models.leads import Lead
from src.services.lead_service import LeadService
from src.services.stats_service import FunnelStats, StatsService

router = Router()
router.message.filter(F.from_user.id == settings.owner_id)
router.callback_query.filter(F.from_user.id == settings.owner_id)


def _format_leads(leads: list[Lead]) -> str:
    if not leads:
        return "Заявок пока нет."

    lines = [
        f"{lead.created_at:%d.%m.%Y %H:%M} — "
        f"{f'@{lead.buyer_username}' if lead.buyer_username else 'без username'} — "
        f"{lead.buyer_contact}"
        for lead in leads
    ]
    return "\n".join(lines)


def _format_stats(stats: FunnelStats) -> str:
    return (
        "📊 Статистика воронки:\n\n"
        f"Подписались: {stats.subscribers}\n"
        f"Получили кейс: {stats.case_views}\n"
        f"Увидели оффер: {stats.offer_views}\n"
        f"Купили: {stats.purchases}\n"
        f"Конверсия: {stats.conversion_rate:.1f}%"
    )


@router.message(Command("leads"))
async def leads_handler(message: Message, lead_service: LeadService) -> None:
    leads = await lead_service.list_leads(settings.owner_id)
    await message.answer(_format_leads(leads))


@router.callback_query(F.data == "owner_menu_leads")
async def leads_callback_handler(callback: CallbackQuery, lead_service: LeadService) -> None:
    leads = await lead_service.list_leads(settings.owner_id)
    await callback.message.answer(_format_leads(leads))
    await callback.answer()


@router.message(Command("stats"))
async def stats_handler(message: Message, stats_service: StatsService) -> None:
    stats = await stats_service.get_funnel_stats()
    await message.answer(_format_stats(stats))


@router.callback_query(F.data == "owner_menu_stats")
async def stats_callback_handler(callback: CallbackQuery, stats_service: StatsService) -> None:
    stats = await stats_service.get_funnel_stats()
    await callback.message.answer(_format_stats(stats))
    await callback.answer()
