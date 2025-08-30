# bot/scheduler.py
from datetime import time, datetime, timedelta
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from bot.buttons import work_buttons_keyboard, get_start_day_btn
from service.task import TaskService
from service.user import UserService
from service.reminder import ReminderService
from collections import defaultdict
from typing import Set
from messages import *
from ai_client import *
import pytz
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
SYSTEM_TIMEZONE = os.environ.get('TZ', 'UTC')
logger.info(f"System timezone: {SYSTEM_TIMEZONE}")

scheduler: AsyncIOScheduler = AsyncIOScheduler(timezone=pytz.timezone(SYSTEM_TIMEZONE))
notified_task_ids = set()
sent_notifications: defaultdict[int, Set[str]] = defaultdict(set)
notified_reminder_ids: Set[int] = set()

async def initialize_scheduler(bot: Bot):
    try:
        scheduler.start()
        logger.info("Scheduler started successfully")
        
        await remove_duplicate_jobs()
        await schedule_all_users_jobs(bot)
        
        notifier = get_notifier_instance(bot)
        if notifier:
            await notifier.schedule_all_task_notifications()
        
        scheduler.add_job(
            cleanup_expired_jobs,
            trigger="interval",
            minutes=30,
            id="cleanup_expired_jobs",
            replace_existing=True
        )

        scheduler.add_job(
            check_upcoming_reminders,
            trigger="interval",
            minutes=1,
            id="check_upcoming_reminders",
            replace_existing=True,
            kwargs={"bot": bot}  
        )
        
        logger.info("[STARTUP] Scheduler initialized with cleanup")
        return scheduler
        
    except Exception as e:
        logger.error(f"Failed to initialize scheduler: {e}")
        raise

async def remove_duplicate_jobs():
    try:
        jobs = scheduler.get_jobs()
        job_counts = {}
        to_remove = []
        
        for job in jobs:
            if '_message_' in job.id:
                parts = job.id.split('_')
                if len(parts) >= 3:
                    job_type = parts[0]  
                    user_id = parts[2]   
                    key = f"{job_type}_{user_id}"
                    
                    if key not in job_counts:
                        job_counts[key] = []
                    job_counts[key].append(job)
        
        for key, jobs_list in job_counts.items():
            if len(jobs_list) > 1:
                logger.warning(f"Found {len(jobs_list)} duplicate jobs for {key}")
                cron_job = None
                for job in jobs_list:
                    if 'cron' in str(type(job.trigger)).lower():
                        cron_job = job
                        break
                
                for job in jobs_list:
                    if job != cron_job:
                        to_remove.append(job.id)
        
        for job_id in to_remove:
            try:
                scheduler.remove_job(job_id)
                logger.info(f"Removed duplicate job: {job_id}")
            except Exception as e:
                logger.error(f"Error removing duplicate job {job_id}: {e}")
                
        logger.info(f"Removed {len(to_remove)} duplicate jobs")
        
    except Exception as e:
        logger.error(f"Error in remove_duplicate_jobs: {e}")

async def update_user_job(user_id: int, when: time, bot: Bot, job_type: str, timezone_str: str = None):
    if not when:
        logger.warning(f"No time provided for job '{job_type}' (user_id={user_id})")
        return

    try:
        tz = pytz.timezone(timezone_str) if timezone_str else pytz.UTC
        job_id = f"{job_type}_message_{user_id}"
        job_func = send_morning_message if job_type == "wake" else send_evening_message

        if scheduler.get_job(job_id):
            scheduler.remove_job(job_id)
            logger.info(f"Removed old job: {job_id}")

        scheduler.add_job(
            job_func,
            trigger=CronTrigger(
                hour=when.hour,
                minute=when.minute,
                second=0,
                timezone=tz
            ),
            args=[bot, user_id],
            id=job_id,
            replace_existing=True,
            max_instances=1,
            misfire_grace_time=300
        )

        logger.info(f"Scheduled daily {job_type} job for user {user_id} at {when.strftime('%H:%M')} ({timezone_str})")
        
    except Exception as e:
        logger.error(f"Error scheduling job for user {user_id}: {e}")


