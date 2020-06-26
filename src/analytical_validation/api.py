import json

from flask_restful import Resource, reqparse

from analytical_validation.validators.linearity_validator import LinearityValidator

parser = reqparse.RequestParser()
parser.add_argument('analytical_data')
parser.add_argument('concentration_data')


class LinearityValidation(Resource):
    def post(self):
        args = parser.parse_args()

        analytical_data = json.loads(args['analytical_data'])
        concentration_data = json.loads(args['concentration_data'])
        try:
            linearity_validator = LinearityValidator(analytical_data, concentration_data)
            is_valid = linearity_validator.validate()
            return is_valid, 201
        except Exception as err:
            return err, 400
