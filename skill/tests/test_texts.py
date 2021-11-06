from fluentcheck import Check

import skill.texts as texts


def test_hello_start_session():
    text, tts = texts.hello()
    Check(text).is_not_none().is_string().contains_char(
        "Привет! Это цифровой дневник для Санкт-Петербурга."
    ).contains_char("Готовы продолжить?")
