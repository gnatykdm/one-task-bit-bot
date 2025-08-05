# bot/scheduler.py
from datetime import time, datetime, timedelta
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from messages import send_morning_message, send_evening_message
from bot.buttons import work_buttons_keyboard
from service.task import TaskService
from service.user import UserService

scheduler: AsyncIOScheduler = AsyncIOScheduler()
notified_task_ids = set()

def initialize_scheduler():
    scheduler.start()
    return scheduler

def update_user_job(user_id: int, when: time, bot: Bot, job_type: str):
    job_id = f"{job_type}_message_{user_id}"

    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    scheduler.add_job(
        send_morning_message if job_type == "wake" else send_evening_message,
        trigger=CronTrigger(hour=when.hour, minute=when.minute),
        args=[bot, user_id],
        id=job_id,
        replace_existing=True
    )

    print(f"[INFO] - User with id: {user_id} updated job, {job_id}")

async def schedule_all_users_jobs(bot: Bot):
    users = await UserService.get_all_users()
    for user in users:
        if user["wake_time"]:
            update_user_job(user["id"], user["wake_time"], bot, job_type="wake")
        if user["sleep_time"]:
            update_user_job(user["id"], user["sleep_time"], bot, job_type="sleep")

async def check_upcoming_tasks(bot: Bot):
    now = datetime.now()
    print("[TASK CHECK] - Checking for upcoming tasks at {}".format(now.strftime('%Y-%m-%d %H:%M:%S')))

    tasks = await TaskService.get_all_upcoming_tasks()

    for task in tasks:
        task_time = task.get("start_time")
        if not task_time:
            continue

        task_id = task["id"]
        user_id = task["user_id"]
        task_name = task["task_name"]
        language: str = await UserService.get_user_language(user_id)

        time_diff = (task_time - now).total_seconds()
        time_after_start = (now - task_time).total_seconds()

        print(f"[DEBUG] - Task: '{task_name}' | user_id: {user_id} | time_diff: {time_diff:.2f} sec | start_time: {task_time.strftime('%H:%M:%S')}")

        if 1790 <= time_diff <= 1810:
            print(f"[NOTIFY] - User {user_id} - Task '{task_name}' starts in 30 min")
            await send_task_notification(language, bot, user_id, task_name, 30)
        elif 890 <= time_diff <= 910:
            print(f"[NOTIFY] - User {user_id} - Task '{task_name}' starts in 15 min")
            await send_task_notification(language, bot, user_id, task_name, 15)
        elif 290 <= time_diff <= 310:
            print(f"[NOTIFY] - User {user_id} - Task '{task_name}' starts in 5 min")
            await send_task_notification(language, bot, user_id, task_name, 5)
        elif -60 <= time_diff <= 60:
            print(f"[NOTIFY] - User {user_id} - Task '{task_name}' starts now")
            await send_task_notification(language, bot, user_id, task_name, 0, task_id)

        if time_after_start >= 0:
            started = await TaskService.get_started_status(task_id)
            print(f"[DEBUG REMINDER] Task {task_id}, started: {started}, time_after_start: {time_after_start:.2f}")

            for target_minute in [5, 10, 15]:
                lower = target_minute * 60 - 60
                upper = target_minute * 60 + 60
                if lower <= time_after_start <= upper:
                    reminder_key = (task_id, f"late_{target_minute}")
                    if reminder_key not in notified_task_ids:
                        print(f"[REMIND] - Sending reminder for task {task_id} after {target_minute} min")
                        await send_task_notification(language, bot, user_id, task_name, target_minute, task_id)
                        notified_task_ids.add(reminder_key)


async def send_task_notification(language: str, bot: Bot, user_id: int, task_name: str, minutes: int, task_id: int):
    messages = {
        "UKRAINIAN": {
            "soon": f"⏰ Завдання *\"{task_name}\"* почнеться через {minutes} хвилин!",
            "now": f"🚀 Завдання *\"{task_name}\"* починається прямо зараз!\nПочинаємо?",
            "reminder": f"⚠️ Нагадування: завдання *\"{task_name}\"* мало початися {minutes} хвилин тому, але не розпочате."
        },
        "ENGLISH": {
            "soon": f"⏰ Task *\"{task_name}\"* will start in {minutes} minutes!",
            "now": f"🚀 Task *\"{task_name}\"* is starting right now!\nStart it?",
            "reminder": f"⚠️ Reminder: task *\"{task_name}\"* was supposed to start {minutes} minutes ago but not started yet."
        }
    }

    lang_key = language.upper()
    message_set = messages.get(lang_key, messages["ENGLISH"])

    if minutes == 0:
        text = message_set["now"]
    elif minutes in [5, 10, 15]:
        text = message_set["reminder"]
    else:
        text = message_set["soon"]

    try:
        await bot.send_message(user_id, text, reply_markup=work_buttons_keyboard(task_id))
        print(f"[BOT] Sent message to {user_id}: {text}")
    except Exception as e:
        print(f"[ERROR] Failed to send message to {user_id}: {e}")