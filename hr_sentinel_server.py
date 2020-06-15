# hr_sentinel_server.py

from flask import Flask, request, jsonify
import logging
from datetime import datetime


app = Flask(__name__)
attending_db = list()
patient_hr_db = list()


def add_new_attending(username_id, email, phone):
    new_attending = {"attending_username": username_id,
                     "attending_email": email,
                     "attending_phone": phone}
    attending_db.append(new_attending)
    print(attending_db)
    return True


def validate_new_attending(new_dict):
    expected_keys = ("attending_username",
                     "attending_email", "attending_phone")
    expected_types = (str, str, str)
    for key, types in zip(expected_keys, expected_types):
        if key not in new_dict.keys():
            return "{} key not found".format(key)
        if type(new_dict[key]) != types:
            return "{} key is the wrong value type".format(key)
    return True


@app.route("/api/new_attending", methods=["POST"])
def post_new_attending():
    new_dict = request.get_json()
    validate = validate_new_attending(new_dict)
    if validate is not True:
        return validate, 400
    attending = add_new_attending(new_dict["attending_username"],
                                  new_dict["attending_email"],
                                  new_dict["attending_phone"])
    if attending is True:
        logging.info("New Attending Physician Added!")
        logging.info("Physician User Name: {}".format(
                    new_dict["attending_username"]))
        logging.info("Physician Email: {}".format(
                    new_dict["attending_email"]))
        return "New Attending Physician Successfully Added", 200
    else:
        return "Failed to Add New Attending Physician", 400


def start_logging():
    logging.basicConfig(filename='my_log.log', filemode='w',
                        level=logging.DEBUG)
    logging.info("-----New Run-----\n")
    return True


def validate_incoming_heart_rate(in_dict):
    expected_keys = ("patient_id", "heart_rate")
    expected_types = (int, int)
    for key, types in zip(expected_keys, expected_types):
        if key not in in_dict.keys():
            return "{} key not found".format(key)
        try:
            in_dict[key] = int(in_dict[key])
        except ValueError:
            return "{} is the wrong value type".format(key)
    return True


def add_patient_hr(patient_id, heart_rate):
    recorded_datetime = datetime.now()
    string_recorded_datetime = datetime.strftime(
            recorded_datetime,  "%m-%d-%y %H:%M:%S")
    if not any(patient["patient_id"] == patient_id
               for patient in patient_hr_db):
        new_patient = {"patient_id": patient_id,
                       "heart_rate": [heart_rate],
                       "timestamp": string_recorded_datetime}
        patient_hr_db.append(new_patient)
        return "New Patient Added to Track HR"
    else:
        for patient in patient_hr_db:
            if patient["patient_id"] != patient_id:
                continue
            elif patient["patient_id"] is patient_id:
                patient["heart_rate"].append(heart_rate)
                patient["timestamp"] = string_recorded_datetime
                return "Current Patient Edited: Added New HR"


@app.route("/api/heart_rate", methods=["POST"])
def post_heart_rate():
    new_dict = request.get_json()
    validate = validate_incoming_heart_rate(new_dict)
    if validate is not True:
        return validate, 400
    new_heart_rate = add_patient_hr(new_dict["patient_id"],
                                    new_dict["heart_rate"])
    if new_heart_rate == "New Patient Added to Track HR":
        logging.info("New Patient Added to Track HR")
        return "New Patient Added to Track HR", 200
    elif new_heart_rate == "Current Patient Edited: Added New HR":
        logging.info("Current Patient Edited: Added New HR")
        return "Current Patient Edited: Added New HR", 200
    else:
        return "Unable to add new heart rate data", 400


if __name__ == '__main__':
    start_logging()
    app.run()
