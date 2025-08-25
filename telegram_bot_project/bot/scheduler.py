# bot/scheduler.py
from datetime import time, datetime, timedelta
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger 
from bot.buttons import work_buttons_keyboard, get_start_day_btn
from service.task import TaskService
from service.user import UserService
from collections import defaultdict
from typing import Set
from messages import *
from service.myday import MyDayService

scheduler: AsyncIOScheduler = AsyncIOScheduler()
notified_task_ids = set()
sent_notifications: defaultdict[int, Set[str]] = defaultdict(set)

def initialize_scheduler():
    scheduler.start()
    return scheduler

def update_user_job(user_id: int, when: time, bot: Bot, job_type: str):
    if not when:
        print(f"[WARNING] - No time provided for job '{job_type}' (user_id={user_id})")
        return

    job_id = f"{job_type}_message_{user_id}"

    job_func = send_morning_message if job_type == "wake" else send_evening_message
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
        print(f"[INFO] - Removed old job: {job_id}")

    scheduler.add_job(
        job_func,
        trigger=CronTrigger(hour=when.hour, minute=when.minute),
        args=[bot, user_id],
        id=job_id,
        replace_existing=True
    )

    print(f"[INFO] - Scheduled {job_type} job for user {user_id} at {when.strftime('%H:%M')}")


async def schedule_all_users_jobs(bot: Bot):
    users = await UserService.get_all_users()
    for user in users:
        if user["wake_time"]:
            update_user_job(user["id"], user["wake_time"], bot, job_type="wake")
        if user["sleep_time"]:
            update_user_job(user["id"], user["sleep_time"], bot, job_type="sleep")

class PreciseTaskNotifier:
    def __init__(self, bot: Bot, scheduler: AsyncIOScheduler):
        self.bot = bot
        self.scheduler = scheduler
        self.scheduled_jobs = {} 
    
    async def schedule_task_notifications(self, task_id: int, user_id: int, task_name: str, start_time: datetime, language: str):
        now = datetime.now()
        
        notification_times = [
            (start_time - timedelta(minutes=30), 30, "30min"),
            (start_time - timedelta(minutes=15), 15, "15min"),
            (start_time - timedelta(minutes=5), 5, "5min"),
            (start_time, 0, "now")
        ]
        
        for notification_time, minutes, notification_type in notification_times:
            if notification_time > now:
                job_id = f"task_{task_id}_{notification_type}"
                
                try:
                    if self.scheduler.get_job(job_id):
                        self.scheduler.remove_job(job_id)
                except:
                    pass  
                
                try:
                    self.scheduler.add_job(
                        self._send_notification,
                        trigger=DateTrigger(run_date=notification_time),
                        args=[language, user_id, task_name, minutes, task_id],
                        id=job_id,
                        replace_existing=True
                    )
                    self.scheduled_jobs[job_id] = True
                    print(f"[SCHEDULED] - Notification for task {task_id} at {notification_time.strftime('%H:%M:%S')}")
                except Exception as e:
                    print(f"[ERROR] Failed to schedule notification for task {task_id}: {e}")
    
    async def _send_notification(self, language: str, user_id: int, task_name: str, minutes: int, task_id: int):
        try:
            await send_task_notification(language, self.bot, user_id, task_name, minutes, task_id)
            print(f"[PRECISE NOTIFY] - Sent notification to user {user_id} for task {task_id}")
            
            notification_key = f"{task_id}_{minutes}min" if minutes > 0 else f"{task_id}_now"
            sent_notifications[user_id].add(notification_key)
            
        except Exception as e:
            print(f"[ERROR] Failed to send precise notification: {e}")
    
    async def schedule_all_task_notifications(self):
        try:
            tasks = await TaskService.get_all_upcoming_tasks()
            print(f"[INFO] Scheduling notifications for {len(tasks)} tasks")
            
            for task in tasks:
                task_time = task.get("start_time")
                if not task_time:
                    continue
                
                task_id = task["id"]
                user_id = task["user_id"]
                task_name = task["task_name"]
                language = await UserService.get_user_language(user_id)
                
                await self.schedule_task_notifications(task_id, user_id, task_name, task_time, language)
                
        except Exception as e:
            print(f"[ERROR] Failed to schedule task notifications: {e}")

    async def remove_task_notifications(self, task_id: int):
        notification_types = ["30min", "15min", "5min", "now"]
        
        for notification_type in notification_types:
            job_id = f"task_{task_id}_{notification_type}"
            try:
                if self.scheduler.get_job(job_id):
                    self.scheduler.remove_job(job_id)
                    if job_id in self.scheduled_jobs:
                        del self.scheduled_jobs[job_id]
                    print(f"[REMOVED] - Notification job {job_id}")
            except Exception as e:
                print(f"[ERROR] Failed to remove notification job {job_id}: {e}")

