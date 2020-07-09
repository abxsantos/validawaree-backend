from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from analytical_validation.api import LinearityValidation

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(LinearityValidation, '/linearity_result')

if __name__ == '__main__':
    app.run()