async def update_single_user_job(user_id: int, when: time, bot: Bot, job_type: str, timezone_str: str = None):
    if not when:
        logger.warning(f"No time provided for job '{job_type}' (user_id={user_id})")
        return

    try:
        if not timezone_str:
            timezone_str = await UserService.get_user_timezone(user_id) or "UTC"
            
        tz = pytz.timezone(timezone_str)
        job_id = f"{job_type}_message_{user_id}"
        job_func = send_morning_message if job_type == "wake" else send_evening_message

        if scheduler.get_job(job_id):
            scheduler.remove_job(job_id)
            logger.info(f"Removed old job: {job_id}")

        scheduler.add_job(
            job_func,
            trigger=CronTrigger(
                hour=when.hour,
                minute=when.minute,
                second=0,
                timezone=tz
            ),
            args=[bot, user_id],
            id=job_id,
            replace_existing=True,
            max_instances=1,
            misfire_grace_time=300
        )

        logger.info(f"Updated {job_type} job for user {user_id} at {when.strftime('%H:%M')} ({timezone_str})")
        
        now = datetime.now(tz)
        target_time = datetime.combine(now.date(), when)
        target_time = tz.localize(target_time) if target_time.tzinfo is None else target_time.replace(tzinfo=tz)
        time_until_target = (target_time - now).total_seconds()
        
        if 300 < time_until_target <= 86400: 
            today_job_id = f"{job_type}_today_{user_id}"
            
            if scheduler.get_job(today_job_id):
                scheduler.remove_job(today_job_id)
                
            scheduler.add_job(
                job_func,
                trigger=DateTrigger(run_date=target_time),
                args=[bot, user_id],
                id=today_job_id,
                replace_existing=True,
                max_instances=1,
                misfire_grace_time=60
            )
            logger.info(f"Scheduled today's {job_type} message for user {user_id} at {target_time}")
            
        elif time_until_target <= 300:
            logger.info(f"Skipping today's {job_type} job for user {user_id} - too close to execution time ({time_until_target:.0f}s remaining)")
        
    except Exception as e:
        logger.error(f"Error updating job for user {user_id}: {e}")


async def schedule_all_users_jobs(bot: Bot):
    try:
        users = await UserService.get_all_users()
        logger.info(f"Scheduling jobs for {len(users)} users")
        
        successful_schedules = 0
        for user in users:
            user_id = user.get("id")
            user_timezone = await UserService.get_user_timezone(user_id) or "UTC"
            
            try:
                wake_time = user.get("wake_time")
                if wake_time:
                    await update_user_job(
                        user_id=user_id,
                        when=wake_time,
                        bot=bot,
                        job_type="wake",
                        timezone_str=user_timezone
                    )
                    successful_schedules += 1

                sleep_time = user.get("sleep_time")
                if sleep_time:
                    await update_user_job(
                        user_id=user_id,
                        when=sleep_time,
                        bot=bot,
                        job_type="sleep",
                        timezone_str=user_timezone
                    )
                    successful_schedules += 1
                    
            except Exception as e:
                logger.error(f"Failed to schedule jobs for user {user_id}: {e}")
                
        logger.info(f"Successfully scheduled {successful_schedules} jobs")
        
    except Exception as e:
        logger.error(f"Error in schedule_all_users_jobs: {e}")


async def cleanup_expired_jobs():
    try:
        jobs = scheduler.get_jobs()
        removed_count = 0
        now = datetime.now(pytz.UTC)
        
        for job in jobs:
            try:
                if '_today_' in job.id and job.next_run_time:
                    job_time_utc = job.next_run_time.astimezone(pytz.UTC)
                    
                    if (now - job_time_utc).total_seconds() > 300:
                        scheduler.remove_job(job.id)
                        removed_count += 1
                        logger.info(f"Removed expired today job: {job.id}")
                        
            except Exception as e:
                logger.error(f"Error processing job {job.id}: {e}")
                
        if removed_count > 0:
            logger.info(f"Cleaned up {removed_count} expired jobs")
            
    except Exception as e:
        logger.error(f"Error cleaning up expired jobs: {e}")

