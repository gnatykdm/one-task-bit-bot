from typing import List, Dict, Any
import logging
from datetime import datetime, timezone as dt_timezone
import pytz
from openai import AsyncOpenAI
from config import get_openai_key
from service.user import UserService
from service.focus import FocusService
from service.idea import IdeaService
from service.routine import RoutineService
from service.task import TaskService
from service.reminder import ReminderService

logger = logging.getLogger(__name__)
client = AsyncOpenAI(api_key=get_openai_key())
SYSTEM_PROMPT_TEMPLATE = """You are Rocky, a helpful AI assistant focused on productivity and personal organization.

Your role:
- Help users manage their tasks, routines, ideas, and focus areas
- Provide personalized advice based on their schedule and preferences
- Communicate in the user's preferred language
- Be encouraging and supportive while staying practical

User Context:
{user_context}

Guidelines:
- Always respond in the user's preferred language ({language})
- Consider their timezone ({timezone}) when discussing time-sensitive matters
- Reference their active focuses, routines, and tasks when relevant
- Keep responses concise but helpful (aim for 2-3 sentences unless more detail is needed)
- If the user asks about something not in their data, politely explain and offer alternative help
"""

EVENING_MESSAGE_PROMPT = """Generate a personalized evening message for the user based on their daily activity and data. 

The message should:
1. Provide a brief summary/statistics of what they accomplished today
2. Include encouraging words about their progress
3. End with a positive wish for tomorrow or good night message
4. Be written in their preferred language
5. Keep it warm, personal, and motivating (2-4 sentences)

Focus on:
- Completed tasks today
- Routines they maintained
- Ideas they captured
- Progress on their focus areas
- Be encouraging even if they had a less productive day

Make it feel personal and supportive, like a friend checking in on their day."""

def get_user_timezone_obj(timezone_str: str) -> pytz.BaseTzInfo:
    """Convert timezone string to timezone object, with fallback to UTC."""
    try:
        return pytz.timezone(timezone_str)
    except pytz.exceptions.UnknownTimeZoneError:
        logger.warning(f"Unknown timezone: {timezone_str}, falling back to UTC")
        return pytz.UTC

def get_user_now(user_timezone: str) -> datetime:
    """Get current datetime in user's timezone."""
    tz = get_user_timezone_obj(user_timezone)
    return datetime.now(tz)

def get_user_today(user_timezone: str) -> datetime.date:
    """Get today's date in user's timezone."""
    return get_user_now(user_timezone).date()

def is_same_date_in_timezone(dt: datetime, target_date: datetime.date, user_timezone: str) -> bool:
    """Check if a datetime falls on the target date in user's timezone."""
    if not dt:
        return False
    
    # If datetime is naive, assume it's in UTC
    if dt.tzinfo is None:
        dt = pytz.UTC.localize(dt)
    
    # Convert to user's timezone
    tz = get_user_timezone_obj(user_timezone)
    dt_in_user_tz = dt.astimezone(tz)
    
    return dt_in_user_tz.date() == target_date

