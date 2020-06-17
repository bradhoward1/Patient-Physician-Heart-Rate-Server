# hr_sentinel_server.py

from flask import Flask, request, jsonify
import logging
from datetime import datetime
import requests


app = Flask(__name__)
attending_db = list()
patient_hr_db = list()
patient_db = []

# patient_hr_db = [{"patient_id": 1,
#                   "heart_rate": [80]},
#                  {"patient_id": 2,
#                   "heart_rate": [70, 80]},
#                  {"patient_id": 3,
#                   "heart_rate": [50, 60, 70]}]
# patient_db = [{"patient_id": 1,
#                 "attending_username": "Smith.J",
#                 "patient_age": 50},
#               {"patient_id": 2,
#                 "attending_username": "Howard.B",
#                 "patient_age": 25},
#               {"patient_id": 3,
#                    "attending_username": "Smith.J",
#                    "patient_age": 32}]
# attending_db = [{"attending_username": "Smith.J",
#                  "attending_email": "smith@test.com",
#                  "attending_phone": "919-867-5309"},
#                 {"attending_username": "Howard.B",
#                  "attending_email": "brad@test.com",
#                  "attending_phone": "239-595-7067"}]


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
    patient = add_new_patient(new_dict["patient_id"],
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
                       "timestamp": [string_recorded_datetime]}
        patient_hr_db.append(new_patient)
        print(patient_hr_db)
        return "New Patient Added to Track HR"
    else:
        for patient, patient_name in zip(patient_hr_db, patient_db):
            if patient["patient_id"] != patient_id:
                continue
            elif patient["patient_id"] is patient_id:
                patient["heart_rate"].append(heart_rate)
                patient["timestamp"].append(string_recorded_datetime)
                age = patient_name["patient_age"]
                result = is_tachycardic(age, heart_rate)
                if result is True:
                    attending_phys = patient_name["attending_username"]
                    for attending in attending_db:
                        if attending["attending_username"] != attending_phys:
                            continue
                        else:
                            attending_email = attending["attending_email"]
                            logging.info("Tachycardic heart rate identified")
                            logging.info("Patient ID: {}".format(patient_id))
                            logging.info("Patient Heart Rate"
                                         ": {}".format(heart_rate))
                            logging.info("Attending Physician Email"
                                         ": {}".format(attending_email))
                            send_email(attending_email, patient_id)
                print(patient_hr_db)
                return "Current Patient Edited: Added New HR"


def send_email(attending_email, patient_id):
    x = {
         "from_email": "brad@test.com",
         "to_email": attending_email,
         "subject": "Update about patient " + str(patient_id),
         "content": str(patient_id) + " is tachycardic"}
    r = requests.post("http://vcm-7631.vm.duke.edu:5007/hrss/send_email",
                      json=x)
    print(r.status_code)
    print(r.text)


def avg_hr_calc(patient_hr_db, patient_id, time):
    patient_id = int(patient_id)
    for patient in patient_hr_db:
        if patient_id == patient["patient_id"]:
            timestamp = patient["timestamp"].index(time)
            hr_vals = patient["heart_rate"]
            hr_vals = hr_vals.reverse()
            indicator = len(patient["heart_rate"]) - timestamp
            relevant_hr = patient["heart_rate"][:indicator]
            avg_hr = sum(relevant_hr) / len(relevant_hr)
            return avg_hr, True
        else:
            continue


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def post_hr_avg():
    new_dict = request.get_json()
    patient_id = new_dict["patient_id"]
    timestampOI = new_dict["heart_rate_average_since"]
    # patient_hr_db should be of global scope
    validate = avg_hr_calc(patient_hr_db, patient_id, timestampOI)
    if validate[1] is not True:
        return validate, 400
    else:
        return validate[0]


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


def heart_rate_list(patient_id):
    patient_id = int(patient_id)
    for patient in patient_hr_db:
        if patient["patient_id"] != patient_id:
            continue
        elif patient["patient_id"] is patient_id:
            hr_list = patient["heart_rate"]
    return hr_list


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_heart_rate_list(patient_id):
    hr_list = heart_rate_list(patient_id)
    print(hr_list)
    if hr_list:
        return jsonify(hr_list), 200
    else:
        return "Heart Rate List not able to be returned", 400


def patient_status(patient_id):
    patient_id = int(patient_id)
    for patient, names in zip(patient_hr_db, patient_db):
        if patient["patient_id"] != patient_id:
            continue
        elif patient["patient_id"] is patient_id:
            list_size = len(patient["heart_rate"])
            latest_hr = patient["heart_rate"][list_size-1]
            datetime = patient["timestamp"][list_size-1]
            age = names["patient_age"]
            hr_result = is_tachycardic(age, latest_hr)
            if hr_result is False:
                out_dict = {"heart_rate": latest_hr,
                            "status": "not tachycardic",
                            "timestamp": datetime}
                return out_dict
            elif hr_result is True:
                out_dict = {"heart_rate": latest_hr,
                            "status": "tachycardic",
                            "timestamp": datetime}
                return out_dict


@app.route("/api/status/<patient_id>", methods=["GET"])
def get_patient_status(patient_id):
    status_dict = patient_status(patient_id)
    if status_dict:
        print(status_dict)
        return jsonify(status_dict), 200
    else:
        return "Patient Status not able to be returned", 400


def total_hr_avg(patient_id):
    patient_id = int(patient_id)
    for patient in patient_hr_db:
        if patient_id == patient["patient_id"]:
            hr_vals = patient["heart_rate"]
            avg_hr = sum(hr_vals) / len(hr_vals)
            out_dict = {"Average heart rate": avg_hr}
            return out_dict
        else:
            continue


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def get_hr_avg(patient_id):
    status_dict = total_hr_avg(patient_id)
    if status_dict:
        print(status_dict)
        return jsonify(status_dict), 200
    else:
        return "Patient's average heart rate not able to be returned", 400


def attending_patients(patient_db, attending_username, patient_hr_db):
    attending_patient_list = []
    for patient in patient_db:
        out_dict = {"patient_id": 0, "last_heart_rate": 0,
                    "last_time": "", "status": ""}
        out_dict["patient_id"] = patient["patient_id"]
        # I think age is in the right place- needs to update each i
        age = patient["patient_age"]
        if attending_username == patient["attending_username"]:
            x = patient["patient_id"]
            for patient in patient_hr_db:
                if x == patient["patient_id"]:
                    index = len(patient["heart_rate"]) - 1
                    out_dict["last_heart_rate"] = patient["heart_rate"][index]
                    out_dict["last_time"] = patient["timestamp"][index]
                    result = is_tachycardic(age, out_dict["last_heart_rate"])
                    if result is True:
                        out_dict["status"] = "tachycardic"
                    else:
                        out_dict["status"] = "not tachycardic"
            attending_patient_list.append(out_dict)
    # should be global scope of attending_db
    attending_check = []
    for attending in attending_db:
        if attending_username == attending["attending_username"]:
            attending_check.append("Exists")
    print(len(attending_check))
    if len(attending_check) == 0:
        return False, "Attending Physician does not exist in the database"
    print(attending_patient_list)
    return True, attending_patient_list


@app.route("/api/patients/<attending_username>", methods=["GET"])
def get_attending_username(patient_db, attending_username, patient_hr_db):
    status_dict = attending_patients(patient_db, attending_username,
                                     patient_hr_db)
    # First element is "True", Second element is the dictionary
    if status_dict[0] is true:
        return jsonify(status_dict), 200
    else:
        return "Patient's average heart rate not able to be returned", 400


if __name__ == '__main__':
    start_logging()
    app.run()
