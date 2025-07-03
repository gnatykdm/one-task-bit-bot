from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup

from bot.buttons import get_idea_conf_keyboard
from messages import MESSAGES
from service.user import UserService

async def process_idea_save(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    if not user_find or not user_find.get("id"):
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    language = await UserService.get_user_language(user_id)
    idea = message.text

    print(f"--[INFO] User with id: {user_id} - provide idea.")
    try:
        await state.update_data(idea=idea)

        dividers: str = "\n" + ("-" * int(len(MESSAGES[language]['IDEA_ACTION']) * 1.65))
        keyboard: InlineKeyboardMarkup = get_idea_conf_keyboard()
        await message.answer(MESSAGES[language]['IDEA_ACTION'] + dividers + f"\nIDEA: {idea}", reply_markup=keyboard)
    except Exception as e:
        print(f"[ERROR] Saving idea failed: {e}")
        await message.answer(MESSAGES[language].get('ERROR_SAVING_IDEA', 'Ошибка при сохранении идеи. Попробуйте позже.'))
