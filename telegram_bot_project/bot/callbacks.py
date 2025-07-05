from typing import Optional, Any
from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.buttons import menu_reply_keyboard, idea_reply_keyboard
from messages import MESSAGES
from service.idea import IdeaService
from service.task import TaskService
from service.user import UserService
from states import DialogStates


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


async def callback_idea_process(callback_query: types.CallbackQuery, state: FSMContext) -> None:
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
        case "delete_idea":
            print(f"--[INFO] - User {user_id} ({user_name}) deleted idea.")
            await callback_query.message.answer(MESSAGES[language]["IDEA_DELETE"], reply_markup=idea_reply_keyboard())
            await state.clear()
        case "save_idea":
            try:
                data: Any = await state.get_data()
                idea: str = data.get("idea")

                if not idea:
                    print(f"--[INFO] - User {user_id} ({user_name}) sent empty idea.")
                    await callback_query.message.answer(MESSAGES[language]["IDEA_PROBLEM"], reply_markup=idea_reply_keyboard())
                    return
                else:
                    await IdeaService.create_user_idea(user_id, idea)

                    print(f"--[INFO] - User {user_id} ({user_name}) saved idea: {idea}")
                    await callback_query.message.answer(MESSAGES[language]["IDEA_SAVED"], reply_markup=idea_reply_keyboard())
                    await state.clear()
            except Exception as e:
                await callback_query.message.answer(MESSAGES[language]["IDEA_PROBLEM"])
        case _:
            print(f"--[INFO] - User {user_id} ({user_name}) sent invalid callback: {callback_query.data}")
            await callback_query.message.answer(MESSAGES[language]["IDEA_PROBLEM"], reply_markup=idea_reply_keyboard())

async def callback_task_deadline(callback_query: types.CallbackQuery, state: FSMContext) -> None:
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
        case "yes_task":
            await state.set_state(DialogStates.task_deadline)
            await callback_query.message.answer(MESSAGES[language]["TASK_DEADLINE_YES"])
        case "no_task":
            data = await state.get_data()
            saved_task = data.get("task")
            print(f"--[INFO] - User {user_id} ({user_name}) saved task: {saved_task}")

            await TaskService.create_task(user_id, saved_task, False)
            await callback_query.message.answer(MESSAGES[language]["TASK_DEADLINE_NO"], reply_markup=menu_reply_keyboard())
            await state.clear()
        case _:
            print(f"--[INFO] - User {user_id} ({user_name}) sent invalid callback: {callback_query.data}")
            await callback_query.message.answer(MESSAGES[language]["TASK_DEADLINE_INVALID"])