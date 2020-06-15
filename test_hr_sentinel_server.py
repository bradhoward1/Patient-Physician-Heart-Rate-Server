# test_hr_sentinel_server.py

import pytest


patient_hr_db = [{"patient_id": 1,
                  "heart_rate": [80]},
                 {"patient_id": 2,
                  "heart_rate": [70, 80]},
                 {"patient_id": 3,
                  "heart_rate": [50, 60, 70]}]


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


@pytest.mark.parametrize("result1, result2, expected",
                         [(4, 45, "New Patient Added"
                          " to Track HR")])
def test_add_patient_hr(result1, result2, expected):
    from hr_sentinel_server import add_patient_hr
    answer = add_patient_hr(result1, result2)
    assert answer == expected
