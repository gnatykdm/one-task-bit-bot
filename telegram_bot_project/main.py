import asyncio
from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy import lambda_stmt
from sqlalchemy.util import await_fallback

from bot.callbacks import *
from bot.commands import *
from bot.handlers import *
from config import TOKEN
from messages import *
from states import DialogStates

storage: MemoryStorage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Command Handlers
@dp.message(Command("start"))
async def start(message: Message):
    await start_command(message)

@dp.message(Command("help"))
async def help(message: Message):
    await help_command(message)

@dp.message(Command("menu"))
@dp.message(lambda m: m.text == MENU_BUTTON)
async def menu(message: Message):
    await menu_command(message)

@dp.message(Command("language"))
async def language(message: Message):
    await language_command(message)

@dp.message(lambda m: m.text == SETTINGS_BUTTON_LANGUAGE)
async def language(message: Message):
    await language_command(message)

@dp.message(Command("idea"))
@dp.message(lambda m: m.text == BUTTON_IDEA)
async def idea(message: Message, state: FSMContext):
    await idea_command(message, state)

@dp.message(Command("ideas"))
@dp.message(lambda m: m.text == ALL_IDEAS)
async def ideas(message: Message):
    await ideas_command(message)

@dp.message(lambda m: m.text == DEL_IDEA_BUTTON)
async def delete_idea(message: Message, state: FSMContext):
    await delete_idea_command(message, state)

@dp.message(lambda m: m.text == UPDATE_IDEA_BUTTON)
async def update_idea(message: Message, state: FSMContext):
    await update_idea_command(message, state)

@dp.message(Command("task"))
async def task(message: Message, state: FSMContext):
    await task_command(message, state)

@dp.message(lambda m: m.text == BUTTON_ADD_TASK)
async def add_task(message: Message, state: FSMContext):
    await task_command(message, state)

@dp.message(Command("taskmenu"))
async def task_menu(message: Message):
    await task_menu_command(message)

@dp.message(Command("tasks"))
async def show_tasks(message: Message):
    await tasks_show_command(message)

@dp.message(Command("complete"))
async def complete_task(message: Message, state: FSMContext):
    await complete_task_command(message, state)

@dp.message(lambda m: m.text == BUTTON_TOGGLE_STATUS)
async def toggle_task_status(message: Message, state: FSMContext):
    await complete_task_command(message, state)

@dp.message(lambda m: m.text == BUTTON_ALL_TASKS)
async def show_all_tasks(message: Message):
    await tasks_show_command(message)

@dp.message(lambda m: m.text == BUTTON_DELETE_TASK)
async def delete_task(message: Message, state: FSMContext):
    await delete_task_command(message, state)

@dp.message(Command("droptask"))
async def drop_task(message: Message, state: FSMContext):
    await delete_task_command(message, state)

@dp.message(Command("updatetask"))
async def update_task(message: Message, state: FSMContext):
    await update_task_command(message, state)

@dp.message(lambda m: m.text == BUTTON_EDIT_TASK)
async def edit_task(message: Message, state: FSMContext):
    await update_task_command(message, state)

@dp.message(lambda m: m.text == BUTTON_SETTINGS)
async def settings(message: Message):
    await setting_menu_command(message)

@dp.message(Command("settings"))
async def settings(message: Message):
    await setting_menu_command(message)

@dp.message(Command("routinetime"))
async def waketime(message: Message):
    await routine_time_command(message)

@dp.message(lambda m: m.text == SETTINGS_BUTTON_ROUTINE_TIME)
async def waketime(message: Message):
    await routine_time_command(message)

@dp.message(lambda m: m.text == ROUTINE_MY_TIME)
async def my_routine_time(message: Message):
    await routine_time_command(message)

@dp.message(Command("setwake"))
async def set_waketime(message: Message, state: FSMContext):
    await set_wake_time_command(message, state)

@dp.message(Command("time"))
async def my_routine_time(message: Message):
    await routine_time_command(message)

@dp.message(Command("setsleep"))
async def set_sleep_time(message: Message, state: FSMContext):
    await set_sleep_time_command(message, state)

@dp.message(lambda m: m.text == ROUTINE_SET_SLEEP_BUTTON)
async def set_sleep_time(message: Message, state: FSMContext):
    await set_sleep_time_command(message, state)

@dp.message(lambda m: m.text == ROUTINE_SET_WAKE_BUTTON)
async def set_waketime(message: Message, state: FSMContext):
    await set_wake_time_command(message, state)

