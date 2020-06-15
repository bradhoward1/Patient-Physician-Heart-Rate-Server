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


def test_add_new_patient():
    from hr_sentinel_server import add_new_patient
    input_id = 123
    attending_id = "Smith.J"
    input_age = 50
    answer = add_new_patient(input_id, attending_id, input_age)
    expected = True
    assert answer == expected


@pytest.mark.parametrize("result, expected",
                         [({"patient_id": 700,
                           "attending_username": "Howard.B",
                            "patient_age": 50}, True),
                          ({"patient_id": "700",
                           "attending_username": "Howard.B",
                            "patient_age": 50}, True),
                          ({"patient_id": "700",
                           "attending_username": "Howard.B",
                            "patient_age": "50"}, True),
                          ({"patient_id": "700a",
                           "attending_username": "Howard.B",
                            "patient_age": "50"},
                           "700a is an invalid input"),
                          ({"patient_id": "a700",
                           "attending_username": "Howard.B",
                            "patient_age": "50"},
                           "a700 is an invalid input"),
                          ({"patient_id": "700",
                           "attending_username": "Howard.B",
                            "patient_age": "a"},
                           "a is an invalid input"),
                          ({"patient_id": "700",
                           "attending_username": "Howard",
                            "patient_age": "50"},
                           "Howard is an invalid input"),
                          ({"patient_id": "700",
                           "attending_username": "Howard.Ba",
                            "patient_age": "50"},
                           "Howard.Ba is an invalid format"),
                          ({"patient_id": "700",
                           "attending_username": "70",
                            "patient_age": "50"},
                           "70 is an invalid input")])
def test_validate_new_patient(result, expected):
    from hr_sentinel_server import validate_new_patient
    answer = validate_new_patient(result)
    assert answer == expected


def test_start_logging():
    from hr_sentinel_server import start_logging
    answer = start_logging()
    expected = True
    assert answer == expected
