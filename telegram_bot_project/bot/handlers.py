from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.buttons import get_idea_conf_keyboard, menu_reply_keyboard, idea_reply_keyboard, task_reply_keyboard, task_menu_keyboard
from messages import MESSAGES
from service.idea import IdeaService
from service.task import TaskService
from service.user import UserService
from states import DialogStates

async def process_idea_save(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    if not user_find or not user_find.get("id"):
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    language = await UserService.get_user_language(user_id) or "ENGLISH"
    idea = message.text.strip()

    exist = await IdeaService.get_by_idea_name(idea)
    if exist:
        await message.answer(
            MESSAGES[language]['IDEA_EXIST'],
            reply_markup=menu_reply_keyboard()
        )
        return

    print(f"--[INFO] User with id: {user_id} provided idea.")

    try:
        await state.update_data(idea=idea)

        divider = "\n" + ("-" * int(len(MESSAGES[language]['IDEA_ACTION']) * 1.65))

        keyboard = get_idea_conf_keyboard()

        await message.answer(
            f"{MESSAGES[language]['IDEA_ACTION']}{divider}\n💡 *Idea:* {idea}",
            reply_markup=keyboard
        )

    except Exception as e:
        print(f"[ERROR] Saving idea failed: {e}")
        await message.answer(
            MESSAGES[language]['ERROR_SAVING_IDEA'],
            reply_markup=idea_reply_keyboard()
        )

async def process_idea_delete(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    if not user_find or not user_find.get("id"):
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    language = await UserService.get_user_language(user_id) or "ENGLISH"
    ideas = await IdeaService.get_all_ideas_by_user_id(user_id)

    print(f"--[DEBUG] User {user_id} ideas: {ideas}")

    try:
        user_number = int(message.text.strip())
    except ValueError:
        await message.answer(MESSAGES[language]['NOT_VALID_IDEA_NUM'], reply_markup=idea_reply_keyboard())
        return

    index = user_number - 1
    if not (0 <= index < len(ideas)):
        await message.answer(MESSAGES[language]['INVALID_IDEA_NUM'], reply_markup=idea_reply_keyboard())
        return

    idea_to_delete = ideas[index]
    real_id = idea_to_delete["id"]

    print(f"--[DEBUG] Deleting idea with id {real_id} for user {user_id}")

    await IdeaService.delete_user_idea(real_id)

    await message.answer(MESSAGES[language]['IDEA_DELETED'].format(user_number, idea_to_delete['idea_name']), reply_markup=idea_reply_keyboard())
    await state.clear()


async def process_idea_update(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    if not user_find or not user_find.get("id"):
        await message.answer(MESSAGES["ENGLISH"]["AUTHORIZATION_PROBLEM"])
        return

    language = await UserService.get_user_language(user_id) or "ENGLISH"
    ideas = await IdeaService.get_all_ideas_by_user_id(user_id)

    print(f"--[DEBUG] User {user_id} ideas: {ideas}")

    try:
        user_number = int(message.text.strip())
    except ValueError:
        await message.answer(
            MESSAGES[language]["NOT_VALID_IDEA_NUM"],
            reply_markup=idea_reply_keyboard()
        )
        return

    index = user_number - 1
    if not (0 <= index < len(ideas)):
        await message.answer(
            MESSAGES[language]["INVALID_IDEA_NUM"],
            reply_markup=idea_reply_keyboard()
        )
        return

    idea_to_update = ideas[index]
    real_id = idea_to_update["id"]

    print(f"--[DEBUG] Selected idea with id {real_id} for update by user {user_id}")

    await state.update_data(idea_id=real_id, idea_number=user_number)
    await state.set_state(DialogStates.waiting_for_update_text)

    await message.answer(
        MESSAGES[language]["ASK_NEW_IDEA_TEXT"].format(user_number, idea_to_update["idea_name"]),
        reply_markup=idea_reply_keyboard()
    )

async def process_save_updated_idea_text(message: Message, state: FSMContext):
    data = await state.get_data()
    idea_id = data.get("idea_id")
    idea_number = data.get("idea_number")

    language = await UserService.get_user_language(message.from_user.id) or "ENGLISH"

    new_text = message.text.strip()
    idea_exists = await IdeaService.get_by_idea_name(new_text)

    if idea_exists:
        await message.answer(
            MESSAGES[language]["IDEA_EXIST"],
            reply_markup=menu_reply_keyboard()
        )
    else:
        await IdeaService.update_user_idea(idea_id, new_text)

        await message.answer(
            MESSAGES[language]["IDEA_UPDATED"].format(idea_number),
            reply_markup=idea_reply_keyboard()
        )

    await state.clear()

async def process_task_save(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or "ENGLISH"
    if not user_find:
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return
    else:
        task = message.text.strip()
        print(f"--[INFO] User with id: {user_id} provided task: {task}")

        await message.answer(MESSAGES[language]['TASK_DEADLINE_ASK'], reply_markup=task_reply_keyboard())
        await state.update_data(task=task)

from datetime import datetime

async def process_task_deadline(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    data = await state.get_data()
    task = data.get("task")

    deadline_str = message.text.strip()

    try:
        time_obj = datetime.strptime(deadline_str, "%H:%M").time()
        deadline_dt = datetime.combine(datetime.now().date(), time_obj)

        print(f"--[INFO] User with id: {user_id} provided deadline: {deadline_dt}")

        await TaskService.create_task(user_id, task, False, deadline_dt)
        await message.answer(MESSAGES[language]['TASK_SAVED'], reply_markup=task_menu_keyboard())
        await state.clear()

    except ValueError:
        await message.answer(MESSAGES[language]['TASK_DEADLINE_INVALID'])