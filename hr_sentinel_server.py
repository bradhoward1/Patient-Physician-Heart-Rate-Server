# hr_sentinel_server.py

from flask import Flask, request, jsonify
import logging
from datetime import datetime
import requests


app = Flask(__name__)
attending_db = list()
patient_hr_db = list()
patient_db = []

patient_hr_db = [{"patient_id": 1,
                  "heart_rate": [80, 90, 160],
                  "timestamp": ["2018-03-09 11:00:36",
                                "2018-03-09 11:10:36",
                                "2018-03-09 11:20:36"]},
                 {"patient_id": 2,
                  "heart_rate": [70, 80],
                  "timestamp": ["2019-07-10 1:30:50",
                                "2020-05-10 1:50:50"]},
                 {"patient_id": 3,
                  "heart_rate": [50, 60, 70],
                  "timestamp": ["2018-03-09 11:00:36",
                                "2018-03-09 11:20:36",
                                "2018-03-09 11:50:36"]}]
patient_db = [{"patient_id": 1,
               "attending_username": "Smith.J",
               "patient_age": 50},
              {"patient_id": 2,
               "attending_username": "Howard.B",
               "patient_age": 25},
              {"patient_id": 3,
               "attending_username": "Smith.J",
               "patient_age": 32}]
attending_db = [{"attending_username": "Smith.J",
                 "attending_email": "smith@test.com",
                 "attending_phone": "919-867-5309"},
                {"attending_username": "Howard.B",
                 "attending_email": "brad@test.com",
                 "attending_phone": "239-595-7067"}]


def add_new_attending(username_id, email, phone):
    """Creates a dictionary for a new attending physician

    Every time the user wants to add a new attending physician
    to the attending physician database, this function
    must be called. This function reads in from the user the
    physician’s user name, their email, and their phone
    number. Then, it adds a dictionary containing the
    keys “attending_username”, “attending_email”,
    and “attending_phone” to the attending database.
    If this is successful, then ‘True’ is outputted.

    Parameters
    ----------
    username_id : String
        Gives the unique username of the attending physician
    email: String
        Gives the unique email of the attending physician
    phone: String
        Gives the unique phone number of the attending physician

    Returns
    -------
    bool
        True if successful
    """
    new_attending = {"attending_username": username_id,
                     "attending_email": email,
                     "attending_phone": phone}
    attending_db.append(new_attending)
    print(attending_db)
    return True


def validate_new_attending(attending_dict):
    """Ensures that inputs are in the correct format

    When a new attending physician is added, it is important
    to ensure that the inputs from the user are in the correct
    format. It takes in the newest attending physician dictionary
    as the input, and checks to see that each entry in the
    dictionary is a string. If so, then the code will return True.
    If this is not the case, then the program will return either
    of the following:
        - “{} key not found”
        - “{} key is the wrong value type”

    Parameters
    ----------
    attending_dict : dictionary
        Dictionary of attending physician’s information

    Returns
    -------
    bool
        True if successful, other message if otherwise
    """
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
    """Posts attending physician information to the server

    This method generates the new attending physician’s
    dictionary with all of his/her information, then validates
    that all of the information is the correct type. If the
    validation stage is satisfied, then the attending’s
    dictionary is added to the database.

    Parameters
    ----------
    N/A

    Returns
    -------
    String
        result of adding a new attending
    """
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
    """Creates a dictionary for a new patient

    Every time the user wants to add a new patient
    to the patient database, this function
    must be called. This function reads in from the user the
    patient's ID, attending physician, and age. Then, it
    adds a dictionary containing the
    keys "patient_id", "attending_username",
    and "patient_age" to the patient database.
    If this is successful, then ‘True’ is outputted.

    Parameters
    ----------
    id : String
        Gives the unique username of the attending physician
    attending: String
        Gives the unique email of the attending physician
    age: int
        Gives the unique phone number of the attending physician

    Returns
    -------
    bool
        True if successful
    """
    new_patient = {"patient_id": id,
                   "attending_username": attending,
                   "patient_age": age}
    patient_db.append(new_patient)
    print(patient_db)
    return True


