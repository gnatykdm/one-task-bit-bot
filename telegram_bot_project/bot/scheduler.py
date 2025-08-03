from apscheduler.schedulers.asyncio import AsyncIOScheduler

def initialize_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.start()
    return scheduler
