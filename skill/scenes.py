import inspect
import sys
from dataclasses import asdict
from typing import List

from skill import diary_api, entities, intents, state, texts
from skill.alice import Request, button, image_button, image_list
from skill.dates_transformations import (
    transform_yandex_datetime_value_to_datetime as ya_date_transform,
)
from skill.scenes_util import Scene
from skill.schemas import Homework, PlannedLesson, Student

# region Общие сцены

# класс общая сцена


class GlobalScene(Scene):
    def reply(self, request: Request):
        pass  # Здесь не нужно пока ничего делать

    def handle_global_intents(self, request):
        if (
            intents.HELP in request.intents
            or intents.WHAT_CAN_YOU_DO in request.intents
        ):
            return HelpMenu()
        if intents.GET_HOMEWORK in request.intents:
            return GetHomework()
        if intents.GET_SCHEDULE in request.intents:
            return GetSchedule()
        if intents.RESET in request.intents:
            return Settings_Reset()

    def handle_local_intents(self, request: Request):
        pass  # Здесь не нужно пока ничего делать

    def fallback(self, request: Request):
        if request.session.get(state.NEED_FALLBACK, False):
            text, tts = texts.sorry_and_goodbye()
            return self.make_response(request, text, tts, end_session=True)
        else:
            save_state = {}
            # Сохраним важные состояние
            for save in state.MUST_BE_SAVE:
                if save in request.session:
                    save_state.update({save: request.session[save]})
            save_state[state.NEED_FALLBACK] = True
            text, tts = texts.help_menu_fallback()
            return self.make_response(
                request,
                text,
                tts,
                buttons=HELP,
                state=save_state,
            )


class Welcome(GlobalScene):
    def reply(self, request: Request):
        saved_list = request.user.get(state.STUDENTS, [])
        if saved_list:
            text, tts = texts.hello_user_variable()
            buttons = []
        else:
            text, tts = texts.hello()
            buttons = [
                button("Да"),
                button("Помощь"),
            ]

        return self.make_response(
            request,
            text,
            tts,
            buttons=buttons,
        )

    def handle_local_intents(self, request: Request):
        if intents.CONFIRM in request.intents:
            return Settings_FirstScene()
        elif intents.REJECT in request.intents:
            return MaybeHelp()
        elif intents.GET_SCHEDULE in request.intents:
            return GetSchedule()
        elif intents.RESET in request.intents:
            return Settings_Reset()


