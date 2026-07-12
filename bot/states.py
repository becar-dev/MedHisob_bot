from aiogram.fsm.state import State, StatesGroup


class DoctorStates(StatesGroup):
    choosing_analysis_type = State()
    waiting_for_full_name = State()
    waiting_for_birth_date = State()
    waiting_for_phone = State()
    waiting_for_field_manual_value = State()
