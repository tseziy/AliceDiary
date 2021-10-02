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
        return f"{self.name} в {self.time.strftime('%H:%M')}"


@dataclass
class Homework:
    lesson: str
    homework: str