class Goodbye(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.goodbye()
        return self.make_response(request, text, tts, end_session=True)


class SorryAndGoodbye(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.sorry_and_goodbye()
        return self.make_response(request, text, tts, end_session=True)


class HaveMistake(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.mistake()
        return self.make_response(request, text, tts, end_session=True)


class MaybeHelp(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.maybe_you_need_help()
        return self.make_response(request, text, tts, buttons=YES_NO)

    def handle_local_intents(self, request: Request):
        if intents.CONFIRM in request.intents:
            return HelpMenu()
        elif intents.REJECT in request.intents:
            return Goodbye()


class HelpMenu(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.help_menu()
        return self.make_response(
            request,
            text,
            tts,
            buttons=[],
            state={},
        )


# endregion


# region settings


# region start


class Settings_FirstScene(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.start_setting()
        return self.make_response(request, text, tts, buttons=HELP)

    def handle_local_intents(self, request: Request):
        if entities.FIO in request.entities_list:
            return Settings_GetSchool()

    def fallback(self, request: Request):
        return global_fallback(self, request, texts.start_setting_fallback())


# endregion

# region school


class Settings_GetSchool(GlobalScene):
    def reply(self, request: Request):
        name = request.entity(entities.FIO)[0]["first_name"].capitalize()

        text, tts = texts.what_school(name)
        return self.make_response(
            request,
            text,
            tts,
            buttons=HELP,
            state={state.TEMP_NAME: name},
        )

    def handle_local_intents(self, request: Request):
        if entities.NUMBER in request.entities_list:
            return Settings_GetClassNumber()

    def fallback(self, request: Request):
        return global_fallback(self, request, texts.what_school_fallback())


# endregion

# region class number


class Settings_GetClassNumber(GlobalScene):
    def reply(self, request: Request):
        school_num = request.entity(entities.NUMBER)[0]
        text, tts = texts.what_classnumber()
        return self.make_response(
            request,
            text,
            tts,
            buttons=HELP,
            state={state.TEMP_SCHOOL: school_num},
        )

    def handle_local_intents(self, request: Request):
        if entities.NUMBER in request.entities_list:
            class_num = request.entity(entities.NUMBER)[0]
            if 1 <= class_num <= 11:
                class_letter = request.tokens[-1]
                if "А" <= class_letter.upper() <= "Я":
                    return Settings_Confirm()
                else:
                    return Settings_GetClassLetter()
            else:
                return Settings_IncorrectClassNumber()

    def fallback(self, request: Request):
        return global_fallback(self, request, texts.what_classnumber_fallback())


class Settings_IncorrectClassNumber(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.incorrect_classnumber()
        return self.make_response(
            request,
            text,
            tts,
            buttons=HELP,
        )

    def handle_local_intents(self, request: Request):
        if entities.NUMBER in request.entities_list:
            class_num = request.entity(entities.NUMBER)[0]
            if 1 <= class_num <= 11:
                class_letter = request.tokens[-1].upper()
                if len(class_letter) == 1 and "А" <= class_letter <= "Я":
                    return Settings_Confirm()
                else:
                    return Settings_GetClassLetter()
            else:
                return Settings_IncorrectClassNumber()

    def fallback(self, request):
        text, tts = texts.sorry_and_goodbye()
        return self.make_response(request, text, tts, end_session=True)


# endregion

# region class letter


class Settings_GetClassLetter(GlobalScene):
    def reply(self, request: Request):
        class_num = request.entity(entities.NUMBER)[0]
        text, tts = texts.what_classletter()
        return self.make_response(
            request,
            text,
            tts,
            buttons=[
                button("А"),
                button("Б"),
                button("В"),
                button("Г"),
                button("Д"),
                button("Помощь"),
            ],
            state={state.TEMP_CLASS_ID: str(class_num)},
        )

    def handle_local_intents(self, request: Request):
        class_letter = request.tokens[-1].upper()
        if len(class_letter) == 1:
            if "А" <= class_letter <= "Я":
                return Settings_Confirm()
            else:
                return Settings_IncorrectClassLetter()

    def fallback(self, request: Request):
        return global_fallback(self, request, texts.what_classlatter_fallback())


class Settings_IncorrectClassLetter(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.incorrect_classletter()
        return self.make_response(
            request,
            text,
            tts,
            buttons=HELP,
        )

    def handle_local_intents(self, request: Request):
        class_letter = request.tokens[-1]
        if "А" <= class_letter.capitalize() <= "Я":
            return Settings_Confirm()
        else:
            return SorryAndGoodbye()

    def fallback(self, request):
        text, tts = texts.sorry_and_goodbye()
        return self.make_response(request, text, tts, end_session=True)


# endregion


class Settings_Confirm(GlobalScene):
    def reply(self, request: Request):
        prev_session = request.session.get("scene")
        if prev_session == "Settings_GetClassNumber":  # назвали класс полностью
            class_num = request.entity(entities.NUMBER)[0]
            class_letter = request.tokens[-1]
        else:
            class_num = request.session.get(state.TEMP_CLASS_ID)
            class_letter = request.tokens[-1]
        class_id = str(class_num) + class_letter.upper()

        text, tts = texts.confirm_settings(
            request.session.get(state.TEMP_NAME),
            request.session.get(state.TEMP_SCHOOL),
            class_id,
        )

        return self.make_response(
            request,
            text,
            tts,
            buttons=YES_NO,
            state={state.TEMP_CLASS_ID: class_id},
        )

    def handle_local_intents(self, request: Request):
        if intents.CONFIRM in request.intents:
            return Settings_OneMore()
        elif intents.REJECT in request.intents:
            return Settings_LetsCorrect()


class Settings_OneMore(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.one_more_student()

        name = request.session.get(state.TEMP_NAME)
        school = request.session.get(state.TEMP_SCHOOL)
        class_id = request.session.get(state.TEMP_CLASS_ID)

        return self.make_response(
            request,
            text,
            tts,
            user_state={
                state.STUDENTS: [
                    asdict(
                        Student(
                            name,
                            school,
                            class_id,
                        )
                    )
                ]
            },
        )

    def handle_local_intents(self, request: Request):
        if intents.CONFIRM in request.intents:
            return Settings_FirstScene()
        else:
            return ChooseScenario()


# endregion


class Settings_LetsCorrect(Settings_FirstScene):
    def reply(self, request: Request):
        text, tts = texts.discard_settings()
        return self.make_response(
            request,
            text,
            tts,
            buttons=HELP,
            state={state.TEMP_NAME: "", state.TEMP_SCHOOL: "", state.TEMP_CLASS_ID: ""},
        )


class Settings_Reset(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.confirm_reset()
        return self.make_response(request, text, tts, buttons=YES_NO)

    def handle_local_intents(self, request: Request):
        if intents.CONFIRM in request.intents:
            return Settings_ResetConfirm()
        else:
            return Settings_RejectReset()


class Settings_ResetConfirm(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.reset_settings()
        return self.make_response(
            request,
            text,
            tts,
            state={},
            user_state={state.STUDENTS: []},
            end_session=True,
        )


class Settings_RejectReset(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.reject_reset()
        return self.make_response(request, text, tts)


# endregion

# region base scenario


class ChooseScenario(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.choose_scenario()
        return self.make_response(request, text, tts)

    def handle_local_intents(self, request: Request):
        if intents.GET_SCHEDULE in request.intents:
            return GetSchedule()
        elif intents.GET_HOMEWORK in request.intents:
            return GetHomework()
        elif intents.REJECT in request.intents:
            return MaybeHelp()


class GetSchedule(GlobalScene):
    # TODO
    # - обработка ошибок при получении студента
    # - выбор дня (не только завтра)
    def reply(self, request: Request):
        saved_list = request.user.get(state.STUDENTS, [])
        students = [Student(**s) for s in saved_list]
        if entities.DATETIME in request.entities_list:
            ya_date = request.entity(entities.DATETIME)[0]
            ya_date = ya_date_transform(ya_date)
        else:
            ya_date = None
        if students:
            current_student: Student = students[0]
        lesson_list = diary_api.get_schedule(
            current_student.school_id,
            current_student.class_id,
            ya_date,
        )
        if not lesson_list:
            text, tts = texts.no_schedule()
            return self.make_response(
                request,
                text,
                tts,
                buttons=[
                    button("Домашнее задание"),
                    button("Расписание"),
                ],
            )
        else:
            cards = _prepare_cards_lessons(lesson_list)
            text, tts = texts.tell_about_schedule(lesson_list)
            buttons = [
                button("Домашнее задание"),
                button("Расписание"),
            ]
            return self.make_response(
                request,
                text,
                tts,
                card=image_list(cards, header=text),
                buttons=buttons,
            )

        return self.make_response(request, text, tts)


    def handle_local_intents(self, request: Request):
        if intents.REJECT in request.intents:
            return MaybeHelp()


class GetHomework(GlobalScene):
    # Домашнее задание можно спросить указав предмет и дату на какую надо
    def reply(self, request: Request):
        # 1. Выделим дату. Ее может и не быть
        if entities.DATETIME in request.entities_list:
            ya_date = request.entity(entities.DATETIME)[0]
            ya_date = ya_date_transform(ya_date)
        else:
            ya_date = None

        # 2. Выделим предметы. Их тоже может не быть
        lessons = []
        slots = request.intents.get("homework", {}).get("slots", {})
        for i in range(1, 10):
            subject = "subject" + str(i)
            if subject in slots:
                lesson = slots.get(subject).get("value")
                lessons = lessons + entities.subjects.get(lesson)

        saved_list = request.user.get(state.STUDENTS, [])
        students = [Student(**s) for s in saved_list]
        if students:
            current_student: Student = students[0]

        homework = diary_api.get_homework(
            current_student.school_id, current_student.class_id, ya_date, lessons
        )
        if not homework:
            text, tts = texts.no_homework()
            return self.make_response(
                request,
                text,
                tts,
                buttons=[
                    button("Домашнее задание"),
                    button("Расписание"),
                ],
            )
        else:
            hw = _split_homework(homework)[0]
            cards = _prepare_cards_hw(hw)
            text, tts = texts.tell_about_homework(hw, len(homework))
            if len(homework) > 3:
                buttons = [
                    button("Назад"),
                    button("Дальше"),
                    button("Главное меню"),
                ]
            else:
                buttons = [
                    button("Домашнее задание"),
                    button("Расписание"),
                ]
            return self.make_response(
                request,
                text,
                tts,
                card=image_list(cards, header=text),
                buttons=buttons,
                state={
                    state.LIST_HW: [asdict(x) for x in homework],
                    state.TASKS_HW: len(homework),
                    state.SKIP_HW: 0,
                },
            )

    def handle_local_intents(self, request: Request):
        if intents.NEXT in request.intents:
            return TellAboutHomework(1)
        if intents.PREV in request.intents:
            return TellAboutHomework(-1)
        if intents.REPEAT in request.intents:
            return TellAboutHomework(0)


class TellAboutHomework(GlobalScene):
    def __init__(self, step=0):
        self.__step = step

    def reply(self, request: Request):
        hw_dict = request.session.get(state.LIST_HW)
        hw = _split_homework([Homework(**x) for x in hw_dict])
        full = request.session.get(state.TASKS_HW)
        step = (request.session.get(state.SKIP_HW) + self.__step) % len(hw)

        cards = _prepare_cards_hw(hw[step])

        text, tts = texts.tell_about_homework(hw[step], full)
        if full > 3:
            buttons = [
                button("Назад"),
                button("Дальше"),
                button("Главное меню"),
            ]
        else:
            buttons = [
                button("Домашнее задание"),
                button("Расписание"),
            ]
        return self.make_response(
            request,
            text,
            tts,
            card=image_list(cards, header=text),
            buttons=buttons,
            state={state.SKIP_HW: step},
        )

    def handle_local_intents(self, request: Request):
        if intents.NEXT in request.intents:
            return TellAboutHomework(1)
        if intents.PREV in request.intents:
            return TellAboutHomework(-1)
        if intents.REPEAT in request.intents:
            return TellAboutHomework(0)


# endregion


def global_fallback(self, request: Request, response):
    if request.session.get(state.NEED_FALLBACK, False):
        return SorryAndGoodbye()
    else:
        text, tts = response
        return self.make_response(
            request,
            text,
            tts,
            buttons=HELP,
            state={state.NEED_FALLBACK: True},
        )


def _split_homework(homework: list):
    n = 3
    if len(homework) <= n:
        list_hw = [homework]
    else:
        list_hw = [homework[i : i + n] for i in range(0, len(homework), n)]  # nopep8
        if len(list_hw) > 1 and len(list_hw[-1]) == 1:
            # последний урок из ПРЕДПОСЛЕДНЕЙ групп становится ПЕРВЫМ в последней группе
            list_hw[-1].insert(0, list_hw[-2].pop(2))
    return list_hw


def _prepare_cards_hw(homeworks: List[Homework]):
    return [
        image_button(title=x.lesson.capitalize(), description=x.task) for x in homeworks
    ]


def _prepare_cards_lessons(lessons: List[PlannedLesson]):
    return [
        image_button(title=x.name.capitalize(), description=x.duration) for x in lessons
    ]


def _list_scenes():
    current_module = sys.modules[__name__]
    scenes = []
    for name, obj in inspect.getmembers(current_module):
        if inspect.isclass(obj) and issubclass(obj, Scene):
            scenes.append(obj)
    return scenes


SCENES = {scene.id(): scene for scene in _list_scenes()}

DEFAULT_SCENE = Welcome
YES_NO = [button("Да"), button("Нет")]
HELP = [button("Помощь")]
