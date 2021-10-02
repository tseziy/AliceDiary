from dataclasses import dataclass
from datetime import time


@dataclass
class Student:
    name: str
    school_id: str
    class_id: str


@dataclass
class PlannedLesson:
    name: str
    time: time

    def __str__(self):
        # TODO операция со временем
        return f"{self.name} в {self.time}"


@dataclass
class Homework:
    lesson_name: str
    assignment_text: str
