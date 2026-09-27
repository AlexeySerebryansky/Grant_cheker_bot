from aiogram.fsm.state import State, StatesGroup


class ProfileState(StatesGroup):
    waiting_for_first_profile = State()
    waiting_for_new_profile = State()
    waiting_for_update = State()