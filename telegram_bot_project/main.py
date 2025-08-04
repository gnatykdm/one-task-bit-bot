import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import TOKEN
from bot.scheduler import initialize_scheduler, schedule_all_users_jobs
from bot.commands import *
from bot.callbacks import *
from bot.fallbacks import *
from messages import *

storage: MemoryStorage = MemoryStorage()
dp = Dispatcher(storage=storage)

focus_times = {}
FOCUS_ZONE_START_TIME: int = None

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
@dp.message(lambda m: m.text == BUTTON_ADD_TASK)
async def task(message: Message, state: FSMContext):
    await task_command(message, state)

@dp.message(Command("taskmenu"))
async def task_menu(message: Message):
    await task_menu_command(message)

@dp.message(Command("tasks"))
@dp.message(lambda m: m.text == BUTTON_ALL_TASKS)
async def show_tasks(message: Message):
    await tasks_show_command(message)

@dp.message(Command("complete"))
@dp.message(lambda m: m.text == BUTTON_TOGGLE_STATUS)
async def complete_task(message: Message, state: FSMContext):
    await complete_task_command(message, state)

@dp.message(Command("droptask"))
@dp.message(lambda m: m.text == BUTTON_DELETE_TASK)
async def drop_task(message: Message, state: FSMContext):
    await delete_task_command(message, state)

@dp.message(Command("updatetask"))
@dp.message(lambda m: m.text == BUTTON_EDIT_TASK)
async def update_task(message: Message, state: FSMContext):
    await update_task_command(message, state)

@dp.message(Command("settings"))
@dp.message(lambda m: m.text == BUTTON_SETTINGS)
async def settings(message: Message):
    await setting_menu_command(message)

@dp.message(Command("time_manage"))
@dp.message(lambda m: m.text == ROUTINE_MY_TIME)
@dp.message(lambda m: m.text == SETTINGS_BUTTON_ROUTINE_TIME)
async def my_routine_time(message: Message):
    await routine_time_command(message)

@dp.message(lambda m: m.text == ROUTINE_SET_SLEEP_BUTTON)
async def set_sleep_time(message: Message, state: FSMContext):
    await set_sleep_time_command(message, state)

@dp.message(lambda m: m.text == ROUTINE_SET_WAKE_BUTTON)
async def set_waketime(message: Message, state: FSMContext):
    await set_wake_time_command(message, state)

@dp.message(Command("routine"))
@dp.message(lambda m: m.text == SETTINGS_BUTTON_ROUTINE)
async def routine(message: Message):
    await routine_menu_command(message)

@dp.message(lambda m: m.text == MORNING_ROUTINE_ADD_BTN)
async def morning_add(message: Message, state: FSMContext):
    await state.set_state(DialogStates.add_morning_routine)
    await state.update_data(routine_type="morning")
    await set_morning_routine(message, state)

@dp.message(Command("morning_routine"))
@dp.message(lambda m: m.text == ROUTINE_MORNING_VIEW)
@dp.message(lambda m: m.text == MY_MORNING_ROUTINE_BTN)
async def morning_routines(message: Message):
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

@dp.message(Command("evening_routine"))
@dp.message(lambda m: m.text == ROUTINE_EVENING_VIEW)
@dp.message(lambda m: m.text == MY_EVENING_ROUTINE_BTN)
async def morning_routines(message: Message):
    await show_evening_routines(message)

@dp.message(Command("feedback"))
@dp.message(lambda m: m.text == SETTINGS_BUTTON_FEEDBACK)
async def feedback(message: Message, state: FSMContext):
    await send_feedback_command(message, state)

@dp.message(Command("myday"))
@dp.message(lambda m: m.text == BUTTON_MYDAY)
async def my_day(message: Message):
    await show_daily_stats_command(message)

@dp.message(Command("focus"))
async def focus(message: Message):
    await show_focus_menu(message)

@dp.message(lambda m: m.text == FOCUS_ZONE_START)
async def focus_start(message: Message):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
        return

    global FOCUS_STATUS
    FOCUS_STATUS = True
    focus_times[user_id] = datetime.now()

    await message.answer(
        MESSAGES[language]['START_FOCUS_MSG'],
        reply_markup=focus_menu_keyboard(FOCUS_STATUS)
    )


@dp.message(lambda m: m.text == FOCUS_ZONE_END)
async def focus_end(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
        return

    global FOCUS_STATUS
    FOCUS_STATUS = False

    start_time = focus_times.get(user_id)

    if not start_time:
        await message.answer(
            MESSAGES[language]['NOT_FOUND_FOCUS_SESSION'],
            reply_markup=focus_menu_keyboard(FOCUS_STATUS)
        )
        return

    end_time = datetime.now()
    delta = end_time - start_time

    total_seconds = int(delta.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    focus_times.pop(user_id, None)

    await state.update_data(duration=f"{minutes}m:{seconds}s")
    await message.answer(
        MESSAGES[language]['STOP_FOCUS_MSG'].format(minutes, seconds) +
        '\n' + MESSAGES[language]['SAVE_FOCUS_ZONE'],
        reply_markup=focus_save_question_keyboard()
    )

@dp.message(Command("focuses"))
@dp.message(lambda m: m.text == ALL_FOCUSES_BTN)
async def show_saved_focus(message: Message):
    await show_all_focuses(message)

@dp.message(lambda m: m.text == DELETE_FOCUS)
async def delete_focus(message: Message, state: FSMContext):
    await delete_focus_session(message, state)

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

@dp.callback_query(F.data.in_({"save_focus", "not_save_focus"}))
async def callback_focus_save(callback_query: CallbackQuery, state: FSMContext):
    await callback_focus(callback_query, state)

@dp.callback_query(F.data.in_({"add_title", "not_add_title"}))
async def callback_focus_title_save(callback_query: CallbackQuery, state: FSMContext):
    await callback_focus_title(callback_query, state)

@dp.message()
async def process_fallback(message: Message, state: FSMContext):
    await fallback(message, state)

# Main Function
async def main():
    bot = Bot(token=TOKEN)

    scheduler: AsyncIOScheduler = initialize_scheduler()
    scheduler.add_job(
        MyDayService.create_stats_for_all_users,
        trigger='cron',
        hour='0',
        minute='0'
    )

    await schedule_all_users_jobs(bot)
    await dp.start_polling(bot)

# Start point
if __name__ == "__main__":
    print("-- STARTING ROCKY --\n")
    asyncio.run(main())