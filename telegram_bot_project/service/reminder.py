# service/reminder.py
from sqlalchemy import text
from config import get_session
from typing import Any, List, Optional
from datetime import datetime, timedelta

class ReminderService:
    @staticmethod
    async def create_reminder(user_id: int, title: str, remind_time: datetime,
                              remind_status: bool = False) -> int:
        async with get_session() as session:
            result: Any = await session.execute(
                text(
                    """
                    INSERT INTO reminders (user_id, title, remind_status, remind_time)
                    VALUES (:user_id, :title, :remind_status, :remind_time)
                    RETURNING id
                    """
                ),
                {
                    "user_id": user_id,
                    "title": title,
                    "remind_status": remind_status,
                    "remind_time": remind_time
                }
            )
            reminder_id: int = result.scalar_one()
            await session.commit()
            return reminder_id

    @staticmethod
    async def get_reminder_by_id(reminder_id: int) -> Optional[dict]:
        async with get_session() as session:
            result: Any = await session.execute(
                text(
                    """
                    SELECT id, user_id, title, remind_status, remind_time, creation_date
                    FROM reminders
                    WHERE id = :reminder_id
                    """
                ),
                {"reminder_id": reminder_id}
            )
            reminder = result.fetchone()
            if reminder:
                return {
                    "id": reminder.id,
                    "user_id": reminder.user_id,
                    "title": reminder.title,
                    "remind_status": reminder.remind_status,
                    "remind_time": reminder.remind_time,
                    "creation_date": reminder.creation_date
                }
            return None

    @staticmethod
    async def get_user_reminders(user_id: int) -> List[dict]:
        async with get_session() as session:
            result: Any = await session.execute(
                text(
                    """
                    SELECT id, user_id, title, remind_status, remind_time, creation_date
                    FROM reminders
                    WHERE user_id = :user_id
                    ORDER BY creation_date DESC
                    """
                ),
                {"user_id": user_id}
            )
            reminders = result.fetchall()
            return [
                {
                    "id": r.id,
                    "user_id": r.user_id,
                    "title": r.title,
                    "remind_status": r.remind_status,
                    "remind_time": r.remind_time,
                    "creation_date": r.creation_date
                }
                for r in reminders
            ]
    @staticmethod
    async def get_upcoming_reminders() -> List[dict]:
        async with get_session() as session:
            result = await session.execute(
                text(
                    """
                    SELECT id, user_id, title, remind_status, remind_time, creation_date
                    FROM reminders
                    WHERE remind_status = FALSE
                    """
                )
            )
            reminders = result.fetchall()
            return [
                {
                    "id": r.id,
                    "user_id": r.user_id,
                    "title": r.title,
                    "remind_status": r.remind_status,
                    "remind_time": r.remind_time,
                    "creation_date": r.creation_date
                }
                for r in reminders
            ]
            
    @staticmethod
    async def mark_as_sent(reminder_id: int):
        async with get_session() as session:
            await session.execute(
                text("UPDATE reminders SET remind_status = TRUE WHERE id = :id"),
                {"id": reminder_id}
            )
            await session.commit()

    @staticmethod
    async def update_reminder(reminder_id: int, title: Optional[str] = None,
                              remind_status: Optional[bool] = None,
                              remind_time: Optional[datetime] = None) -> bool:
        async with get_session() as session:
            exists: Any = await session.execute(
                text("SELECT 1 FROM reminder WHERE id = :reminder_id"),
                {"reminder_id": reminder_id}
            )
            if not exists.scalar():
                return False

            update_fields: dict = {}
            if title is not None:
                update_fields["title"] = title
            if remind_status is not None:
                update_fields["remind_status"] = remind_status
            if remind_time is not None:
                update_fields["remind_time"] = remind_time

            if update_fields:
                query = text(
                    f"""
                    UPDATE reminders
                    SET {', '.join(f'{k} = :{k}' for k in update_fields.keys())}
                    WHERE id = :reminder_id
                    """
                )
                update_fields["reminder_id"] = reminder_id
                await session.execute(query, update_fields)
                await session.commit()
            return True

    @staticmethod
    async def delete_reminder(reminder_id: int) -> bool:
        async with get_session() as session:
            result: Any = await session.execute(
                text(
                    """
                    DELETE FROM reminders
                    WHERE id = :reminder_id
                    RETURNING id
                    """
                ),
                {"reminder_id": reminder_id}
            )
            deleted = result.scalar_one_or_none()
            await session.commit()
            return deleted is not None

    @staticmethod
    async def toggle_remind_status(reminder_id: int) -> bool:
        async with get_session() as session:
            result: Any = await session.execute(
                text(
                    """
                    UPDATE reminders
                    SET remind_status = NOT remind_status
                    WHERE id = :reminder_id
                    RETURNING id
                    """
                ),
                {"reminder_id": reminder_id}
            )
            updated = result.scalar_one_or_none()
            await session.commit()
            return updated is not None
