import skill.main as main
import skill.state as state
from skill.tests.mock_alice import AliceAnswer, AliceEntity, AliceIntent, AliceRequest


def get_next_scene(answer):
    return answer["session_state"].get("scene", None)


# region start


def test_start_settings():

    req = (
        AliceRequest().from_scene("Welcome").add_intent(AliceIntent().confirm()).build()
    )
    ans = main.handler(req, None)

    answer = AliceAnswer(ans)
    assert answer is not None


def test_say_name():

    req = (
        AliceRequest()
        .from_scene("FirstSettingsScene")
        .add_entity(AliceEntity().fio(first_name="Добрыня"))
        .build()
    )
    ans = main.handler(req, None)

    answer = AliceAnswer(ans)

    assert answer.get_state_session(state.TEMP_NAME) == "Добрыня"


def test_say_num_school():

    req = (
        AliceRequest()
        .from_scene("Settings_GetSchool")
        .add_entity(AliceEntity().number(666))
        .build()
    )
    ans = main.handler(req, None)

    answer = AliceAnswer(ans)
    assert answer.get_state_session(state.TEMP_SCHOOL) == 666
    assert answer.next_scene == "Settings_GetClassNumber"


def test_say_class_num_with_letter():

    req = (
        AliceRequest()
        .from_scene("Settings_GetClassNumber")
        .set_command("11 Б")
        .add_entity(AliceEntity().number(11))
        .build()
    )
    ans = main.handler(req, None)

    answer = AliceAnswer(ans)
    assert answer.get_state_session(state.TEMP_CLASS_ID) == "11Б"
    assert answer.next_scene == "Settings_Confirm"


def test_say_class_num_without_letter():

    req = (
        AliceRequest()
        .from_scene("Settings_GetClassNumber")
        .set_command("11")
        .add_entity(AliceEntity().number(11))
        .build()
    )
    ans = main.handler(req, None)

    answer = AliceAnswer(ans)
    assert answer.get_state_session(state.TEMP_CLASS_ID) == "11"
    assert answer.next_scene == "Settings_GetClassLetter"
