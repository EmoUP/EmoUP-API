"""UTILS
Misc helpers/utils functions
"""

# # Native # #
from time import time
from uuid import uuid4
from typing import Union
from datetime import date, timedelta, datetime

__all__ = ("get_time", "get_uuid", "get_week_timestamp")


def get_time(seconds_precision=True) -> Union[int, float]:
    """Returns the current time as Unix/Epoch timestamp, seconds precision by default"""
    return time() if not seconds_precision else int(time())

def timestamp(date) -> int:
    """Returns the date as Unix/Epoch timestamp, seconds precision by default"""
    return int(datetime.strptime(str(date), "%Y-%m-%d").timestamp())


def get_uuid() -> str:
    """Returns an unique UUID (UUID4)"""
    return str(uuid4())

def get_week_timestamp():
    today = date.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    start = int(datetime.strptime(str(start), "%Y-%m-%d").timestamp())
    end = int(datetime.strptime(str(end), "%Y-%m-%d").timestamp())

    return start,end