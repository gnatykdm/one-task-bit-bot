# bot/commands.py
from typing import List
from aiogram.fsm.context import FSMContext

from bot.utills import format_date, calculate_awake_hours
from service.idea import IdeaService
from service.task import TaskService
from bot.buttons import *
from states import DialogStates
from service.myday import MyDayService

# Start Command Handler
async def start_command(message: types.Message):
    user_id: int = message.from_user.id
    user_name: str = message.from_user.username or "unknown"

    print(f"[INFO] - User {user_id} ({user_name}) - started the bot")
    user_find = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)
    if user_find:
        await message.answer(MESSAGES[language]["START_MSG"])
        await message.answer(MESSAGES[language]["MENU_MSG"], reply_markup=menu_reply_keyboard())
    else:
        await UserService.create_user(user_id, user_name)
        await message.answer(MESSAGES['ENGLISH']['START_MSG'])
        keyboard = get_language_keyboard()
        await message.answer(MESSAGES['ENGLISH']['LANGUAGE_ASK'], reply_markup=keyboard)

# Help Command Handler
async def help_command(message: types.Message):
    user_id: int = message.from_user.id
    user_name: str = message.from_user.username or "unknown"

    language: str = await UserService.get_user_language(user_id)
    print(f"[INFO] - User {user_id} ({user_name}) - asked for help")
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
        await message.answer(MESSAGES[language]['IDEA_RESPONSE'])
        await state.set_state(DialogStates.waiting_for_idea)

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
                f"# {num}. {idea['idea_name']}\n\n  - 📅 - [{format_date(idea['creation_date'])}]\n"
                for num, idea in enumerate(ideas, start=1)
            )

            await message.answer(formatted_ideas, reply_markup=idea_reply_keyboard())

# Delete Idea Handler
async def delete_idea_command(message: types.Message, state: FSMContext):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        await message.answer(MESSAGES[language]['DELETE_IDEA'])
        await state.set_state(DialogStates.delete_idea)

# Update Idea Handler
async def update_idea_command(message: types.Message, state: FSMContext):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        await message.answer(MESSAGES[language]['UPDATE_IDEA'])
        await state.set_state(DialogStates.update_idea)

# Create Task Handler
async def task_command(message: types.Message, state: FSMContext):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        print(f"[INFO] - User with id: {user_id} - opened /task.")

        await message.answer(MESSAGES[language]['TASK_ADD'])
        await state.set_state(DialogStates.confirm_task)

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

    response_text = f"📋 *{MESSAGES[language]['YOUR_TASKS']}*:\n\n"
    for i, task in enumerate(tasks, 1):
        status_icon = "✅" if task['status'] else "❌"
        start_time = task['start_time'].strftime("%Y-%m-%d %H:%M") if task['start_time'] else "—"
        response_text += (
            f"*{i}. {task['task_name']}* {status_icon}\n"
            f"🕒 *Start:* {start_time}\n"
            f"📅 *Created:* {task['creation_date'].strftime('%Y-%m-%d')}\n\n"
        )

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

        await message.answer(MESSAGES[language]['TASK_DELETE_MSG'])
        await state.set_state(DialogStates.delete_task)
        await state.update_data(tasks=tasks)

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

        await message.answer(MESSAGES[language]['COMPLETE_TASK_MSG'])
        await state.set_state(DialogStates.complete_task)
        await state.update_data(tasks=tasks)

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

        await message.answer(MESSAGES[language]['UPDATE_TASK_MSG'])
        await state.set_state(DialogStates.update_task_id)
        await state.update_data(tasks=tasks)

#Setting Menu Open Command
async def setting_menu_command(message: types.Message):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        await message.answer(MESSAGES[language]['SETTINGS_MENU'], reply_markup=settings_menu_keyboard())

#Routine Time Command Handler
async def routine_time_command(message: types.Message):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        wake_time, sleep_time = await UserService.get_wake_and_sleep_times(user_id)
        if not wake_time and not sleep_time:
            await message.answer(MESSAGES[language]['ROUTINE_TIME_NOT'], reply_markup=routine_time_keyboard())
            return
        wake_time = None if not wake_time else wake_time.strftime("%H:%M")
        sleep_time = None if not sleep_time else sleep_time.strftime("%H:%M")
        awake_time = calculate_awake_hours(wake_time, sleep_time)
        await message.answer(MESSAGES[language]['ROUTINE_TIME'].format(wake_time, sleep_time, awake_time), reply_markup=routine_time_keyboard())

