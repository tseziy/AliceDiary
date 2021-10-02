import os
from datetime import date
from typing import List

import pandas
import pandas as pd

from skill.schemas import Homework, PlannedLesson

df = pd.read_csv(
    os.path.abspath("skill/database.csv"),
    sep=";",
    encoding="utf-8",
    dtype="str",
)
df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y")
df.fillna("", inplace=True)


class NotFoundError(Exception):
    pass


def get_schedule(
    school_id: str, class_id: str, day=None, lessons=[]
) -> List[PlannedLesson]:

    all_schedule = df.loc[(df["school_id"] == str(school_id)) & (df["class_id"] == str(class_id))]
    if day is None:
        day = date.today()

    schedule = __schedule(all_schedule, day, lessons)
    result = [
        PlannedLesson(row["lesson"], row["time_start"])
        for index, row in schedule.iterrows()
    ]

    return result


def __schedule(schedule: pandas.DataFrame, day: date, lessons: list):
    return schedule.loc[
        (schedule["date"] == pd.Timestamp(pd.Timestamp(day.combine(day.date(), day.min.time()))))
        & (not lessons or schedule["lesson"].isin(lessons))
    ]


def get_homework(school_id: str, class_id: str, day=None, lessons=[]) -> List[Homework]:
    all_schedule = df.loc[(df["school_id"] == school_id) & (df["class_id"] == class_id)]

    if day is not None and lessons:
        hw = __homework_day_lessons(all_schedule, day, lessons)
    elif day is not None and not lessons:
        hw = __homework_day_no_lessons(all_schedule, day)
    elif day is None and lessons:
        hw = __homework_no_day_lessons(all_schedule, lessons)
    elif day is None and not lessons():
        hw = __homework_no_day_no_lessons(all_schedule)
    else:
        raise Exception("Этого быть не может")

    homework = [
        Homework(row["lesson"], row["homework"]) for index, row in hw.iterrows()
    ]
    return homework


def __homework_day_lessons(schedule: pandas.DataFrame, day: date, lessons: list):
    return __slice_schedule(schedule, day, lessons)


def __homework_day_no_lessons(schedule: pandas.DataFrame, day: date):
    lessons = [row["lesson"] for index, row in __schedule(schedule, day, []).iterrows()]
    return __slice_schedule(schedule, day, lessons)


def __homework_no_day_lessons(schedule: pandas.DataFrame, lessons: list):
    day = date.today() + date.timedelta(days=1)
    return __slice_schedule(schedule, day, lessons)


def __homework_no_day_no_lessons(schedule: pandas.DataFrame):
    today = date.today()
    tomorrow = date.today() + date.timedelta(days=1)
    lessons = [
        row["lesson"] for index, row in __schedule(schedule, today, []).iterrows()
    ] + [row["lesson"] for index, row in __schedule(schedule, tomorrow, []).iterrows()]

    return __slice_schedule(schedule, tomorrow, lessons)


def __slice_schedule(schedule: pandas.DataFrame, day: date, lessons: list):

    df_prev = schedule.loc[
        (schedule["date"] <= pd.Timestamp(day)) & (schedule["lesson"].isin(lessons))
    ]
    df_prev = df_prev.groupby("lesson").agg({"date": "max"})
    slice = schedule.merge(df_prev, on=["date", "lesson"], how="inner")
    homework = slice.loc[(slice["homework"] != "")]

    return homework
