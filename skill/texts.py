import datetime
import locale
import random
from typing import List

import pymorphy2

from skill.schemas import Homework, PlannedLesson, Student

locale.setlocale(locale.LC_TIME, ("RU", "UTF8"))  # the ru locale is installed
morph = pymorphy2.MorphAnalyzer()


def __inflect(word, case):

    return " ".join([morph.parse(x)[-1].inflect(case).word for x in word.split(" ")])


def hello():

    text = (
        "Привет! Это цифровой дневник для Санкт-Петербурга.\n"
        "Я могу подсказать расписание уроков на любой день.\n"
        "Но для начала нужно выполнить простые настройки. Готовы продолжить?"
    )
    tts = (
        "Привет! Это цифровой дневник для школьников из города Санкт-Петербурга."
        "Я могу подсказать расписание уроков на любой день."
        "Скажите sil<[100]>Что ты умеешь? и расскажу подробнее."
        "Но для начала работы надо выполнить простые настройки. Продолжим?"
        "Если готовы, скажите ДА"
    )

    return text, tts


def todo_list(todo):
    result = ["Привет! Это Цифровой дневник.", "Вот список дел на сегодня."]
    for name, task in todo.items():
        if task[0] == 0 and task[1] == 0:
            result.append(__all_empty(name))
        if task[0] != 0 and task[1] == 0:
            result.append(__only_homework(name, task[0]))
        if task[0] == 0 and task[1] != 0:
            result.append(__only_schedule(name, task[1]))
        if task[0] != 0 and task[1] != 0:
            result.append(__full_work(name, task[0], task[1]))

    result.append("Чтобы проверить домашнее задание, спросите меня. Что задали домой?")
    text = "Список дел на сегодня"
    tts = " ".join(result)

    return text, tts


def __all_empty(name):
    options = [
        f"У {__inflect(name, {'gent'})} нет домашнего задания и расписание пустое.",
        f"{__inflect(name, {'datv'})} повезло: ни домашнего задания, ни уроков.",
    ]

    return random.choice(options)


def __only_homework(name, homework):
    options = [
        f"У {__inflect(name, {'gent'})} только домашняя работа, "
        f"{make_agree_with_number('задание', homework)}.",
        f"{__inflect(name, {'datv'})} нужно сделать домашнее задание. "
        f"{make_agree_with_number('задача', homework)}.",
    ]

    return random.choice(options)


def __only_schedule(name, lessons):
    options = [
        f"У {__inflect(name, {'gent'})} нет домашнего задания."
        f"По расписанию {make_agree_with_number('урок', lessons)}",
        f"{__inflect(name, {'datv'})} домой ничего не задали. "
        f"Сегодня будет {make_agree_with_number('урок', lessons)}",
    ]

    return random.choice(options)


def __full_work(name, homework, lessons):
    options = [
        f"{__inflect(name, {'datv'})} домой задали "
        f"{make_agree_with_number('задание', homework)} "
        f"и по расписанию {make_agree_with_number('урок', lessons)}.",
        f"{__inflect(name, {'datv'})} нужно сделать "
        f"{make_agree_with_number('задача', homework)} "
        f"и сегодня у него {make_agree_with_number('урок', lessons)}.",
    ]

    return random.choice(options)


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


# region Меню помощи


def what_can_i_do():
    text = (
        "Этот навык помогает работать с дневником в школе.\n"
        "Я могу подсказать расписание уроков на любой день.\n"
        "Спросите, например, Какие уроки завтра?\n"
        "Рассказать подробнее, что я умею?"
    )

    tts = (
        "Этот навык помогает работать с дневником в школе.\n"
        "Я могу подсказать расписание уроков на любой день.\n"
        "Спросите, например. Какие уроки завтра?"
        "Рассказать подробнее, что я умею?"
    )

    return text, tts


def help_menu_start(students):
    text = (
        "С помощью этого навыка вы сможете узнать "
        "домашнее задание или расписание в школе.\n"
    )

    if not students:
        text += (
            "Пока что ученики не добавлены.\n" "Для этого перейдите в основное меню\n"
        )
        tts = text
    else:
        text += "Сейчас я знаю таких учеников:\n"
        tts = text
        text += "\n".join(
            [
                f"{student.name} учится в школе "
                f"№{student.school_id} в {student.class_id}."
                for student in students
            ]
        )
        tts += "\n".join(
            [
                f"{student.name} учится в школе номер "
                f"{student.school_id} в {student.class_id} классе."
                for student in students
            ]
        )
        text += (
            "\n"
            "Чтобы изменить настройки нажмите "
            "Сбрось настройки и перезапустите навык.\n"
        )
        tts += (
            "Чтобы изменить настройки скажите "
            "Сбрось настройки и перезапуст+ите навык."
        )

    text += "Хотите расскажу как получить домашнее задание?"
    tts += "Хотите расскажу как получить домашнее задание?"

    return text, tts


def help_menu_homework():
    text = (
        "Чтобы узнать, что задали, скажите:\n"
        '"Какое домашнее задание?"\n'
        "Или, если хотите уточнить предмет:\n"
        '"Что задали на завтра по математике?\n'
        "Если есть несколько учеников, добавьте имя:\n"
        '"Что Алисе задали по риторике на послезавтра"\n'
        "Теперь вы знаете как получить домашнюю работу."
        "А еще я могу подсказать расписание. Рассказать, как?"
    )
    tts = text

    return text, tts


def help_menu_suggest_schedule():
    text = "Ладно. А еще я могу подсказать расписание. Рассказать, как?"
    tts = text

    return text, tts


