from typing import Any, List
from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.utills import format_date
from messages import MESSAGES
from service.idea import IdeaService
from service.user import UserService
from bot.buttons import get_language_keyboard, menu_reply_keyboard, idea_reply_keyboard
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
