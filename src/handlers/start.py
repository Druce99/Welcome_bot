from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.core.config import settings
from src.core.enums import UserRole
from src.keyboards.buyer import get_subscription_keyboard
from src.keyboards.owner import get_owner_menu_keyboard, get_persistent_menu_keyboard
from src.services.funnel_service import FunnelService
from src.services.user_service import UserService

router = Router()


@router.message(CommandStart())
async def start_handler(
    message: Message,
    user_service: UserService,
    funnel_service: FunnelService,
) -> None:
    user = await user_service.get_or_create(
        user_id=message.from_user.id,
        username=message.from_user.username,
    )

    if user.id == settings.owner_id:
        if user.role != UserRole.OWNER:
            await user_service.set_role(user, UserRole.OWNER)
        await message.answer(
            "Добро пожаловать! Вы — владелец бота.",
            reply_markup=get_owner_menu_keyboard(),
        )
        await message.answer(
            "Кнопка «🏠 Меню» всегда под рукой — отменит текущее действие и вернёт сюда.",
            reply_markup=get_persistent_menu_keyboard(),
        )
        return

    funnel_settings = await funnel_service.get_by_owner(settings.owner_id)
    if funnel_settings is None:
        await message.answer("Воронка ещё не настроена владельцем. Загляните позже.")
        return

    await message.answer(funnel_settings.welcome_text, reply_markup=get_subscription_keyboard())
