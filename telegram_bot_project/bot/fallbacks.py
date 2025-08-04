# bot/fallbacks.py
from bot.handlers import *
from states import DialogStates

# Fallback
async def fallback(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == DialogStates.waiting_for_idea.state:
        await process_idea_save(message, state)
    elif current_state == DialogStates.delete_idea.state:
        await process_idea_delete(message, state)
    elif current_state == DialogStates.update_idea.state:
        await process_idea_update(message, state)
    elif current_state == DialogStates.waiting_for_update_text:
        await process_save_updated_idea_text(message, state)
    elif current_state == DialogStates.confirm_task:
        await process_task_save(message, state)
    elif current_state == DialogStates.task_deadline:
        await process_task_deadline(message, state)
    elif current_state == DialogStates.delete_task:
        await process_task_delete(message, state)
    elif current_state == DialogStates.complete_task:
        await process_task_complete(message, state)
    elif current_state == DialogStates.update_task_id:
        await process_task_update(message, state)
    elif current_state == DialogStates.update_task_name:
        await process_save_updated_task_name(message, state)
    elif current_state == DialogStates.set_wake_time:
        await process_set_wake_time(message, state)
    elif current_state == DialogStates.set_sleep_time:
        await process_set_sleep_time(message, state)
    elif current_state == DialogStates.add_morning_routine:
        data = await state.get_data()
        routine_type = data.get("routine_type", "morning")
        await process_set_routine(message, state, type=routine_type)
    elif current_state == DialogStates.delete_morning_routine:
        data = await state.get_data()
        routine_type = data.get("routine_type", "morning")
        await process_delete_morning_routine(message, state, type=routine_type)
    elif current_state == DialogStates.update_morning_routine:
        data = await state.get_data()
        routine_type = data.get("routine_type", "morning")
        await process_save_updated_morning_routine(message, state, type=routine_type)
    elif current_state == DialogStates.update_morning_routine_id:
        data = await state.get_data()
        routine_type = data.get("routine_type", "morning")
        await process_update_morning_routine(message, state, type=routine_type)
    elif current_state == DialogStates.feedback_message:
        await process_feedback_message(message, state)
    elif current_state == DialogStates.provide_title_focusing:
        await process_save_focus_session_title(message, state)
    elif current_state == DialogStates.delete_focus:
        await process_delete_focus_session(message, state)