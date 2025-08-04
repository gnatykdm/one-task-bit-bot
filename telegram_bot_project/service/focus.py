from sqlalchemy import text
from config import get_session
from typing import Optional

class FocusService:
    @staticmethod
    async def create_focus(user_id: int, duration: int, title: Optional[str] = None) -> int:
        async with get_session() as session:
            result = await session.execute(
                text("""
                    INSERT INTO focuses (user_id, duration, title)
                    VALUES (:user_id, :duration, :title)
                    RETURNING id
                """),
                {"user_id": user_id, "duration": duration, "title": title}
            )
            await session.commit()
            return result.scalar_one()

    @staticmethod
    async def get_focus_by_id(focus_id: int) -> Optional[dict]:
        async with get_session() as session:
            result = await session.execute(
                text("SELECT * FROM focuses WHERE id = :id"),
                {"id": focus_id}
            )
            row = result.first()
            return dict(row._mapping) if row else None

    @staticmethod
    async def get_focuses_by_user(user_id: int) -> list[dict]:
        async with get_session() as session:
            result = await session.execute(
                text("""
                    SELECT id, user_id, duration, title, created_at
                    FROM focuses
                    WHERE user_id = :user_id
                    ORDER BY created_at DESC
                """),
                {"user_id": user_id}
            )
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]

    @staticmethod
    async def delete_focus(focus_id: int) -> bool:
        async with get_session() as session:
            result = await session.execute(
                text("DELETE FROM focuses WHERE id = :id"),
                {"id": focus_id}
            )
            await session.commit()
            return result.rowcount == 1
