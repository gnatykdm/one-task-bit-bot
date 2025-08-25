# service/myday.py
from sqlalchemy import text
from datetime import datetime
from config import get_session
from typing import Any, Optional

class MyDayService:
    @staticmethod
    async def create_daily_stats(
        user_id: int,
        created_tasks: int = 0,
        created_ideas: int = 0,
        completed_tasks: int = 0
    ) -> int:
        async with get_session() as session:
            result: Any = await session.execute(
                text(
                    """
                    INSERT INTO daily_stats (user_id, created_tasks, created_ideas, completed_tasks, stats_day_date)
                    VALUES (:user_id, :created_tasks, :created_ideas, :completed_tasks, CURRENT_DATE)
                    RETURNING id
                    """
                ),
                {
                    "user_id": user_id,
                    "created_tasks": created_tasks,
                    "created_ideas": created_ideas,
                    "completed_tasks": completed_tasks
                }
            )
            stat_id: int = result.scalar_one()
            await session.commit()
            return stat_id

    @staticmethod
    async def create_stats_for_all_users() -> None:
        print("[INFO] - Creating daily stats for all users")
        async with get_session() as session:
            result = await session.execute(
                text("SELECT id FROM users")
            )
            user_ids = [row.id for row in result.fetchall()]

        for user_id in user_ids:
            try:
                await MyDayService.create_daily_stats(user_id)
            except Exception as e:
                print(f"[ERROR] - Failed to create stats for user {user_id}: {e}")

    @staticmethod
    async def get_today_stats(user_id: int) -> Optional[dict]:
        async with get_session() as session:
            result: Any = await session.execute(
                text(
                    """
                    SELECT id, user_id, created_tasks, created_ideas, completed_tasks, wake_up_time, stats_day_date
                    FROM daily_stats
                    WHERE user_id = :user_id AND stats_day_date = CURRENT_DATE
                    """
                ),
                {"user_id": user_id}
            )
            stat = result.fetchone()
            if stat:
                return {
                    "id": stat.id,
                    "user_id": stat.user_id,
                    "created_tasks": stat.created_tasks or 0,
                    "created_ideas": stat.created_ideas or 0,
                    "completed_tasks": stat.completed_tasks or 0,
                    "wake_up_time": stat.wake_up_time,
                    "stats_day_date": stat.stats_day_date,
                }
            return None


    @staticmethod
    async def increment_task_count(user_id: int) -> None:
        async with get_session() as session:
            await session.execute(
                text(
                    """
                    INSERT INTO daily_stats (user_id, created_tasks, completed_tasks, stats_day_date)
                    VALUES (:user_id, 1, 0, CURRENT_DATE)
                    ON CONFLICT (user_id, stats_day_date)
                    DO UPDATE SET created_tasks = daily_stats.created_tasks + 1
                    """
                ),
                {"user_id": user_id}
            )
            await session.commit()

    @staticmethod
    async def increment_idea_count(user_id: int) -> None:
        async with get_session() as session:
            await session.execute(
                text(
                    """
                    INSERT INTO daily_stats (user_id, created_ideas, completed_tasks, stats_day_date)
                    VALUES (:user_id, 1, 0, CURRENT_DATE)
                    ON CONFLICT (user_id, stats_day_date)
                    DO UPDATE SET created_ideas = daily_stats.created_ideas + 1
                    """
                ),
                {"user_id": user_id}
            )
            await session.commit()

    @staticmethod
    async def increment_completed_tasks(user_id: int) -> None:
        async with get_session() as session:
            await session.execute(
                text(
                    """
                    INSERT INTO daily_stats (user_id, completed_tasks, stats_day_date)
                    VALUES (:user_id, 1, CURRENT_DATE) ON CONFLICT (user_id, stats_day_date)
                    DO
                    UPDATE SET completed_tasks = daily_stats.completed_tasks + 1
                    """
                ),
                {"user_id": user_id}
            )
            await session.commit()

    @staticmethod
    async def decrement_task_count(user_id: int) -> None:
        async with get_session() as session:
            await session.execute(
                text(
                    """
                    INSERT INTO daily_stats (user_id, created_tasks, completed_tasks, stats_day_date)
                    VALUES (:user_id, 0, 0, CURRENT_DATE)
                    ON CONFLICT (user_id, stats_day_date)
                    DO UPDATE SET created_tasks = GREATEST(daily_stats.created_tasks - 1, 0)
                    """
                ),
                {"user_id": user_id}
            )
            await session.commit()

    @staticmethod
    async def decrement_idea_count(user_id: int) -> None:
        async with get_session() as session:
            await session.execute(
                text(
                    """
                    INSERT INTO daily_stats (user_id, created_ideas, completed_tasks, stats_day_date)
                    VALUES (:user_id, 0, 0, CURRENT_DATE)
                    ON CONFLICT (user_id, stats_day_date)
                    DO UPDATE SET created_ideas = GREATEST(daily_stats.created_ideas - 1, 0)
                    """
                ),
                {"user_id": user_id}
            )
            await session.commit()

    @staticmethod
    async def decrement_completed_tasks(user_id: int) -> None:
        async with get_session() as session:
            await session.execute(
                text(
                    """
                    INSERT INTO daily_stats (user_id, completed_tasks, stats_day_date)
                    VALUES (:user_id, 0, CURRENT_DATE)
                    ON CONFLICT (user_id, stats_day_date)
                    DO UPDATE SET completed_tasks = GREATEST(daily_stats.completed_tasks - 1, 0)
                    """
                ),
                {"user_id": user_id}
            )
            await session.commit()
        
    @staticmethod
    async def add_wake_up_time(user_id: int, wake_time_str: str) -> None:
        async with get_session() as session:
            try:
                wake_time = datetime.strptime(wake_time_str, "%H:%M").time()
            except ValueError:
                raise ValueError(f"Invalid time format: {wake_time_str}. Expected HH:MM")
            
            query_stats = text(
                """
                UPDATE daily_stats
                SET wake_up_time = :time
                WHERE user_id = :user_id
                """
            )
            await session.execute(query_stats, {"time": wake_time, "user_id": user_id})
            await session.commit()