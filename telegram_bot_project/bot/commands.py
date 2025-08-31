# bot/commands.py
from aiogram import types
from aiogram.fsm.context import FSMContext
from datetime import datetime
from aiogram.types import FSInputFile
from zoneinfo import ZoneInfo
import asyncio

from service.focus import FocusService
from bot.utills import format_date, calculate_awake_hours
from service.idea import IdeaService
from service.task import TaskService
from bot.buttons import *
from states import DialogStates, AI_CHAT_CONTEXT, TYPING_TASKS
from messages import MESSAGES
from service.myday import MyDayService
from service.reminder import ReminderService

from aiogram import types
from aiogram.types import FSInputFile
from service.user import UserService
from service.routine import RoutineService
from messages import MESSAGES
from bot.utills import typing_animation

TYPING_ANIMATION_DURATION: int = 2

# Start Command Handler
async def start_command(message: types.Message):
    user_id: int = message.from_user.id
    user_name: str = message.from_user.username or "unknown"
    first_name: str = message.from_user.first_name
    second_name: str = message.from_user.last_name

    photo = FSInputFile(path="logo.jpg")
    print(f"[INFO] - User {user_id} ({user_name}) - started the bot")

    user_find = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if user_find:
        await typing_animation(message, TYPING_ANIMATION_DURATION)
        await message.answer(MESSAGES[language]["START_MSG_AGAIN"])
        await message.answer(MESSAGES[language]["MENU_MSG"], reply_markup=menu_reply_keyboard())
    else:
        await UserService.create_user(
            user_id=user_id, 
            user_name=user_name,
            first_name=first_name,
            second_name=second_name)

        await message.answer_photo(
            photo=photo,
            caption=MESSAGES['ENGLISH']['START_MSG']
        )

        await ask_user_timezone_location(message)

# Help Command Handler
async def help_command(message: types.Message):
    user_id: int = message.from_user.id
    user_name: str = message.from_user.username or "unknown"

    language: str = await UserService.get_user_language(user_id)
    print(f"[INFO] - User {user_id} ({user_name}) - asked for help")
    await typing_animation(message, TYPING_ANIMATION_DURATION)
    await message.answer(MESSAGES[language]["HELP_MSG"])

# Language Command Handler
async def language_command(message: types.Message):
    user_id: int = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)
    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        keyboard = get_language_keyboard()
        await message.answer(MESSAGES[language]['LANGUAGE_ASK'], reply_markup=keyboard)

# Menu Command Handler
async def menu_command(message: types.Message):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)
    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        await message.answer(MESSAGES[language]['MENU_MSG'], reply_markup=menu_reply_keyboard())

# Idea Command Handler
async def idea_command(message: types.Message, state: FSMContext):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    print(f"[INFO] - User with id: {user_id} - opened /idea.")
    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        await state.set_state(DialogStates.waiting_for_idea)
        await message.answer(
            MESSAGES[language]['IDEA_RESPONSE'],
            reply_markup=break_button()                
        )

# Show Ideas Handler
async def ideas_command(message: types.Message):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        ideas: List[str] = await IdeaService.get_all_ideas_by_user_id(user_id)
        if not ideas:
            print(f"[INFO] - User with id: {user_id} - has no ideas.")
            await message.answer(MESSAGES[language]['NO_IDEAS'])
        else:
            print(f"[INFO] - User with id: {user_id} - has ideas: {ideas}")

            dividers: str = "\n" + ("-" * int(len(MESSAGES[language]['IDEAS_SHOW']) * 1.65))

            formatted_ideas = MESSAGES[language]['IDEAS_SHOW'] + dividers + "\n" + "\n".join(
                f"{num}) {idea['idea_name']}\n\n  - 📅 - [{format_date(idea['creation_date'])}]\n"
                for num, idea in enumerate(ideas, start=1)
            )

            await typing_animation(message, TYPING_ANIMATION_DURATION)
            await message.answer(formatted_ideas, reply_markup=idea_reply_keyboard())

# Delete Idea Handler
async def delete_idea_command(message: types.Message, state: FSMContext):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        await state.set_state(DialogStates.delete_idea)
        await message.answer(
            MESSAGES[language]['DELETE_IDEA'],
            reply_markup=break_button()
        )

# Update Idea Handler
async def update_idea_command(message: types.Message, state: FSMContext):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        await state.set_state(DialogStates.update_idea)
        await message.answer(
            MESSAGES[language]['UPDATE_IDEA'],
            reply_markup=break_button()
        )

