import json
import logging
import os
import sys

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from skill.alice import Request
from skill.scenes import DEFAULT_SCENE, SCENES
from skill.state import PREVIOUS_MOVES, STATE_REQUEST_KEY
from skill.intents import GET_SCHEDULE, GET_HOMEWORK

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
root.addHandler(handler)


def handler(event, context):

    # если контекст пустой - это отладка или тесты
    if context is not None:
        sentry_logging = LoggingIntegration(
            level=logging.INFO, event_level=logging.ERROR
        )
        sentry_sdk.init(
            dsn=(
                "https://9e08c21c38da43de9c475699b61ab6d4@o241410"
                ".ingest.sentry.io/5974885"
            ),
            integrations=[sentry_logging],
            environment="development"
            if os.environ["DEBUG"] == "True"
            else "production",
        )

    logging.debug(f"REQUEST: {json.dumps(event, ensure_ascii=False)}")
    logging.debug(f"COMMAND: {event['request']['command']}")
    current_scene_id = get_id_scene(event)

    logging.info(f"Current scene: {current_scene_id}")
    request = Request(event)

    try:

        if current_scene_id is None:
            return DEFAULT_SCENE().reply(request)

        current_scene = SCENES.get(current_scene_id, DEFAULT_SCENE)()
        next_scene = current_scene.move(request)

        if next_scene is not None:
            logging.info(f"Moving from scene {current_scene.id()} to {next_scene.id()}")
            return next_scene.reply(request)
        else:
            logging.warning(
                f"Failed to parse user request at scene {current_scene.id()}"
            )
            return current_scene.fallback(request)

    except Exception as e:
        moves = request.session.get(PREVIOUS_MOVES, [])
        logging.exception(e, extra={"moves": moves})
        message = SCENES.get("HaveMistake")()
        return message.reply(request)


def get_id_scene(event):
    res = event.get("state", {}).get(STATE_REQUEST_KEY, {}).get("scene")
    if res is None and event.get("request", {}).get("nlu", {}).get("intents", {}).get(GET_SCHEDULE) is not None:
        res = GET_SCHEDULE
    elif res is None and event.get("request", {}).get("nlu", {}).get("intents", {}).get(GET_HOMEWORK) is not None:
        res = GET_HOMEWORK            
    return res