async def update_user_schedule(user_id: int, wake_time: time = None, sleep_time: time = None, bot: Bot = None):
    try:
        if not bot:
            logger.error("Bot instance is required for updating user schedule")
            return
            
        user_timezone = await UserService.get_user_timezone(user_id) or "UTC"
        
        if wake_time:
            await update_single_user_job(
                user_id=user_id,
                when=wake_time,
                bot=bot,
                job_type="wake",
                timezone_str=user_timezone
            )
            logger.info(f"Updated wake schedule for user {user_id}")
            
        if sleep_time:
            await update_single_user_job(
                user_id=user_id,
                when=sleep_time,
                bot=bot,
                job_type="sleep", 
                timezone_str=user_timezone
            )
            logger.info(f"Updated sleep schedule for user {user_id}")
            
    except Exception as e:
        logger.error(f"Error updating user schedule for {user_id}: {e}")

async def debug_duplicate_jobs():
    try:
        jobs = scheduler.get_jobs()
        job_groups = {}
        
        for job in jobs:
            base_id = job.id.replace('_today_', '_').replace('_next_', '_')
            if base_id not in job_groups:
                job_groups[base_id] = []
            job_groups[base_id].append(job)
        
        duplicates_found = False
        for base_id, jobs_list in job_groups.items():
            if len(jobs_list) > 1:
                duplicates_found = True
                logger.warning(f"DUPLICATE JOBS FOUND for {base_id}:")
                for job in jobs_list:
                    logger.warning(f"  - {job.id}: next run {job.next_run_time}")
        
        if not duplicates_found:
            logger.info("No duplicate jobs found")
            
    except Exception as e:
        logger.error(f"Error in debug_duplicate_jobs: {e}")

async def debug_scheduled_jobs():
    """Отладочная функция для просмотра всех запланированных задач"""
    try:
        jobs = scheduler.get_jobs()
        logger.info(f"=== SCHEDULED JOBS DEBUG ({len(jobs)} total) ===")
        
        for job in jobs:
            logger.info(f"Job ID: {job.id}")
            logger.info(f"  Function: {job.func.__name__}")
            logger.info(f"  Next run: {job.next_run_time}")
            logger.info(f"  Trigger: {job.trigger}")
            logger.info("---")
            
    except Exception as e:
        logger.error(f"Error in debug_scheduled_jobs: {e}")