def validate_new_patient(patient_dict):
    """Ensures that inputs are in the correct format

    When a new patient is added, it is important
    to ensure that the inputs from the user are in the correct
    format. It takes in the newest patient dictionary
    as the input, and checks to see that each entry in the
    dictionary is a string. If so, then the code will return True.
    If this is not the case, then the program will return the following:
        - “{} is an invalid input”

    Parameters
    ----------
    patient_dict : dictionary
        Dictionary of attending physician’s information

    Returns
    -------
    bool
        True if successful, other message if otherwise
    """
    x = patient_dict["patient_id"]
    y = patient_dict["attending_username"]
    z = patient_dict["patient_age"]
    # checking to see if already int or can be converted
    try:
        x = int(x)
    except:
        return("{} is an invalid input".format(x))
    # checking to see if already int or can be converted
    try:
        z = int(z)
    except:
        return("{} is an invalid input".format(z))
    # make sure string is in "Smith.J" format
    try:
        check = y.split(".")
        if len(check[1]) != 1:
            return("{} is an invalid format".format(y))
    except:
        return("{} is an invalid input".format(y))
    return True


@app.route("/api/new_patient", methods=["POST"])
def post_new_patient():
    """Posts new patient information to the server

    This method generates the new patient's
    dictionary with all of his/her information, then validates
    that all of the information is the correct type. If the
    validation stage is satisfied, then the new patient's
    dictionary is added to the database.

    Parameters
    ----------
    N/A

    Returns
    -------
    String
        result of adding a new attending
    """
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
    """Initializes the logging file

    This method is run at the beginning of the main function.
    It initializes the logging file and ensures that proper logging
    will occur within the server.

    Parameters
    ----------
    N/A

    Returns
    -------
    bool
        Returns True
    """
    logging.basicConfig(filename='my_log.log', filemode='w',
                        level=logging.DEBUG)
    logging.info("-----New Run-----\n")
    return True


def validate_incoming_heart_rate(in_dict):
    """Ensures that inputs are in the correct format

    When a new heart rate is added to the database, it is
    important to ensure that the inputs from the user are in
    the correct format. It takes in the newest heart rate
    dictionary as the input, and checks to see that each entry
    in the dictionary is an integer. If so, then the code
    will return True. If this is not the case, then the program
    will return either of the following:
        - “{} key not found”
        - “{} key is the wrong value type”

    Parameters
    ----------
    in_dict : dictionary
        Dictionary of new heart rate information

    Returns
    -------
    bool
        True if successful, other message if otherwise
    """
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
    """Creates a dictionary for new heart rate information

    This method reads in information from the user: patient_id
    and that patient’s most recent heart rate recording. If
    the patient is new, then that patient is added to the patient
    database. In the database, the following dictionary will be
    added.
        {
            “patient_id”: int
            “heart_rate”: list of all heart rates
            “timestamp”: list of all timestamps for all heart rates
        }
    If the patient is not new, then the “heart_rate” and “timestamp”
    keys will be adjusted, having the most recent heart rate and
    most recent timestamp being added to the two lists within
    those keys. If a new patient is added, then the function will
    return “New Patient Added to Track HR”. If the patient already
    exists, then the function will return “Current Patient Edited:
    Added New HR”.
    Furthermore, this function checks the age of the patient
    to see if the most recent information indicates
    tachycardia. If not, then the heart rate is added and the
    function terminates. If it is tachycardic, then an email
    is sent to that patient’s attending physician informing them
    that their patient is suffering from tachycardia.

    Parameters
    ----------
    patient_id : int
        Gives the unique id of the given patient
    heart_rate: int
        Gives the most recent heart rate of the patient

    Returns
    -------
    String
        Differing messages based on results
    """
    recorded_datetime = datetime.now()
    string_recorded_datetime = datetime.strftime(
            recorded_datetime,  "%Y-%m-%d %H:%M:%S")
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
    """Sends email to physician

    If a patient is deemed tachycardic, then their physician
    must be informed. This function reads in a patient’s
    ID as well as that patient’s attending physician’s
    email. Then, it will create a dictionary with the following
    format.
        {
         "from_email": "brad@test.com",
         "to_email": attending_email,
         "subject": "Update about patient " + str(patient_id),
         "content": str(patient_id) + " is tachycardic"}
    This dictionary is posted to a unique server of Dr.
    Ward’s choosing. This indicates a successful
    email submission.

    Parameters
    ----------
    patient_id : int
        Gives the unique id of the given patient
    attending_email: String
        Gives the unique email of the attending physician

    Returns
    -------
    N/A
    """
    x = {
         "from_email": "brad@test.com",
         "to_email": attending_email,
         "subject": "Update about patient " + str(patient_id),
         "content": str(patient_id) + " is tachycardic"}
    r = requests.post("http://vcm-7631.vm.duke.edu:5007/hrss/send_email",
                      json=x)
    print(r.status_code)
    print(r.text)


