import asyncio
from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from config import TOKEN
from bot.commands import start_command, help_command, menu_command, language_command, idea_command
from bot.handlers import process_idea_save
from bot.callbacks import start_callback_language, callback_idea_process
from states import DialogStates

storage: MemoryStorage = MemoryStorage()
dp = Dispatcher(storage=storage)

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

@dp.message(Command("idea"))
async def idea(message: Message, state: FSMContext):
    await idea_command(message, state)

@dp.callback_query(F.data.in_({"lang_ua", "lang_en"}))
async def callback_language(callback_query: CallbackQuery):
    await start_callback_language(callback_query)

@dp.callback_query(F.data.in_({"delete_idea", "save_idea"}))
async def callback_idea(callback_query: CallbackQuery, state: FSMContext):
    await callback_idea_process(callback_query, state)

@dp.message()
async def process_idea_fallback(message: Message, state: FSMContext):
    current_state = await state.get_state()
    print(f"[DEBUG] Current state: {current_state}")
    if current_state == DialogStates.waiting_for_idea.state:
        await process_idea_save(message, state)

# Main Function
async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

# Start point
if __name__ == "__main__":
    print("-- STARTING ROCKY --\n")
    asyncio.run(main())