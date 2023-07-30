from typing import Dict, NamedTuple
from datetime import timedelta, date
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
"""
    Datatypes
"""

class Url(NamedTuple):
    url: str
    name: str
class Bundle(NamedTuple):
    name: str
    price: float
    description: str
    url: str
    books: list[str]
    time_start: date
    time_end: date
    time_countdown: timedelta


