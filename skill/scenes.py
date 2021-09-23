import inspect
import logging
import sys

import skill.texts as texts
from skill import intents, state
from skill.alice import (
    Request,
    big_image,
    button,
    image_button,
    image_gallery,
    image_list,
)
from skill.scenes_util import Scene

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
