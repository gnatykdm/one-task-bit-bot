# main.py
import asyncio
from aiogram import types
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from timezonefinder import TimezoneFinder
import pytz

from config import TOKEN
from bot.scheduler import *
from bot.commands import *
from bot.callbacks import *
from bot.fallbacks import *
from messages import *
from states import *
from bot.scheduler import check_upcoming_tasks_v2
from bot.scheduler import cleanup_old_notifications

bot = Bot(token=TOKEN)
storage: MemoryStorage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Command Handlers
@dp.message(Command("start"))
async def start(message: Message):
    await start_command(message)

async def handle_user_location(message: Message):
    user_id = message.from_user.id
    lat = message.location.latitude
    lon = message.location.longitude

    tf = TimezoneFinder()
    tz = tf.timezone_at(lat=lat, lng=lon)

    if tz:
        await UserService.update_user_timezone(user_id, tz)
        await message.answer(f"🌐 Your timezone has been set to: {tz}")
    else:
        await message.answer("❌ Could not detect your timezone. Please select manually.")

    keyboard = get_language_keyboard()
    await message.answer(MESSAGES['ENGLISH']['LANGUAGE_ASK'], reply_markup=keyboard)

dp.message.register(handle_user_location, F.content_type == "location")

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

@dp.message(Command("note"))
@dp.message(lambda m: m.text == BUTTON_IDEA)
async def idea(message: Message, state: FSMContext):
    await idea_command(message, state)

@dp.message(Command("mynotes"))
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

@dp.message(Command("mytasks"))
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
@dp.message(lambda m: m.text == FOCUS_CALL_BTN)
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

@dp.message(lambda m: m.text == STOP_WORK_SESSION)
async def start_work_btn(message: Message) -> None:
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or 'ENGLISH'

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
        return

    task_info = user_task_start_time.get(user_id)
    if not task_info:
        await message.answer(MESSAGES[language]['AUTHORIZATION_PROBLEM'])
        return
    
    task_id, task_data = task_info
    print(f"[DEBUG] - Task id: {task_id} - Start Time: {task_data}")

    stop_time = datetime.now()
    total_seconds = int((stop_time - task_data).total_seconds())
    minutes, seconds = divmod(total_seconds, 60)

    user_task_start_time.pop(user_id, None)

    print(f"[DEBUG] - User with id {user_id} add duration {total_seconds}s to task {task_id}.")
    await TaskService.add_task_complete_duration(task_id, total_seconds)

    task = await TaskService.get_task_by_id(task_id)

    await TaskService.toggle_task_status(task_id)
    await MyDayService.increment_completed_tasks(user_id)

    task_name = task['task_name'] if task else f"Task {task_id}"

    await message.answer(
        MESSAGES[language]['FINISH_WORK_SESSION'].format(task_name, minutes, seconds),
        reply_markup=menu_reply_keyboard()
    )

@dp.message(lambda m: m.text == STOP_WORK_CANCEL)
async def cancel_work_btn(message: Message) -> None:
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or 'ENGLISH'

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
        return

    user_task_start_time.pop(user_id)
    await message.answer(MESSAGES[language]['BREAK_WORK_SESSION'], reply_markup=menu_reply_keyboard())

@dp.message(lambda m: m.text == START_DAY_BTN)
async def start_day_btn(message: Message) -> None:
    await start_day_command(message)

@dp.message(Command("focuses"))
@dp.message(lambda m: m.text == ALL_FOCUSES_BTN)
async def show_saved_focus(message: Message):
    await show_all_focuses(message)

@dp.message(lambda m: m.text == DELETE_FOCUS)
async def delete_focus(message: Message, state: FSMContext):
    await delete_focus_session(message, state)

@dp.message(lambda m: m.text == MORNING_ROUTINE_TIMER_START_BTN)
async def start_morning_routine_timer(message: Message):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or 'ENGLISH'

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
        return
    
    morning_routine_timer[user_id] = datetime.now()
    await message.answer(
        MESSAGES[language]['MORNING_ROUTINE_TIMES_START'],
        reply_markup=stop_routine_button_timer()
    )

@dp.message(lambda m: m.text == STOP_ROUTINE_TIMER_BTN)
async def stop_routine_timer(message: Message):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or 'ENGLISH'

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
        return
    
    now_time = datetime.now()
    start_time = morning_routine_timer.get(user_id)
    if not start_time:
        await message.answer("⚠️ You don't have an active routine timer.")
        return

    delta = now_time - start_time
    minutes, seconds = divmod(delta.seconds, 60)

    morning_routine_timer.pop(user_id)
    await message.answer(
        MESSAGES[language]['MORNING_TASK_CREATE_TIMER_MSG'].format(minutes, seconds),
        reply_markup=task_menu_keyboard()
    )

@dp.message(lambda m: m.text == MORNING_ROUTINE_TIMER_NOPE_BTN)
async def nope_morning_routine_timer(message: Message):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or 'ENGLISH'

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
        return
    
    await message.answer(
        MESSAGES[language]['MORNING_TASK_CREATE_MSG'],
        reply_markup=task_menu_keyboard()
    )

@dp.message(Command("talk"))
@dp.message(lambda m: m.text == AI_ROCKY_BTN)
async def talk_with_rocky(message: Message, state: FSMContext):
    await talk_with_rocky_command(message, state)

@dp.message(Command("stop_talk"))
@dp.message(lambda m: m.text == STOP_CHAT)
async def stop_talk_with_rocky(message: Message, state: FSMContext):
    await stop_talk_command(message, state)

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

@dp.callback_query(F.data.startswith(("complete_task", "cancel_task")))
async def callback_task_status(callback_query: CallbackQuery) -> None:
    await callback_task_menu(callback_query)

@dp.message()
async def process_fallback(message: Message, state: FSMContext):
    await fallback(message, state)


async def main():
    bot = Bot(token=TOKEN)
    
    scheduler = await initialize_scheduler(bot)
    await MyDayService.schedule_daily_stats(bot, scheduler)

    print(f"[SYSTEM] Scheduler timezone: {scheduler.timezone}")
    scheduler.add_job(
        cleanup_old_notifications,
        trigger='cron',
        hour=1,
        minute=0,
        id='cleanup_notifications'
    )
    
    notifier = PreciseTaskNotifier(bot, scheduler)
    get_notifier_instance(bot) 
    
    print("[STARTUP] Planning precise notifications for all tasks...")
    await notifier.schedule_all_task_notifications()
    
    scheduler.add_job(
        notifier.schedule_all_task_notifications,
        trigger='interval',
        minutes=10,
        id='reschedule_notifications'
    )
    
    scheduler.add_job(
        check_upcoming_tasks_v2,
        trigger='interval',
        minutes=2,
        args=[bot],
        id='backup_task_check'
    )
    
    await schedule_all_users_jobs(bot)
    
    print("[STARTUP] All jobs scheduled successfully")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())