from datetime import date, time
from typing import List

from skill.schemas import Homework, PlannedLesson


class NotFoundError(Exception):
    pass


def get_school_id_by_name(number: int) -> str:
    if number == 49:
        return "some-school-id"
    raise NotFoundError("school not found")


def get_class_id_by_name(name: str) -> str:
    if name == "7Б":
        return "some-class-id"
    raise NotFoundError("class not found")


def get_schedule(school_id: str, class_id: str, day: date) -> List[PlannedLesson]:
    if school_id == "some-school-id" and class_id == "some-class-id":
        return [
            PlannedLesson("Алгебра", time(9, 0)),
            PlannedLesson("Русский язык", time(9, 45)),
        ]
    raise NotFoundError("Schedule not found")


def get_homework(school_id: str, class_id: str, day: date) -> List[Homework]:
    if school_id == "some-school-id" and class_id == "some-class-id":
        return [Homework("Алгебра", "Примеры №42, №43")]
    raise NotFoundError("homework not found")
