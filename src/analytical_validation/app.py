from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from analytical_validation.resources.linearity_api import Linearity

def create_app():
    app = Flask(__name__)
    return app

app = create_app()

### swagger specific ###
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
### end swagger specific ###

CORS(app)
api = Api(app)

api.add_resource(Linearity, '/linearity')


if __name__ == '__main__':
    app.run()
