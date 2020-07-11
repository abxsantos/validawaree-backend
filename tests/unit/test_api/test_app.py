import json

import pytest

url = 'http://127.0.0.1:5000'  # The root url of the flask app

from analytical_validation.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


class TestApp(object):
    def test_linearity_result_page_must_not_allow_get_in_linearity_result_page(self, client):
        response = client.get('/linearity_result') # Assumses that it has a path of "/linearity_result"
        assert response.status_code == 405  # Assumes that it will return a 405 response, method not allowed


    def test_linearity_result_page_must_assert(self, client):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }
        data = {"analytical_data": "[[0.188, 0.192, 0.203], [0.349, 0.346, 0.348]]", "concentration_data": "[[0.008, 0.008, 0.008], [0.016, 0.016, 0.016]]"}

        response = client.post(url + '/linearity_result', data=json.dumps(data), headers=headers)
        assert response.status_code == 201
