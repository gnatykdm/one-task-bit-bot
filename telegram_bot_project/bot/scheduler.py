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

def initialize_scheduler():
    """Инициализация планировщика с правильными настройками"""
    try:
        scheduler.start()
        logger.info("Scheduler started successfully")
        return scheduler
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")
        raise

async def update_user_job(user_id: int, when: time, bot: Bot, job_type: str, timezone_str: str = None):
    if not when:
        logger.warning(f"No time provided for job '{job_type}' (user_id={user_id})")
        return

    try:
        tz = pytz.timezone(timezone_str) if timezone_str else pytz.UTC
        job_id = f"{job_type}_message_{user_id}"
        job_func = send_morning_message if job_type == "wake" else send_evening_message

        # Удаляем старую задачу если существует
        if scheduler.get_job(job_id):
            scheduler.remove_job(job_id)
            logger.info(f"Removed old job: {job_id}")

        # Используем CronTrigger для ежедневного повтора
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


# Упрощенная функция - убираем дублирующие задачи
async def update_single_user_job(user_id: int, when: time, bot: Bot, job_type: str, timezone_str: str = None):
    """Обновление задачи для одного пользователя (используется при изменении времени)"""
    if not when:
        logger.warning(f"No time provided for job '{job_type}' (user_id={user_id})")
        return

    try:
        # Получаем timezone пользователя если не передан
        if not timezone_str:
            timezone_str = await UserService.get_user_timezone(user_id) or "UTC"
            
        tz = pytz.timezone(timezone_str)
        job_id = f"{job_type}_message_{user_id}"
        job_func = send_morning_message if job_type == "wake" else send_evening_message

        # Удаляем старую задачу если существует
        if scheduler.get_job(job_id):
            scheduler.remove_job(job_id)
            logger.info(f"Removed old job: {job_id}")

        # Используем CronTrigger для ежедневного повтора
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
        
        # Проверяем, нужно ли отправить сообщение сегодня
        now = datetime.now(tz)
        target_time = datetime.combine(now.date(), when)
        target_time = tz.localize(target_time)
        
        # Создаем дополнительную задачу на сегодня только если время еще не прошло 
        # И до него осталось больше 2 минут (чтобы избежать дублирования с CronTrigger)
        time_until_target = (target_time - now).total_seconds()
        if time_until_target > 120:  # Больше 2 минут
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
        elif time_until_target > 0:
            logger.info(f"Skipping today's {job_type} job for user {user_id} - too close to CronTrigger execution ({time_until_target:.0f}s remaining)")
        
    except Exception as e:
        logger.error(f"Error updating job for user {user_id}: {e}")


# Упрощенная функция планирования для всех пользователей
async def schedule_all_users_jobs(bot: Bot):
    """Планируем wake и sleep сообщения для всех пользователей с учетом timezone"""
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


# Функция для добавления задачи очистки старых одноразовых задач
async def cleanup_expired_next_jobs():
    """Очищает просроченные одноразовые задачи"""
    try:
        jobs = scheduler.get_jobs()
        removed_count = 0
        
        for job in jobs:
            # Очищаем как _next_ так и _today_ задачи
            if ('_next_' in job.id or '_today_' in job.id) and job.next_run_time and job.next_run_time < datetime.now(job.next_run_time.tzinfo):
                scheduler.remove_job(job.id)
                removed_count += 1
                
        if removed_count > 0:
            logger.info(f"Cleaned up {removed_count} expired jobs")
            
    except Exception as e:
        logger.error(f"Error cleaning up expired jobs: {e}")


# Функция для вызова при изменении времени пользователем
async def update_user_schedule(user_id: int, wake_time: time = None, sleep_time: time = None, bot: Bot = None):
    """Вызывается при изменении расписания пользователя"""
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


# Функция для отладки - показать все запланированные задачи
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
            
            # Время уведомлений
            notification_times = [
                (start_time - timedelta(minutes=30), "30min"),
                (start_time - timedelta(minutes=15), "15min"),
                (start_time - timedelta(minutes=5), "5min"),
                (start_time, "now")
            ]

            scheduled_count = 0
            for notification_time, notification_type in notification_times:
                if notification_time > now - timedelta(seconds=60):
                    job_id = f"task_{task_id}_{notification_type}"
                    if self.scheduler.get_job(job_id):
                        self.scheduler.remove_job(job_id)
                    self.scheduler.add_job(
                        self._send_notification,
                        trigger=DateTrigger(run_date=notification_time, timezone=tz),
                        args=[language, user_id, task_name, notification_type, task_id],
                        id=job_id,
                        replace=True,
                        max_instances=1,
                        misfire_grace_time=300
                    )

                    self.scheduled_jobs[job_id] = True
                    scheduled_count += 1
                    logger.info(f"Scheduled notification {notification_type} for task {task_id} at {notification_time}")
                else:
                    logger.debug(f"Skipping past notification time for task {task_id}: {notification_time}")

            logger.info(f"Scheduled {scheduled_count} notifications for task {task_id}")
            
        except Exception as e:
            logger.error(f"Error scheduling notifications for task {task_id}: {e}")


    async def _send_notification(self, language: str, user_id: int, task_name: str, notification_type: str, task_id: int):
        """Отправка уведомления с учетом типа уведомления"""
        try:
            await send_task_notification(language, self.bot, user_id, task_name, notification_type, task_id)
            sent_notifications[user_id].add(f"{task_id}_{notification_type}")
            logger.info(f"Notification '{notification_type}' sent for task {task_id} to user {user_id}")
        except Exception as e:
            logger.error(f"Failed to send notification '{notification_type}' for task {task_id} to user {user_id}: {e}")


    async def schedule_all_task_notifications(self):
        """ИСПРАВЛЕНИЕ 8: Добавляем детальное логирование"""
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
        """Удаление уведомлений задачи"""
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

