from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    language = State()
    phone = State()
    fio = State()
    conf = State()
    mainmenucheck = State()
    back_from_show_location = State()
    back_from_show_phone = State()
    back_from_price = State()
    back_from_course_info_menu = State()