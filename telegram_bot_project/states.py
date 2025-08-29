# states.py
from aiogram.fsm.state import StatesGroup, State
from typing import Dict, List

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
    delete_morning_routine = State()
    update_morning_routine = State()
    update_morning_routine_id = State()
    feedback_message = State()
    provide_title_focusing = State()
    delete_focus = State()
    start_work = State()
    ai_talk = State()
    provide_remind_name = State()
    provide_remind_time = State()

user_task_start_time = {}
routine_start_time = {}
focus_times = {}
morning_routine_timer = {}
FOCUS_ZONE_START_TIME: int = None
AI_CHAT_CONTEXT: Dict[int, List[Dict[str, str]]] = {}