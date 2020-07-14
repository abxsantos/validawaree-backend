from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from analytical_validation.resources.linearity_api import Linearity
from analytical_validation.resources.api_docs import ApiDocs

def create_app():
    app = Flask(__name__)
    return app

app = create_app()

CORS(app)
api = Api(app)

api.add_resource(ApiDocs, '/api_docs')
api.add_resource(Linearity, '/linearity')


if __name__ == '__main__':
    app.run()
