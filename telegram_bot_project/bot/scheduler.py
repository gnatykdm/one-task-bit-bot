from datetime import datetime, date, time, timedelta
from sqlalchemy import text
from config import get_session
from service.myday import MyDayService

async def create_or_update_daily_stats_for_users():
    async with get_session() as session:
        result = await session.execute(text("SELECT id FROM users"))
        user_ids = result.scalars().all()

        today = date.today()
        start_of_day = datetime.combine(today, time.min)
        start_of_next_day = start_of_day + timedelta(days=1)

        for user_id in user_ids:
            tasks_result = await session.execute(
                text("""
                    SELECT COUNT(*) FROM tasks 
                    WHERE user_id = :user_id AND creation_date >= :start_of_day AND creation_date < :start_of_next_day
                """),
                {
                    "user_id": user_id,
                    "start_of_day": start_of_day,
                    "start_of_next_day": start_of_next_day
                }
            )
            tasks_count = tasks_result.scalar() or 0

            completed_tasks_result = await session.execute(
                text("""
                    SELECT COUNT(*) FROM tasks
                    WHERE user_id = :user_id AND status = TRUE AND creation_date >= :start_of_day AND creation_date < :start_of_next_day
                """),
                {
                    "user_id": user_id,
                    "start_of_day": start_of_day,
                    "start_of_next_day": start_of_next_day
                }
            )
            completed_tasks_count = completed_tasks_result.scalar() or 0

            ideas_result = await session.execute(
                text("""
                    SELECT COUNT(*) FROM ideas
                    WHERE user_id = :user_id AND creation_date >= :start_of_day AND creation_date < :start_of_next_day
                """),
                {
                    "user_id": user_id,
                    "start_of_day": start_of_day,
                    "start_of_next_day": start_of_next_day
                }
            )
            ideas_count = ideas_result.scalar() or 0

            existing = await session.execute(
                text("""
                    SELECT id FROM daily_stats 
                    WHERE user_id = :user_id AND stats_day_date = CURRENT_DATE
                """),
                {"user_id": user_id}
            )
            stat_id = existing.scalar()

            if stat_id is None:
                await MyDayService.create_daily_stats(
                    user_id=user_id,
                    created_tasks=tasks_count,
                    created_ideas=ideas_count,
                    completed_tasks=completed_tasks_count
                )
            else:
                await session.execute(
                    text("""
                        UPDATE daily_stats
                        SET created_tasks = :created_tasks,
                            created_ideas = :created_ideas,
                            completed_tasks = :completed_tasks
                        WHERE id = :stat_id
                    """),
                    {
                        "created_tasks": tasks_count,
                        "created_ideas": ideas_count,
                        "completed_tasks": completed_tasks_count,
                        "stat_id": stat_id
                    }
                )

        await session.commit()
