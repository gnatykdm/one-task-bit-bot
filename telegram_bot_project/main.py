import asyncio
from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from config import TOKEN
from bot.commands import start_command, help_command, menu_command, language_command
from bot.callbacks import start_callback_language

dp = Dispatcher(storage=MemoryStorage())

# Command Handlers
@dp.message(Command("start"))
async def start(message: Message):
    await start_command(message)

@dp.message(Command("help"))
async def help(message: Message):
    await help_command(message)

@dp.message(Command("menu"))
async def menu(message: Message):
    await menu_command(message)

@dp.message(Command("language"))
async def language(message: Message):
    await language_command(message)

@dp.callback_query(lambda c: c.data in ["lang_ua", "lang_en"])
async def callback_language(callback_query: CallbackQuery):
    await start_callback_language(callback_query)

# Main Function
async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

# Start point
if __name__ == "__main__":
    print("-- STARTING ROCKY --\n")
    asyncio.run(main())