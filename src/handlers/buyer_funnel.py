from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.core.config import settings
from src.keyboards.buyer import get_offer_details_keyboard
from src.services.funnel_service import FunnelService
from src.services.lead_service import LeadService
from src.services.scheduling_service import SchedulingService
from src.services.user_service import UserService
from src.states.purchase import PurchaseStates

router = Router()


@router.callback_query(F.data == "check_subscription")
async def check_subscription_handler(
    callback: CallbackQuery,
    user_service: UserService,
    funnel_service: FunnelService,
    lead_service: LeadService,
    scheduling_service: SchedulingService,
) -> None:
    user = await user_service.get_or_create(user_id=callback.from_user.id, username=callback.from_user.username)
    if user.funnel_step >= 1:
        await callback.answer("Вы уже подписаны и получили материал.")
        return

    funnel_settings = await funnel_service.get_by_owner(settings.owner_id)
    if funnel_settings is None:
        await callback.answer("Воронка не настроена.", show_alert=True)
        return

    is_subscribed = await lead_service.check_subscription(
        funnel_settings.channel_username, callback.from_user.id
    )
    if is_subscribed is None:
        await callback.answer("Не удалось проверить подписку. Попробуйте позже.", show_alert=True)
        return

    if not is_subscribed:
        await callback.answer("Вы ещё не подписались на канал!", show_alert=True)
        return

    await user_service.advance_funnel_step(user, 1)
    await scheduling_service.schedule_messages_for_user(user.id)

    await callback.message.edit_text("Спасибо за подписку! Вот ваш материал 🎁")
    await callback.message.answer_document(funnel_settings.lead_magnet_file_id)
    await callback.answer()


@router.callback_query(F.data == "want_to_buy")
async def want_to_buy_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer("Оставьте контакт для связи (телефон или @username):")
    await state.set_state(PurchaseStates.waiting_contact)
    await callback.answer()


@router.callback_query(F.data == "offer_details")
async def offer_details_handler(callback: CallbackQuery, funnel_service: FunnelService) -> None:
    funnel_settings = await funnel_service.get_by_owner(settings.owner_id)
    if funnel_settings is None:
        await callback.answer("Воронка не настроена.", show_alert=True)
        return

    text = f"{funnel_settings.offer_text}\n\nЦена: {funnel_settings.offer_price}"
    await callback.message.answer(text, reply_markup=get_offer_details_keyboard())
    await callback.answer()


@router.callback_query(F.data == "contact_owner_directly")
async def contact_owner_directly_handler(callback: CallbackQuery, user_service: UserService) -> None:
    owner = await user_service.get_by_id(settings.owner_id)
    if owner is not None and owner.username:
        text = f"Напишите нам напрямую: @{owner.username}"
    else:
        text = "Оставьте контакт здесь, и мы свяжемся с вами сами."
    await callback.message.answer(text)
    await callback.answer()


@router.message(PurchaseStates.waiting_contact)
async def process_contact_handler(
    message: Message,
    state: FSMContext,
    lead_service: LeadService,
) -> None:
    lead = await lead_service.create_lead(
        owner_id=settings.owner_id,
        buyer_id=message.from_user.id,
        buyer_username=message.from_user.username,
        buyer_contact=message.text,
    )
    await state.clear()

    if lead is None:
        await message.answer("Вы уже отправляли заявку, владелец скоро свяжется с вами.")
        return

    await message.answer("Спасибо! Владелец скоро свяжется с вами.")