def avg_hr_calc(patient_id, timestamp):
    """Calculates average heart rate

    This method computes a patient's average heart. This function
    takes patient_id and timestamp as input and returns
    the patient's average heart rate since the most recent
    time given. The time given does not have to be the time
    at which a recording was obtained.

    Parameters
    ----------
    patient_id : int
        Gives the unique id of the given patient
    timestamp: String
        Time of requested computation

    Returns
    -------
    int
        average heart rate"""
    patient_id = int(patient_id)
    time_compare = time_converter(timestamp)
    # print("Time compare is {}".format(time_compare))
    for patient in patient_hr_db:
        if patient_id == patient["patient_id"]:
            hr_empty = []
            for i in patient["timestamp"]:
                time_x = time_converter(i)
                # print(time_x)
                if time_compare <= time_x:
                    hr_empty.append(i)
            # hr_empty will now contain list of corresponding times
            # print("HR_EMPTY: {}".format(hr_empty))
            index_array = []
            for j in hr_empty:
                index = patient["timestamp"].index(j)
                index_array.append(index)
            # index_array contains indices of necessary heart rates
            # print("INDEX ARRAY: ".format(index_array))
            HR_VALS = []
            for k in index_array:
                HR = patient["heart_rate"][k]
                # print(HR)
                HR_VALS.append(HR)
            avg_hr = round(sum(HR_VALS) / len(HR_VALS))
            return avg_hr
        else:
            continue


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def post_hr_avg():
    """Posts average heart rate information to the server

    This method posts a patient's average heart rate
    and time since the average heart rate
    calculation was completed.

    Parameters
    ----------
    N/A

    Returns
    -------
    String
        result of adding a new average heart rate
    """
    new_dict = request.get_json()
    patient_id = new_dict["patient_id"]
    time = new_dict["heart_rate_average_since"]
    # patient_hr_db should be of global scope
    validate = avg_hr_calc(patient_id, time)
    # print(validate)
    if validate:
        return jsonify(validate), 200
    else:
        return jsonify(validate), 400


@app.route("/api/heart_rate", methods=["POST"])
def post_heart_rate():
    """Posts heart rate information to the server

    This method generates the patient heart rate
    dictionary with all of his/her information, then validates
    that all of the information is the correct type. If the
    validation stage is satisfied, then the patient’s
    dictionary is added to the database. If this patient
    already exists, then their prior information is appended.

    Parameters
    ----------
    N/A

    Returns
    -------
    String
        result of adding a new heart rate
    """
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
    """Determines if a given heart rate indicates tachycardia

    Every time a new heart rate is added to the server, it is
    necessary to ensure that the given heart rate does not
    indicate tachycardia in that given patient. This function
    reads in an age and a heart rate, then runs through a quick
    algorithm to test to see whether or not that given heart rate
    Indicates tachycardia at that specified age. If the patient
    is tachycardic, then the function returns True. Otherwise,
    the function returns False.

    Parameters
    ----------
    age : int
        Gives the age of a patient
    heart_rate : int
        Gives the heart rate of a patient

    Returns
    -------
    bool
        True if tachycardic, False if not
    """
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
    """Generates a list of heart rates for a given patient

    This function reads in a given patient ID from the user,
    searches for that patient in the database, and returns
    a list of all of that patient’s recorded heart rates.

    Parameters
    ----------
    patient_id : int
        Gives the unique id of the given patient

    Returns
    -------
    list
        List of all heart rates for given patient
    """
    patient_id = int(patient_id)
    hr_list = list()
    for patient in patient_hr_db:
        if patient["patient_id"] != patient_id:
            continue
        elif patient["patient_id"] is patient_id:
            hr_list = patient["heart_rate"]
    return hr_list


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_heart_rate_list(patient_id):
    """Generates a list of heart rates for a given patient

    This function receives information from the server. The URL
    includes which patient the user wants to analyze, and then
    the method uses that inputted ID to search the database,
    find the given patient, and print out all of that patient’s
    heart rates. If it is unsuccessful in retrieving information,
    the function will return “Heart Rate List not able to be
    returned”

    Parameters
    ----------
    patient_id : String
        Gives the unique id of the given patient

    Returns
    -------
    list
        List of all heart rates for given patient
    """
    hr_list = heart_rate_list(patient_id)
    print(hr_list)
    if hr_list:
        return jsonify(hr_list), 200
    else:
        return "Heart Rate List not able to be returned", 400


