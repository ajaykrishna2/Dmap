from datetime import datetime
from datetime import timedelta
from pytz import timezone


def time_date():
    format = "%Y-%m-%d"
    now_utc = datetime.now()
    now_ist = now_utc.astimezone(timezone('Asia/Kolkata'))
    Ist = now_ist.strftime(format)
    yesterday = now_ist - timedelta(days=1)
    yes = yesterday.strftime(format)
    return [yes, Ist]