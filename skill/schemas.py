from dataclasses import dataclass
from datetime import date, time
import datetime


@dataclass
class Student:
    name: str
    school_id: str
    class_id: str

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other

        return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


@dataclass
class PlannedLesson:
    name: str
    start: time
    end: time

    @property
    def start_time(self):
        return time.strftime(self.start, "%H:%M")

    @property
    def end_time(self):
        return time.strftime(self.end, "%H:%M")

    @property
    def duration(self):
        result = ""
        if self.start and self.end:
            result = f"{self.start_time} - {self.end_time}"
        return result


@dataclass
class Homework:
    lesson: str
    task: str

@dataclass
class NextLesson:
    lesson: str
    date: datetime
    time_start: str