@dp.message(Command("routine"))
async def routine(message: Message):
    await routine_menu_command(message)

@dp.message(lambda m: m.text == SETTINGS_BUTTON_ROUTINE)
async def routine(message: Message):
    await routine_menu_command(message)

@dp.message(lambda m: m.text == MORNINGG_ROUTINE_ADD_BTN)
async def morning_add(message: Message, state: FSMContext):
    await state.set_state(DialogStates.add_morning_routine)
    await state.update_data(routine_type="morning")
    await set_morning_routine(message, state)

@dp.message(Command("morning_routines"))
async def morning_routines(message: Message):
    await show_morning_routines(message)

@dp.message(lambda m: m.text == ROUTINE_MORNING_VIEW)
async def morning_routines_view(message: types.Message):
    await show_morning_routines(message)

@dp.message(lambda m: m.text == MY_MORNING_ROUTINE_BTN)
async def morning_routines_show(message: types.Message):
    await show_morning_routines(message)

@dp.message(lambda m: m.text == MORNING_ROUTINE_DELETE_BTN)
async def morning_routines_delete(message: types.Message, state: FSMContext):
    await state.set_state(DialogStates.delete_morning_routine)
    await state.update_data(routine_type="morning")
    await delete_morning_routine(message, state, type="morning")

@dp.message(lambda m: m.text == MORNING_ROUTINE_EDIT_BTN)
async def morning_routines_edit(message: types.Message, state: FSMContext):
    await state.set_state(DialogStates.update_morning_routine)
    await state.update_data(routine_type="morning")
    await update_morning_routine(message, state, type="morning")

@dp.message(lambda m: m.text == EVENING_ROUTINE_ADD_BTN)
async def evening_routine_add(message: Message, state: FSMContext):
    await state.set_state(DialogStates.add_morning_routine)
    await state.update_data(routine_type="evening")
    await set_morning_routine(message, state)

@dp.message(lambda m: m.text == EVENING_ROUTINE_DELETE_BTN)
async def evening_routines_delete(message: types.Message, state: FSMContext):
    await state.set_state(DialogStates.delete_morning_routine)
    await state.update_data(routine_type="evening")
    await delete_morning_routine(message, state, type="evening")

@dp.message(lambda m: m.text == EVENING_ROUTINE_EDIT_BTN)
async def evening_routines_edit(message: types.Message, state: FSMContext):
    await state.set_state(DialogStates.update_morning_routine)
    await state.update_data(routine_type="evening")
    await update_morning_routine(message, state, type="evening")

@dp.message(lambda m: m.text == MY_EVENING_ROUTINE_BTN)
async def evening_routines_show(message: types.Message):
    await show_evening_routines(message)

@dp.message(Command("evening_routines"))
async def morning_routines(message: Message):
    await show_evening_routines(message)

@dp.message(Command("feedback"))
async def feedback(message: Message, state: FSMContext):
    await send_feedback_command(message, state)

@dp.message(lambda m: m.text == SETTINGS_BUTTON_FEEDBACK)
async def feedback(message: Message, state: FSMContext):
    await send_feedback_command(message, state)

@dp.message(lambda m: m.text == ROUTINE_EVENING_VIEW)
async def evening_routines_view(message: types.Message):
    await show_evening_routines(message)

@dp.callback_query(F.data.in_({"morning_view", "evening_view"}))
async def callback_routine(callback_query: CallbackQuery):
    await callback_routines(callback_query)

@dp.callback_query(F.data.in_({"lang_ua", "lang_en"}))
async def callback_language(callback_query: CallbackQuery):
    await start_callback_language(callback_query)

@dp.callback_query(F.data.in_({"delete_idea", "save_idea"}))
async def callback_idea(callback_query: CallbackQuery, state: FSMContext):
    await callback_idea_process(callback_query, state)

@dp.callback_query(F.data.in_({"yes_task", "no_task"}))
async def callback_idea(callback_query: CallbackQuery, state: FSMContext):
    await callback_task_deadline(callback_query, state)

@dp.message()
async def process_fallback(message: Message, state: FSMContext):
    current_state = await state.get_state()
    print(f"-- [DEBUG] - Current state: {current_state}")
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

# Main Function
async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

# Start point
if __name__ == "__main__":
    print("-- STARTING ROCKY --\n")
    asyncio.run(main())