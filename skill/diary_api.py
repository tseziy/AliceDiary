from datetime import date, datetime, time
from typing import List

import requests

from skill.schemas import PlannedLesson

URL_DATA = "https://dnevnik2.petersburgedu.ru/api/journal/schedule/"


class NotFoundError(Exception):
    pass


def get_schedule_on_date(id: str, day=None) -> List[PlannedLesson]:

    if day is None:
        day = date.today()

    start_time = datetime.combine(day, time.min)
    finish_time = datetime.combine(day, time.max)

    response = requests.get(
        URL_DATA + "list-by-education-not-auth",
        params={
            "p_educations[]": id,
            "p_datetime_from": datetime.strftime(start_time, "%d.%m.%Y %H:%M:%S"),
            "p_datetime_to": datetime.strftime(finish_time, "%d.%m.%Y %H:%M:%S"),
        },
    )

    if response.status_code == 500:
        return []

    result = []
    for lesson in response.json().get("data", {}).get("items", []):
        lesson_from = datetime.strptime(
            lesson["datetime_from"], "%d.%m.%Y %H:%M:%S"
        ).time()
        lesson_to = datetime.strptime(lesson["datetime_to"], "%d.%m.%Y %H:%M:%S").time()
        result.insert(
            lesson["number"] - 1,
            PlannedLesson(lesson["subject_name"], lesson_from, lesson_to),
        )
    return result
