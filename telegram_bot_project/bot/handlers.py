# bot/handlers.py
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from datetime import datetime, timedelta
import pytz
from zoneinfo import ZoneInfo

from ai_client import ask_gpt
from service.smtp import SmtpService
from bot.buttons import *
from messages import *
from service.idea import IdeaService
from service.task import TaskService
from service.user import UserService
from states import DialogStates, AI_CHAT_CONTEXT
from service.routine import RoutineService
from bot.utills import check_valid_time, validate_text
from service.myday import MyDayService
from bot.scheduler import update_user_schedule
from service.focus import FocusService
from bot.scheduler import schedule_new_task_notifications
from service.reminder import ReminderService

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

    print(f"[INFO] - User with id: {user_id} provided idea.")

    try:
        await state.update_data(idea=idea)

        divider = "\n" + ("-" * int(len(MESSAGES[language]['IDEA_ACTION']) * 1.65))

        keyboard = get_idea_conf_keyboard()
        await message.answer(
            f"{MESSAGES[language]['IDEA_ACTION']}{divider}\n💡 *Idea:* {idea}",
            reply_markup=keyboard
        )

    except Exception as e:
        print(f"[ERROR] - Saving idea failed: {e}")
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

    print(f"[DEBUG] - User {user_id} ideas: {ideas}")

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

    print(f"[DEBUG] - Deleting idea with id {real_id} for user {user_id}")

    await IdeaService.delete_user_idea(real_id)
    await MyDayService.decrement_idea_count(user_id)

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

    print(f"[DEBUG] - User {user_id} ideas: {ideas}")

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

    print(f"[DEBUG] - Selected idea with id {real_id} for update by user {user_id}")

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
        print(f"[INFO] - User with id: {user_id} provided task: {task}")

        await message.answer(MESSAGES[language]['TASK_DEADLINE_ASK'], reply_markup=task_reply_keyboard())
        await state.update_data(task=task)

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

    if not check_valid_time(deadline_str):
        await message.answer(MESSAGES[language]['TASK_DEADLINE_INVALID'])
        await state.clear()
        return

    reserved_times = await UserService.get_user_reserved_times(user_id)
    reserved_times_hm = [t.split(" ")[-1][:5] if " " in t else t[:5] for t in reserved_times]

    if deadline_str in reserved_times_hm:
        await message.answer(MESSAGES[language]['TIME_RESERVED_MSG'])
        return

    try:
        time_obj = datetime.strptime(deadline_str, "%H:%M").time()
        timezone: str = await UserService.get_user_timezone(user_id) or 'UTC'
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)

        deadline_dt = datetime.combine(now.date(), time_obj)
        deadline_dt = tz.localize(deadline_dt)

        if deadline_dt <= now:
            deadline_dt += timedelta(days=1)

        print(f"[INFO] - User {user_id} set deadline: {deadline_dt} ({timezone})")

        task_id = await TaskService.create_task(
            user_id=user_id,
            task_name=task,
            task_status=False,
            start_time=deadline_dt
        )

        await schedule_new_task_notifications(
            task_id=task_id,
            user_id=user_id,
            task_name=task,
            start_time=deadline_dt,
            language=language
        )

        await MyDayService.increment_task_count(user_id)
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

        print(f"[INFO] - User with id: {user_id} deleted task with id: {real_id}")
        await TaskService.delete_task(real_id)
        await MyDayService.decrement_task_count(user_id)
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

            print(f"[INFO] - User with id: {user_id} completed task with id: {real_id}")
            await TaskService.toggle_task_status(real_id)
            await MyDayService.increment_completed_tasks(user_id)
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
        print(f"[INFO] - User with id: {message.from_user.id} updated task name: {new_task_name}")
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
            MESSAGES[language]['TIMER_INVALID'],
            reply_markup=routine_time_keyboard()
        )
        return

    try:
        time_obj = datetime.strptime(new_wake_time, "%H:%M").time()
    except ValueError:
        await message.answer(
            MESSAGES[language]['TIMER_INVALID'],
            reply_markup=routine_time_keyboard()
        )
        return

    reserved_times = await UserService.get_user_reserved_times(user_id)
    reserved_times_hm = []
    for t in reserved_times:
        if len(t.split(":")) >= 2:
            reserved_times_hm.append(t.split(" ")[-1][:5])
        else:
            reserved_times_hm.append(t[:5])

    if new_wake_time in reserved_times_hm:
        await message.answer(
            MESSAGES[language]['TIME_RESERVED_MSG'],
            reply_markup=routine_time_keyboard()
        )
        return

    print(f"[INFO] - User with id: {user_id} set wake time to: {new_wake_time}")
    await UserService.update_wake_time(user_id, time_obj)
    await update_user_schedule(user_id=user_id, wake_time=time_obj, bot=message.bot)
    await message.answer(
        MESSAGES[language]['TIMER_SET'].format(new_wake_time),
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
            MESSAGES[language]['TIMER_INVALID'],
            reply_markup=routine_time_keyboard()
        )
        return

    try:
        time_obj = datetime.strptime(new_sleep_time, "%H:%M").time()
    except ValueError:
        await message.answer(
            MESSAGES[language]['TIMER_INVALID'],
            reply_markup=routine_time_keyboard()
        )
        return

    reserved_times = await UserService.get_user_reserved_times(user_id)
    reserved_times_hm = []
    for t in reserved_times:
        if len(t.split(":")) >= 2:
            reserved_times_hm.append(t.split(" ")[-1][:5])
        else:
            reserved_times_hm.append(t[:5])

    if new_sleep_time in reserved_times_hm:
        await message.answer(
            MESSAGES[language]['TIME_RESERVED_MSG'],
            reply_markup=routine_time_keyboard()
        )
        return

    print(f"[INFO] - User with id: {user_id} set sleep time to: {new_sleep_time}")
    await UserService.update_sleep_time(user_id, time_obj)
    await update_user_schedule(user_id=user_id, sleep_time=time_obj, bot=message.bot)
    await message.answer(
        MESSAGES[language]['TIMER_SET'].format(new_sleep_time),
        reply_markup=routine_time_keyboard()
    )
    await state.clear()


