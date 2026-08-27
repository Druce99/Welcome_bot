from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

MENU_BUTTON_TEXT = "🏠 Меню"


def get_persistent_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=MENU_BUTTON_TEXT)
    return builder.as_markup(resize_keyboard=True)


def get_owner_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Настроить воронку", callback_data="owner_menu_setup")
    builder.button(text="Мои лиды", callback_data="owner_menu_leads")
    builder.button(text="Статистика", callback_data="owner_menu_stats")
    builder.adjust(1)
    return builder.as_markup()


def get_contact_buyer_keyboard(buyer_username: str | None) -> InlineKeyboardMarkup | None:
    if not buyer_username:
        return None
    builder = InlineKeyboardBuilder()
    builder.button(text="Написать клиенту", url=f"https://t.me/{buyer_username}")
    return builder.as_markup()
