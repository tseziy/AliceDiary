from dataclasses import asdict, dataclass
from datetime import time

from skill.entities import image_ids, subjects


@dataclass
class Student:
    name: str
    id: str

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other

        return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def dump(self):
        return asdict(self)


@dataclass
class PlannedLesson:
    name: str
    start: time
    end: time

    def __str__(self):
        result = self.name.capitalize()

        return result

    @property
    def start_time(self):
        if self.start is not None:
            return time.strftime(self.start, "%H:%M")
        else:
            return ""

    @property
    def end_time(self):
        if self.end is not None:
            return time.strftime(self.end, "%H:%M")
        else:
            return ""

    @property
    def duration(self):
        result = ""
        if self.start and self.end:
            result = f"{self.start} - {self.end}"
        return result

    @property
    def link_url(self):
        result = ""
        for key, value in subjects.items():
            name_subject = ""
            if self.name.lower() in value:
                name_subject = key
            if not image_ids.get(name_subject) is None:
                result = image_ids[name_subject]

        return result

    def inc(self):
        self.count += 1

    def dump(self):
        return asdict(self)


@dataclass
class Homework:
    lesson: str
    task: str

    @property
    def link_url(self):
        result = ""
        for key, value in subjects.items():
            name_subject = ""
            if self.lesson in value:
                name_subject = key
            if not image_ids.get(name_subject) is None:
                result = image_ids[name_subject]

        return result

    def dump(self):
        return asdict(self)
