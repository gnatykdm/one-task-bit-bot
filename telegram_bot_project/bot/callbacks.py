# bot/callbacks.py
from typing import Optional
from datetime import datetime

from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.buttons import *
from messages import MESSAGES
from service.idea import IdeaService
from service.myday import MyDayService
from service.task import TaskService
from service.user import UserService
from states import DialogStates
from service.focus import FocusService
from states import user_task_start_time
from channel_subsc import ChannelSubscChecker

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
            print(f"[INFO] - User {user_id} ({user_name}) set language to ua.")
            await UserService.update_user_language(user_id, 'UKRANIAN')
            await callback_query.message.answer(MESSAGES['UKRANIAN']["LANGUAGE_OK"], reply_markup=menu_reply_keyboard())
        case "lang_en":
            print(f"[INFO] - User {user_id} ({user_name}) set language to en.")
            await UserService.update_user_language(user_id, 'ENGLISH')
            await callback_query.message.answer(MESSAGES['ENGLISH']["LANGUAGE_OK"], reply_markup=menu_reply_keyboard())

        case _:
            print(f"[INFO] - User {user_id} ({user_name}) sent invalid callback: {callback_query.data}")
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
            print(f"[INFO] - User {user_id} ({user_name}) deleted idea.")
            await callback_query.message.answer(MESSAGES[language]["IDEA_DELETE"], reply_markup=idea_reply_keyboard())
            await state.clear()
        case "save_idea":
            try:
                data: Any = await state.get_data()
                idea: str = data.get("idea")

                if not idea:
                    print(f"[INFO] - User {user_id} ({user_name}) sent empty idea.")
                    await callback_query.message.answer(MESSAGES[language]["IDEA_PROBLEM"], reply_markup=idea_reply_keyboard())
                    return
                else:
                    await IdeaService.create_user_idea(user_id, idea)
                    await MyDayService.increment_idea_count(user_id)

                    print(f"[INFO] - User {user_id} ({user_name}) saved idea: {idea}")
                    await callback_query.message.answer(MESSAGES[language]["IDEA_SAVED"], reply_markup=idea_reply_keyboard())
                    await state.clear()
            except Exception as e:
                print(f"[ERROR] - User {user_id} ({user_name}) failed to save idea: {e}")
                await callback_query.message.answer(MESSAGES[language]["IDEA_PROBLEM"])
        case _:
            print(f"[INFO] - User {user_id} ({user_name}) sent invalid callback: {callback_query.data}")
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
            print(f"[INFO] - User {user_id} ({user_name}) saved task: {saved_task}")

            await TaskService.create_task(user_id, saved_task, False)
            await MyDayService.increment_task_count(user_id)
            await callback_query.message.answer(MESSAGES[language]["TASK_DEADLINE_NO"], reply_markup=task_menu_keyboard())
            await state.clear()
        case _:
            print(f"[INFO] - User {user_id} ({user_name}) sent invalid callback: {callback_query.data}")
            await callback_query.message.answer(MESSAGES[language]["TASK_DEADLINE_INVALID"])

async def callback_routines(callback_query: types.CallbackQuery) -> None:
    await callback_query.answer()

    user_id: int = callback_query.from_user.id
    user_find: Optional[dict] = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)
    if not language:
        language = 'ENGLISH'
    if not user_find:
        await callback_query.message.answer(MESSAGES['ENGLISH']["AUTHORIZATION_PROBLEM"])
        return

    match callback_query.data:
        case "morning_view":
            await callback_query.message.answer(MESSAGES[language]['MORNING_ROUTINE'], reply_markup=morning_routine_keyboard())
        case "evening_view":
            await callback_query.message.answer(MESSAGES[language]['EVENING_ROUTINE'], reply_markup=evening_routine_keyboard())
        case _:
            await callback_query.message.answer(MESSAGES[language]["ROUTINES_INVALID"])

