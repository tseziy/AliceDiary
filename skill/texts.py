import random
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


def hello_user_variable(start_text=None):

    hello_mes = [
        """Привет! Это цифровой дневник. Но мы уже знакомы
        Какой вопрос сегодня расписание или домашнее задание?""",
        """Привет! Это цифровой дневник.
        Я могу подсказать расписание уроков или напомнить, что задали домой.""",
    ]

    if start_text is None:
        text = random.choice(hello_mes)

    tts = text
    return text, tts


def mistake():
    text = """Прошу прощения. В навыке возникла непредвиденная ошибка.
    Мы ее обязательно исправим. Возвращайтесь чуть позже."""

    return text, text


def sorry_and_goodbye():
    text = """Прошу прощения. Я очень стараюсь Вас понять.
    Но не получается. Возможно мне надо отдохнуть. Возвращайтесь попозже.
    До свидания!"""

    tts = text
    return text, tts


def maybe_you_need_help():
    text = """Возможно, вам не хватает информации.
    Давайте я расскажу, что умею.
    Рассказать?"""

    tts = text
    return text, tts


def goodbye():
    text = """Возвращайтесь в любое время.
    До свидания!"""
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


def choose_scenario():
    text = "Рассказать что задали сегодня или расписание на завтра?"
    tts = text

    return text, tts


def get_schedule(lessons: List[PlannedLesson]):
    if lessons:
        text = "Список уроков:\n"
        text += "\n".join(str(lesson) for lesson in lessons)
    else:
        text = "Извините, но в расписании ничего нет."
    tts = text

    return text, tts


# region Настройки


def start_setting():
    text = """Надо будет указать школу и класс, который интересует.
    Сейчас добавим одного ученика. Потом можно добавить еще.
    Как зовут ученика?"""

    tts = text
    return text, tts


def start_setting_fallback():
    text = """Простите, что-то я Вас не поняла
    Скажите имя ученика, пожалуйста."""

    tts = "<speaker audio='alice-sounds-human-kids-1.opus'>" + text
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
        "Володя",
        "Максим",
        "Макс",
    ]:
        start_phrase = "Надо же! Одного из создателей навыка тоже так зовут!"
    else:
        start_phrase = "Хорошо."

    text = f"{start_phrase} В какой школе учится? Скажите номер школы"
    tts = text

    return text, tts


def what_school_fallback():
    text = """Простите, что-то я Вас не поняла
    Скажите номер школы, пожалуйста. Например, Лицей 110"""

    tts = "<speaker audio='alice-sounds-human-kids-1.opus'>" + text
    return text, tts


def what_classnumber():
    text = """А в каком классе учится?
    Скажите номер класса. Например, 5 А"""
    tts = """А в каком классе учится?
    Скажите номер класса. Например, пятый - А"""
    return text, tts


def what_classnumber_fallback():
    text = """Простите, что-то я Вас не поняла
    В каком классе сейчас учится? Например, 5 А"""

    tts = """<speaker audio='alice-sounds-human-kids-1.opus'>
    Простите, что-то я Вас не поняла
    В каком классе сейчас учится? Например, пятый - А"""
    return text, tts


def incorrect_classnumber():
    text = """Извините. Похоже Вы назвали неправильный номер класса.
    Нумерация классов начинается с 1 и по 11.
    Повторите, пожалуйста, номер класса? Цифру от 1 до 11"""
    tts = """Извините. Похоже Вы назвали неправильный номер класса.
    Нумерация классов начинается с первого и по одиннадцатый.
    Повторите, пожалуйста, номер класса? Цифру от одного до одиннадцати"""

    return text, tts


def what_classletter():
    text = "Подскажите, какая буква у класса?"
    tts = text

    return text, tts


def what_classlatter_fallback():
    text = """Простите, что-то я Вас не поняла
    Подскажите, какая буква у класса? Например, А"""

    tts = """<speaker audio='alice-sounds-human-kids-1.opus'>
    Простите, что-то я Вас не поняла
    Подскажите, какая буква у класса? Например, А"""
    return text, tts


def incorrect_classletter():
    text = """Извините. Похоже Вы назвали неправильную букву класса.
    Классы содержат буквы от А до Я.
    Повторите, пожалуйста, букву класса? От А до Я"""
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


def discard_settings():
    text = """Ох, ну надо же! Все мы допускаем ошибки. Давайте попробуем еще раз.
    Как зовут ученика?"""

    tts = text
    return text, tts


# endregion
