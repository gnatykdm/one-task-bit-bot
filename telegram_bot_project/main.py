import asyncio

from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message

from config import TOKEN
from bot.commands import start_command

dp: Dispatcher = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await start_command(message)


async def main():
    bot: Bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())