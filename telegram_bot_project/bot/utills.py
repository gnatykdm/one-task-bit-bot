from datetime import datetime, timedelta

def format_date(dt: datetime) -> str:
    return dt.strftime("%d.%m.%Y %H:%M")

def check_valid_time(time_str: str) -> bool:
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def calculate_awake_hours(wake_time, sleep_time) -> str:
    if isinstance(wake_time, str):
        wake_time = datetime.strptime(wake_time, "%H:%M").time()
    if isinstance(sleep_time, str):
        sleep_time = datetime.strptime(sleep_time, "%H:%M").time()

    if not wake_time or not sleep_time:
        return "N/A"

    today = datetime.today().date()
    wake_dt = datetime.combine(today, wake_time)
    sleep_dt = datetime.combine(today, sleep_time)

    if sleep_dt <= wake_dt:
        sleep_dt += timedelta(days=1)

    awake_duration = sleep_dt - wake_dt
    total_hours = awake_duration.seconds // 3600
    total_minutes = (awake_duration.seconds % 3600) // 60

    return f"{total_hours}h {total_minutes}m"

def validate_text(text: str) -> bool:
    return text and len(text) <= 100