async def process_set_routine(message: Message, state: FSMContext, type: str):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    routine_title: str = message.text.strip()
    routine_keyboard: ReplyKeyboardMarkup = morning_routine_keyboard() if type == "morning" else evening_routine_keyboard()
    if not validate_text(routine_title):
        await message.answer(MESSAGES[language]['INVALID_MORNING_ROUTINE'], reply_markup=routine_keyboard)
        return

    try:
        await RoutineService.create_routine(user_id, routine_type=type, routine_name=routine_title)

        print(f"[INFO] - User with id: {user_id} set routine title: {routine_title}")
        await message.answer(MESSAGES[language]['ROUTINE_SAVED'].format(routine_title), reply_markup=routine_keyboard)
        await state.clear()
    except:
        await message.answer(MESSAGES[language]['ROUTINE_EXISTS'], reply_markup=routine_keyboard)

async def process_delete_morning_routine(message: Message, state: FSMContext, type: str):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or "ENGLISH"
    routine_keyboard: ReplyKeyboardMarkup = morning_routine_keyboard() if type == "morning" else evening_routine_keyboard()

    if not user_find:
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    routine_num: int = int(message.text.strip())
    if (routine_num < 1):
        await message.answer(MESSAGES[language]['COMPLETE_TASK_INVALID'], reply_markup=routine_keyboard)
        return
    else:
        data = await state.get_data()
        routines = data.get("morning_routine")

        routine_to_delete = routines[routine_num - 1]
        real_id = routine_to_delete["id"]

        await RoutineService.delete_routine(real_id)
        print(f"[INFO] - User with id: {user_id} deleted routine with id: {real_id}")

        await message.answer(MESSAGES[language]['ROUTINE_DELETED'].format(routine_num, routine_to_delete['routine_name']), reply_markup=routine_keyboard)
        await state.clear()

async def process_update_morning_routine(message: Message, state: FSMContext, type: str):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or "ENGLISH"
    routine_keyboard: ReplyKeyboardMarkup = morning_routine_keyboard() if type == "morning" else evening_routine_keyboard()

    if not user_find:
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    routine_num: int = int(message.text.strip())
    if (routine_num < 1):
        await message.answer(MESSAGES[language]['COMPLETE_TASK_INVALID'], reply_markup=routine_keyboard)
        return
    else:
        data = await state.get_data()
        routines = data.get("morning_routine")

        routine_to_update = routines[routine_num - 1]
        real_id = routine_to_update["id"]

        await message.answer(MESSAGES[language]['NEW_ROUTINE_NAME'], reply_markup=routine_keyboard)
        await state.update_data(routine_id=real_id)
        await state.set_state(DialogStates.update_morning_routine)

