from typing import Optional
from aiogram import types

from bot.buttons import menu_reply_keyboard
from messages import MESSAGES
from service.user import UserService

async def start_callback_language(callback_query: types.CallbackQuery) -> None:
    await callback_query.answer()

    user_id: int = callback_query.from_user.id
    user_name: str = callback_query.from_user.username or "unknown"
    user_find: Optional[dict] = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)
    if not language:
        language = 'ENGLISH'

    if not user_find:
        await callback_query.message.answer(MESSAGES['ENGLISH']["AUTHORIZATION_PROBLEM"])
        return

    match callback_query.data:
        case "lang_ua":
            print(f"--[INFO] - User {user_id} ({user_name}) set language to ua.")
            await UserService.update_user_language(user_id, 'UKRANIAN')
            await callback_query.message.answer(MESSAGES['UKRANIAN']["LANGUAGE_OK"], reply_markup=menu_reply_keyboard())
        case "lang_en":
            print(f"--[INFO] - User {user_id} ({user_name}) set language to en.")
            await UserService.update_user_language(user_id, 'ENGLISH')
            await callback_query.message.answer(MESSAGES['ENGLISH']["LANGUAGE_OK"], reply_markup=menu_reply_keyboard())

        case _:
            print(f"--[INFO] - User {user_id} ({user_name}) sent invalid callback: {callback_query.data}")
            await callback_query.message.answer(MESSAGES[language]["LANGUAGE_INVALID"])