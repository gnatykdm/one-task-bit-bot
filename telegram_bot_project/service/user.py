from sqlalchemy import text
from config import get_session
from typing import Optional
from datetime import datetime

class UserService:
    @staticmethod
    async def create_user(user_id: int, user_name: str, language: str = "ENGLISH") -> int:
        async with get_session() as session:
            result = await session.execute(
                text("""
                    INSERT INTO users (id, user_name, language)
                    VALUES (:id, :user_name, :language)
                    RETURNING id
                """),
                {"id": user_id, "user_name": user_name, "language": language}
            )
            await session.commit()
            return result.scalar_one()

    @staticmethod
    async def get_all_users() -> list[dict]:
        async with get_session() as session:
            result = await session.execute(
                text("SELECT id, wake_time, sleep_time FROM users")
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
