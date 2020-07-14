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
        response = client.get('/linearity')
        assert response.status_code == 405

    def test_linearity_result_page_must_assert(self, client):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        json_data = {"analytical_data": '[[0.188, 0.192, 0.203], [0.349, 0.346, 0.348]]',
                     "concentration_data": '[[0.008, 0.008, 0.008], [0.016, 0.016, 0.016]]'}
        assert client.post(url + '/linearity', data=json.dumps(json_data), headers=headers).status_code == 201

    @pytest.mark.parametrize('param_json_data, param_error', [
        ({"analytical_data": '"AAAAAA"', "concentration_data": '[[0.008, 0.008, 0.008], [0.016, 0.016, 0.016]]'},
         "One of the input data is not a list."),
        ({"analytical_data": '["BBBB",[1,2,3]]',
          "concentration_data": '[[0.008, 0.008, 0.008], [0.016, 0.016, 0.016]]'},
         'The given data is not a list of lists.'),
        ({"analytical_data": '[["CCCC",1,2],[1,2,3]]',
          "concentration_data": '[[0.008, 0.008, 0.008], [0.016, 0.016, 0.016]]'},
         "Non number values are not valid. Check and try again."),
        ({"analytical_data": "[[-3,1,2],[1,2,3]]",
             "concentration_data": "[[0.008, 0.008, 0.008], [0.016, 0.016, 0.016]]"
         }, "Negative values are not valid. Check and try again.")])
    def test_api_must_serve_exceptions_to_frontend(self, client, param_json_data, param_error):
        """"Given data that`s not a list, the api must send a message to frontend with the error"""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = client.post(url + '/linearity', data=json.dumps(param_json_data), headers=headers)
        assert response.status_code == 400
        assert response.json["body"] == param_error
