# hr_sentinel_server.py

from flask import Flask, request, jsonify

app = Flask(__name__)
attending_db = list()


def add_new_attending(username_id, email, phone):
    new_attending = {"attending_username": username_id,
                     "attending_email": email,
                     "attending_phone": phone}
    attending_db.append(new_attending)
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