# Create Task Handler
async def task_command(message: types.Message, state: FSMContext):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        print(f"[INFO] - User with id: {user_id} - opened /task.")

        await state.set_state(DialogStates.confirm_task)
        await message.answer(
            MESSAGES[language]['TASK_ADD'],
            reply_markup=break_button()
        )

# Open task menu handler
async def task_menu_command(message: types.Message):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        await message.answer(MESSAGES[language]['TASK_MENU'], reply_markup=task_menu_keyboard())

#Show all tasks handler
async def tasks_show_command(message: types.Message):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
        return

    tasks = await TaskService.get_user_tasks(user_id)
    if not tasks:
        await message.answer(MESSAGES[language]['NO_TASKS'], reply_markup=task_menu_keyboard())
        return

    USER_TZ = ZoneInfo(await UserService.get_user_timezone(user_id))
    response_text = f"📋 *{MESSAGES[language]['YOUR_TASKS']}*:\n\n"
    for i, task in enumerate(tasks, 1):
        status_icon = "✅" if task['status'] else "❌"
        start_time = task['start_time'].astimezone(USER_TZ).strftime("%Y-%m-%d %H:%M") if task['start_time'] else "—"
        response_text += (
            f"{i}) {task['task_name']} - {status_icon}\n"
            f"🕒 *Start:* {start_time}\n"
            f"📅 *Created:* {task['creation_date'].strftime('%Y-%m-%d')}\n\n"
        )

    await typing_animation(message, TYPING_ANIMATION_DURATION)
    await message.answer(response_text, parse_mode="Markdown", reply_markup=task_menu_keyboard())

#Delete Task Command
async def delete_task_command(message: types.Message, state: FSMContext):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        tasks = await TaskService.get_user_tasks(user_id)
        if not tasks:
            await message.answer(MESSAGES[language]['NO_TASKS'], reply_markup=task_menu_keyboard())
            return
        await state.set_state(DialogStates.delete_task)
        await state.update_data(tasks=tasks)
        await message.answer(
            MESSAGES[language]['TASK_DELETE_MSG'],
            reply_markup=break_button()
        )

#Complete Task Command
async def complete_task_command(message: types.Message, state: FSMContext):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        tasks = await TaskService.get_user_tasks(user_id)
        if not tasks:
            await message.answer(MESSAGES[language]['NO_TASKS'], reply_markup=task_menu_keyboard())
            return

        await state.set_state(DialogStates.complete_task)
        await state.update_data(tasks=tasks)
        await message.answer(
            MESSAGES[language]['COMPLETE_TASK_MSG'],
            reply_markup=break_button()
        )

#Update Task Command
async def update_task_command(message: types.Message, state: FSMContext):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        tasks = await TaskService.get_user_tasks(user_id)
        if not tasks:
            await message.answer(MESSAGES[language]['NO_TASKS'], reply_markup=task_menu_keyboard())
            return

        await state.set_state(DialogStates.update_task_id)
        await state.update_data(tasks=tasks)
        await message.answer(
            MESSAGES[language]['UPDATE_TASK_MSG'],
            reply_markup=break_button()
        )

#Setting Menu Open Command
async def setting_menu_command(message: types.Message):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        await message.answer(MESSAGES[language]['SETTINGS_MENU'], reply_markup=settings_menu_keyboard())

# Routine Time Command Handler
async def routine_time_command(message: types.Message):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
        return

    wake_time, sleep_time = await UserService.get_wake_and_sleep_times(user_id)

    if not wake_time and not sleep_time:
        await message.answer(
            MESSAGES[language]['ROUTINE_TIME_NOT'],
            reply_markup=routine_time_keyboard()
        )
        return

    wake_display = wake_time.strftime("%H:%M") if wake_time else "—"
    sleep_display = sleep_time.strftime("%H:%M") if sleep_time else "—"

    awake_time = calculate_awake_hours(wake_time, sleep_time) if (wake_time and sleep_time) else "unknown"
    msg_text = MESSAGES[language]['ROUTINE_TIME'].format(
        wake=wake_display,
        sleep=sleep_display,
        duration=awake_time
    )

    await message.answer(msg_text, reply_markup=routine_time_keyboard())

