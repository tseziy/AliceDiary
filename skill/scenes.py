import inspect
import sys
from dataclasses import asdict
from datetime import date, timedelta

import skill.texts as texts
from skill import diary_api, intents, state
from skill.alice import Request, button
from skill.scenes_util import Scene
from skill.schemas import Student
from skill.dates_transformations import transform_yandex_datetime_value_to_datetime

# region Общие сцены

# класс общая сцена


class GlobalScene(Scene):
    def reply(self, request: Request):
        pass

    def handle_global_intents(self, request):
        if (
            intents.HELP in request.intents
            or intents.WHAT_CAN_YOU_DO in request.intents
        ):
            return HelpMenu()

    def handle_local_intents(self, request: Request):
        pass

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
            text, tts = texts.start_setting_fallback()
            return self.make_response(
                request,
                text,
                tts,
                buttons=[button("Помощь")],
                state=save_state,
            )


class Welcome(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.hello()

        return self.make_response(
            request,
            text,
            tts,
            buttons=[
                button("Да"),
                button("Помощь"),
            ],
        )

    def handle_local_intents(self, request: Request):
        if intents.CONFIRM in request.intents:
            return Settings_FirstScene()
        elif intents.REJECT in request.intents:
            return MaybeHelp()


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
        return self.make_response(request, text, tts, buttons=[button("Помощь")])

    def handle_local_intents(self, request: Request):
        if intents.FIO in request.entities_list:
            return Settings_GetSchool()

    def fallback(self, request: Request):
        if request.session.get(state.NEED_FALLBACK, False):
            text, tts = texts.sorry_and_goodbye()
            return self.make_response(request, text, tts, end_session=True)
        else:
            text, tts = texts.start_setting_fallback()
            return self.make_response(
                request,
                text,
                tts,
                buttons=[button("Помощь")],
                state={state.NEED_FALLBACK: True},
            )


# endregion

# region school


class Settings_GetSchool(GlobalScene):
    def reply(self, request: Request):
        name = request.entity(intents.FIO)[0]["first_name"].capitalize()

        text, tts = texts.what_school(name)
        return self.make_response(
            request,
            text,
            tts,
            buttons=[button("Помощь")],
            state={state.TEMP_NAME: name},
        )

    def handle_local_intents(self, request: Request):
        if intents.NUMBER in request.entities_list:
            return Settings_GetClassNumber()

    def fallback(self, request: Request):
        if request.session.get(state.NEED_FALLBACK, False):
            text, tts = texts.sorry_and_goodbye()
            return self.make_response(request, text, tts, end_session=True)
        else:
            text, tts = texts.what_school_fallback()
            return self.make_response(
                request,
                text,
                tts,
                buttons=[button("Помощь")],
                state={state.NEED_FALLBACK: True},
            )


# endregion

# region class number


class Settings_GetClassNumber(GlobalScene):
    def reply(self, request: Request):
        school_num = request.entity(intents.NUMBER)[0]
        text, tts = texts.what_classnumber()
        return self.make_response(
            request,
            text,
            tts,
            buttons=[button("Помощь")],
            state={state.TEMP_SCHOOL: school_num},
        )

    def handle_local_intents(self, request: Request):
        if intents.NUMBER in request.entities_list:
            class_num = request.entity(intents.NUMBER)[0]
            if 1 <= class_num <= 11:
                class_letter = request.tokens[-1]
                if "А" <= class_letter.upper() <= "Я":
                    return Settings_Confirm()
                else:
                    return Settings_GetClassLetter()
            else:
                return Settings_IncorrectClassNumber()

    def fallback(self, request: Request):
        if request.session.get(state.NEED_FALLBACK, False):
            text, tts = texts.sorry_and_goodbye()
            return self.make_response(request, text, tts, end_session=True)
        else:
            text, tts = texts.what_classnumber_fallback()
            return self.make_response(
                request,
                text,
                tts,
                buttons=[button("Помощь")],
                state={state.NEED_FALLBACK: True},
            )


class Settings_IncorrectClassNumber(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.incorrect_classnumber()
        return self.make_response(
            request,
            text,
            tts,
            buttons=[button("Помощь")],
        )

    def handle_local_intents(self, request: Request):
        if intents.NUMBER in request.entities_list:
            class_num = request.entity(intents.NUMBER)[0]
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
        class_num = request.entity(intents.NUMBER)[0]
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


class Settings_IncorrectClassLetter(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.incorrect_classletter()
        return self.make_response(
            request,
            text,
            tts,
            buttons=[button("Помощь")],
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
            class_num = request.entity(intents.NUMBER)[0]
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
            buttons=[button("Да"), button("Нет")],
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
        else:  # TODO Переход на другую основную сцену
            return Welcome()


# endregion


class Settings_LetsCorrect(Settings_FirstScene):
    def reply(self, request: Request):
        text, tts = texts.discard_settings()
        text, tts = texts.start_setting()
        return self.make_response(
            request,
            text,
            tts,
            buttons=[button("Помощь")],
            state={state.TEMP_NAME: "", state.TEMP_SCHOOL: "", state.TEMP_CLASS_ID: ""},
        )


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


class GetSchedule(GlobalScene):
    # TODO
    # - обработка ошибок при получении студента
    # - выбор дня (не только завтра)
    def reply(self, request: Request):
        saved_list = request.user.get(state.STUDENTS, [])
        students = [Student(**s) for s in saved_list]
        date = transform_yandex_datetime_value_to_datetime(yandex_datetime_value_dict=(request.entity(intents.DATETIME)))
        if students:
            current_student: Student = students[0]
        lesson_list = diary_api.get_schedule(
            current_student.school_id,
            current_student.class_id,
            date.today() + timedelta(days=1),
        )
        text, tts = texts.get_schedule(lesson_list)
        return self.make_response(request, text, tts)

    def handle_local_intents(self, request: Request):
        return ChooseScenario()


class GetHomework(GlobalScene):
    ...
    # TODO


# endregion


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