# ИСПРАВЛЕНИЕ 9: Добавляем функцию для проверки здоровья планировщика
async def check_scheduler_health():
    """Проверка состояния планировщика"""
    try:
        if not scheduler.running:
            logger.error("Scheduler is not running!")
            return False
        
        jobs = scheduler.get_jobs()
        logger.info(f"Scheduler is running with {len(jobs)} active jobs")
        
        # Логируем информацию о ближайших задачах
        for job in jobs[:5]:  # Показываем первые 5 задач
            logger.info(f"Job {job.id}: next run at {job.next_run_time}")
        
        return True
    except Exception as e:
        logger.error(f"Error checking scheduler health: {e}")
        return False

async def check_upcoming_tasks_v2(bot: Bot):
    """ИСПРАВЛЕНИЕ 10: Улучшенная резервная проверка задач"""
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
                
                # Правильная работа с timezone
                if task_time.tzinfo is None:
                    task_time = tz.localize(task_time)
                else:
                    task_time = task_time.astimezone(tz)
                    
                now = datetime.now(tz)
                time_diff = (task_time - now).total_seconds()
                time_after_start = (now - task_time).total_seconds()

                logger.debug(f"Task {task_id}: time_diff={time_diff:.0f}s, after_start={time_after_start:.0f}s")

                # Проверяем уведомления
                notifications_to_check = [
                    (1800, 30, "30min"),  # 30 минут до
                    (900, 15, "15min"),   # 15 минут до  
                    (300, 5, "5min"),     # 5 минут до
                    (0, 0, "now")         # сейчас
                ]

                for target_seconds, minutes, notification_type in notifications_to_check:
                    if abs(time_diff - target_seconds) <= 60:  # В пределах минуты
                        notification_key = f"{task_id}_{notification_type}"
                        if notification_key not in sent_notifications[user_id]:
                            logger.info(f"Backup notification: User {user_id}, Task '{task_name}', type: {notification_type}")
                            await send_task_notification(language, bot, user_id, task_name, notification_type, task_id)
                            sent_notifications[user_id].add(notification_key)

                # Проверяем напоминания для просроченных задач
                if time_after_start >= 300:  # 5+ минут после начала
                    try:
                        started = await TaskService.get_started_status(task_id)
                        if not started:  # Задача не начата
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
    """Отправка уведомления о задаче с правильной логикой soon/now/reminder"""
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
    """Очистка старых уведомлений"""
    global sent_notifications
    old_size = sum(len(notifications) for notifications in sent_notifications.values())
    sent_notifications.clear()
    logger.info(f"Cleaned up {old_size} old notification entries")

# Глобальный экземпляр уведомителя
_notifier_instance = None

def get_notifier_instance(bot: Bot = None) -> PreciseTaskNotifier:
    global _notifier_instance
    if _notifier_instance is None and bot:
        _notifier_instance = PreciseTaskNotifier(bot, scheduler)
    return _notifier_instance

async def schedule_new_task_notifications(task_id: int, user_id: int, task_name: str, start_time: datetime, language: str):
    """Планирование уведомлений для новой задачи"""
    notifier = get_notifier_instance()
    if notifier:
        timezone_str = await UserService.get_user_timezone(user_id) or "UTC"
        await notifier.schedule_task_notifications(task_id, user_id, task_name, start_time, language, timezone_str)

async def remove_task_notifications(task_id: int):
    """Удаление уведомлений задачи"""
    notifier = get_notifier_instance()
    if notifier:
        await notifier.remove_task_notifications(task_id)

async def send_morning_message(bot: Bot, user_id: int):
    """Отправка утреннего сообщения"""
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
    """Отправка вечернего сообщения"""
    try:
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
                "Here's your daily recap:\n\n"
                f"⏰ Wake up time: {wake_up_time or '—'}\n"
                f"🚩 Tasks added: {created_tasks}\n"
                f"✏️ Notes created: {created_ideas}\n"
                f"✅ Tasks completed: {completed_tasks}\n\n"
                "Recharge well — tomorrow is a new day 💫"
            )

        await bot.send_message(user_id, evening_message)
        logger.info(f"Sent evening message to user {user_id}")
        
    except Exception as e:
        logger.error(f"Failed to send evening message to user {user_id}: {e}")