async def check_upcoming_tasks_v2(bot: Bot):
    now = datetime.now()
    print(f"[BACKUP CHECK] - Checking for upcoming tasks at {now.strftime('%Y-%m-%d %H:%M:%S')}")

    try:
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

            notifications_to_check = [
                (1800, 30, "30min"), 
                (900, 15, "15min"),   
                (300, 5, "5min"),     
                (0, 0, "now")         
            ]

            for target_seconds, minutes, notification_type in notifications_to_check:
                if target_seconds - 60 <= time_diff <= target_seconds + 60:
                    notification_key = f"{task_id}_{notification_type}"
                    
                    if notification_key not in sent_notifications[user_id]:
                        print(f"[BACKUP NOTIFY] - User {user_id} - Task '{task_name}' notification: {notification_type}")
                        await send_task_notification(language, bot, user_id, task_name, minutes, task_id)
                        sent_notifications[user_id].add(notification_key)

            if time_after_start >= 300: 
                try:
                    started = await TaskService.get_started_status(task_id)
                    print(f"[DEBUG REMINDER] Task {task_id}, started: {started}, time_after_start: {time_after_start:.2f}")

                    for target_minute in [5, 10, 15]:
                        lower = target_minute * 60 - 60
                        upper = target_minute * 60 + 60
                        if lower <= time_after_start <= upper:
                            reminder_key = f"{task_id}_late_{target_minute}"
                            if reminder_key not in sent_notifications[user_id]:
                                print(f"[BACKUP REMIND] - Sending reminder for task {task_id} after {target_minute} min")
                                await send_task_notification(language, bot, user_id, task_name, target_minute, task_id)
                                sent_notifications[user_id].add(reminder_key)
                except Exception as e:
                    print(f"[ERROR] Failed to check task status for {task_id}: {e}")

    except Exception as e:
        print(f"[ERROR] Failed in backup task check: {e}")

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
        await bot.send_message(user_id, text, reply_markup=work_buttons_keyboard(task_id), parse_mode="Markdown")
        print(f"[BOT] Sent message to {user_id}: {text}")
    except Exception as e:
        print(f"[ERROR] Failed to send message to {user_id}: {e}")

async def cleanup_old_notifications():
    global sent_notifications
    sent_notifications.clear()
    print("[CLEANUP] - Cleared old notification cache")

_notifier_instance = None

def get_notifier_instance(bot: Bot = None) -> PreciseTaskNotifier:
    global _notifier_instance
    if _notifier_instance is None and bot:
        _notifier_instance = PreciseTaskNotifier(bot, scheduler)
    return _notifier_instance

async def schedule_new_task_notifications(task_id: int, user_id: int, task_name: str, start_time: datetime, language: str):
    notifier = get_notifier_instance()
    if notifier:
        await notifier.schedule_task_notifications(task_id, user_id, task_name, start_time, language)

async def remove_task_notifications(task_id: int):
    notifier = get_notifier_instance()
    if notifier:
        await notifier.remove_task_notifications(task_id)

async def send_morning_message(bot: Bot, user_id: int):
    language = await UserService.get_user_language(user_id) or "ENGLISH"
    user = await UserService.get_user_by_id(user_id)  

    user_name = user.get('user_name', 'User') if user else 'User'

    await bot.send_message(
        user_id,
        MESSAGES[language]['WAKE_UP_MESSAGE'].format(user_name),
        reply_markup=get_start_day_btn()
    )

async def send_evening_message(bot: Bot, user_id: int):
    language = await UserService.get_user_language(user_id) or "ENGLISH"
    stats = await MyDayService.get_today_stats(user_id)
    user = await UserService.get_user_by_id(user_id)

    if not stats:
        created_ideas, completed_tasks, created_tasks, wake_up_time = 0, 0, 0, None
    else:
        created_ideas = stats["created_ideas"]
        completed_tasks = stats["completed_tasks"]
        created_tasks = stats["created_tasks"]
        wake_up_time = stats["wake_up_time"]
        if wake_up_time:
            wake_up_time = wake_up_time.strftime("%H:%M")

    if language.upper() == "UKRANIAN":
        evening_message = (
            f"🌙 Доброго вечора, {user['user_name']}!\n\n"
            "Сподіваюся, твій день був продуктивним 🙌\n"
            "Ось твоя статистика за сьогодні:\n\n"
            f"⏰ Час пробудження: {wake_up_time or '—'}\n"
            f"🚩 Додано завдань: {created_tasks}\n"
            f"✏️ Створено нотаток: {created_ideas}\n"
            f"✅ Виконано завдань: {completed_tasks}\n\n"
            "Бережи сили, завтра новий день 💫"
        )
    else:
        evening_message = (
            f"🌙 Good evening, {user['user_name']}!\n\n"
            "I hope your day was productive 🙌\n"
            "Here’s your daily recap:\n\n"
            f"⏰ Wake up time: {wake_up_time or '—'}\n"
            f"🚩 Tasks added: {created_tasks}\n"
            f"✏️ Notes created: {created_ideas}\n"
            f"✅ Tasks completed: {completed_tasks}\n\n"
            "Recharge well — tomorrow is a new day 💫"
        )

    await bot.send_message(user_id, evening_message)