async def process_save_updated_morning_routine(message: Message, state: FSMContext, type: str):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or "ENGLISH"
    routine_keyboard: ReplyKeyboardMarkup = morning_routine_keyboard() if type == "morning" else evening_routine_keyboard()

    if not user_find:
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    routine_title: str = message.text.strip()
    if not validate_text(routine_title):
        await message.answer(MESSAGES[language]['INVALID_MORNING_ROUTINE'], reply_markup=routine_keyboard)
        return

    data = await state.get_data()
    routine_id = data.get("routine_id")

    try:
        await RoutineService.update_routine(routine_id, routine_title)
        print(f"[INFO] - User with id: {user_id} updated routine title: {routine_title}")
        await message.answer(MESSAGES[language]['ROUTINE_NAME_SET'].format(routine_title), reply_markup=routine_keyboard)
        await state.clear()
    except:
        await message.answer(MESSAGES[language]['ROUTINE_EXISTS'], reply_markup=routine_keyboard)


async def process_feedback_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    user_name = message.from_user.username
    language = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    feedback_message = message.text.strip()
    if not feedback_message:
        await message.answer(MESSAGES["ENGLISH"]['INVALID_MESSAGE'])
        return

    print(f"[INFO] - Feedback message from user with id: {user_id} is: {feedback_message}")
    await SmtpService.send_feedback_message(feedback_message, user_id, user_name)
    await message.answer(MESSAGES[language]['SMTP_MESSAGE_SENT'], reply_markup=settings_menu_keyboard())
    await state.clear()

