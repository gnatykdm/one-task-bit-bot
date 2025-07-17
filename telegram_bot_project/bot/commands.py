from typing import Any, List
from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.utills import format_date
from messages import MESSAGES
from service.idea import IdeaService
from service.task import TaskService
from service.user import UserService
from bot.buttons import get_language_keyboard, menu_reply_keyboard, idea_reply_keyboard, task_menu_keyboard
from states import DialogStates

# Start Command Handler
async def start_command(message: types.Message):
    user_id: int = message.from_user.id
    user_name: str = message.from_user.username or "unknown"

    print(f"--[INFO] - User {user_id} ({user_name}) - started the bot")
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
    print(f"--[INFO] - User {user_id} ({user_name}) - asked for help")
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

    print(f"--[INFO] - User with id: {user_id} - opened /idea.")
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
            print(f"--[INFO] - User with id: {user_id} - has no ideas.")
            await message.answer(MESSAGES[language]['NO_IDEAS'])
        else:
            print(f"--[INFO] - User with id: {user_id} - has ideas: {ideas}")

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
        print(f"--[INFO] - User with id: {user_id} - opened /task.")

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