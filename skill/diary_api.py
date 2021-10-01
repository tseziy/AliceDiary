import os
from datetime import date
from typing import List

import pandas as pd

from skill.schemas import Homework, PlannedLesson

df = pd.read_csv(
    os.path.abspath("skill/database.csv"),
    sep=";",
    encoding="utf-8",
    dtype="str",
)
df.fillna("", inplace=True)


class NotFoundError(Exception):
    pass


def get_schedule(
    school_id: str, class_id: str, day=None, lessons=[]
) -> List[PlannedLesson]:

    result = []

    if day is None:
        day = date.today().strftime("%d.%m.%Y")

    temp = df.loc[
        (df["school_id"] == school_id)
        & (df["class_id"] == class_id)
        & (df["date"] == day)
    ]

    if lessons:
        temp = temp.loc[temp["lesson"].isin(lessons)]

    for index, row in temp.iterrows():
        result.append(PlannedLesson(row["lesson"], row["time_start"]))

    return result


def get_homework(school_id: str, class_id: str, day=None, lessons=[]) -> List[Homework]:

    result = []

    if day is None:
        day = date.today().strftime("%d.%m.%Y")

    temp = df.loc[
        (df["school_id"] == school_id)
        & (df["class_id"] == class_id)
        & (df["homework"] != "")
        & (df["date"] == day)
    ]

    if lessons:
        temp = temp.loc[temp["lesson"].isin(lessons)]

    for index, row in temp.iterrows():
        result.append(Homework(row["lesson"], row["homework"]))

    return result
