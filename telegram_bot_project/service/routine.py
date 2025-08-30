# service/routine.py
from sqlalchemy import text
from config import get_session
from typing import Any, List, Optional

class RoutineService:
    @staticmethod
    async def create_routine(user_id: int, routine_type: str, routine_name: str) -> int:
        async with get_session() as session:
            result: Any = await session.execute(
                text(
                    """
                    INSERT INTO routines (user_id, routine_type, routine_name)
                    VALUES (:user_id, :routine_type, :routine_name)
                    RETURNING id
                    """
                ),
                {
                    "user_id": user_id,
                    "routine_type": routine_type,
                    "routine_name": routine_name
                }
            )
            routine_id: int = result.scalar_one()
            await session.commit()
            return routine_id

    @staticmethod
    async def get_routine_id_by_name(routine_name: str) -> Optional[dict]:
        async with get_session() as session:
            result: Any = await session.execute(
                text(
                    """
                    SELECT id
                    FROM routines
                    WHERE routine_name = :routine_name
                    """
                ),
                {"routine_name": routine_name}
            )
            routine = result.fetchone()
            if routine:
                return {"id": routine.id}
            return None

    @staticmethod
    async def get_routine_by_id(routine_id: int) -> Optional[dict]:
        async with get_session() as session:
            result: Any = await session.execute(
                text(
                    """
                    SELECT id, user_id, routine_type, routine_name
                    FROM routines
                    WHERE id = :routine_id
                    """
                ),
                {"routine_id": routine_id}
            )
            routine = result.fetchone()
            if routine:
                return {
                    "id": routine.id,
                    "user_id": routine.user_id,
                    "routine_type": routine.routine_type,
                    "routine_name": routine.routine_name
                }
            return None

    @staticmethod
    async def get_user_routines(user_id: int, routine_type: Optional[str] = None) -> List[dict]:
        async with get_session() as session:
            if routine_type:
                result: Any = await session.execute(
                    text(
                        """
                        SELECT id, user_id, routine_type, routine_name
                        FROM routines
                        WHERE user_id = :user_id AND routine_type = :routine_type
                        ORDER BY id DESC
                        """
                    ),
                    {"user_id": user_id, "routine_type": routine_type}
                )
            else:
                result: Any = await session.execute(
                    text(
                        """
                        SELECT id, user_id, routine_type, routine_name
                        FROM routines
                        WHERE user_id = :user_id
                        ORDER BY id DESC
                        """
                    ),
                    {"user_id": user_id}
                )
            routines = result.fetchall()
            return [
                {
                    "id": r.id,
                    "user_id": r.user_id,
                    "routine_type": r.routine_type,
                    "routine_name": r.routine_name
                }
                for r in routines
            ]

    @staticmethod
    async def update_routine(routine_id: int, routine_name: Optional[str] = None,
                             routine_type: Optional[str] = None) -> bool:
        async with get_session() as session:
            exists: Any = await session.execute(
                text("SELECT 1 FROM routines WHERE id = :routine_id"),
                {"routine_id": routine_id}
            )
            if not exists.scalar():
                return False

            update_fields: dict = {}
            if routine_name is not None:
                update_fields["routine_name"] = routine_name
            if routine_type is not None:
                update_fields["routine_type"] = routine_type

            if update_fields:
                query = text(
                    f"""
                    UPDATE routines
                    SET {', '.join(f'{k} = :{k}' for k in update_fields.keys())}
                    WHERE id = :routine_id
                    """
                )
                update_fields["routine_id"] = routine_id
                await session.execute(query, update_fields)
                await session.commit()
            return True

    @staticmethod
    async def delete_routine(routine_id: int) -> bool:
        async with get_session() as session:
            result: Any = await session.execute(
                text(
                    """
                    DELETE FROM routines
                    WHERE id = :routine_id
                    RETURNING id
                    """
                ),
                {"routine_id": routine_id}
            )
            deleted = result.scalar_one_or_none()
            await session.commit()
            return deleted is not None