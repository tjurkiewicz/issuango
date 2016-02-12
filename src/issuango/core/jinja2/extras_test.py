import datetime
import freezegun

import extras


@freezegun.freeze_time('2000-01-01 00:00:00')
def test_strftime():
    assert extras.strftime('%Y-%m-%d %H:%M:%S') == '2000-01-01 00:00:00'


def test_stftime_no_default():
    dt = datetime.datetime(2000, 1, 1, 0, 0, 0)
    assert extras.strftime('%Y-%m-%d %H:%M:%S', dt) == '2000-01-01 00:00:00'