def patient_status(patient_id):
    """Creates a dictionary to document patient status

    This function reads in the patient_id from the user.
    With this ID, this function searches the database for
    that patient, finds their latest heart rate and its
    time stamp, determines whether or not this heart rate
    indicates tachycardia, and returns a dictionary
    containing the result. The dictionary will have the following
    format.
                           {"heart_rate": latest_hr,
                            "status": "not tachycardic" | “tachycardic”,
                            "timestamp": datetime}

    If the patient is tachycardic, the dictionary above will return
    that, but if the patient is not tachycardic, the dictionary
    above will return “not tachycardic”. Then, the dictionary
    is returned.

    Parameters
    ----------
    patient_id : String
        Gives the unique id of the given patient

    Returns
    -------
    dictionary
        Dictionary containing patient heart status
    """
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
    """Generates a dictionary regarding patient status

    This function receives information from the server. The URL
    includes which patient the user wants to analyze, and then
    the method uses that inputted ID to search the database,
    find the given patient, determine that patient’s latest heart
    rate with its corresponding time stamp, and test to see
    whether this heart rate indicates tachycardia. Then, it
    will generate a dictionary using the ‘patient_status()’
    function and output that patient’s heart status.

    Parameters
    ----------
    patient_id : String
        Gives the unique id of the given patient

    Returns
    -------
    dictionary
        Dictionary containing patient heart status
    String
        If unable to get dictionary, prints errors message
    """
    status_dict = patient_status(patient_id)
    if status_dict:
        print(status_dict)
        return jsonify(status_dict), 200
    else:
        return "Patient Status not able to be returned", 400


def total_hr_avg(patient_id):
    """Average heart rate calculator

    Used exclusively for calculating a patient's
    total heart rate across all measurements.
    Takes a patient's ID as input.

    Parameters
    ----------
    patient_id : String
        Gives the unique id of the given patient

    Returns
    -------
    int
        total average heart rate
    """
    patient_id = int(patient_id)
    for patient in patient_hr_db:
        if patient_id == patient["patient_id"]:
            hr_vals = patient["heart_rate"]
            avg_hr = round(sum(hr_vals) / len(hr_vals))
            out_dict = {"Average heart rate": avg_hr}
            return out_dict
        else:
            continue


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def get_hr_avg(patient_id):
    """Generates the average heart rate for a given patient

    This method should return the patient's average heart
    rate, as an integer, of all measurements that have
    been stored for a patient.

    Parameters
    ----------
    patient_id : String
        Gives the unique id of the given patient

    Returns
    -------
    int
        Average heart rate
    """
    status_dict = total_hr_avg(patient_id)
    if status_dict:
        print(status_dict)
        return jsonify(status_dict), 200
    else:
        return "Patient's average heart rate not able to be returned", 400


def attending_patients(attending_username):
    """Compiles list of an attending physician's patients

    This function receives an attending physician's
    username and in return, returns a list of the
    information of all an attending physician's
    patients.

    Parameters
    ----------
    attending_username: String
        ID of attending physician

    Returns
    -------
    list
        List of dictionaries of info of all
        patients of an attending physician.
    """
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
    if len(attending_check) == 0:
        return "Attending Physician does not exist in the database"
    print(attending_patient_list)
    return attending_patient_list


@app.route("/api/patients/<attending_username>", methods=["GET"])
def get_attending_username(attending_username):
    """Returns information on all patients of a physician

    This route should return a list where each entry of the list
    represents data from a patient of this physician. Each entry
    in the list should be a JSON string in the following format:
    {
    "patient_id": 1,
    "last_heart_rate": 80,
    "last_time": "2018-03-09 11:00:36",
    "status":  "tachycardic" | "not tachycardic"
    }

    Parameters
    ----------
    attending_username: String
        Username of attending physician

    Returns
    -------
    list
        List of all patient data for an attending physician
    """
    status_dict = attending_patients(attending_username)
    # First element is "True", Second element is the dictionary
    if status_dict:
        return jsonify(status_dict), 200
    elif status_dict == "Attending Physician does not exist in the database":
        return "Patient's average heart rate not able to be returned", 400


def time_converter(time_stamp):
    """Timestamp converter

    Turns a string timestamp into a datetime timestamp.

    Parameters
    ----------
    time_stamp : String
        time at which average heart rate is being
        calculated since.

    Returns
    -------
    datetime.datetime
        timestamp
    """
    time_split = time_stamp.split()
    y_m_d = time_split[0]
    y_m_d = y_m_d.split("-")
    y = int(y_m_d[0])
    # print("y = {}".format(y))
    m = int(y_m_d[1])
    # print("m = {}".format(m))
    d = int(y_m_d[2])
    # print("d = {}".format(d))
    h_m_s = time_split[1]
    h_m_s = h_m_s.split(":")
    h = int(h_m_s[0])
    mi = int(h_m_s[1])
    s = int(h_m_s[2])
    timestamp = datetime(y, m, d, h, mi, s, 0)
    # print("TimeSTAMP = {}".format(timestamp))
    return timestamp

if __name__ == '__main__':
    start_logging()
    app.run()
