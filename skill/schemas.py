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
    start: time
    end: time

    @property
    def start_time(self):
        return time.strftime(self.start, "%Н:%M")

    @property
    def end_time(self):
        return time.strftime(self.end, "%Н:%M")

    @property
    def duration(self):
        result = ""
        if self.start and self.end:
            result = f'{self.start_time} - {self.end_time}'
        return result


@dataclass
class Homework:
    lesson: str
    task: str
