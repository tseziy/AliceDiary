from fluentcheck import Check

import skill.texts as texts


def test_hello_start_session():
    text, tts = texts.hello()
    Check(text).is_not_none().is_string().matches(
        "^Привет\\! Это цифровой дневник\\."
    ).matches(".*Готовы продолжить\\?$")
