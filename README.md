[![Build Status](https://travis-ci.com/BME547-Summer2020/heart-rate-sentinel-server-audibuild.svg?token=sKsYGbJ1i9ydp1r9jhAy&branch=master)](https://travis-ci.com/BME547-Summer2020/heart-rate-sentinel-server-audibuild)

# Patient-Physician Heart Rate Oversight Server
Team AudiBuild. Team name inspiration is from our Tympanometer Design Project with Dr. Palmeri.

This README.md file provides an in depth analysis of the functionality of the heart-rate-sentinel-server-audibuild repository.

## Instructions

### Running the Program

The `hr_sentinel_server.py` must be run through the command terminal if running it locally. It is currently running in a virtual machine, but if the user desires to test and view the server locally, contact either Robert Baldoni, Jr., or Bradley Howard, the two designers of the server, to gain access to it. If you have contacted us and have been verified to use the server, ensure that a virtual environment has been created in Python and that all of the packages mentioned in the 'requirements.txt' file are installed as well before running the server file. Note that this repository was deployed with Travis CI and follows the pep8 style guide.

### The Server

The server is developed in the `hr_sentinel_server.py` Python file. THE SERVER IS CURRENTLY TURNED ON AND LOCATED ON A SEPARATE VIRTUAL MACHINE. The host for this server is "vcm-15218.vm.duke.edu" and is located on port 5000. Thus, when attempting to run functions on the server, the user must ensure that the following is entered as the base URL:

1. "http://vcm-15218.vm.duke.edu:5000"

Within this server, the following functions have been implemented:

+ `POST /api/new_patient`
+ `POST /api/new_attending`
+ `POST /api/heart_rate`
+ `GET /api/status/<patient_id>`
+ `GET /api/heart_rate/<patient_id>`
+ `GET /api/heart_rate/average/<patient_id>`
+ `POST /api/heart_rate/interval_average`
+ `GET /api/patients/<attending_username>`

To perform unit tests on this server file (located in `test_hr_sentinel_server.py`), it was necessary to initialize a database that the server could post to and access information from. These "databases" are represented by three distinct lists. These lists are contained between lines 13 to 42. The server is currently ON with these lists commented out of the code, but the version of the server file that is listed in this repository has these lists included in the code. Comment these lines out if necessary.

Furthermore, one more change was made to the server file within the virtual machine that is different than the server file within this repository. To actually access this server outside of the virtual machine, the following `host` parameter is passed to the Flask handler command:

app.run(host="vcm-15218.vm.duke.edu")

With this change, it is possible to carry out functions in the server while outside of the virtual machine.  

### The Client

There is a client test file called `client_tests.py`. This file executes all of the implemented functions of the server. When the client file was uploaded to GitHub, the local host was utilized, so the following URL was used:

2. "http://127.0.0.1:5000"

If the user wants to test the server that is running on the vcm-15218.vm.duke.edu host, then it is necessary to replace the URL referenced by the number 2 above with the URL referenced by the number 1 at the beginning of the README.md file. 
