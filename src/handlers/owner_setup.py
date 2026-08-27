from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.core.config import settings
from src.schemas.funnel_settings import FunnelSettingsCreate, FunnelSettingsUpdate
from src.services.funnel_service import FunnelService
from src.states.setup import SetupStates

router = Router()
router.message.filter(F.from_user.id == settings.owner_id)
router.callback_query.filter(F.from_user.id == settings.owner_id)


@router.message(Command("setup"))
async def setup_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(SetupStates.waiting_channel)
    await message.answer("Введите username канала (например, @my_channel):")


@router.callback_query(F.data == "owner_menu_setup")
async def setup_start_callback_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SetupStates.waiting_channel)
    await callback.message.answer("Введите username канала (например, @my_channel):")
    await callback.answer()


@router.message(SetupStates.waiting_channel)
async def setup_channel_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(channel_username=message.text)
    await state.set_state(SetupStates.waiting_welcome_text)
    await message.answer("Введите текст приветственного сообщения:")


@router.message(SetupStates.waiting_welcome_text)
async def setup_welcome_text_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(welcome_text=message.text)
    await state.set_state(SetupStates.waiting_lead_magnet)
    await message.answer("Отправьте файл лид-магнита (документ):")


@router.message(SetupStates.waiting_lead_magnet, F.document)
async def setup_lead_magnet_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(lead_magnet_file_id=message.document.file_id)
    await state.set_state(SetupStates.waiting_warmup_text)
    await message.answer("Введите текст прогревающего сообщения (кейс через 24ч):")


@router.message(SetupStates.waiting_lead_magnet)
async def setup_lead_magnet_invalid_handler(message: Message) -> None:
    await message.answer("Пожалуйста, отправьте файл лид-магнита как документ.")


@router.message(SetupStates.waiting_warmup_text)
async def setup_warmup_text_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(warm_up_text=message.text)
    await state.set_state(SetupStates.waiting_offer_text)
    await message.answer("Введите текст оффера (через 48ч):")


@router.message(SetupStates.waiting_offer_text)
async def setup_offer_text_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(offer_text=message.text)
    await state.set_state(SetupStates.waiting_offer_price)
    await message.answer("Введите цену оффера:")


@router.message(SetupStates.waiting_offer_price)
async def setup_offer_price_handler(
    message: Message,
    state: FSMContext,
    funnel_service: FunnelService,
) -> None:
    data = await state.get_data()
    data["offer_price"] = message.text

    existing = await funnel_service.get_by_owner(settings.owner_id)
    if existing is None:
        await funnel_service.create(FunnelSettingsCreate(owner_id=settings.owner_id, **data))
    else:
        await funnel_service.update(existing, FunnelSettingsUpdate(**data))

    await state.clear()
    await message.answer("Воронка настроена! ✅")
