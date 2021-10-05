import random
from typing import List

import pymorphy2
from skill.schemas import Homework, PlannedLesson, Student

morph = pymorphy2.MorphAnalyzer()


def __inflect(word, case):
    return " ".join([morph.parse(x)[-1].inflect(case).word for x in word.split(" ")])


def hello(start_text=None):

    if start_text is None:
        text = (
            "Привет! Это цифровой дневник.\n"
            "Я могу подсказать расписание уроков или напомнить, что задали домой.\n"
            "Но для начала нужно выполнить простые настройки. Готовы продолжить?"
        )

    tts = text
    return text, tts


def hello_user_variable(start_text=None):

    hello_mes = [
        (
            "Привет! Это цифровой дневник. Мы уже знакомы.\n"
            "Какой вопрос сегодня? Расписание или домашнее задание?"
        ),
        (
            "Привет! Это цифровой дневник.\n"
            "Я могу подсказать расписание уроков или напомнить, что задали домой."
        ),
    ]

    if start_text is None:
        text = random.choice(hello_mes)

    tts = text
    return text, tts


def mistake():
    text = (
        "Прошу прощения, в навыке возникла непредвиденная ошибка.\n"
        "Мы её обязательно исправим. Возвращайтесь чуть позже."
    )

    return text, text


def sorry_and_goodbye():
    text = (
        "Прошу прощения, я очень стараюсь вас понять.\n"
        "Но пока не получается. Возможно, мне стоит отдохнуть. Возвращайтесь позже.\n"
        "До свидания!"
    )

    tts = text
    return text, tts


def maybe_you_need_help():
    text = "Попробую вам помочь. Рассказать, что я умею?"

    tts = text
    return text, tts


def goodbye():
    text = "Возвращайтесь в любое время. До свидания!"
    tts = "<speaker audio='alice-sounds-game-loss-3.opus'>" + text
    return text, tts


def help_menu():
    text = "Это меню помощи."
    tts = "Это меню помощи."

    return text, tts


def help_menu_fallback():
    text = (
        "Извините, я вас не поняла. Пожалуйста, повторите.\n"
        'Скажите "Помощь", чтобы вернуться к подсказкам.'
    )

    return text, text


def choose_scenario():
    text = "Рассказать что задали сегодня или расписание на завтра?"
    tts = text

    return text, tts


# region Расписание уроков


def no_schedule():
    text = "По расписанию ничего нет."
    tts = (
        "По расписанию ничего нет."
        "Можно провести этот день с пользой. Погулять или заняться физкультурой."
        "Хотите узнать домашнее задание?"
    )

    return text, tts


def tell_next_lessons(list_of_lessons: List[PlannedLesson]):
    text = "Следующий урок будет "
    tts = text
    lesson = list_of_lessons[0]
    tts += __tell_about_next_lesson(lesson.date.date().strftime("%d.%m.%Y"), 
        lesson.time_start.time().strftime("%H:%M"))
    tts += (
        "sil<[200]> Скажите Повтори, если хотите послушать еще раз."
    )
    return text, tts


def tell_about_schedule(list_of_lessons: List[PlannedLesson]):
    text = "Уроков: " + str(len(list_of_lessons))
    tts = "Всего " + __how_many_lessons(len(list_of_lessons))
    for lesson in list_of_lessons:
        tts += __tell_about_lesson(lesson.name, lesson.end_time)
    tts += (
        "sil<[200]> Скажите Повтори, если хотите послушать еще раз."
        "Хотите узнать домашнее задание?"
    )
    return text, tts


def __tell_about_lesson(lesson: str, time: str):
    return f"sil<[200]> {lesson} начинается в sil<[300]> {time}"


def __tell_about_next_lesson(date_lesson: str, time: str):
    return f"sil<[200]> {date_lesson} начинается в sil<[300]> {time}"


def __how_many_lessons(n: int) -> str:
    tasks = morph.parse("урок")[0].make_agree_with_number(n).word
    return str(n) + " " + tasks


# endregion

# region Настройки


def start_setting():
    text = (
        "Сейчас добавим одного ученика. Затем, можно будет добавить ещё.\n"
        "Как зовут ученика?"
    )

    tts = text
    return text, tts


def start_setting_fallback():
    text = "Простите, я вас не поняла. Скажите имя ученика, пожалуйста."

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

    text = f"{start_phrase} В какой школе учится? Скажите номер школы."
    tts = text

    return text, tts


def what_school_fallback():
    text = (
        "Простите, я вас не поняла.\n"
        "Скажите номер школы, пожалуйста. Например, Лицей 110"
    )

    tts = "<speaker audio='alice-sounds-human-kids-1.opus'>" + text
    return text, tts


def what_classnumber():
    text = "В каком классе учится? Скажите номер класса. Например, 5 А."
    tts = "В каком классе учится? Скажите номер класса. Например, пятый - А."
    return text, tts


def what_classnumber_fallback():
    text = "Простите, я вас не поняла. В каком классе сейчас учится? Например, 5 А."

    tts = (
        "<speaker audio='alice-sounds-human-kids-1.opus'>"
        "Простите, я вас не поняла."
        "В каком классе сейчас учится? Например, пятый А."
    )
    return text, tts


