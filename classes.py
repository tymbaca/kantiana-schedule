from typing import NamedTuple
from enum import Enum
import datetime


class Lesson(NamedTuple):
    """
    Базовый класс, содержит инфу о конкретной паре:
        - предмет,
        - время,
        - аудитория,
        - преподаватель,
        - ...
    """
    subject: str
    teacher: str
    location: str
    date: datetime.date
    time: str
    subgroup: str
    type_: str


class ScheduleItemType(Enum):
    SINGLE = 1
    DOUBLE = 2


class ScheduleItem(NamedTuple):
    period: Lesson | list[Lesson]
    item_type: ScheduleItemType = ScheduleItemType.SINGLE


class Schedule(NamedTuple):
    """
    Содержит список из экземпляров класса ____, а также:
        - дата
    """
    items: list[ScheduleItem] | None
    date: datetime.date
    group: int
