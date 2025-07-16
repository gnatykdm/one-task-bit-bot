import asyncio
from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery
from config import TOKEN
from bot.commands import *
from bot.handlers import *
from bot.callbacks import start_callback_language, callback_idea_process, callback_task_deadline
from messages import *
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
@dp.message(lambda m: m.text == MENU_BUTTON)
async def menu(message: Message):
    await menu_command(message)

@dp.message(Command("language"))
async def language(message: Message):
    await language_command(message)

@dp.message(Command("idea"))
@dp.message(lambda m: m.text == BUTTON_IDEA)
async def idea(message: Message, state: FSMContext):
    await idea_command(message, state)

@dp.message(Command("ideas"))
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
async def task(message: Message, state: FSMContext):
    await task_command(message, state)

@dp.message(lambda m: m.text == BUTTON_ADD_TASK)
async def add_task(message: Message, state: FSMContext):
    await task_command(message, state)

@dp.callback_query(F.data.in_({"lang_ua", "lang_en"}))
async def callback_language(callback_query: CallbackQuery):
    await start_callback_language(callback_query)

@dp.callback_query(F.data.in_({"delete_idea", "save_idea"}))
async def callback_idea(callback_query: CallbackQuery, state: FSMContext):
    await callback_idea_process(callback_query, state)

@dp.callback_query(F.data.in_({"yes_task", "no_task"}))
async def callback_idea(callback_query: CallbackQuery, state: FSMContext):
    await callback_task_deadline(callback_query, state)

@dp.message()
async def process_fallback(message: Message, state: FSMContext):
    current_state = await state.get_state()
    print(f"[DEBUG] Current state: {current_state}")
    if current_state == DialogStates.waiting_for_idea.state:
        await process_idea_save(message, state)
    elif current_state == DialogStates.delete_idea.state:
        await process_idea_delete(message, state)
    elif current_state == DialogStates.update_idea.state:
        await process_idea_update(message, state)
    elif current_state == DialogStates.waiting_for_update_text:
        await process_save_updated_idea_text(message, state)
    elif current_state == DialogStates.confirm_task:
        await process_task_save(message, state)
    elif current_state == DialogStates.task_deadline:
        await process_task_deadline(message, state)

# Main Function
async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

# Start point
if __name__ == "__main__":
    print("-- STARTING ROCKY --\n")
    asyncio.run(main())