async def callback_focus(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await callback_query.answer()

    user_id: int = callback_query.from_user.id
    user_find: Optional[dict] = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)
    if not language:
        language = 'ENGLISH'
    if not user_find:
        await callback_query.message.answer(MESSAGES['ENGLISH']["AUTHORIZATION_PROBLEM"])
        return

    match callback_query.data:
        case "save_focus":
            await callback_query.message.answer(MESSAGES[language]["TITLE_FOCUS_ZONE_MSG"], reply_markup=focus_title_ask_keyboard())
        case "not_save_focus":
            await callback_query.message.answer(MESSAGES[language]["NOT_SAVED_FOCUS_MSG"], reply_markup=focus_menu_keyboard())
        case _:
            await callback_query.message.answer(MESSAGES[language]["FOCUS_INVALID"], reply_markup=focus_menu_keyboard())

async def callback_focus_title(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await callback_query.answer()

    user_id: int = callback_query.from_user.id
    user_find: Optional[dict] = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)
    if not language:
        language = 'ENGLISH'
    if not user_find:
        await callback_query.message.answer(MESSAGES['ENGLISH']["AUTHORIZATION_PROBLEM"])
        return

    match callback_query.data:
        case "add_title":
            await state.set_state(DialogStates.provide_title_focusing)
            await callback_query.message.answer(MESSAGES[language]["FOCUS_TITLE_ASK"])
        case "not_add_title":
            print(f"[INFO] - User {user_id} canceled adding title.")

            data = await state.get_data()
            time_d = data.get("duration")
            await FocusService.create_focus(user_id, duration=time_d)

            print(f"[INFO] - User {user_id} saved focus: {time_d}")
            await callback_query.message.answer(MESSAGES[language]["SAVED_FOCUS_MSG"], reply_markup=focus_menu_keyboard())
            await state.clear()
        case _:
            await callback_query.message.answer(MESSAGES[language]["FOCUS_INVALID"], reply_markup=focus_menu_keyboard())

async def callback_work_buttons(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await callback_query.answer()

    user_id: int = callback_query.from_user.id
    user_find: Optional[dict] = await UserService.get_user_by_id(user_id)
    if not user_find:
        await callback_query.message.answer(MESSAGES['ENGLISH']["AUTHORIZATION_PROBLEM"])
        return

async def callback_task_menu(callback_query: types.CallbackQuery) -> None:
    await callback_query.answer()

    user_id: int = callback_query.from_user.id
    user_find: Optional[dict] = await UserService.get_user_by_id(user_id)
    language: str = await UserService.get_user_language(user_id)
    if not language:
        language = 'ENGLISH'
    if not user_find:
        await callback_query.message.answer(MESSAGES['ENGLISH']["AUTHORIZATION_PROBLEM"])
        return

    data = callback_query.data
    action, task_id_str = data.split(":")
    task_id = int(task_id_str)

    print(f"[DEBUG] - Task id: {task_id}")
    task = await TaskService.get_task_by_id(task_id)
    task_name = task['task_name']

    match action:
        case "complete_task":
            await TaskService.update_started_status(task_id)
            user_task_start_time[user_id] = (task_id, datetime.now())  
            await callback_query.message.answer(MESSAGES[language]['REMIND_WORK_START'].format(task_name),
                                                reply_markup=get_work_session_keyboard())
        case "cancel_task":
            await TaskService.update_started_status(task_id)
            user_task_start_time[user_id] = (task_id, datetime.now())  
            await callback_query.message.answer(MESSAGES[language]['REMIND_WORK_CANCEL'],
                                                reply_markup=menu_reply_keyboard())
            
async def callback_check_subscr(callback_query: types.CallbackQuery) -> None:
    await callback_query.answer()

    user_id: int = callback_query.from_user.id
    data: str = callback_query.data

    if data == "check_sub":
        status: bool = await ChannelSubscChecker.check_subscr_status(user_id)

        if status:
            await callback_query.message.answer("✅ You are subscribed to the channel!")
        else:
            await callback_query.message.answer("❌ You are not subscribed. Please subscribe to the channel.")
