import datetime
import json
from bs4 import BeautifulSoup, Tag

from classes import *
from settings import *


def _bake_lesson_data(raw_dict: dict[str, str]) -> dict:
    nice_dict = {}

    subject_and_teacher = raw_dict["teacher"].split(",")
    if len(subject_and_teacher) != 2:
        raise Exception(f"Какая то хуйня с ключем 'teacher'. После деления он содержит {len(subject_and_teacher)} элемент(-ов_)")
    date_string = raw_dict["date"].split(" ")[0]

    nice_dict["subject"] = subject_and_teacher[0]
    nice_dict["teacher"] = subject_and_teacher[1]
    nice_dict["date"] = datetime.datetime.strptime(date_string, DATE_FORMAT)
    nice_dict["time"] = raw_dict["time"]
    nice_dict["location"] = raw_dict["lesson"]
    nice_dict["subgroup"] = raw_dict["subgroup"]
    nice_dict["type_"] = raw_dict["type_"]

    return nice_dict


def _get_lesson_type(lesson_element):
    lesson_type_element = lesson_element.find("p", {"class": "card-text rounded-3 text-center"})
    lesson_type = lesson_type_element.text
    return lesson_type


def _get_raw_lesson_data(lesson_element: Tag, is_double_lesson: bool = False) -> dict:
    teacher_cl_button: Tag = lesson_element.find("button", {"class": "btn btn-success teacherCL"})
    teacher_cl_value = teacher_cl_button.attrs["value"]
    teacher_cl_dict = json.loads(teacher_cl_value)

    classroom_button: Tag = lesson_element.find("button", {"class": "btn btn-success classroom"})
    classroom_value = classroom_button.attrs["value"]
    classroom_dict = json.loads(classroom_value)

    data_dict = teacher_cl_dict | classroom_dict

    b_tags = lesson_element.find_all("b")
    data_dict["subgroup"] = b_tags[-1].text
    data_dict["type_"] = _get_lesson_type(lesson_element)
    #
    # if lesson_element.find("a"):
    #     data_dict[""]

    # if is_double_lesson:
    #     b_tags = lesson_element.find_all("b")
    #     for b_tag in b_tags:
    #         if "подгруппа" in b_tag.text:
    #             data_dict["subgroup"] = b_tag.text
    # else:
    #     data_dict["subgroup"] = "Общая"

    return data_dict


def _get_lesson(lesson_element: Tag, is_double_lesson: bool = False) -> Lesson:
    raw_data_dict = _get_raw_lesson_data(lesson_element, is_double_lesson)
    data_dict = _bake_lesson_data(raw_data_dict)

    return Lesson(subject=data_dict["subject"],
                  teacher=data_dict["teacher"],
                  location=data_dict["location"],
                  date=data_dict["date"],
                  time=data_dict["time"],
                  subgroup=data_dict["subgroup"],
                  type_=data_dict["type_"])


def _get_schedule_item(card: Tag) -> ScheduleItem:
    row = card.find("div", {"class": "row"})
    row_items = row.find_all("div")

    if len(row_items) == 2:
        lesson_element = row_items[1]
        lesson = _get_lesson(lesson_element)
        return ScheduleItem(lesson, ScheduleItemType.SINGLE)

    elif len(row_items) == 3:
        lessons: list[Lesson] = []
        for lesson_element in row_items[1:]:
            lesson = _get_lesson(lesson_element, is_double_lesson=True)
            lessons.append(lesson)
        return ScheduleItem(lessons, ScheduleItemType.DOUBLE)

    else:
        raise Exception("Какая то хуйня с содержание карточки (card-body.row). Вруби дебаггер.")


def _get_schedule_items(soup: BeautifulSoup) -> list[ScheduleItem]:
    items: list[ScheduleItem] = []
    cards = soup.find_all("div", {"class": "card-body"})
    for card in cards:
        item = _get_schedule_item(card)
        items.append(item)
    return items


def _get_group(soup: BeautifulSoup) -> int:
    group_parent_element = soup.find("div", {"class": "schedule"})
    group_element = group_parent_element.find("b")
    group_string = group_element.text
    group = int(group_string[-1])
    return group


def _get_date(soup: BeautifulSoup) -> datetime.date:
    date_element = soup.find("input", {"name": "setdate", "class": "form-control"})
    date_string = date_element.attrs["value"]

    date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    date = date.date()
    return date


def _bake_schedule(soup: BeautifulSoup) -> Schedule:
    date = _get_date(soup)
    group = _get_group(soup)

    if not soup.find("div", {"class": "accordion-item"}):
        schedule = Schedule(None, date, group)
    else:
        schedule_items = _get_schedule_items(soup)
        schedule = Schedule(schedule_items, date, group)
    return schedule


def bake_schedules(html_list: list[str]) -> list[Schedule]:
    schedule_list: list[Schedule] = []

    for html in html_list:
        soup = BeautifulSoup(html)
        schedule = _bake_schedule(soup)
        schedule_list.append(schedule)

    return schedule_list
