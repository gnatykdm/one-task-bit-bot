from typing import List, Dict, Any
import logging
from datetime import datetime
from openai import AsyncOpenAI
from config import get_openai_key
from service.user import UserService
from service.focus import FocusService
from service.idea import IdeaService
from service.routine import RoutineService
from service.task import TaskService

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
        timezone = user.get("timezone", "UTC")
        wake_time = user.get("wake_time", "Not set")
        sleep_time = user.get("sleep_time", "Not set")

        focuses = await FocusService.get_focuses_by_user(user_id)
        ideas = await IdeaService.get_all_ideas_by_user_id(user_id)
        routines = await RoutineService.get_user_routines(user_id)
        tasks = await TaskService.get_user_tasks(user_id)

        context_lines = [
            f"User: {user_name} (Telegram username, not real name)",
            f"First Name: {first_name}",
            f"Second_Name: {second_name}",
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
                context_lines.append(f"   - {f.get('title')} (Created: {f.get('creation_date')})")
        else:
            context_lines.append("• Active Focuses: None")

        if ideas:
            context_lines.append("• Ideas:")
            for i in ideas:
                context_lines.append(
                    f"   - {i.get('idea_name')} "
                    f"(Created: {i.get('creation_date')}, "
                )
        else:
            context_lines.append("• Ideas: None")

        if routines:
            context_lines.append("• Routines:")
            for r in routines:
                context_lines.append(
                    f"   - {r.get('routine_name')} | "
                    f"Schedule: {r.get('schedule', 'Not set')} | "
                    f"Status: {r.get('status', 'Unknown')}"
                )
        else:
            context_lines.append("• Routines: None")

        if tasks:
            context_lines.append(f"• Tasks ({len(tasks)} total):")
            for t in tasks:
                context_lines.append(
                    f"   - {t.get('task_name')} | "
                    f"Status: {t.get('status')} | "
                    f"Start: {t.get('start_time')} | "
                    f"Created: {t.get('creation_date')}"
                )
        else:
            context_lines.append("• Tasks: None")

        return {
            "context_text": "\n".join(context_lines),
            "language": language,
            "timezone": timezone,
            "user_data": {
                "user": user,
                "focuses": focuses,
                "ideas": ideas,
                "routines": routines,
                "tasks": tasks
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
        tasks = await TaskService.get_user_tasks(user_id)
        completed_today = len([t for t in tasks if t.get('status') == 'completed' and 
                              t.get('completed_date') and 
                              t['completed_date'].date() == datetime.now().date()])
        
        routines = await RoutineService.get_user_routines(user_id)
        routines_completed = len([r for r in routines if r.get('last_completed_date') and 
                                 r['last_completed_date'].date() == datetime.now().date()])
        
        ideas = await IdeaService.get_all_ideas_by_user_id(user_id)
        ideas_today = len([i for i in ideas if i.get('created_at') and 
                          i['created_at'].date() == datetime.now().date()])
        
        return {
            "tasks_completed": completed_today,
            "routines_completed": routines_completed,
            "ideas_added": ideas_today,
            "total_pending_tasks": len([t for t in tasks if t.get('status') != 'completed'])
        }
        
    except Exception as e:
        logger.error(f"Error getting daily stats for user {user_id}: {str(e)}")
        return {
            "tasks_completed": 0,
            "routines_completed": 0,
            "ideas_added": 0,
            "total_pending_tasks": 0
        }

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

async def send_evening_message_ai(user_id: int) -> str:
    try:
        context_data = await get_user_context(user_id)
        daily_stats = await get_daily_stats(user_id)
        
        stats_summary = f"""Today's Statistics:
        • Tasks completed: {daily_stats['tasks_completed']}
        • Routines maintained: {daily_stats['routines_completed']}
        • New ideas captured: {daily_stats['ideas_added']}
        • Pending tasks remaining: {daily_stats['total_pending_tasks']}
        """
        
        evening_prompt = f"{EVENING_MESSAGE_PROMPT}\n\n{stats_summary}\n\n{context_data}and add emoji's some for user friendly experience"
        messages = [
            {"role": "user", "content": evening_prompt}
        ]
        
        evening_message = await ask_gpt(
            messages=messages,
            user_id=user_id,
            temperature=0.7,  
            max_tokens=300    
        )
        
        logger.info(f"Generated evening message for user {user_id}")
        return evening_message
        
    except Exception as e:
        logger.error(f"Error generating evening message for user {user_id}: {str(e)}")
        return "Good evening! 🌙 Take a moment to reflect on today's progress. Rest well and get ready for tomorrow's opportunities!"