def incorrect_classnumber():
    text = "Извините, я не поняла номер класса. Назовите, пожалуйста, число от 1 до 11"
    tts = "Извините, я не поняла номер класса. Назовите, пожалуйста, число от одного до одиннадцати."

    return text, tts


def what_classletter():
    text = "Какая буква у класса?"
    tts = text

    return text, tts


def what_classlatter_fallback():
    text = "Простите, я вас не поняла. Подскажите, какая буква у класса? Например, А."

    tts = (
        "<speaker audio='alice-sounds-human-kids-1.opus'>"
        "Простите, я вас не поняла."
        "Подскажите, какая буква у класса? Например, А."
    )
    return text, tts


def incorrect_classletter():
    text = "Извините, я не поняла букву класса. Назовите, пожалуйста, букву от А до Я"
    tts = text

    return text, tts


def confirm_settings(name: str, school: str, class_id: str):
    text = (
        "Почти готово. Давайте всё проверим.\n"
        f"{name} учится в {school} школе, в классе {class_id}." + "\n"
        "Всё верно?"
    )
    tts = text

    return text, tts


def one_more_student():
    text = "Здорово! Всё запомнила. Добавим еще одного ученика?"
    tts = text

    return text, tts


def discard_settings():
    text = (
        "Ох, ну надо же! Все мы допускаем ошибки.\n"
        "Давайте попробуем еще раз. Как зовут ученика?"
    )

    tts = text
    return text, tts


def reset_settings():
    text = "Очень жаль! Надеюсь вы ещё вернетесь."
    tts = text

    return text, tts


def confirm_reset():
    text = "Вы уверены, что хотите сбросить все настройки?"
    tts = text

    return text, tts


def reject_reset():
    text = (
        "Уф, а я уже подумала, что вы уходите.\n"
        "Что будем искать, расписание или домашнее задание?"
    )
    tts = text

    return text, tts


# endregion


# region Домашняя работа


def no_next_lessons():
    text = ("В ближайщее время, этого урока не ожидается.")
    tts = text
    return text, tts


def no_homework():
    text = (
        "Ничего не задали. Можно отдохнуть или заняться любимым делом.\n"
        "Хотите узнать расписание уроков?"
    )
    tts = text
    return text, tts


def tell_about_homework(list_of_homework: List[Homework], tasks: int):

    text = f"Заданий: {tasks}"
    tts = "Всего " + __how_many_tasks(tasks)
    for hw in list_of_homework:
        tts += __tell_about_task(hw.lesson, hw.task)
    tts += "sil<[200]> Скажите Повтори, если хотите послушать еще раз"
    if tasks > 3:
        tts += "Скажите Вперед Назад для пролистывания списка"

    return text, tts


def __tell_about_task(lesson: str, task: str):
    return f"sil<[200]> {lesson} sil<[300]> {task}"


def __how_many_tasks(n: int) -> str:
    tasks = morph.parse("задание")[0].make_agree_with_number(n).word
    return str(n) + " " + tasks


# endregion


def not_found(students: list):
    list_of_students = " ,".join(students)

    text = (
        "Не нашла настроек ученика с таким именем.\n"
        "Сейчас вы можете проверить учеников:\n"
        f"{list_of_students}."
    )
    tts = text + "Повторите еще раз, пожалуйста"

    return text, tts


def no_settings():
    text = "Пока что не выполнены базовые настройки.\n" + "Хотите сделать это сейчас?"
    tts = text

    return text, tts


def choose_homework(students: List[Student]):
    text = """Чье домашнее задание хотите узнать?"""
    last = students.pop()
    tts = (
        text
        + " ,".join([__inflect(s.name, {"gent"}).capitalize() for s in students])
        + " или "
        + __inflect(last.name, {"gent"}).capitalize()
    )

    return text, tts


def choose_schedule(students: List[Student]):
    text = """Чье расписание хотите узнать?"""
    last = students.pop()
    tts = (
        text
        + " ,".join([__inflect(s.name, {"gent"}).capitalize() for s in students])
        + " или "
        + __inflect(last.name, {"gent"}).capitalize()
    )

    return text, tts


def choose_student_fallback(students: List[Student]):
    text = "Извините, я вас не поняла.\n" + "Повторите, пожалуйста, имя ученика"
    last = students.pop()
    tts = (
        text
        + " ,".join([__inflect(s.name, {"gent"}).capitalize() for s in students])
        + " или "
        + __inflect(last.name, {"gent"}).capitalize()
    )

    return text, tts


def wrong_student_fallback(students: List[Student]):
    text = (
        "Не нашла настроек ученика с таким именем.\n"
        "Выберите, пожалуйста, имя ученика"
    )
    last = students.pop()
    tts = (
        text
        + " ,".join([__inflect(s.name, {"gent"}).capitalize() for s in students])
        + " или "
        + __inflect(last.name, {"gent"}).capitalize()
    )

    return text, tts