class PreciseTaskNotifier:
    def __init__(self, bot: Bot, scheduler: AsyncIOScheduler):
        self.bot = bot
        self.scheduler = scheduler
        self.scheduled_jobs = {}

    async def schedule_task_notifications(self, task_id: int, user_id: int, task_name: str, start_time: datetime, language: str, timezone_str: str = "UTC"):
        """Планирование уведомлений для задачи с учетом времени, включая ближайшие"""
        try:
            tz = pytz.timezone(timezone_str)
            now = datetime.now(tz)
            
            if start_time.tzinfo is None:
                start_time = tz.localize(start_time)
            else:
                start_time = start_time.astimezone(tz)
            
            logger.info(f"Scheduling notifications for task {task_id}: {start_time} ({timezone_str})")
            
            if start_time <= now:
                logger.warning(f"Task {task_id} start time is in the past: {start_time} <= {now}")
                return
            
            notification_times = [
                (start_time - timedelta(minutes=30), "30min"),
                (start_time - timedelta(minutes=15), "15min"),
                (start_time - timedelta(minutes=5), "5min"),
                (start_time, "now")
            ]

            scheduled_count = 0
            for notification_time, notification_type in notification_times:
                if notification_time > now:
                    job_id = f"task_{task_id}_{notification_type}"
                    
                    if self.scheduler.get_job(job_id):
                        self.scheduler.remove_job(job_id)
                        logger.debug(f"Removed existing job {job_id}")
                        
                    self.scheduler.add_job(
                        self._send_notification,
                        trigger=DateTrigger(run_date=notification_time, timezone=tz),
                        args=[language, user_id, task_name, notification_type, task_id],
                        id=job_id,
                        replace_existing=True,
                        max_instances=1,
                        misfire_grace_time=300
                    )

                    self.scheduled_jobs[job_id] = True
                    scheduled_count += 1
                    logger.info(f"Scheduled notification {notification_type} for task {task_id} at {notification_time}")
                else:
                    logger.debug(f"Skipping past notification time for task {task_id}: {notification_time} (now: {now})")

            logger.info(f"Successfully scheduled {scheduled_count}/4 notifications for task {task_id}")
            
            if scheduled_count == 0:
                logger.warning(f"No notifications scheduled for task {task_id} - all times are in the past")
            
        except Exception as e:
            logger.error(f"Error scheduling notifications for task {task_id}: {e}")



    async def _send_notification(self, language: str, user_id: int, task_name: str, notification_type: str, task_id: int):
        try:
            await send_task_notification(language, self.bot, user_id, task_name, notification_type, task_id)
            sent_notifications[user_id].add(f"{task_id}_{notification_type}")
            logger.info(f"Notification '{notification_type}' sent for task {task_id} to user {user_id}")
        except Exception as e:
            logger.error(f"Failed to send notification '{notification_type}' for task {task_id} to user {user_id}: {e}")


    async def schedule_all_task_notifications(self):
        try:
            tasks = await TaskService.get_all_upcoming_tasks()
            logger.info(f"Found {len(tasks)} upcoming tasks to schedule")

            successful_schedules = 0
            for task in tasks:
                try:
                    task_time = task.get("start_time")
                    if not task_time:
                        logger.warning(f"Task {task['id']} has no start_time")
                        continue

                    task_id = task["id"]
                    user_id = task["user_id"]
                    task_name = task["task_name"]
                    language = await UserService.get_user_language(user_id)
                    timezone_str = await UserService.get_user_timezone(user_id) or "UTC"
                    
                    await self.schedule_task_notifications(
                        task_id, user_id, task_name, task_time, language, timezone_str
                    )
                    successful_schedules += 1
                    
                except Exception as e:
                    logger.error(f"Failed to schedule notifications for task {task.get('id', 'unknown')}: {e}")

            logger.info(f"Successfully scheduled notifications for {successful_schedules} tasks")
            
        except Exception as e:
            logger.error(f"Error in schedule_all_task_notifications: {e}")

    async def remove_task_notifications(self, task_id: int):
        notification_types = ["30min", "15min", "5min", "now"]
        removed_count = 0
        
        for notification_type in notification_types:
            job_id = f"task_{task_id}_{notification_type}"
            try:
                if self.scheduler.get_job(job_id):
                    self.scheduler.remove_job(job_id)
                    removed_count += 1
                    
                if job_id in self.scheduled_jobs:
                    del self.scheduled_jobs[job_id]
                    
            except Exception as e:
                logger.error(f"Failed to remove notification job {job_id}: {e}")
        
        logger.info(f"Removed {removed_count} notification jobs for task {task_id}")

async def check_scheduler_health():
    try:
        if not scheduler.running:
            logger.error("Scheduler is not running!")
            return False
        
        jobs = scheduler.get_jobs()
        logger.info(f"Scheduler is running with {len(jobs)} active jobs")
        
        for job in jobs[:5]:  
            logger.info(f"Job {job.id}: next run at {job.next_run_time}")
        
        return True
    except Exception as e:
        logger.error(f"Error checking scheduler health: {e}")
        return False

