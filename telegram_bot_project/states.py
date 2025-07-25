from aiogram.fsm.state import StatesGroup, State

class DialogStates(StatesGroup):
    waiting_for_idea = State()
    confirm_idea = State()
    delete_idea = State()
    update_idea = State()
    waiting_for_update_text = State()
    confirm_task = State()
    task_deadline = State()
    delete_task = State()
    complete_task = State()
    update_task_id = State()
    update_task_name = State()
    set_wake_time = State()
    set_sleep_time = State()
    add_morning_routine = State()