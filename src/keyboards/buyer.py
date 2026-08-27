from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_subscription_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Я подписался ✅", callback_data="check_subscription")
    return builder.as_markup()


def get_offer_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Хочу купить 🛒", callback_data="want_to_buy")
    builder.button(text="Узнать подробнее", callback_data="offer_details")
    builder.adjust(1)
    return builder.as_markup()


def get_offer_details_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Хочу купить 🛒", callback_data="want_to_buy")
    builder.button(text="Написать напрямую", callback_data="contact_owner_directly")
    builder.adjust(1)
    return builder.as_markup()