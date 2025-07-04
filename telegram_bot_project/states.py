from aiogram.fsm.state import StatesGroup, State

class DialogStates(StatesGroup):
    waiting_for_idea = State()
    confirm_idea = State()
    delete_idea = State()