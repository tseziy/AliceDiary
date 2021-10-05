import datetime
import os
from datetime import date, time
from typing import List

import pandas as pd

from skill.schemas import Homework, PlannedLesson, NextLesson

df = pd.read_csv(
    os.path.abspath("skill/database.csv"),
    sep=";",
    encoding="utf-8",
    dtype="str",
)
df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y")
df["time_start"] = pd.to_datetime(df["time_start"], format="%H:%M")
df["time_end"] = pd.to_datetime(df["time_end"], format="%H:%M")
df["lesson"] = df["lesson"].str.lower()
df.fillna("", inplace=True)


class NotFoundError(Exception):
    pass


def get_schedule(
    school_id: str, class_id: str, day=None, lessons=[]
) -> List[PlannedLesson]:

    all_schedule = df.loc[
        (df["school_id"] == str(school_id)) & (df["class_id"] == str(class_id))
    ]
    if day is None:
        day = date.today()

    schedule = __schedule(all_schedule, day, lessons)
    result = [
        PlannedLesson(row["lesson"], row["time_start"].time(), row["time_end"].time())
        for index, row in schedule.iterrows()
    ]

    return result


def __schedule(schedule: pd.DataFrame, day: date, lessons: list) -> pd.DataFrame:
    lessons_filter = [x.lower() for x in lessons]
    return schedule.loc[
        (schedule["date"] == pd.Timestamp(datetime.datetime.combine(day, time())))
        & (not lessons or schedule["lesson"].isin(lessons_filter))
    ]

def get_date_lessons(school_id: str, class_id: str, lessons=[])-> List[NextLesson]:
    day = date.today()
    all_schedule = df.loc[
        (df["school_id"] == str(school_id)) & (df["class_id"] == class_id)
    ]
    next_lessons = __slice_schedule_next_lessons(all_schedule, day, lessons)
    res = [
        NextLesson(row["lesson"], row["date"], row["time_start"]) for index, row in next_lessons.iterrows()
        ]
    return res

def get_homework(school_id: str, class_id: str, day=None, lessons=[]) -> List[Homework]:
    all_schedule = df.loc[
        (df["school_id"] == str(school_id)) & (df["class_id"] == class_id)
    ]

    if day is not None and lessons:
        hw = __homework_day_lessons(all_schedule, day, lessons)
    elif day is not None and not lessons:
        hw = __homework_day_no_lessons(all_schedule, day)
    elif day is None and lessons:
        hw = __homework_no_day_lessons(all_schedule, lessons)
    elif day is None and not lessons:
        hw = __homework_no_day_no_lessons(all_schedule)
    else:
        raise ValueError("Этого быть не может")

    homework = [
        Homework(row["lesson"], row["homework"]) for index, row in hw.iterrows()
    ]
    return homework


def __homework_day_lessons(schedule: pd.DataFrame, day: date, lessons: list):
    return __slice_schedule(schedule, day, lessons)


def __homework_day_no_lessons(schedule: pd.DataFrame, day: date):
    lessons = [row["lesson"] for index, row in __schedule(schedule, day, []).iterrows()]
    return __slice_schedule(schedule, day, lessons)


def __homework_no_day_lessons(schedule: pd.DataFrame, lessons: list):
    tomorrow = date.today() + datetime.timedelta(days=1)
    return __slice_schedule(schedule, tomorrow, lessons)


def __homework_no_day_no_lessons(schedule: pd.DataFrame):
    today = date.today()
    tomorrow = today + datetime.timedelta(days=1)
    lessons = [
        row["lesson"] for index, row in __schedule(schedule, today, []).iterrows()
    ] + [row["lesson"] for index, row in __schedule(schedule, tomorrow, []).iterrows()]

    return __slice_schedule(schedule, tomorrow, lessons)


def __slice_schedule(schedule: pd.DataFrame, day: date, lessons: list):
    lessons_filter = [x.lower() for x in lessons]
    df_prev = schedule.loc[
        (schedule["date"] <= pd.Timestamp(day))
        & (schedule["lesson"].isin(lessons_filter))
    ]
    homework_group = df_prev.groupby("lesson").agg({"date": "max"})
    homework_slice = schedule.merge(homework_group, on=["date", "lesson"], how="inner")
    homework = homework_slice.loc[(homework_slice["homework"] != "")]

    return homework

def __slice_schedule_next_lessons(schedule: pd.DataFrame, day: date, lessons: list):
    lessons_filter = [x.lower() for x in lessons]
    df_prev = schedule.loc[
        (schedule["date"] > pd.Timestamp(day))
        & (schedule["lesson"].isin(lessons_filter))
    ]

    return df_prev
