from fluentcheck import Check

import skill.diary_api as api


def test_get_all_lesson_by_date():
    test_date = "27.09.2021"
    result = api.get_schedule("5", "1А", day=test_date)
    Check(result).is_list()
    assert len(result) == 4


def test_get_filter_lesson_by_date():
    test_date = "27.09.2021"
    lessons = ["Чтение"]
    result = api.get_schedule("5", "1А", day=test_date, lessons=lessons)
    Check(result).is_list()
    assert len(result) == 1


def test_get_filter_lesson_by_date_must_be_empty():
    test_date = "27.09.2021"
    lessons = ["Русский язык"]
    result = api.get_schedule("5", "1А", day=test_date, lessons=lessons)
    Check(result).is_list()
    assert len(result) == 0


def test_get_all_homework_by_date():
    test_date = "28.09.2021"
    result = api.get_homework("5", "1А", day=test_date)
    Check(result).is_list()
    assert len(result) == 3


def test_get_filter_homework_by_date():
    test_date = "28.09.2021"
    lessons = ["Чтение"]
    result = api.get_homework("5", "1А", day=test_date, lessons=lessons)
    Check(result).is_list()
    assert len(result) == 1


def test_get_filter_homework_by_date_must_be_empty():
    test_date = "28.09.2021"
    lessons = ["Математика"]
    result = api.get_homework("5", "1А", day=test_date, lessons=lessons)
    Check(result).is_list()
    assert len(result) == 0