def help_menu_schedule():
    text = (
        "Чтобы узнать расписание скажите:\n"
        '"Подскажи расписание?"\n'
        "Или, если хотите на определенный день:\n"
        '"Какие уроки завтра?"\n'
        "Если есть несколько учеников, добавьте имя:\n"
        '"Какое расписание у Алисы послезавтра?"\n'
        "Теперь вы знаете как узнать расписание учеников."
        "Хотите расскажу о моих специальных возможностях?"
    )
    tts = text

    return text, tts


def help_menu_suggest_spec():
    text = "Ладно. Хотите расскажу о моих специальных возможностях?"
    tts = text

    return text, tts


def help_menu_spec():
    text = (
        "У меня есть несколько режимов запуска:\n"
        "Можете сказать:\n"
        '"Алиса, запусти навык Цифровой дневник"\n'
        "И попадете в это приложение:\n"
        "А можете сказать:\n"
        '"Алиса, спроси у Цифрового дневника что задали?"\n'
        "Тогда я сразу отвечу на ваш вопрос.\n"
        "Теперь вы знаете как пользоваться навыком. \n"
        'Скажите "Главное меню" или попробуйте узнать домашнее задание.'
    )
    tts = text

    return text, tts


def help_menu_fallback():
    text = (
        "Извините, я вас не поняла. Пожалуйста, повторите.\n"
        'Скажите "Помощь", чтобы узнать как работает навык.'
    )

    return text, text


# endregion

# region Расписание уроков


def no_schedule():

    text = "По расписанию ничего нет."
    tts = (
        "По расписанию ничего нет."
        "Можно провести этот день с пользой. Погулять или заняться физкультурой."
        "Хотите узнать домашнее задание?"
    )

    return text, tts


def tell_about_schedule(list_of_lessons: List[PlannedLesson], lessons):

    text = "Уроков: " + str(lessons)
    tts = "Всего " + __how_many_lessons(lessons)
    for lesson in list_of_lessons:
        tts += __tell_about_lesson(lesson)
    tts += "sil<[200]> Скажите Повтори, если хотите послушать еще раз."
    return text, tts


def __tell_about_lesson(lesson):
    text = lesson.name
    if lesson.count > 1:
        text += " " + str(lesson.count) + " урока"
    return f"sil<[200]> {text}"


def __how_many_lessons(n: int) -> str:
    return make_agree_with_number("урок", n)


def make_agree_with_number(word: str, num: int) -> str:
    return str(num) + " " + morph.parse(word)[0].make_agree_with_number(num).word


# endregion

# region Домашняя работа


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
    else:
        tts += "Хотите узнать расписание уроков?"

    return text, tts


def __tell_about_task(lesson: str, task: str):
    tell_task = (
        task.replace("§", "параграф ")
        .replace("№№", "номера ")
        .replace("№", "номер ")
        .replace("стр.", "страница ")
        .replace("с.", "страница ")
        .replace("упр.", "упражнение ")
        .replace("у.", "упражнение ")
        .replace("ур.", "урок ")
    )
    return f"sil<[200]> {lesson} sil<[300]> {tell_task}"


def __how_many_tasks(n: int) -> str:
    tasks = morph.parse("задание")[0].make_agree_with_number(n).word
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


def duplicate_name():
    text = "Уже добавили ученика с таким именем.\n" "Выберите, пожалуйста, другое имя."

    tts = text
    return text, tts


def start_setting_fallback():
    text = "Простите, я вас не поняла. Скажите имя ученика, пожалуйста."

    tts = "<speaker audio='alice-sounds-human-kids-1.opus'>" + text
    return text, tts


def what_ID(name):

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

    text = (
        f"{start_phrase} Теперь введите идентификатор ученика."
        f"Удобнее всего это сделать на телефоне."
    )
    tts = text

    return text, tts


def get_id_settings_fallback():
    text = (
        "Простите, я вас не поняла. Введите идентификатор ученика"
        "Удобнее всего это сделать на телефоне."
    )
    tts = text

    return text, tts


def confirm_settings(name: str, id: int):
    str_id = str(id)
    split_id = " ".join(str_id[i : i + 1] for i in range(0, len(str_id), 1))
    text = (
        "Почти готово. Давайте всё проверим.\n"
        f"Добавляе {name}.\n"
        f"Идентификатор {id}.\n"
        "Всё верно?"
    )
    tts = (
        "Почти готово. Давайте всё проверим.\n"
        f"Добавляе {name}.\n"
        f"Идентификатор {split_id} "
        "Всё верно?"
    )

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


def no_settings():
    text = "Пока что не выполнены базовые настройки.\n" + "Хотите сделать это сейчас?"
    tts = text

    return text, tts


# region Выбор ученика


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


def not_found(students: list):
    list_of_students = " ,".join(students)

    text = (
        "Не нашла настроек ученика с таким именем.\n"
        "Сейчас вы можете проверить учеников:\n"
        f"{list_of_students}."
    )
    tts = text + "Повторите еще раз, пожалуйста"

    return text, tts


# endregion


def title(student, date):
    if date is None:
        str_date = "Сегодня"
    elif date.date() in KNOWN_DATES:
        str_date = KNOWN_DATES[date.date()]
    else:
        str_date = datetime.date.strftime(date.date(), "%d %B")

    text = student.name.capitalize() + ". " + str_date
    tts = f"У {__inflect(student.name, {'gent'})} на {str_date}"

    return text, tts


def _days_between(d1, d2):

    return abs((d2 - d1).days)


KNOWN_DATES = {
    datetime.date.today(): "Сегодня",
    datetime.date.today() + datetime.timedelta(days=1): "Завтра",
    datetime.date.today() + datetime.timedelta(days=2): "Послезавтра",
    datetime.date.today() + datetime.timedelta(days=-1): "Вчера",
    datetime.date.today() + datetime.timedelta(days=-2): "Позавчера",
}