#Set Wake Time Command Handler
async def set_wake_time_command(message: types.Message, state: FSMContext):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        await state.set_state(DialogStates.set_wake_time)
        await message.answer(
            MESSAGES[language]['SET_TIME_MSG'],
            reply_markup=break_button()
        )

# Set Sleep Time Command Handler
async def set_sleep_time_command(message: types.Message, state: FSMContext):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        await state.set_state(DialogStates.set_sleep_time)
        await message.answer(
            MESSAGES[language]['SET_TIME_MSG'],
            reply_markup=break_button()
        )

# Routine Menu Command Handler
async def routine_menu_command(message: types.Message):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        await message.answer(MESSAGES[language]['ROUTINE_MENU_DAY'], reply_markup=routine_menu_keyboard())

# Set Morning Routine Command Handler
async def set_morning_routine(message: types.Message, state: FSMContext):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        await state.set_state(DialogStates.add_morning_routine)
        await message.answer(
            MESSAGES[language]['ADD_MORNING_ROUTINE'],
            reply_markup=break_button()
        )

async def show_morning_routines(message: types.Message):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
        return

    print(f"[INFO] - User with id: {user_id} - opened /morning_routines.")
    morning_routine = await RoutineService.get_user_routines(user_id, routine_type="morning")
    morning_routine = list(reversed(morning_routine))
    if not morning_routine:
        await message.answer(MESSAGES[language]['NO_MORNING_ROUTINE'])
        return

    dividers: str = "\n" + ("-" * int(len(MESSAGES[language]['MORNING_ROUTINE_SHOW']) * 1.65))

    formatted_routine_items = "\n".join(
        f"{idx}) {routine['routine_name']}"
        for idx, routine in enumerate(morning_routine, start=1)
    )

    formatted_morning_routine = (
        MESSAGES[language]['MORNING_ROUTINE_SHOW'] +
        dividers +
        "\n" +
        formatted_routine_items
    )

    await typing_animation(message, TYPING_ANIMATION_DURATION)
    await message.answer(formatted_morning_routine, reply_markup=morning_routine_keyboard())

# Delete Morning Routine Command Handler
async def delete_morning_routine(message: types.Message, state: FSMContext, type: str):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:

        morning_routine = await RoutineService.get_user_routines(user_id, routine_type=type)
        morning_routine = list(reversed(morning_routine))
        if not morning_routine:
            await message.answer(MESSAGES[language]['NO_MORNING_ROUTINE'])
            return
        await state.update_data(morning_routine=morning_routine)
        await state.set_state(DialogStates.delete_morning_routine)
        await message.answer(
            MESSAGES[language]['PROVIDE_ROUTINE_ID'],
            reply_markup=break_button()
        )

# Update Morning Routine Command Handler
async def update_morning_routine(message: types.Message, state: FSMContext, type: str):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        morning_routine = await RoutineService.get_user_routines(user_id, routine_type=type)
        morning_routine = list(reversed(morning_routine))
        if not morning_routine:
            await message.answer(MESSAGES[language]['NO_MORNING_ROUTINE'])
            return
        else:
            await state.update_data(morning_routine=morning_routine)
            await state.set_state(DialogStates.update_morning_routine_id)
            await message.answer(
                MESSAGES[language]['PROVIDE_ROUTINE_ID'],
                reply_markup=break_button()
            )

# Show Evening Routine Command Handler
async def show_evening_routines(message: types.Message):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
        return

    print(f"[INFO] - User with id: {user_id} - opened /morning_routines.")
    morning_routine = await RoutineService.get_user_routines(user_id, routine_type="evening")
    morning_routine = list(reversed(morning_routine))
    if not morning_routine:
        await message.answer(MESSAGES[language]['NO_MORNING_ROUTINE'])
        return

    morning_routine = list(reversed(morning_routine))
    dividers: str = "\n" + ("-" * int(len(MESSAGES[language]['MORNING_ROUTINE_SHOW']) * 1.65))

    formatted_routine_items = "\n".join(
        f"{idx}) {routine['routine_name']}"
        for idx, routine in enumerate(morning_routine, start=1)
    )

    formatted_morning_routine = (
        MESSAGES[language]['MORNING_ROUTINE_SHOW'] +
        dividers +
        "\n" +
        formatted_routine_items
    )

    await typing_animation(message, TYPING_ANIMATION_DURATION)    
    await message.answer(formatted_morning_routine, reply_markup=evening_routine_keyboard())

