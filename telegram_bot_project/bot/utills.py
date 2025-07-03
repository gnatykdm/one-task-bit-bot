from datetime import datetime

def format_date(dt: datetime) -> str:
    return dt.strftime("%d.%m.%Y %H:%M")