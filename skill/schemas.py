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


@dataclass
class Homework:
    lesson: str
    task: str
