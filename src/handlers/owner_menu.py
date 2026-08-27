from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.core.config import settings
from src.keyboards.owner import MENU_BUTTON_TEXT, get_owner_menu_keyboard

router = Router()
router.message.filter(F.from_user.id == settings.owner_id)


@router.message(F.text == MENU_BUTTON_TEXT)
async def menu_button_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Главное меню:", reply_markup=get_owner_menu_keyboard())
