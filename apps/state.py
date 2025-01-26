from aiogram.fsm.state import State, StatesGroup


class AddUser(StatesGroup):
    waiting_for_id = State()


class DelUser(StatesGroup):
    waiting_for_id = State()


class CheckIMEI(StatesGroup):
    waiting_for_imei = State()