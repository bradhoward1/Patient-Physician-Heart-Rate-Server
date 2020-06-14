# test_hr_sentinel_server.py

import pytest


def test_add_new_attending():
    from hr_sentinel_server import add_new_attending
    input_name = "Howard.B"
    input_email = "bradhtest@test.com"
    input_phone = "919-867-5309"
    answer = add_new_attending(input_name, input_email, input_phone)
    expected = True
    assert answer == expected


@pytest.mark.parametrize("result, expected",
                         [({"attending_username": "Howard.B",
                            "attending_email": "bradhtest@test.com",
                            "attending_phone": "919-867-5309"}, True),
                          ({"attending_username": "Howard.B",
                            "attending_email": "bradhtest@test.com",
                            "attending_phone": 919-867-5309}, 'attending_phone'
                          ' key is the wrong value type'),
                          ({"attending_user": "Howard.B",
                            "attending_email": "bradhtest@test.com",
                            "attending_phone": "919-867-5309"},
                          'attending_username key not found')])
def test_validate_new_attending(result, expected):
    from hr_sentinel_server import validate_new_attending
    answer = validate_new_attending(result)
    assert answer == expected


def test_start_logging():
    from hr_sentinel_server import start_logging
    answer = start_logging()
    expected = True
    assert answer == expected


@pytest.mark.parametrize("result, expected",
                         [({"patient_id": "1",
                            "heart_rate": 100}, True),
                          ({"patient_id": 1,
                            "heart_rate": 100}, True),
                          ({"patient_id": "1",
                            "heart_rate": "100"}, True),
                          ({"patient_id": "1a",
                            "heart_rate": 100}, 'patient_id'
                          ' is the wrong value type'),
                          ({"patient_id": "1",
                            "heart_rate": "10a0"}, 'heart_rate'
                          ' is the wrong value type'),
                          ({"patient_": "1",
                            "heart_rate": 100}, 'patient_id'
                          ' key not found'),
                          ({"patient_id": "1",
                            "heart_ra": 100}, 'heart_rate'
                          ' key not found')])
def test_validate_incoming_heart_rate(result, expected):
    from hr_sentinel_server import validate_incoming_heart_rate
    answer = validate_incoming_heart_rate(result)
    assert answer == expected
