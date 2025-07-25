from aiogram.fsm.context import FSMContext
from aiogram.types import Message, message

from bot.buttons import *
from messages import MESSAGES
from service.idea import IdeaService
from service.task import TaskService
from service.user import UserService
from states import DialogStates
from service.routine import RoutineService
from bot.utills import check_valid_time, validate_text

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
        await state.clear()

async def process_task_delete(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    data = await state.get_data()
    tasks = data.get("tasks")

    try:
        max_task_num = len(tasks)
        user_number = int(message.text.strip())

        if user_number > max_task_num or user_number < 1:
            await message.answer(MESSAGES[language]['INVALID_TASK_NUM'], reply_markup=task_menu_keyboard())
            return

        task_to_delete = tasks[user_number - 1]
        real_id = task_to_delete["id"]

        print(f"--[INFO] User with id: {user_id} deleted task with id: {real_id}")
        await TaskService.delete_task(real_id)
        await message.answer(MESSAGES[language]['TASK_DELETED'].format(user_number, task_to_delete['task_name']), reply_markup=task_menu_keyboard())
        await state.clear()

    except ValueError:
        await message.answer(MESSAGES[language]['TASK_DELETE_PROBLEM'], reply_markup=task_menu_keyboard())
        await state.clear()

async def process_task_complete(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    data = await state.get_data()
    tasks = data.get("tasks")
    max_task_num = len(tasks)

    try:
        user_number = int(message.text.strip())
        if user_number > max_task_num or user_number < 1:
            await message.answer(MESSAGES[language]['COMPLETE_TASK_INVALID'], reply_markup=task_menu_keyboard())
            return
        else:
            task_to_complete = tasks[user_number - 1]
            real_id = task_to_complete["id"]

            print(f"--[INFO] User with id: {user_id} completed task with id: {real_id}")
            await TaskService.toggle_task_status(real_id)
            await message.answer(MESSAGES[language]['COMPLETE_TASK_SUCCESS'].format(user_number, task_to_complete['task_name']), reply_markup=task_menu_keyboard())
            await state.clear()
    except ValueError:
        await message.answer(MESSAGES[language]['COMPLETE_TASK_PROBLEM'], reply_markup=task_menu_keyboard())
        await state.clear()

async def process_task_update(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    data = await state.get_data()
    tasks = data.get("tasks")
    max_task_num = len(tasks)

    try:
        user_number = int(message.text.strip())
        if user_number > max_task_num or user_number < 1:
            await message.answer(MESSAGES[language]['INVALID_TASK_NUM'], reply_markup=task_menu_keyboard())
        else:
            task_to_update = tasks[user_number - 1]
            real_id = task_to_update["id"]

            await message.answer(MESSAGES[language]['UPDATE_TASK_NAME_MSG'])
            await state.update_data(task_id=real_id, u_number=user_number)
            await state.set_state(DialogStates.update_task_name)

    except ValueError:
        await message.answer(MESSAGES[language]['UPDATE_TASK_PROBLEM'], reply_markup=task_menu_keyboard())
        await state.clear()

async def process_save_updated_task_name(message: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get("task_id")
    user_number = data.get("u_number")

    new_task_name = message.text.strip()

    if not new_task_name:
        await message.answer(MESSAGES["ENGLISH"]['UPDATE_TASK_NAME_INVALID'], reply_markup=task_menu_keyboard())
        return
    else:
        print(f"--[INFO] User with id: {message.from_user.id} updated task name: {new_task_name}")
        await TaskService.update_task(task_id=task_id, task_name=new_task_name)
        await message.answer(MESSAGES["ENGLISH"]['UPDATE_TASK_SUCCESS'].format(user_number), reply_markup=task_menu_keyboard())
        await state.clear()

async def process_set_wake_time(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    new_wake_time = message.text.strip()
    if not new_wake_time or not check_valid_time(new_wake_time):
        await message.answer(
            MESSAGES["ENGLISH"]['WAKE_TIME_INVALID'],
            reply_markup=routine_time_keyboard()
        )
        return

    try:
        time_obj = datetime.strptime(new_wake_time, "%H:%M").time()
    except ValueError:
        await message.answer(
            MESSAGES["ENGLISH"]['WAKE_TIME_INVALID'],
            reply_markup=routine_time_keyboard()
        )
        return

    print(f"--User with id: {user_id} set wake time to: {new_wake_time}")
    await UserService.update_wake_time(user_id, time_obj)
    await message.answer(
        MESSAGES[language]['WAKE_TIME_SET'].format(new_wake_time),
        reply_markup=routine_time_keyboard()
    )
    await state.clear()


async def process_set_sleep_time(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    new_sleep_time = message.text.strip()
    if not new_sleep_time or not check_valid_time(new_sleep_time):
        await message.answer(
            MESSAGES["ENGLISH"]['SLEEP_TIME_INVALID'],
            reply_markup=routine_time_keyboard()
        )
        return

    try:
        time_obj = datetime.strptime(new_sleep_time, "%H:%M").time()
    except ValueError:
        await message.answer(
            MESSAGES["ENGLISH"]['SLEEP_TIME_INVALID'],
            reply_markup=routine_time_keyboard()
        )
        return

    print(f"--User with id: {user_id} set sleep time to: {new_sleep_time}")
    await UserService.update_sleep_time(user_id, time_obj)
    await message.answer(
        MESSAGES[language]['SLEEP_TIME_SET'].format(new_sleep_time),
        reply_markup=routine_time_keyboard()
    )
    await state.clear()

async def process_set_routine_time(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    routine_title: str = message.text.strip()
    if not validate_text(routine_title):
        await message.answer(MESSAGES[language]['INVALID_MORNING_ROUTINE'], reply_markup=morning_routine_keyboard())
        return

    try:
        await RoutineService.create_routine(user_id, routine_type="morning", routine_name=routine_title)

        print(f"User with id: {user_id} set routine title: {routine_title}")
        await message.answer(MESSAGES[language]['ROUTINE_SAVED'].format(routine_title), reply_markup=morning_routine_keyboard())
        await state.clear()
    except:
        await message.answer(MESSAGES[language]['ROUTINE_EXISTS'], reply_markup=morning_routine_keyboard())

async def process_delete_morning_routine(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    routine_num: int = int(message.text.strip())
    if (routine_num < 1):
        await message.answer(MESSAGES[language]['COMPLETE_TASK_INVALID'], reply_markup=morning_routine_keyboard())
        return
    else:
        data = await state.get_data()
        routines = data.get("morning_routine")

        routine_to_delete = routines[routine_num - 1]
        real_id = routine_to_delete["id"]

        await RoutineService.delete_routine(real_id)
        print(f"User with id: {user_id} deleted routine with id: {real_id}")

        await message.answer(MESSAGES[language]['ROUTINE_DELETED'].format(routine_num, routine_to_delete['routine_name']), reply_markup=morning_routine_keyboard())
        await state.clear()