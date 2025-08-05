from sqlalchemy import text
from config import get_session
from typing import Any, List, Optional
from datetime import datetime, timedelta


class TaskService:
    @staticmethod
    async def create_task(user_id: int, task_name: str, task_status: bool = False, start_time: Optional[datetime] = None) -> int:
        async with get_session() as session:
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

    @staticmethod
    async def get_task_by_id(task_id: int) -> Optional[dict]:
        async with get_session() as session:
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
            task = result.fetchone()
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

    @staticmethod
    async def get_user_tasks(user_id: int) -> List[dict]:
        async with get_session() as session:
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
            tasks = result.fetchall()
            return [
                {
                    "id": task.id,
                    "user_id": task.user_id,
                    "task_name": task.task_name,
                    "status": task.status,
                    "start_time": task.start_time,
                    "creation_date": task.creation_date
                }
                for task in tasks
            ]

    @staticmethod
    async def get_all_upcoming_tasks() -> List[dict]:
        async with get_session() as session:
            now = datetime.now()
            past = now - timedelta(minutes=20)
            future = now + timedelta(minutes=31)
            result = await session.execute(
                text(
                    """
                    SELECT id, user_id, task_name, status, start_time, creation_date
                    FROM tasks
                    WHERE start_time IS NOT NULL
                      AND start_time BETWEEN :past AND :future
                      AND status = FALSE
                    """
                ),
                {"past": past, "future": future}
            )
            tasks = result.fetchall()
            return [
                {
                    "id": task.id,
                    "user_id": task.user_id,
                    "task_name": task.task_name,
                    "status": task.status,
                    "start_time": task.start_time,
                    "creation_date": task.creation_date
                }
                for task in tasks
            ]

    @staticmethod
    async def update_task(task_id: int, task_name: Optional[str] = None,
                          status: Optional[bool] = None,
                          start_time: Optional[datetime] = None) -> bool:
        async with get_session() as session:
            exists: Any = await session.execute(
                text("SELECT 1 FROM tasks WHERE id = :task_id"),
                {"task_id": task_id}
            )
            if not exists.scalar():
                return False

            update_fields: dict = {}
            if task_name is not None:
                update_fields["task_name"] = task_name
            if status is not None:
                update_fields["status"] = status
            if start_time is not None:
                update_fields["start_time"] = start_time

            if update_fields:
                query = text(
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

    @staticmethod
    async def delete_task(task_id: int) -> bool:
        async with get_session() as session:
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
            deleted = result.scalar_one_or_none()
            await session.commit()
            return deleted is not None

    @staticmethod
    async def toggle_task_status(task_id: int) -> bool:
        async with get_session() as session:
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
            updated = result.scalar_one_or_none()
            await session.commit()
            return updated is not None

    @staticmethod
    async def get_started_status(task_id: int) -> bool:
        async with get_session() as session:
            result: Any = await session.execute(
                text(
                    """
                    SELECT started
                    FROM tasks
                    WHERE id = :task_id
                    """
                ),
                {"task_id": task_id}
            )
            started = result.scalar_one_or_none()
            print(f"[DEBUG DB] get_started_status({task_id}) -> {started}")
            return bool(started)

    @staticmethod
    async def update_started_status(task_id):
        async with get_session() as session:
            result: Any = await session.execute(
                text(
                    """
                    UPDATE tasks
                    SET started = TRUE
                    WHERE id = :task_id"""
                ),
                {"task_id": task_id}
            )

            await session.commit()
            return result.rowcount == 1