async def get_user_context(user_id: int) -> Dict[str, Any]:
    try:
        user = await UserService.get_user_by_id(user_id)
        if not user:
            return {
                "context_text": "User data not found.",
                "language": "ENGLISH",
                "timezone": "UTC",
                "user_data": None
            }

        user_name = user.get("user_name", "User")
        first_name = user.get("first_name", "Unknown First Name")
        second_name = user.get("second_name", "Unknown Second Name")
        language = user.get("language", "ENGLISH")
        
        # Get timezone from user table or use service method
        try:
            timezone = await UserService.get_user_timezone(user_id)
            if not timezone:
                timezone = user.get("time_zone", "UTC")  # DB column is 'time_zone'
        except Exception as e:
            logger.warning(f"Error getting timezone for user {user_id}: {e}")
            timezone = user.get("time_zone", "UTC")
            
        wake_time = user.get("wake_time", "Not set")
        sleep_time = user.get("sleep_time", "Not set")

        focuses = await FocusService.get_focuses_by_user(user_id)
        ideas = await IdeaService.get_all_ideas_by_user_id(user_id)
        routines = await RoutineService.get_user_routines(user_id)
        tasks = await TaskService.get_user_tasks(user_id)
        reminders = await ReminderService.get_user_reminders(user_id)  

        context_lines = [
            f"User: {user_name} (Telegram username, not real name)",
            f"First Name: {first_name}",
            f"Second Name: {second_name}",
            f"Preferred Language: {language}",
            f"Timezone: {timezone}",
            f"Wake Time: {wake_time}",
            f"Sleep Time: {sleep_time}",
            "",
            "===== Current Data ====="
        ]

        if focuses:
            context_lines.append("• Active Focuses:")
            for f in focuses:
                # DB schema uses 'created_at' for focuses
                context_lines.append(f"   - {f.get('title')} (Created: {f.get('created_at')})")
        else:
            context_lines.append("• Active Focuses: None")

        if ideas:
            context_lines.append("• Ideas:")
            for i in ideas:
                # DB schema uses 'creation_date' for ideas
                context_lines.append(
                    f"   - {i.get('idea_name')} "
                    f"(Created: {i.get('creation_date')})"
                )
        else:
            context_lines.append("• Ideas: None")

        if routines:
            context_lines.append("• Routines:")
            for r in routines:
                # DB schema has 'routine_name' and 'routine_type'
                context_lines.append(
                    f"   - {r.get('routine_name')} | "
                    f"Type: {r.get('routine_type', 'Unknown')}"
                )
        else:
            context_lines.append("• Routines: None")

        if tasks:
            context_lines.append(f"• Tasks ({len(tasks)} total):")
            for t in tasks:
                # DB schema: status is BOOLEAN (not string), uses 'creation_date'
                status = "Completed" if t.get('status') else "Pending"
                started = "Started" if t.get('started') else "Not Started"
                context_lines.append(
                    f"   - {t.get('task_name')} | "
                    f"Status: {status} | "
                    f"Started: {started} | "
                    f"Start Time: {t.get('start_time', 'Not set')} | "
                    f"Created: {t.get('creation_date')}"
                )
        else:
            context_lines.append("• Tasks: None")

        if reminders:
            context_lines.append(f"• Reminders ({len(reminders)} total):")
            for r in reminders:
                # DB schema uses 'remind_status' as BOOLEAN and 'remind_time'
                status = "Completed" if r.get('remind_status') else "Pending"
                context_lines.append(
                    f"   - {r.get('title')} | "
                    f"Time: {r.get('remind_time')} | "
                    f"Status: {status}"
                )
        else:
            context_lines.append("• Reminders: None")

        return {
            "context_text": "\n".join(context_lines),
            "language": language,
            "timezone": timezone,
            "user_data": {
                "user": user,
                "focuses": focuses,
                "ideas": ideas,
                "routines": routines,
                "tasks": tasks,
                "reminders": reminders  
            }
        }

    except Exception as e:
        logger.error(f"Error getting user context for user {user_id}: {str(e)}")
        return {
            "context_text": "Error retrieving user data.",
            "language": "ENGLISH",
            "timezone": "UTC",
            "user_data": None
        }

async def get_daily_stats(user_id: int) -> Dict[str, Any]:
    try:
        # Get user's timezone
        try:
            user_timezone = await UserService.get_user_timezone(user_id)
            if not user_timezone:
                # Fallback to user table's time_zone column
                user = await UserService.get_user_by_id(user_id)
                user_timezone = user.get("time_zone", "UTC") if user else "UTC"
        except Exception as e:
            logger.warning(f"Error getting timezone for user {user_id}: {e}")
            user_timezone = "UTC"
        
        # Get today's date in user's timezone
        today = get_user_today(user_timezone)
        
        # Get user data
        tasks = await TaskService.get_user_tasks(user_id)
        routines = await RoutineService.get_user_routines(user_id)
        ideas = await IdeaService.get_all_ideas_by_user_id(user_id)
        
        # Count completed tasks today (in user's timezone)
        # In DB: status is BOOLEAN (True = completed, False = pending)
        completed_today = 0
        for task in tasks:
            if task.get('status') is True:  # Explicitly check for True (completed)
                # Check if task was created today (no completion_date field in schema)
                # Using creation_date as proxy for completion
                if (task.get('creation_date') and
                    is_same_date_in_timezone(task['creation_date'], today, user_timezone)):
                    completed_today += 1
        
        # Count routines - no completion tracking in schema, so count all active routines
        routines_completed = 0  # Cannot determine from schema
        
        # Count ideas added today (in user's timezone)
        ideas_today = 0
        for idea in ideas:
            # DB schema uses 'creation_date' for ideas
            if (idea.get('creation_date') and 
                is_same_date_in_timezone(idea['creation_date'], today, user_timezone)):
                ideas_today += 1
        
        # Count pending tasks (status = False)
        total_pending_tasks = len([t for t in tasks if t.get('status') is False])
        
        return {
            "tasks_completed": completed_today,
            "routines_completed": routines_completed,
            "ideas_added": ideas_today,
            "total_pending_tasks": total_pending_tasks
        }
        
    except Exception as e:
        logger.error(f"Error getting daily stats for user {user_id}: {str(e)}")
        return {
            "tasks_completed": 0,
            "routines_completed": 0,
            "ideas_added": 0,
            "total_pending_tasks": 0
        }

