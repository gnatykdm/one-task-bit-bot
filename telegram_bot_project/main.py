import asyncio

from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message

from config import TOKEN
from bot.commands import *

dp: Dispatcher = Dispatcher()

# Commands Handlers
@dp.message(Command("start"))
async def start(message: Message):
    await start_command(message)

@dp.message(Command("help"))
async def help(message: Message):
    await help_command(message)

@dp.message(Command("menu"))
async def menu(message: Message):
    await menu_command(message)

# Main Function
async def main():
    bot: Bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

# Start point
if __name__ == "__main__":
    print("-- STARTING ROCKY --\n")
    asyncio.run(main())