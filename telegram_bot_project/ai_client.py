from typing import List, Dict, Any
import logging
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
            f"Preferred Language: {language}",
            f"Timezone: {timezone}",
            f"Wake Time: {wake_time}",
            f"Sleep Time: {sleep_time}",
            "",
            "Current Data:",
            f"• Active Focuses: {', '.join(f['title'] for f in focuses) if focuses else 'None set'}",
            f"• Ideas: {len(ideas)} saved ideas" + (f" ({', '.join(i['idea_name'][:30] + '...' if len(i['idea_name']) > 30 else i['idea_name'] for i in ideas[:3])}{'...' if len(ideas) > 3 else ''})" if ideas else ""),
            f"• Routines: {len(routines)} active routines" + (f" ({', '.join(r['routine_name'] for r in routines[:3])}{'...' if len(routines) > 3 else ''})" if routines else ""),
            f"• Tasks: {len([t for t in tasks if t.get('status') != 'completed'])} pending tasks" if tasks else "• Tasks: No pending tasks"
        ]

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
            "model": kwargs.get("model", "gpt-4o-mini"),
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