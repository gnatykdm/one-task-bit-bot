# bot/utills.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from datetime import datetime, timedelta, time
from channel_subsc import ChannelSubscChecker
import pytz
import asyncio

def format_date(dt: datetime) -> str:
    return dt.strftime("%d.%m.%Y %H:%M")

def check_valid_time(time_str: str) -> bool:
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def calculate_awake_hours(wake_time, sleep_time) -> str:
    if isinstance(wake_time, str):
        wake_time = datetime.strptime(wake_time, "%H:%M").time()
    if isinstance(sleep_time, str):
        sleep_time = datetime.strptime(sleep_time, "%H:%M").time()

    if not wake_time or not sleep_time:
        return "N/A"

    today = datetime.today().date()
    wake_dt = datetime.combine(today, wake_time)
    sleep_dt = datetime.combine(today, sleep_time)

    if sleep_dt <= wake_dt:
        sleep_dt += timedelta(days=1)

    awake_duration = sleep_dt - wake_dt
    total_hours = awake_duration.seconds // 3600
    total_minutes = (awake_duration.seconds % 3600) // 60

    return f"{total_hours}h {total_minutes}m"

def validate_text(text: str) -> bool:
    return text and len(text) <= 100

def validate_time(target_time: time, timezone_str: str) -> bool:
    tz = pytz.timezone(timezone_str)
    now = datetime.now(tz)
    today_target = datetime.combine(now.date(), target_time, tzinfo=tz)
    return today_target > now 

async def check_subscription_procedure(user_id: int, message: Message, channel_name: str) -> bool:
    channel_status: bool = await ChannelSubscChecker.check_subscr_status(user_id)
    if not channel_status:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔗 Subscribe", url=f"https://t.me/{channel_name}")],
                [InlineKeyboardButton(text="✅ Check subscription", callback_data="check_sub")]
            ]
        )
        await message.answer(
            "⚠️ To use this bot, you must subscribe to the channel.",
            reply_markup=kb
        )
        return False
    return True

async def keep_typing_while(chat_id, func, bot):
    cancel = {'cancel': False}

    async def keep_typing():
        while not cancel['cancel']:
            try:
                await bot.send_chat_action(chat_id, 'typing')
            except Exception as e:
                print(f"Failed to send chat action: {e}")
                break
            await asyncio.sleep(5)

    async def executor():
        await func()
        cancel['cancel'] = True

    await asyncio.gather(
        keep_typing(),
        executor(),
    )

async def typing_animation(seconds, bot, chat_id) -> None:
    interval = 1 
    for _ in range(seconds // interval):
        try:
            await bot.send_chat_action(chat_id, 'typing')
        except Exception:
            break
        await asyncio.sleep(interval)
