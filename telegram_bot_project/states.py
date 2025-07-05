from aiogram.fsm.state import StatesGroup, State

class DialogStates(StatesGroup):
    waiting_for_idea = State()
    confirm_idea = State()
    delete_idea = State()
    update_idea = State()
    waiting_for_update_text = State()
    confirm_task = State()
    task_deadline = State()