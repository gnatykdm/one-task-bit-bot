from sqlalchemy import text
from config import get_session
from typing import Any, Optional

class MyDayService:
    @staticmethod
    async def create_daily_stats(user_id: int, created_tasks: int = 0, created_ideas: int = 0) -> int:
        async with get_session() as session:
            result: Any = await session.execute(
                text(
                    """
                    INSERT INTO daily_stats (user_id, created_tasks, created_ideas)
                    VALUES (:user_id, :created_tasks, :created_ideas)
                    RETURNING id
                    """
                ),
                {
                    "user_id": user_id,
                    "created_tasks": created_tasks,
                    "created_ideas": created_ideas,
                }
            )
            stat_id: int = result.scalar_one()
            await session.commit()
            return stat_id

    @staticmethod
    async def get_today_stats(user_id: int) -> Optional[dict]:
        async with get_session() as session:
            result: Any = await session.execute(
                text(
                    """
                    SELECT id, user_id, created_tasks, created_ideas, stats_day
                    FROM daily_stats
                    WHERE user_id = :user_id AND DATE(stats_day) = CURRENT_DATE
                    """
                ),
                {"user_id": user_id}
            )
            stat = result.fetchone()
            if stat:
                return {
                    "id": stat.id,
                    "user_id": stat.user_id,
                    "created_tasks": stat.created_tasks,
                    "created_ideas": stat.created_ideas,
                    "stats_day": stat.stats_day
                }
            return None

    @staticmethod
    async def increment_task_count(user_id: int) -> None:
        async with get_session() as session:
            await session.execute(
                text(
                    """
                    INSERT INTO daily_stats (user_id, created_tasks)
                    VALUES (:user_id, 1)
                    ON CONFLICT (user_id, stats_day::date)
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
                    INSERT INTO daily_stats (user_id, created_ideas)
                    VALUES (:user_id, 1)
                    ON CONFLICT (user_id, stats_day::date)
                    DO UPDATE SET created_ideas = daily_stats.created_ideas + 1
                    """
                ),
                {"user_id": user_id}
            )
            await session.commit()
