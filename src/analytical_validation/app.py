from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from analytical_validation.api import LinearityValidation


def create_app():
    app = Flask(__name__)
    return app

app = create_app()

CORS(app)
api = Api(app)
api.add_resource(LinearityValidation, '/linearity_result')


if __name__ == '__main__':
    app.run()
