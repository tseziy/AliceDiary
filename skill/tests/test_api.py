from datetime import datetime

import skill.diary_api as api


def test_get_schedule():
    date = datetime.strptime("01.10.2021", "%d.%m.%Y")
    res = api.get_schedule_on_date(161685, date)

    assert len(res) == 6
