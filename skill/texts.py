import random
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

# test
def __inflect(word, case):
    return " ".join([morph.parse(x)[-1].inflect(case).word for x in word.split(" ")])


def hello(start_text=None):

    if start_text is None:
        text = (
            "Привет! Это цифровой дневник."
            "Я могу подсказать расписание уроков или напомнить, что задали домой."
            "Но для начала надо выполнить простые настройки."
            "Готовы продолжить?"
        )
    tts = text
    return text, tts


def mistake():
    text = (
        "Прошу прощения. В навыке возникла непредвиденная ошибка."
        "Мы ее обязательно исправим. Возвращайтесь чуть позже."
    )

    return text, text


def goodbye():
    text = (
        "Возвращайтесь в любое время."
        "До свидания!"
    )
    tts = "<speaker audio='alice-sounds-game-loss-3.opus'>" + text
    return text, tts


def help_menu():
    text = "Это меню помощи."
    tts = "Это меню помощи."

    return text, tts


def help_menu_fallback():
    text = f"""Извините, я вас не понял. Пожалуйста, повторите что Вы сказали.
                Скажите "Помощь", чтобы снова получить подсказки."""

    return text, text
