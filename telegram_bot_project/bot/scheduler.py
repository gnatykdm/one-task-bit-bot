# bot/scheduler.py
from datetime import time
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from messages import *

from messages import send_morning_message, send_evening_message
from service.user import UserService

scheduler: AsyncIOScheduler = AsyncIOScheduler()

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