async def process_save_focus_session_title(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    focus_title: str = message.text.strip()
    if not validate_text(focus_title):
        await message.answer(MESSAGES[language]['FOCUS_INVALID'])
        return

    data = await state.get_data()
    time_d = data.get("duration")

    try:
        await FocusService.create_focus(user_id, time_d, focus_title)

        print(f"[INFO] - User with id: {user_id} created focus session with title: {focus_title}")
        await message.answer(MESSAGES[language]['SAVED_FOCUS_MSG'].format(focus_title), reply_markup=focus_menu_keyboard())
        await state.clear()
    except Exception as e:
        print(f"[ERROR] - {e}")
        await message.answer(MESSAGES[language]['FOCUS_INVALID'])

async def process_delete_focus_session(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    number = message.text.strip()
    if not number.isdigit():
        await message.answer(MESSAGES[language]['FOCUS_INVALID'])
        return

    data = await state.get_data()
    focus_sessions = data.get("focuses")

    try:
        focus_to_delete = focus_sessions[int(number) - 1]
        real_id = focus_to_delete["id"]

        print(f"[INFO] - User with id: {user_id} deleted focus session with id: {real_id}")
        await FocusService.delete_focus(real_id)
        await message.answer(MESSAGES[language]['FOCUS_DELETED'].format(number, focus_to_delete['title']), reply_markup=focus_menu_keyboard())
        await state.clear()
    except Exception as e:
        print(f"[ERROR] - {e}")
        await message.answer(MESSAGES[language]['FOCUS_INVALID'])

async def process_ai_talk(message: Message):
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or "ENGLISH"
    user_timezone_str = await UserService.get_user_timezone(user_id)

    if not user_find:
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return
    
    message_type = message.content_type
    if message_type != "text":
        await message.answer(
            MESSAGES[language]['AI_CHAT_TYPE_MSG_INVALID']
        )
        return

    text: str = message.text.strip()
    now_utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    if user_id not in AI_CHAT_CONTEXT:
        AI_CHAT_CONTEXT[user_id] = []

    AI_CHAT_CONTEXT[user_id].append({
        "role": "user",
        "content": text,
        "date": now_utc
    })

    try:
        messages_for_gpt = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in AI_CHAT_CONTEXT[user_id]
        ]

        response: str = await ask_gpt(messages=messages_for_gpt, user_id=user_id)

        tz = ZoneInfo(user_timezone_str) if user_timezone_str else None
        now_user = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S") if tz else now_utc

        AI_CHAT_CONTEXT[user_id].append({
            "role": "assistant",
            "content": response,
            "date": now_user
        })

        await message.answer(response, parse_mode="Markdown")
    except Exception as e:
        print(f"[ERROR] AI talk process: {e}")
        await message.answer(MESSAGES[language]['AI_CHAT_PROBLEM'])

async def process_reminder_name_set(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    reminder_name = message.text.strip()
    if not reminder_name:
        await message.answer(MESSAGES[language]['INVALID_MESSAGE'])
        return

    await state.set_data({"reminder_name": reminder_name})
    await message.answer(MESSAGES[language]['REMINDER_TIME_MSG'])
    await state.set_state(DialogStates.provide_remind_time)

async def process_save_reminder(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    language = await UserService.get_user_language(user_id) or "ENGLISH"

    if not user_find:
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    user_timezone = await UserService.get_user_timezone(user_id) or "UTC"
    reminder_time_str = message.text.strip()

    if not check_valid_time(reminder_time_str):
        await message.answer(MESSAGES[language]['TIMER_INVALID'])
        return

    reserved_times = await UserService.get_user_reserved_times(user_id)
    reserved_times_hm = []
    for t in reserved_times:
        if len(t.split(":")) >= 2:
            reserved_times_hm.append(t.split(" ")[-1][:5])
        else:
            reserved_times_hm.append(t[:5])
            
    if reminder_time_str in reserved_times_hm:
        await message.answer(
            MESSAGES[language]['TIME_RESERVED_MSG']
        )
        return

    tz = pytz.timezone(user_timezone)
    now = datetime.now(tz)

    hour, minute = map(int, reminder_time_str.split(":"))
    remind_datetime = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

    if remind_datetime < now:
        remind_datetime += timedelta(days=1)

    if remind_datetime.tzinfo is None:
        remind_datetime = tz.localize(remind_datetime)

    data = await state.get_data()
    reminder_name = data.get("reminder_name")
    remind_datetime_utc = remind_datetime.astimezone(pytz.UTC)

    print(f"[INFO] - User with id: {user_id} created reminder at {remind_datetime.isoformat()}")
    try:
        await ReminderService.create_reminder(
            user_id=user_id,
            title=reminder_name,
            remind_time=remind_datetime_utc,  
            remind_status=False
        )

        await message.answer(
            MESSAGES[language]["REMINDER_SAVED_MSG"].format(reminder_name, reminder_time_str),
            reply_markup=get_reminder_menu_btn()
        )

        await state.clear()
    except Exception as e:
        print(f"[ERROR] - {e}")
        await message.answer(
            MESSAGES[language]["SOME_PROBLEM"],
            reply_markup=get_reminder_menu_btn()
        )

async def reminder_delete_process(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    user_find = await UserService.get_user_by_id(user_id)
    if not user_find or not user_find.get("id"):
        await message.answer(MESSAGES["ENGLISH"]['AUTHORIZATION_PROBLEM'])
        return

    language = await UserService.get_user_language(user_id) or "ENGLISH"
    reminders = await ReminderService.get_user_reminders(user_id)

    print(f"[DEBUG] - User {user_id} reminders: {reminders}")

    try:
        user_number = int(message.text.strip())
    except ValueError:
        await message.answer(
            MESSAGES[language]['NOT_VALID_REMINDER_NUM'], 
            reply_markup=get_reminder_menu_btn()
        )
        return

    index = user_number - 1
    if not (0 <= index < len(reminders)):
        await message.answer(
            MESSAGES[language]['INVALID_REMINDER_NUM'], 
            reply_markup=get_reminder_menu_btn()
        )
        return

    reminder_to_delete = reminders[index]
    real_id = reminder_to_delete["id"]

    print(f"[DEBUG] - Deleting reminder with id {real_id} for user {user_id}")

    await ReminderService.delete_reminder(real_id)

    await message.answer(
        MESSAGES[language]['REMINDER_DELETED'].format(user_number, reminder_to_delete['title']),
        reply_markup=get_reminder_menu_btn()
    )
    await state.clear()
