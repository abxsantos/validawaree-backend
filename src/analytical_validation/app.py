from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from analytical_validation.resources.linearity_api import Linearity


def create_app():
    return Flask(__name__)


app = create_app()

SWAGGER_URL = '/api_docs'
API_URL = '/static/openapi.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "VALIDAWAREE"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

CORS(app)
api = Api(app)

api.add_resource(Linearity, '/linearity')

if __name__ == '__main__':
    app.run()
