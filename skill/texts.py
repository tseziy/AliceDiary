from typing import List

import pymorphy2

from skill.schemas import PlannedLesson

morph = pymorphy2.MorphAnalyzer()


def __inflect(word, case):
    return " ".join([morph.parse(x)[-1].inflect(case).word for x in word.split(" ")])


def hello(start_text=None):

    if start_text is None:
        text = """Привет! Это цифровой дневник.
        Я могу подсказать расписание уроков или напомнить, что задали домой.
        Но для начала надо выполнить простые настройки.
        Готовы продолжить?"""

    tts = text
    return text, tts


def mistake():
    text = """Прошу прощения. В навыке возникла непредвиденная ошибка.
    Мы ее обязательно исправим. Возвращайтесь чуть позже."""

    return text, text


def goodbye():
    text = "Возвращайтесь в любое время." "До свидания!"
    tts = "<speaker audio='alice-sounds-game-loss-3.opus'>" + text
    return text, tts


def help_menu():
    text = "Это меню помощи."
    tts = "Это меню помощи."

    return text, tts


def help_menu_fallback():
    text = """Извините, я вас не поняла. Пожалуйста, повторите что Вы сказали.
    Скажите "Помощь", чтобы снова получить подсказки."""

    return text, text


def setup():
    #  TODO полноценный сценарий настройки
    text = "Укажите данные учеников"
    tts = text

    return text, tts


def choose_scenario():
    text = "Рассказать что задали сегодня или расписание на завтра?"
    tts = text

    return text, tts


def get_schedule(lessons: List[PlannedLesson]):
    text = "Список уроков:\n"
    text += "\n".join(str(lesson) for lesson in lessons)
    tts = text

    return text, tts


# region Настройки


def start_setting():
    text = """Надо будет указать школу и класс, который интересует.
    Сейчас добавим одного ученика. Потом можно добавить еще.
    Как зовут ученика?"""

    tts = text
    return text, tts


def what_school(name):

    if name == "Алиса":
        start_phrase = "Ух ты! Какое совпадение!"
    elif name in [
        "Андрей",
        "Тимур",
        "Егор",
        "Артем",
        "Артём",
        "Вова",
        "Владимир",
        "Максим",
    ]:
        start_phrase = "Надо же! Одного из моих создателей тоже так зовут!"
    else:
        start_phrase = "Хорошо."

    text = f"{start_phrase} В какой школе учится?"
    tts = text

    return text, tts


def what_classnumber():
    text = "А в каком классе учится?"
    tts = text

    return text, tts


def what_classletter():
    text = "Подскажите, какая буква у класса?"
    tts = text

    return text, tts


def confirm_settings(name: str, school: str, class_id: str):
    text = f"""Так. Давай все проверим.
    {name} учится в {school} школе, в классе {class_id}.
    Все верно?"""
    tts = text

    return text, tts


def one_more_student():
    text = "Здорово! Все запомнила. Добавим еще одного ученика?"
    tts = text

    return text, tts


# endregion
