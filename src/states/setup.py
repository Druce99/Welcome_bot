from aiogram.fsm.state import State, StatesGroup


class SetupStates(StatesGroup):
    waiting_channel = State()
    waiting_welcome_text = State()
    waiting_lead_magnet = State()
    waiting_warmup_text = State()
    waiting_offer_text = State()
    waiting_offer_price = State()