async def check_upcoming_tasks_v2(bot: Bot):
    try:
        tasks = await TaskService.get_all_upcoming_tasks()
        logger.debug(f"Backup check: found {len(tasks)} upcoming tasks")

        for task in tasks:
            try:
                task_time = task.get("start_time")
                if not task_time:
                    continue

                task_id = task["id"]
                user_id = task["user_id"]
                task_name = task["task_name"]
                language: str = await UserService.get_user_language(user_id)
                timezone_str: str = await UserService.get_user_timezone(user_id) or "UTC"

                tz = pytz.timezone(timezone_str)
                
                if task_time.tzinfo is None:
                    task_time = tz.localize(task_time)
                else:
                    task_time = task_time.astimezone(tz)
                    
                now = datetime.now(tz)
                time_diff = (task_time - now).total_seconds()
                time_after_start = (now - task_time).total_seconds()

                logger.debug(f"Task {task_id}: time_diff={time_diff:.0f}s, after_start={time_after_start:.0f}s")

                notifications_to_check = [
                    (1800, 30, "30min"),  
                    (900, 15, "15min"),     
                    (300, 5, "5min"),     
                    (0, 0, "now")         
                ]

                for target_seconds, minutes, notification_type in notifications_to_check:
                    if abs(time_diff - target_seconds) <= 60: 
                        notification_key = f"{task_id}_{notification_type}"
                        if notification_key not in sent_notifications[user_id]:
                            logger.info(f"Backup notification: User {user_id}, Task '{task_name}', type: {notification_type}")
                            await send_task_notification(language, bot, user_id, task_name, notification_type, task_id)
                            sent_notifications[user_id].add(notification_key)

                if time_after_start >= 300:  
                    try:
                        started = await TaskService.get_started_status(task_id)
                        if not started:  
                            for target_minute in [5, 10, 15]:
                                lower = target_minute * 60 - 60
                                upper = target_minute * 60 + 60
                                if lower <= time_after_start <= upper:
                                    reminder_key = f"{task_id}_late_{target_minute}"
                                    if reminder_key not in sent_notifications[user_id]:
                                        logger.info(f"Backup reminder: Task {task_id} after {target_minute} min")
                                        await send_task_notification(language, bot, user_id, task_name, "reminder", task_id)
                                        sent_notifications[user_id].add(reminder_key)
                                        
                    except Exception as e:
                        logger.error(f"Error checking task status for {task_id}: {e}")
                        
            except Exception as e:
                logger.error(f"Error processing task {task.get('id', 'unknown')}: {e}")

    except Exception as e:
        logger.error(f"Error in backup task check: {e}")

