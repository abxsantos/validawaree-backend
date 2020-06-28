from flask import Flask
from flask_restful import Api

from analytical_validation.api import LinearityValidation

app = Flask(__name__)
api = Api(app)

api.add_resource(LinearityValidation, '/linearity_data')

if __name__ == '__main__':
    app.run(debug=True)
