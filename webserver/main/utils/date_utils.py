from datetime import datetime, timedelta
import pytz
from funcy import group_by


def get_current_time_ist():
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist).replace(tzinfo=None)


def get_timestamp():
    return int(datetime.now().timestamp())


def get_current_time_utc():
    ist = pytz.utc
    return datetime.now(ist)


def groupify_list_of_datetimes_by_month_year(list_of_datetimes):
    return {key: len(value) for key, value in group_by(lambda s: s.strftime("%Y-%m"), list_of_datetimes).items()}


if __name__ == "__main__":
    print(get_timestamp())
