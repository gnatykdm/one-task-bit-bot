from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.buttons import menu_reply_keyboard
from messages import MESSAGES
from service.idea import IdeaService
from service.user import UserService

async def process_idea_save(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.username or "unknown"

    user_find = await UserService.get_user_by_id(user_id)
    if not user_find or not user_find.get("id"):
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    language = await UserService.get_user_language(user_id)
    idea = message.text

    print(f"--[INFO] User with id: {user_id} - provide idea.")
    try:
        await IdeaService.create_user_idea(user_id, idea)
        print(f"--[INFO] - User {user_id} ({user_name}) saved idea: {idea}")
        await message.answer(MESSAGES[language]['IDEA_SAVED'], reply_markup=menu_reply_keyboard())
        await state.clear()
    except Exception as e:
        print(f"[ERROR] Saving idea failed: {e}")
        await message.answer(MESSAGES[language].get('ERROR_SAVING_IDEA', 'Ошибка при сохранении идеи. Попробуйте позже.'))
