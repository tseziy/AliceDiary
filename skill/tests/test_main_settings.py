import skill.main as main
import skill.state as state
from skill.tests.mock_alice import AliceAnswer, AliceEntity, AliceIntent, AliceRequest

# region start


def test_start_settings_confirm():

    req = (
        AliceRequest().from_scene("Welcome").add_intent(AliceIntent().confirm()).build()
    )
    ans = main.handler(req, None)

    answer = AliceAnswer(ans)

    assert answer.next_scene == "Settings_FirstScene"


def test_start_settings_reject():

    req = (
        AliceRequest().from_scene("Welcome").add_intent(AliceIntent().reject()).build()
    )
    ans = main.handler(req, None)

    answer = AliceAnswer(ans)

    assert answer.next_scene == "MaybeHelp"


def test_say_name():

    req = (
        AliceRequest()
        .from_scene("Settings_FirstScene")
        .add_entity(AliceEntity().fio(first_name="Добрыня"))
        .build()
    )
    ans = main.handler(req, None)

    answer = AliceAnswer(ans)

    assert answer.get_state_session(state.TEMP_NAME) == "Добрыня"
    assert answer.next_scene == "Settings_GetId"


def test_dont_say_name():

    req = (
        AliceRequest()
        .from_scene("Settings_FirstScene")
        .set_command("Слава Империи")
        .build()
    )
    ans = main.handler(req, None)

    answer = AliceAnswer(ans)

    assert answer.get_state_session(state.TEMP_NAME) is None
    assert answer.get_state_session(state.NEED_FALLBACK)
    assert answer.next_scene == "Settings_FirstScene"
    assert "Простите, я вас не поняла." in answer.text


def test_say_duplicate_name():

    req = (
        AliceRequest()
        .from_scene("Settings_FirstScene")
        .add_entity(AliceEntity().fio(first_name="Добрыня"))
        .add_to_state_user(state.STUDENTS, [{"name": "Добрыня", "id": "111"}])
        .build()
    )
    ans = main.handler(req, None)

    answer = AliceAnswer(ans)

    assert answer.next_scene == "Settings_Duplicate"
    assert "Уже добавили ученика с таким именем" in answer.text


def test_say_id():

    req = (
        AliceRequest()
        .from_scene("Settings_GetId")
        .add_entity(AliceEntity().number(111))
        .add_to_state_session(state.TEMP_NAME, "Добрыня")
        .build()
    )
    ans = main.handler(req, None)
    answer = AliceAnswer(ans)

    assert answer.get_state_session(state.TEMP_NAME) == "Добрыня"
    assert answer.get_state_session(state.TEMP_ID) == 111
    assert answer.next_scene == "Settings_Confirm"
