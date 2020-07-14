# VALIDAWAREE (backend)
Branch | Travis | Codecov
-------|--------|---------
master | [![Build Status](https://travis-ci.org/abxsantos/validawaree-backend.svg?branch=master)](https://travis-ci.org/abxsantos/validawaree-backend) | [![codecov](https://codecov.io/gh/abxsantos/validawaree-backend/branch/master/graph/badge.svg)](https://codecov.io/gh/abxsantos/validawaree-backend)

VALIDAWAREE is a scientific web application capable of validating experimental analytical data based on the latest ANVISA (Brazilian National Sanitary Surveillance Agency). 

This repository contains the backend for this application, which can also be installed and used as a python package, or as an API.

## Setup

Currently the project runs on python 3.6 +.

- Install python version 3.6+
- Create a and activate a virtual environment:
    ```
   virtualenv venv --python=python3
   source ./venv/bin/activate
   ```
    
     
- Install the dependencies:
    ```
    pip -r requirements.txt
    ```
- To run the app use:
    ```
    flask run
    ```
- Navigate to http://localhost:5000 in your browser.
- See http://localhost:5000/api_docs for the API documentation.

## Run tests

The tests are located inside the tests folder in the root directory. 
To check, simply run in the terminal with the virtual environment activated:
    ```
    pytest tests/
    ```
    
## Branches

The repository contains one permanent branch:

- **master**: Contains the code that has been released.