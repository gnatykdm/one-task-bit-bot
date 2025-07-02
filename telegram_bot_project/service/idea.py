from sqlalchemy import text
from config import get_session

class IdeaService:
    @staticmethod
    async def create_user_idea(user_id: int, idea_name: str) -> int:
        async with get_session() as session:
            query = text("""
                INSERT INTO ideas (user_id, idea_name)
                VALUES (:user_id, :idea_name)
                RETURNING id
            """)
            result = await session.execute(query, {
                "user_id": user_id,
                "idea_name": idea_name
            })
            await session.commit()
            return result.scalar()

    @staticmethod
    async def update_user_idea(idea_id: int, new_name: str) -> None:
        async with get_session() as session:
            query = text("""
                UPDATE ideas
                SET idea_name = :new_name
                WHERE id = :idea_id
            """)
            await session.execute(query, {
                "idea_id": idea_id,
                "new_name": new_name
            })
            await session.commit()

    @staticmethod
    async def delete_user_idea(idea_id: int) -> None:
        async with get_session() as session:
            query = text("""
                DELETE FROM ideas
                WHERE id = :idea_id
            """)
            await session.execute(query, {"idea_id": idea_id})
            await session.commit()

    @staticmethod
    async def get_all_ideas_by_user_id(user_id: int) -> list[dict]:
        async with get_session() as session:
            query = text("""
                SELECT id, idea_name, creation_date
                FROM ideas
                WHERE user_id = :user_id
                ORDER BY creation_date DESC
            """)
            result = await session.execute(query, {"user_id": user_id})
            rows = result.fetchall()
            ideas = [
                {
                    "id": row.id,
                    "idea_name": row.idea_name,
                    "creation_date": row.creation_date
                }
                for row in rows
            ]
            return ideas
