# hr_sentinel_server.py

from flask import Flask, request, jsonify
import logging
from datetime import datetime


app = Flask(__name__)
attending_db = list()
patient_hr_db = list()
patient_db = []


def add_new_attending(username_id, email, phone):
    new_attending = {"attending_username": username_id,
                     "attending_email": email,
                     "attending_phone": phone}
    attending_db.append(new_attending)
    print(attending_db)
    return True


def validate_new_attending(attending_dict):
    expected_keys = ("attending_username",
                     "attending_email", "attending_phone")
    expected_types = (str, str, str)
    for key, types in zip(expected_keys, expected_types):
        if key not in attending_dict.keys():
            return "{} key not found".format(key)
        if type(attending_dict[key]) != types:
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


def add_new_patient(id, attending, age):
    new_patient = {"patient_id": id,
                   "attending_username": attending,
                   "patient_age": age}
    patient_db.append(new_patient)
    print(patient_db)
    return True


def validate_new_patient(patient_dict):
    x = patient_dict["patient_id"]
    y = patient_dict["attending_username"]
    z = patient_dict["patient_age"]
    # checking to see if already int or can be converted
    try:
        x = int(x)
    except:
        logging.error("{} is an invalid input".format(x))
        return("{} is an invalid input".format(x))
    # checking to see if already int or can be converted
    try:
        z = int(z)
    except:
        logging.error("{} is an invalid input".format(z))
        return("{} is an invalid input".format(z))
    # make sure string is in "Smith.J" format
    try:
        check = y.split(".")
        if len(check[1]) != 1:
            logging.error("{} is an invalid format".format(y))
            return("{} is an invalid format".format(y))
    except:
        logging.error("{} is an invalid input".format(y))
        return("{} is an invalid input".format(y))
    return True


@app.route("/api/new_patient", methods=["POST"])
def post_new_patient():
    new_dict = request.get_json()
    validate = validate_new_patient(new_dict)
    if validate is not True:
        return validate, 400
    patient = add_new_attending(new_dict["patient_id"],
                                new_dict["attending_username"],
                                new_dict["patient_age"])
    if patient is True:
        logging.info("New Patient Added!")
        logging.info("Patient ID: {}".format(
                    new_dict["patient_id"]))
        return "New Patient Successfully Added", 200
    else:
        return "Failed to Add New Patient", 400


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
        for patient, patient_name in zip(patient_hr_db, patient_db):
            if patient["patient_id"] != patient_id:
                continue
            elif patient["patient_id"] is patient_id:
                patient["heart_rate"].append(heart_rate)
                patient["timestamp"] = string_recorded_datetime
                age = patient_name["patient_age"]
                result = is_tachycardic(age, heart_rate)
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


def is_tachycardic(age, heart_rate):
    if 1 <= age <= 2 and heart_rate > 151:
        return True
    elif 3 <= age <= 4 and heart_rate > 137:
        return True
    elif 5 <= age <= 7 and heart_rate > 133:
        return True
    elif 8 <= age <= 11 and heart_rate > 130:
        return True
    elif 12 <= age <= 15 and heart_rate > 119:
        return True
    elif age >= 15 and heart_rate > 100:
        return True
    else:
        return False


if __name__ == '__main__':
    start_logging()
    app.run()
