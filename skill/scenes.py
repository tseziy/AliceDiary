import inspect
import sys
from dataclasses import asdict
from datetime import date, timedelta

import skill.texts as texts
from skill import diary_api, intents, state
from skill.alice import Request, button
from skill.scenes_util import Scene
from skill.schemas import Student

# region Базовые классы


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
        for_save = {}
        # Сохраним важные состояние
        for save in state.MUST_BE_SAVE:
            if save in request.session:
                for_save.update({save: request.session[save]})
        return self.make_response(
            request=request,
            text="Извините, я вас не понял. Пожалуйста, повторите что Вы сказали",
            state=for_save,
        )


class Welcome(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.hello()

        return self.make_response(
            request,
            text,
            tts,
            buttons=[
                button("Помощь"),
            ],
        )

    def handle_local_intents(self, request: Request):
        if intents.HELP in request.intents:
            return HelpMenu()
        if intents.CONFIRM in request.intents:
            return SetupScene()


class HaveMistake(GlobalScene):
    def reply(self, request: Request):
        text, tts = texts.mistake()

        return self.make_response(request, text, tts, end_session=True)


# region Меню помощи


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

# region Setup


class SetupScene(GlobalScene):
    # TODO полноценная логика с указанием:
    # - количества учеников
    # - заполнением их school_id, class_id, name по ответам пользователя

    def reply(self, request: Request):
        text, tts = texts.setup()
        return self.make_response(
            request,
            text,
            tts,
            # Пока просто замокал сценарий
            user_state={
                state.STUDENTS: [
                    asdict(
                        Student(
                            "Кузьма",
                            "some-school-id",
                            "some-class-id",
                        )
                    )
                ]
            },
        )

    def handle_local_intents(self, request: Request):
        return ChooseScenario()


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
