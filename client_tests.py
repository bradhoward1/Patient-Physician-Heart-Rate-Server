# client_tests.py

import requests

# Testing /api/new_patient

out = {"patient_id": 1,
       "attending_username": "Smith.J",
       "patient_age": 50}
r = requests.post("http://127.0.0.1:5000/api/new_patient", json=out)
print("{}, {}".format(r.text, r.status_code))

out = {"patient_id": 2,
       "attending_username": "Howard.B",
       "patient_age": 25}
r = requests.post("http://127.0.0.1:5000/api/new_patient", json=out)
print("{}, {}".format(r.text, r.status_code))

out_json = {"patient_id": 3,
            "attending_username": "Smith.J",
            "patient_age": 32}
r = requests.post("http://127.0.0.1:5000/api/new_patient", json=out_json)
print("{}, {}".format(r.text, r.status_code))

# Testing /api/new_attending

out = {"attending_username": "Smith.J",
       "attending_email": "smith@test.com",
       "attending_phone": "919-867-5309"}
r = requests.post("http://127.0.0.1:5000/api/new_attending", json=out)
print("{}, {}".format(r.text, r.status_code))

out = {"attending_username": "Howard.B",
       "attending_email": "brad@test.com",
       "attending_phone": "239-595-7067"}
r = requests.post("http://127.0.0.1:5000/api/new_attending", json=out)
print("{}, {}".format(r.text, r.status_code))

# Testing /api/heart_rate
out = {"patient_id": 1,
       "heart_rate": 100}
r = requests.post("http://127.0.0.1:5000/api/heart_rate", json=out)
print("{}, {}".format(r.text, r.status_code))

out = {"patient_id": 1,
       "heart_rate": 120}
r = requests.post("http://127.0.0.1:5000/api/heart_rate", json=out)
print("{}, {}".format(r.text, r.status_code))

out = {"patient_id": 1,
       "heart_rate": 90}
r = requests.post("http://127.0.0.1:5000/api/heart_rate", json=out)
print("{}, {}".format(r.text, r.status_code))

out = {"patient_id": 1,
       "heart_rate": 80}
r = requests.post("http://127.0.0.1:5000/api/heart_rate", json=out)
print("{}, {}".format(r.text, r.status_code))

out = {"patient_id": 2,
       "heart_rate": 120}
r = requests.post("http://127.0.0.1:5000/api/heart_rate", json=out)
print("{}, {}".format(r.text, r.status_code))

out = {"patient_id": 2,
       "heart_rate": 90}
r = requests.post("http://127.0.0.1:5000/api/heart_rate", json=out)
print("{}, {}".format(r.text, r.status_code))

out = {"patient_id": 2,
       "heart_rate": 200}
r = requests.post("http://127.0.0.1:5000/api/heart_rate", json=out)
print("{}, {}".format(r.text, r.status_code))

out = {"patient_id": 3,
       "heart_rate": 160}
r = requests.post("http://127.0.0.1:5000/api/heart_rate", json=out)
print("{}, {}".format(r.text, r.status_code))
# Testing /api/status/<patient_id>

r = requests.get("http://127.0.0.1:5000/api/status/1")
print("{}, {}".format(r.text, r.status_code))

r = requests.get("http://127.0.0.1:5000/api/status/2")
print("{}, {}".format(r.text, r.status_code))

# Testing /api/heart_rate/<patient_id>

r = requests.get("http://127.0.0.1:5000/api/heart_rate/1")
print("{}, {}".format(r.text, r.status_code))

r = requests.get("http://127.0.0.1:5000/api/heart_rate/2")
print("{}, {}".format(r.text, r.status_code))

# Testing /api/heart_rate_average/<patient_id>

r = requests.get("http://127.0.0.1:5000/api/heart_rate/average/1")
print("{}, {}".format(r.text, r.status_code))

r = requests.get("http://127.0.0.1:5000/api/heart_rate/average/2")
print("{}, {}".format(r.text, r.status_code))

# Testing /api/heart_rate/interval_average

out = {"patient_id": 2,
       "heart_rate_average_since": "2019-12-20 14:53:43"}
r = requests.post("http://127.0.0.1:5000/api/"
                  "heart_rate/interval_average", json=out)
print("{}, {}".format(r.text, r.status_code))

# Testing /api/patients/<attending_username>

r = requests.get("http://127.0.0.1:5000/api/patients/Smith.J")
print("{}, {}".format(r.text, r.status_code))
