from datetime import datetime, timezone


def time_adapter(time):
    return str(time)


def now():
    return datetime.now(timezone.utc).time()