async def send_task_notification(language: str, bot: Bot, user_id: int, task_name: str, notification_type: str, task_id: int):
    messages = {
        "UKRANIAN": {
            "30min": f"⏰ Завдання *\"{task_name}\"* почнеться через 30 хвилин!",
            "15min": f"⏰ Завдання *\"{task_name}\"* почнеться через 15 хвилин!",
            "5min":  f"⏰ Завдання *\"{task_name}\"* почнеться через 5 хвилин!",
            "now":   f"🚀 Завдання *\"{task_name}\"* починається прямо зараз!\nПочинаємо?",
            "reminder": f"⚠️ Нагадування: завдання *\"{task_name}\"* мало початися, але не розпочате."
        },
        "ENGLISH": {
            "30min": f"⏰ Task *\"{task_name}\"* will start in 30 minutes!",
            "15min": f"⏰ Task *\"{task_name}\"* will start in 15 minutes!",
            "5min":  f"⏰ Task *\"{task_name}\"* will start in 5 minutes!",
            "now":   f"🚀 Task *\"{task_name}\"* is starting right now!\nStart it?",
            "reminder": f"⚠️ Reminder: task *\"{task_name}\"* was supposed to start but not started yet."
        }
    }

    lang_key = language.upper()
    message_set = messages.get(lang_key, messages["ENGLISH"])
    text = message_set.get(notification_type, message_set["reminder"])

    if notification_type in ["30min", "15min", "5min"]:
        reply_markup = None
    else:
        reply_markup = work_buttons_keyboard(task_id)

    try:
        await bot.send_message(
            user_id,
            text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        logger.info(f"Sent '{notification_type}' notification to user {user_id} for task {task_id}")
    except Exception as e:
        logger.error(f"Failed to send message to user {user_id}: {e}")

async def cleanup_old_notifications():
    global sent_notifications
    old_size = sum(len(notifications) for notifications in sent_notifications.values())
    sent_notifications.clear()
    logger.info(f"Cleaned up {old_size} old notification entries")

_notifier_instance = None

async def check_upcoming_reminders(bot: Bot):
    try:
        reminders = await ReminderService.get_upcoming_reminders()
        logger.info(f"Found {len(reminders)} upcoming reminders")

        now_utc = datetime.now(pytz.UTC)

        for r in reminders:
            reminder_id = r["id"]
            user_id = r["user_id"]
            title = r["title"]
            scheduled_time = r["remind_time"]

            if reminder_id in notified_reminder_ids:
                continue

            timezone_str = await UserService.get_user_timezone(user_id) or "UTC"
            tz = pytz.timezone(timezone_str)

            if scheduled_time.tzinfo is None:
                scheduled_time = tz.localize(scheduled_time)
            else:
                scheduled_time = scheduled_time.astimezone(tz)

            scheduled_time_utc = scheduled_time.astimezone(pytz.UTC)
            now_utc = datetime.now(pytz.UTC)

            if abs((scheduled_time_utc - now_utc).total_seconds()) < 45:
                message = await send_reminder_message(user_id, title)
                try:
                    await bot.send_message(
                        user_id,
                        message,
                        parse_mode="Markdown"
                    )
                    logger.info(f"Sent reminder {reminder_id} to user {user_id}")
                    notified_reminder_ids.add(reminder_id)
                    await ReminderService.mark_as_sent(reminder_id)
                except Exception as e:
                    logger.error(f"Failed to send reminder {reminder_id} to user {user_id}: {e}")

    except Exception as e:
        logger.error(f"Error checking reminders: {e}")

def get_notifier_instance(bot: Bot = None) -> PreciseTaskNotifier:
    global _notifier_instance
    if _notifier_instance is None and bot:
        _notifier_instance = PreciseTaskNotifier(bot, scheduler)
    return _notifier_instance

async def schedule_new_task_notifications(task_id: int, user_id: int, task_name: str, start_time: datetime, language: str):
    try:
        notifier = get_notifier_instance()
        if notifier:
            timezone_str = await UserService.get_user_timezone(user_id) or "UTC"
            await notifier.schedule_task_notifications(task_id, user_id, task_name, start_time, language, timezone_str)
            logger.info(f"Scheduled notifications for new task {task_id} ({task_name}) for user {user_id}")
        else:
            logger.error("Notifier instance not available - cannot schedule task notifications")
    except Exception as e:
        logger.error(f"Error scheduling notifications for new task {task_id}: {e}")

async def remove_task_notifications(task_id: int):
    notifier = get_notifier_instance()
    if notifier:
        await notifier.remove_task_notifications(task_id)

async def send_morning_message(bot: Bot, user_id: int):
    try:
        language = await UserService.get_user_language(user_id) or "ENGLISH"
        user = await UserService.get_user_by_id(user_id)
        user_name = user.get('user_name', 'User') if user else 'User'
        
        await bot.send_message(
            user_id,
            MESSAGES[language]['WAKE_UP_MESSAGE'].format(user_name),
            reply_markup=get_start_day_btn()
        )
        logger.info(f"Sent morning message to user {user_id}")
        
    except Exception as e:
        logger.error(f"Failed to send morning message to user {user_id}: {e}")

async def send_evening_message(bot: Bot, user_id: int):
    message = await send_evening_message_ai(user_id)
    await bot.send_message(user_id, message)
    logger.info(f"Sent evening message to user {user_id}")