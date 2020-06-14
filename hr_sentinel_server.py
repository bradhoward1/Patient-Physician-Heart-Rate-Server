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