async def get_evening_message(user_id: int) -> str:
    """Generate a personalized evening message based on daily stats."""
    try:
        context_data = await get_user_context(user_id)
        daily_stats = await get_daily_stats(user_id)
        
        evening_prompt = f"""
            {EVENING_MESSAGE_PROMPT}
            
            Today's Statistics:
            - Tasks completed: {daily_stats['tasks_completed']}
            - Ideas added: {daily_stats['ideas_added']}
            - Pending tasks: {daily_stats['total_pending_tasks']}
            
            User Context:
            {context_data['context_text']}
        """

        messages = [
            {"role": "user", "content": evening_prompt}
        ]

        evening_message = await ask_gpt(
            messages=messages,
            user_id=user_id,
            temperature=0.8,
            max_tokens=200
        )

        logger.info(f"Generated evening message for user {user_id}")
        return evening_message

    except Exception as e:
        logger.error(f"Error generating evening message for user {user_id}: {str(e)}")
        return "Good evening! I hope you had a productive day. Rest well and get ready for tomorrow's opportunities! 🌙"

async def ask_gpt(messages: List[Dict[str, str]], user_id: int, **kwargs) -> str:
    try:
        context_data = await get_user_context(user_id)
        
        system_content = SYSTEM_PROMPT_TEMPLATE.format(
            user_context=context_data["context_text"],
            language=context_data["language"],
            timezone=context_data["timezone"]
        )
        
        api_messages = [
            {"role": "system", "content": system_content},
            *messages
        ]
        
        api_params = {
            "model": kwargs.get("model", "gpt-4o-mini-2024-07-18"),
            "messages": api_messages,
            "max_tokens": kwargs.get("max_tokens", 500),
            "temperature": kwargs.get("temperature", 0.8),
            "presence_penalty": kwargs.get("presence_penalty", 0.1),
            "frequency_penalty": kwargs.get("frequency_penalty", 0.1)
        }
        
        logger.info(f"Making OpenAI API call for user {user_id}")
        response = await client.chat.completions.create(**api_params)
        
        content = response.choices[0].message.content
        if not content:
            logger.warning(f"Empty response from OpenAI for user {user_id}")
            return "I apologize, but I couldn't generate a response. Please try again."
            
        return content.strip()
        
    except Exception as e:
        logger.error(f"Error in ask_gpt for user {user_id}: {str(e)}")
        raise Exception(f"Failed to get AI response: {str(e)}")

async def send_reminder_message(user_id: int, reminder_title: str) -> str:
    try:
        context_data = await get_user_context(user_id)

        reminder_prompt = f"""
            Generate a friendly reminder message for the user.

            Details:
            - Reminder Title: {reminder_title}
            - User Context: {context_data['context_text']}

            Guidelines:
            - Respond in {context_data['language']}
            - Keep the message warm, supportive, and motivating
            - Include 1-2 emojis to make it feel friendly
            - Keep it short (1-2 sentences)
        """

        messages = [
            {"role": "user", "content": reminder_prompt}
        ]

        reminder_message = await ask_gpt(
            messages=messages,
            user_id=user_id,
            temperature=0.7,
            max_tokens=100
        )

        logger.info(f"Generated reminder message for user {user_id}: {reminder_title}")
        return reminder_message

    except Exception as e:
        logger.error(f"Error generating reminder message for user {user_id}: {str(e)}")
        return f"⏰ Reminder: {reminder_title}. Stay on track!"

async def send_evening_message_ai(user_id: int) -> str:
    try:
        context_data = await get_user_context(user_id)
        daily_stats = await get_daily_stats(user_id)

        evening_prompt = f"""
        {EVENING_MESSAGE_PROMPT}

        Today's Summary:
        - ✅ Tasks completed: {daily_stats['tasks_completed']}
        - 📝 Ideas added: {daily_stats['ideas_added']}
        - ⏳ Pending tasks: {daily_stats['total_pending_tasks']}
        - 🌙 Keep up your routines!

        User Context:
        {context_data['context_text']}

        Guidelines:
        - Add friendly emojis where appropriate
        - Keep it 2-4 sentences
        - Encourage the user even if the day was less productive
        """

        messages = [
            {"role": "user", "content": evening_prompt}
        ]

        evening_message = await ask_gpt(
            messages=messages,
            user_id=user_id,
            temperature=0.8,
            max_tokens=200
        )

        logger.info(f"Sent evening message to user {user_id}")
        return evening_message

    except Exception as e:
        logger.error(f"Error sending evening message for user {user_id}: {str(e)}")
        return (
            "🌙 Good evening! I hope you had a productive day. "
            "Keep up the great work and get ready for tomorrow's opportunities! ✨"
        )
