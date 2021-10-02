from datetime import datetime

from fluentcheck import Check

import skill.diary_api as api

# region Расписание


def test_get_all_lesson_by_date():
    test_date = datetime(2021, 9, 27, 0, 0)
    result = api.get_schedule("5", "1А", day=test_date)
    Check(result).is_list()
    assert len(result) == 4


def test_get_filter_lesson_by_date():
    test_date = datetime(2021, 9, 27, 0, 0)
    lessons = ["Чтение"]
    result = api.get_schedule("5", "1А", day=test_date, lessons=lessons)
    Check(result).is_list()
    assert len(result) == 1


def test_get_filter_lesson_by_date_must_be_empty():
    test_date = datetime(2021, 9, 27, 0, 0)
    lessons = ["Русский язык"]
    result = api.get_schedule("5", "1А", day=test_date, lessons=lessons)
    Check(result).is_list()
    assert len(result) == 0


# endregion


# region Домашнее задание


def test_get_all_homework_by_date():
    test_date = datetime(2021, 9, 28, 0, 0)
    result = api.get_homework("5", "1А", day=test_date)
    Check(result).is_list()
    assert len(result) == 2


def test_get_filter_homework_by_date():
    test_date = "28.09.2021"
    lessons = ["Чтение"]
    result = api.get_homework("5", "1А", day=test_date, lessons=lessons)
    Check(result).is_list()
    assert len(result) == 1


def test_get_filter_homework_by_date_must_be_empty():
    test_date = "28.09.2021"
    lessons = ["Технология"]
    result = api.get_homework("5", "1А", day=test_date, lessons=lessons)
    Check(result).is_list()
    assert len(result) == 0


# endregion