#Set Wake Time Command Handler
async def set_wake_time_command(message: types.Message, state: FSMContext):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        await message.answer(MESSAGES[language]['SET_TIME_MSG'])
        await state.set_state(DialogStates.set_wake_time)


# Set Sleep Time Command Handler
async def set_sleep_time_command(message: types.Message, state: FSMContext):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        await message.answer(MESSAGES[language]['SET_TIME_MSG'])
        await state.set_state(DialogStates.set_sleep_time)


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
        await message.answer(MESSAGES[language]['ADD_MORNING_ROUTINE'])
        await state.set_state(DialogStates.add_morning_routine)

async def show_morning_routines(message: types.Message):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
        return

    print(f"[INFO] - User with id: {user_id} - opened /morning_routines.")
    morning_routine = await RoutineService.get_user_routines(user_id, routine_type="morning")
    if not morning_routine:
        await message.answer(MESSAGES[language]['NO_MORNING_ROUTINE'])
        return

    dividers: str = "\n" + ("-" * int(len(MESSAGES[language]['MORNING_ROUTINE_SHOW']) * 1.65))

    formatted_routine_items = "\n".join(
        f"# {idx}. {routine['routine_name']}"
        for idx, routine in enumerate(morning_routine, start=1)
    )

    formatted_morning_routine = (
        MESSAGES[language]['MORNING_ROUTINE_SHOW'] +
        dividers +
        "\n" +
        formatted_routine_items
    )

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
        if not morning_routine:
            await message.answer(MESSAGES[language]['NO_MORNING_ROUTINE'])
            return

        await message.answer(MESSAGES[language]['PROVIDE_ROUTINE_ID'])
        await state.update_data(morning_routine=morning_routine)
        await state.set_state(DialogStates.delete_morning_routine)

# Update Morning Routine Command Handler
async def update_morning_routine(message: types.Message, state: FSMContext, type: str):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        morning_routine = await RoutineService.get_user_routines(user_id, routine_type=type)
        if not morning_routine:
            await message.answer(MESSAGES[language]['NO_MORNING_ROUTINE'])
            return
        else:
            await message.answer(MESSAGES[language]['PROVIDE_ROUTINE_ID'])
            await state.update_data(morning_routine=morning_routine)
            await state.set_state(DialogStates.update_morning_routine_id)

# Show Evening Routine Command Handler
async def show_evening_routines(message: types.Message):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
        return

    print(f"[INFO] - User with id: {user_id} - opened /evening_routines.")
    evening_routine = await RoutineService.get_user_routines(user_id, routine_type="evening")
    if not evening_routine:
        await message.answer(MESSAGES[language]['NO_MORNING_ROUTINE'])
        return

    dividers: str = "\n" + ("-" * int(len(MESSAGES[language]['EVENING_ROUTINE_SHOW']) * 1.65))
    formatted_routine_items = "\n".join(
        f"# {idx}. {routine['routine_name']}"
        for idx, routine in enumerate(evening_routine, start=1)
    )

    formatted_morning_routine = (
            MESSAGES[language]['EVENING_ROUTINE_SHOW'] +
            dividers +
            "\n" +
            formatted_routine_items
    )

    await message.answer(formatted_morning_routine, reply_markup=evening_routine_keyboard())

# Send feedback message command
async def send_feedback_command(message: types.Message, state: FSMContext):
    user_id: int = message.from_user.id
    user_find: Any = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)

    if not user_find:
        await message.answer(MESSAGES['ENGLISH']['AUTHORIZATION_PROBLEM'])
    else:
        await message.answer(MESSAGES[language]['SMTP_MESSAGE_TEXT'])
        await state.set_state(DialogStates.feedback_message)

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
        created_ideas = 0
        completed_tasks = 0
        created_tasks = 0
    else:
        created_ideas = stats.get("created_ideas", 0)
        completed_tasks = stats.get("completed_tasks", 0)
        created_tasks = stats.get("created_tasks", 0)

    text = generate_daily_stats_message(language, created_ideas, completed_tasks, created_tasks)
    await message.answer(text, parse_mode="Markdown", reply_markup=menu_reply_keyboard())