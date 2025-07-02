from sqlalchemy import text
from config import get_session

class UserService:
    @staticmethod
    async def create_user(user_id: int, user_name: str, language: str = "ENGLISH") -> int:
        async for session in get_session():
            result = await session.execute(
                text("""
                    INSERT INTO users (id, user_name, language)
                    VALUES (:id, :user_name, :language)
                    RETURNING id
                """),
                {"id": user_id, "user_name": user_name, "language": language}
            )
            await session.commit()
            inserted_id = result.scalar_one()
            return inserted_id
        return None

    @staticmethod
    async def get_user_by_id(user_id: int):
        async for session in get_session():
            result = await session.execute(
                text("SELECT * FROM users WHERE id = :id"),
                {"id": user_id}
            )
            row = result.first()
            return dict(row._mapping) if row else None
        return None

    @staticmethod
    async def update_user_language(user_id: int, new_language: str) -> bool:
        async for session in get_session():
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
        return None

    @staticmethod
    async def get_user_language(user_id: int) -> str:
        async for session in get_session():
            result = await session.execute(
                text("SELECT language FROM users WHERE id = :id"),
                {"id": user_id}
            )
            return result.scalar_one_or_none()
        return None
