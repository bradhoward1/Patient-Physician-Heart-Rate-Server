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


def test_avg_hr_calc():
    from hr_sentinel_server import avg_hr_calc
    patient_hr_db = [{"patient_id": 1,
                      "heart_rate": [80, 90, 160],
                      "timestamp": ["2018-03-09 11:00:36",
                                    "2018-03-09 11:10:36",
                                    "2018-03-09 11:20:36"]},
                     {"patient_id": 2,
                      "heart_rate": [70, 80],
                      "timestamp": ["2020-07-10 1:30:50",
                                    "2020-07-10 1:50:50"]},
                     {"patient_id": 3,
                      "heart_rate": [50, 60, 70],
                      "timestamp": ["2018-03-09 11:00:36",
                                    "2018-03-09 11:20:36",
                                    "2018-03-09 11:50:36"]}]
    answer = avg_hr_calc(patient_hr_db, 3, "2018-03-09 11:20:36")
    expected = 65, True
    assert answer == expected


def test_total_hr_avg():
    from hr_sentinel_server import total_hr_avg
    patient_hr_db = [{"patient_id": 1,
                      "heart_rate": [80, 90, 160],
                      "timestamp": ["2018-03-09 11:00:36",
                                    "2018-03-09 11:10:36",
                                    "2018-03-09 11:20:36"]},
                     {"patient_id": 2,
                      "heart_rate": [70, 80],
                      "timestamp": ["2020-07-10 1:30:50",
                                    "2020-07-10 1:50:50"]},
                     {"patient_id": 3,
                      "heart_rate": [50, 60, 70],
                      "timestamp": ["2018-03-09 11:00:36",
                                    "2018-03-09 11:20:36",
                                    "2018-03-09 11:50:36"]}]
    answer = total_hr_avg(patient_hr_db, 3)
    expected = {"Average heart rate": 60}, True
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
    hr_db = [
             {"patient_id": 1,
              "heart_rate": [80, 90, 100, 120],
              "timestamp": "string_recorded_datetime"},
             {"patient_id": 2,
              "heart_rate": [40, 50, 20],
              "timestamp": "string_recorded_datetime"},
             {"patient_id": 3,
              "heart_rate": [60, 70, 50, 45],
              "timestamp": "string_recorded_datetime"}]
    answer = heart_rate_list(hr_db, 2)
    expected = [40, 50, 20]
    assert answer == expected


def test_patient_status_tachycardic():
    from hr_sentinel_server import patient_status
    patient_hr_db = [{"patient_id": 1,
                      "heart_rate": [80, 90, 160],
                      "timestamp": "2018-03-09 11:00:36"},
                     {"patient_id": 2,
                      "heart_rate": [70, 80],
                      "timestamp": "2020-07-10 1:30:50"},
                     {"patient_id": 3,
                      "heart_rate": [50, 60, 70],
                      "timestamp": "2018-03-09 11:00:36"}]
    patient_db = [{"patient_id": 1,
                   "attending_username": "Smith.J",
                   "patient_age": 50},
                  {"patient_id": 2,
                   "attending_username": "Howard.B",
                   "patient_age": 25},
                  {"patient_id": 3,
                   "attending_username": "Smith.J",
                   "patient_age": 32}]
    answer = patient_status(patient_hr_db, patient_db, 1)
    expected = {"heart_rate": 160,
                "status": "tachycardic",
                "timestamp": "2018-03-09 11:00:36"}
    assert answer == expected


def test_patient_status_not_tachycardic():
    from hr_sentinel_server import patient_status
    patient_hr_db = [
                     {"patient_id": 1,
                      "heart_rate": [80, 90, 160],
                      "timestamp": "2018-03-09 11:00:36"},
                     {"patient_id": 2,
                      "heart_rate": [70, 80],
                      "timestamp": "2020-07-10 1:30:50"},
                     {"patient_id": 3,
                      "attending_username": "Smith.J",
                      "patient_age": 32}
                    ]
    patient_db = [{"patient_id": 1,
                   "attending_username": "Smith.J",
                   "patient_age": 50},
                  {"patient_id": 2,
                   "attending_username": "Howard.B",
                   "patient_age": 25},
                  {"patient_id": 3,
                   "attending_username": "Smith.J",
                   "patient_age": 32}]
    answer = patient_status(patient_hr_db, patient_db, 2)
    expected = {"heart_rate": 80,
                "status": "not tachycardic",
                "timestamp": "2020-07-10 1:30:50"}
    assert answer == expected
