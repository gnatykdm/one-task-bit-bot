from sqlalchemy import text
from config import get_session
from typing import Any, List, Optional
from datetime import datetime

class TaskService:
    @staticmethod
    async def create_task(user_id: int, task_name: str, task_status: bool = False, start_time: Optional[datetime] = None) -> int:
        async for session in get_session():
            result: Any = await session.execute(
                text(
                    """
                    INSERT INTO tasks (user_id, task_name, status, start_time)
                    VALUES (:user_id, :task_name, :status, :start_time)
                    RETURNING id
                    """
                ),
                {
                    "user_id": user_id,
                    "task_name": task_name,
                    "status": task_status,
                    "start_time": start_time
                }
            )
            task_id: int = result.scalar_one()
            await session.commit()
            return task_id
        return None

    @staticmethod
    async def get_task_by_id(task_id: int) -> Optional[dict]:
        async for session in get_session():
            result: Any = await session.execute(
                text(
                    """
                    SELECT id, user_id, task_name, status, start_time, creation_date
                    FROM tasks
                    WHERE id = :task_id
                    """
                ),
                {"task_id": task_id}
            )
            task: int = result.fetchone()
            if task:
                return {
                    "id": task.id,
                    "user_id": task.user_id,
                    "task_name": task.task_name,
                    "status": task.status,
                    "start_time": task.start_time,
                    "creation_date": task.creation_date
                }
            return None
        return None

    @staticmethod
    async def get_user_tasks(user_id: int) -> List[dict]:
        async for session in get_session():
            result: Any = await session.execute(
                text(
                    """
                    SELECT id, user_id, task_name, status, start_time, creation_date
                    FROM tasks
                    WHERE user_id = :user_id
                    ORDER BY creation_date DESC
                    """
                ),
                {"user_id": user_id}
            )
            return [
                {
                    "id": task.id,
                    "user_id": task.user_id,
                    "task_name": task.task_name,
                    "status": task.status,
                    "start_time": task.start_time,
                    "creation_date": task.creation_date
                }
                for task in result.fetchall()
            ]
        return None

    @staticmethod
    async def update_task(task_id: int, task_name: Optional[str] = None,
                        status: Optional[bool] = None,
                        start_time: Optional[datetime] = None) -> bool:
        async for session in get_session():
            exists: Any = await session.execute(
                text("SELECT 1 FROM tasks WHERE id = :task_id"),
                {"task_id": task_id}
            )
            if not exists.scalar():
                return False

            update_fields: Any = {}
            if task_name is not None:
                update_fields["task_name"] = task_name
            if status is not None:
                update_fields["status"] = status
            if start_time is not None:
                update_fields["start_time"] = start_time

            if update_fields:
                query: Any = text(
                    f"""
                    UPDATE tasks
                    SET {', '.join(f'{k} = :{k}' for k in update_fields.keys())}
                    WHERE id = :task_id
                    """
                )
                update_fields["task_id"] = task_id
                await session.execute(query, update_fields)
                await session.commit()
            return True
        return None

    @staticmethod
    async def delete_task(task_id: int) -> bool:
        async for session in get_session():
            result: Any = await session.execute(
                text(
                    """
                    DELETE FROM tasks
                    WHERE id = :task_id
                    RETURNING id
                    """
                ),
                {"task_id": task_id}
            )
            deleted: Any = result.scalar_one_or_none()
            await session.commit()
            return deleted is not None
        return None

    @staticmethod
    async def toggle_task_status(task_id: int) -> bool:
        async for session in get_session():
            result: Any = await session.execute(
                text(
                    """
                    UPDATE tasks
                    SET status = NOT status
                    WHERE id = :task_id
                    RETURNING id
                    """
                ),
                {"task_id": task_id}
            )
            updated: Any = result.scalar_one_or_none()
            await session.commit()
            return updated is not None
        return None