# ONDC BPP Protocol Layer(Python)
BPP Protocol Layer written in python

## Features
1) uses json-schema for schema-validation for request and responses of Network calls
2) handles async operation (getting results from client and sending back to network)


## Local Setup
1. Install [Python3](https://www.python.org/downloads/) and [pip3](https://www.activestate.com/resources/quick-reads/how-to-install-and-use-pip3/)
2. Install the current version of Mongo DB from [here](https://docs.mongodb.com/manual/installation/)
3. Create virtual environment and activate [here](https://docs.python.org/3/library/venv.html))
4. `pip3 install -r requirements.txt`
5. `export ENV=dev`
6. Make webserver as root directory and `cd webserver`
7. `python -m manage`

