from datetime import datetime, timezone, date


def convert_unix_time_to_datetime(unix_time: float) -> datetime:
    return datetime.fromtimestamp(unix_time, tz=timezone.utc)


def convert_unix_time_to_date(unix_time: float) -> date:
    return date.fromtimestamp(unix_time)
