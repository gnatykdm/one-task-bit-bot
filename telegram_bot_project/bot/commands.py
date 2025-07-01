from typing import Any
from aiogram.types import Message

from messages import *
from service.user import UserService

# Start Command Handler
async def start_command(message: Message)-> None:

    user_id: int = message.from_user.id
    user_name: str = message.from_user.username

    print(f"--[INFO] - User {user_id} ({user_name}) - started the bot")
    user_find: int = await UserService.get_user_by_id(user_id)
    if user_find:
        await message.answer(START_MSG_AGAIN)
    else:
        await UserService.create_user(user_id, user_name)
        await message.answer(START_MSG)

# Help Command Handler
async def help_command(message: Message) -> None:

    user_id: int = message.from_user.id
    user_name: str = message.from_user.username

    print(f"--[INFO] - User {user_id} ({user_name}) - asked for help")

    await message.answer(HELP_MSG)

# Menu Command Handler
async def menu_command(message: Message) -> None:

    user_id: int = message.from_user.id
    user_name: str = message.from_user.username

    print(f"--[INFO] - User {user_id} ({user_name}) - asked for menu")

    await message.answer(MENU_MSG)