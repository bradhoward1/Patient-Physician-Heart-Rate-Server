# test_hr_sentinel_server.py

import pytest
import datetime


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
    attending_id = "Smithh.J"
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


# Tests for existing timestamp and time in between timestamps
@pytest.mark.parametrize("id, stamp, expected",
                         [(1, "2018-03-09 11:00:36", 110),
                          (3, "2018-03-09 11:10:36", 65)])
def test_avg_hr_calc(id, stamp, expected):
    from hr_sentinel_server import avg_hr_calc
    answer = avg_hr_calc(id, stamp)
    assert answer == expected


def test_total_hr_avg():
    from hr_sentinel_server import total_hr_avg
    answer = total_hr_avg(3)
    expected = {"Average heart rate": 60}
    assert answer == expected


@pytest.mark.parametrize("result1, result2, expected",
                         [(1, 152, True),
                          (1, 151, False),
                          (3, 140, True),
                          (3, 130, False),
                          (6, 135, True),
                          (7, 130, False),
                          (9, 131, True),
                          (9, 130, False),
                          (13, 130, True),
                          (13, 100, False),
                          (33, 120, True),
                          (33, 90, False)])
def test_is_tachycardic(result1, result2, expected):
    from hr_sentinel_server import is_tachycardic
    answer = is_tachycardic(result1, result2)
    assert answer == expected


def test_heart_rate_list():
    from hr_sentinel_server import heart_rate_list
    answer = heart_rate_list(2)
    expected = [70, 80]
    assert answer == expected


def test_patient_status_tachycardic():
    from hr_sentinel_server import patient_status
    answer = patient_status(1)
    expected = {"heart_rate": 160,
                "status": "tachycardic",
                "timestamp": "2018-03-09 11:20:36"}
    assert answer == expected


def test_patient_status_not_tachycardic():
    from hr_sentinel_server import patient_status
    answer = patient_status(2)
    expected = {"heart_rate": 80,
                "status": "not tachycardic",
                "timestamp": "2020-05-10 1:50:50"}
    assert answer == expected


def test_attending_patients():
    from hr_sentinel_server import attending_patients
    answer = attending_patients("Smith.J")
    expected = [{"patient_id": 1, "last_heart_rate": 160,
                 "last_time": "2018-03-09 11:20:36",
                 "status": "tachycardic"},
                {"patient_id": 3, "last_heart_rate": 70,
                 "last_time": "2018-03-09 11:50:36", "status":
                 "not tachycardic"}]
    assert answer == expected


# Checking to ensure answer is datetime object type
def test_time_converter():
    from hr_sentinel_server import time_converter
    answer = time_converter("2018-03-09 11:05:36")
    assert type(answer) == datetime.datetime
