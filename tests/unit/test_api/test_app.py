import json

import pytest
from flask import url_for

url = 'http://127.0.0.1:5000'  # The root url of the flask app

from analytical_validation.app import create_app

@pytest.fixture
def client():
    return create_app().test_client()



def test_linearity_result_page_must_not_allow_get_in_linearity_result_page(client):
    r = client.get('http://127.0.0.1:5000/linearity_result') # Assumses that it has a path of "/linearity_result"
    assert r.status_code == 405  # Assumes that it will return a 405 response, method not allowed


def test_linearity_result_page_must_assert(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {"analytical_data": "[[0.188, 0.192, 0.203], [0.349, 0.346, 0.348]]", "concentration_data": "[[0.008, 0.008, 0.008], [0.016, 0.016, 0.016]]"}

    r = client.post(url + '/linearity_result', data=json.dumps(data), headers=headers)
    assert r.status_code == 200