# Send feedback message command
async def send_feedback_command(message: types.Message, state: FSMContext):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        await state.set_state(DialogStates.feedback_message)
        await message.answer(
            MESSAGES[language]['SMTP_MESSAGE_TEXT'],
            reply_markup=break_button()
        )

# Show daily stats command
async def show_daily_stats_command(message: types.Message):
    user_id: int = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
        return

    stats = await MyDayService.get_today_stats(user_id)

    if not stats:
        created_ideas, completed_tasks, created_tasks, wake_up_time = 0, 0, 0, None
    else:
        created_ideas = stats["created_ideas"]
        completed_tasks = stats["completed_tasks"]
        created_tasks = stats["created_tasks"]
        wake_up_time = stats["wake_up_time"]

        if wake_up_time:
            wake_up_time = wake_up_time.strftime("%H:%M")

    text = generate_daily_stats_message(
        language, created_ideas, completed_tasks, created_tasks, wake_up_time
    )

    await typing_animation(message, TYPING_ANIMATION_DURATION)
    await message.answer(text, parse_mode="Markdown", reply_markup=menu_reply_keyboard())

# Focus Zone Menu Handler
async def show_focus_menu(message: types.Message) -> None:
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        print(f"[INFO] - User with id: {user_id} - opened /focus.")
        await message.answer(MESSAGES[language]['WELCOME_TO_FOCUS'], reply_markup=focus_menu_keyboard())

# Show All Focus Sessions Handler
async def show_all_focuses(message: types.Message) -> None:
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES[language]['AUTHORIZATION_PROBLEM'])
        return

    print(f"[INFO] - User with id: {user_id} - opened /show_all_focuses.")
    focuses = await FocusService.get_focuses_by_user(user_id)

    if not focuses:
        await message.answer(MESSAGES[language]['NO_FOCUS_SESSIONS'])
        return

    dividers: str = "\n" + ("-" * int(len(MESSAGES[language]['FOCUS_LIST_TITLE']) * 1.65))
    formatted_focuses = "\n".join(
        f"{idx}) {focus['title']} ({focus['duration']}) – {focus['created_at'].strftime('%Y-%m-%d %H:%M')}"
        for idx, focus in enumerate(focuses, start=1)
    )

    formatted_response = (
        MESSAGES[language]['FOCUS_LIST_TITLE'] +
        dividers +
        "\n" +
        formatted_focuses
    )

    await typing_animation(message, TYPING_ANIMATION_DURATION)
    await message.answer(formatted_response, reply_markup=focus_menu_keyboard())

# Delete Focus Session Handler
async def delete_focus_session(message: types.Message, state: FSMContext) -> None:
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        focuses = await FocusService.get_focuses_by_user(user_id)
        if not focuses:
            await message.answer(MESSAGES[language]['NO_FOCUS_SESSIONS'])
            return

        await state.update_data(focuses=focuses)
        await state.set_state(DialogStates.delete_focus)
        await message.answer(
            MESSAGES[language]['DELETE_FOCUS_SESSION_MSG'],
            reply_markup=break_button()
        )

async def start_day_command(message: types.Message) -> None:
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id) or 'ENGLISH'

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
        return

    morning_routine = await RoutineService.get_user_routines(user_id, routine_type="morning")
    morning_routine = list(reversed(morning_routine))
    print(f"[INFO] - Sending morning routine to user with id {user_id}")

    time_str = datetime.now().strftime("%H:%M")  
    await MyDayService.add_wake_up_time(user_id, time_str)

    if morning_routine:
        formatted_routine_items = "\n".join(
            f"✦ {idx}. {routine['routine_name']}" 
            for idx, routine in enumerate(morning_routine, start=1)
        )
    else:
        formatted_routine_items = MESSAGES[language]['NO_MORNING_ROUTINE']

    await message.answer(
        f"{MESSAGES[language]['SEND_MORNING_MSG']}\n{formatted_routine_items}",
        reply_markup=get_morning_timer_menu()
    )

# Talk with Rocky Command
async def talk_with_rocky_command(message: types.Message, state: FSMContext) -> None:
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id) or 'ENGLISH'
    
    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
        return
   
    user_name: str = user_find.get("user_name", "unknown")
    print(f"[INFO] - User with id: {user_id} opened ai chat")
    
    await state.set_state(DialogStates.ai_talk)
    
    await message.answer(
        MESSAGES[language]['AI_ROCKY_TALK_MSG'].format(user_name),
        reply_markup=get_stop_chat_btn()
    )

