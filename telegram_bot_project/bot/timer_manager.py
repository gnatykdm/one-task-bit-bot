from datetime import datetime
from typing import Dict

active_timers: Dict[int, datetime] = {}
active_work: Dict[int, str] = {}

def start_timer(user_id: int):
    active_timers[user_id] = datetime.now()

def stop_timer(user_id: int) -> int:
    start_time = active_timers.pop(user_id, None)
    if start_time:
        elapsed = (datetime.now() - start_time).total_seconds()
        return int(elapsed)
    return 0

def is_timer_running(user_id: int) -> bool:
    return user_id in active_timers