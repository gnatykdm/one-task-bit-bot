# service/user.py
from sqlalchemy import text
from config import get_session
from typing import Optional, List, Any
from datetime import datetime
from zoneinfo import ZoneInfo
from service.reminder import ReminderService

class UserService:
    @staticmethod
    async def create_user(
        user_id: int,
        user_name: str,
        first_name: str,
        second_name: str,
        language: str = "ENGLISH",
        timezone: str | None = None
    ) -> int:
        async with get_session() as session:
            result = await session.execute(
                text("""
                    INSERT INTO users (id, user_name, first_name, second_name, language, timezone)
                    VALUES (:id, :user_name, :first_name, :second_name, :language, :timezone)
                    RETURNING id
                """),
                {
                    "id": user_id,
                    "user_name": user_name,
                    "first_name": first_name,
                    "second_name": second_name,
                    "language": language,
                    "timezone": timezone,
                }
            )
            await session.commit()
            return result.scalar_one()

    @staticmethod
    async def update_user_timezone(user_id: int, timezone: str):
        async with get_session() as session:
            await session.execute(
                text("UPDATE users SET timezone = :timezone WHERE id = :id"),
                {"timezone": timezone, "id": user_id}
            )
            await session.commit()

    @staticmethod
    async def get_user_timezone(user_id: int) -> str:
        user = await UserService.get_user_by_id(user_id)
        if user:
            return user.get("timezone", "UTC")
        return "UTC"

    @staticmethod
    async def get_all_users() -> list[dict]:
        async with get_session() as session:
            result = await session.execute(
                text("SELECT id, wake_time, sleep_time, timezone FROM users")
            )
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]

    @staticmethod
    async def get_user_by_id(user_id: int):
        async with get_session() as session:
            result = await session.execute(
                text("SELECT * FROM users WHERE id = :id"),
                {"id": user_id}
            )
            row = result.first()
            return dict(row._mapping) if row else None

    @staticmethod
    async def update_user_language(user_id: int, new_language: str) -> bool:
        async with get_session() as session:
            result = await session.execute(
                text("""
                    UPDATE users
                    SET language = :language
                    WHERE id = :id
                """),
                {"language": new_language, "id": user_id}
            )
            await session.commit()
            return result.rowcount == 1

    @staticmethod
    async def get_user_language(user_id: int) -> str:
        async with get_session() as session:
            result = await session.execute(
                text("SELECT language FROM users WHERE id = :id"),
                {"id": user_id}
            )
            return result.scalar_one_or_none()

    @staticmethod
    async def update_wake_time(user_id: int, wake_time: datetime) -> bool:
        async with get_session() as session:
            result = await session.execute(
                text("""
                    UPDATE users
                    SET wake_time = :wake_time
                    WHERE id = :id
                """),
                {"wake_time": wake_time, "id": user_id}
            )
            await session.commit()
            return result.rowcount == 1

    @staticmethod
    async def get_wake_and_sleep_times(user_id: int) -> tuple[datetime, Optional[datetime]]:
        async with get_session() as session:
            result = await session.execute(
                text("""
                    SELECT wake_time, sleep_time
                    FROM users
                    WHERE id = :id
                """),
                {"id": user_id}
            )

            row = result.first()
            if row:
                return row.wake_time, row.sleep_time
            return None, None

    @staticmethod
    async def update_sleep_time(user_id: int, sleep_time: datetime) -> bool:
        async with get_session() as session:
            result = await session.execute(
                text("""
                    UPDATE users
                    SET sleep_time = :sleep_time
                    WHERE id = :id
                """),
                {"sleep_time": sleep_time, "id": user_id}
            )
            await session.commit()
            return result.rowcount == 1

    @staticmethod
    async def get_user_reserved_times(user_id: int) -> List[str]:
        tz_str = await UserService.get_user_timezone(user_id)
        user_tz = ZoneInfo(tz_str or "UTC")

        reserved_times: List[str] = []

        async with get_session() as session:
            result: Any = await session.execute(
                text(
                    """
                    SELECT wake_time, sleep_time
                    FROM users
                    WHERE id = :user_id
                    """
                ),
                {"user_id": user_id}
            )
            row = result.fetchone()

            if row:
                if row[0]:  
                    reserved_times.append(str(row[0]))
                if row[1]:  
                    reserved_times.append(str(row[1]))

        reminders = await ReminderService.get_user_reminders(user_id)
        for r in reminders:
            dt = r.get("remind_time")
            if dt and isinstance(dt, datetime):
                local_time = dt.astimezone(user_tz).strftime("%Y-%m-%d %H:%M")
                reserved_times.append(local_time)

        async with get_session() as session:
            result = await session.execute(
                text(
                    """
                    SELECT start_time
                    FROM tasks
                    WHERE user_id = :user_id
                    AND start_time IS NOT NULL
                    ORDER BY start_time ASC
                    """
                ),
                {"user_id": user_id}
            )
            rows = result.fetchall()

        for row in rows:
            dt = row[0]
            if dt and isinstance(dt, datetime):
                local_time = dt.astimezone(user_tz).strftime("%Y-%m-%d %H:%M")
                reserved_times.append(local_time)

        return reserved_times