async def stop_talk_command(message: types.Message, state: FSMContext) -> None:
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id) or 'ENGLISH'
    
    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
        return
   
    user_name: str = user_find.get("user_name", message.from_user.username or "unknown")
    print(f"[INFO] - User with id: {user_id} stop ai chat")
    
    if user_id in TYPING_TASKS:
        task, stop_event = TYPING_TASKS[user_id]
        stop_event.set()
        try:
            await task
        except asyncio.CancelledError:
            pass
        TYPING_TASKS.pop(user_id, None)
        print(f"[INFO] - Stopped typing animation for user {user_id}")
    
    if user_id in AI_CHAT_CONTEXT:
        AI_CHAT_CONTEXT.pop(user_id)
        print(f"[INFO] - Cleared AI chat context for user {user_id}")
    
    await state.clear()
    
    await message.answer(
        MESSAGES[language]['AI_ROCKY_TALK_END_MSG'].format(user_name),
        reply_markup=menu_reply_keyboard()
    )


# Timezone Command Handler
async def timezone_command(message: types.Message) -> None:
    user_id = message.from_user.id
    user_timezone = await UserService.get_user_timezone(user_id)
    language = await UserService.get_user_language(user_id)

    await message.answer(
        text=MESSAGES[language]['CURRENT_TIMEZONE'].format(user_timezone),
        reply_markup=timezone_menu_keyboard()
    )

# Change Timezon Handler
async def change_timezone_command(message: types.Message) -> None:
    user_id = message.from_user.id
    language = await UserService.get_user_language(user_id)

    await message.answer(
        text=MESSAGES[language]['TIMEZONE_BTN_MSG'],
        reply_markup=timezone_btn(message)
    )

# Remind Menu Command Handler 
async def reminders_menu_command(message: types.Message) -> None:
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id) or 'ENGLISH'

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
        return
    
    await message.answer(
        MESSAGES[language]['REMINDERS_MENU'],
        reply_markup=get_reminder_menu_btn()
    )

# Create Reminder Command
async def create_reminder_command(message: types.Message, state: FSMContext) -> None:
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id) or 'ENGLISH'

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
        return
    
    await message.answer(
        MESSAGES[language]['REMINDER_CREATE_MSG'],
        reply_markup=break_button()
    )
    await state.set_state(DialogStates.provide_remind_name)

# Show All Reminders Handler
async def show_reminders_command(message: types.Message) -> None:
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES[language]['AUTHORIZATION_PROBLEM'])
        return

    print(f"[INFO] - User with id: {user_id} - opened /show_reminders.")
    reminders = await ReminderService.get_user_reminders(user_id)

    if not reminders:
        await message.answer(MESSAGES[language]['NO_REMINDS_FOUND'])
        return

    USER_TZ = ZoneInfo(await UserService.get_user_timezone(user_id))

    dividers: str = "\n" + ("-" * int(len(MESSAGES[language]['REMINDER_LIST_MSG']) * 1.65))
    formatted_reminders = "\n".join(
        f"• {rem['title']} – "
        f"{rem['remind_time'].astimezone(USER_TZ).strftime('%Y-%m-%d %H:%M')} "
        f"({'✅' if rem['remind_status'] else '❌'})"
        for idx, rem in enumerate(reminders, start=1)
    )

    formatted_response = (
        MESSAGES[language]['REMINDER_LIST_MSG'] +
        dividers +
        "\n" +
        formatted_reminders
    )

    await typing_animation(message, TYPING_ANIMATION_DURATION)
    await message.answer(formatted_response, reply_markup=get_reminder_menu_btn())

# Drop Reminder Handler
async def delete_reminder_handler(message: types.Message, state: FSMContext) -> None:
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES[language]['AUTHORIZATION_PROBLEM'])
        return

    await message.answer(
        MESSAGES[language]['DELETE_REMINDER'],
        reply_markup=break_button()
    )
    await state.set_state(DialogStates.provide_reminder_index)

# Break Operation Command Handler
async def break_operation_command(message: types.Message, state: FSMContext) -> None:
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES[language]['AUTHORIZATION_PROBLEM'])
        return
    
    await message.answer(
        MESSAGES[language]['BREAK_OPERATION_MSG'],
        reply_markup=menu_reply_keyboard()
    )
    await state.clear()