from flask import Flask
from flask_restful import Api

from analytical_validation.api import UploadData, ViewData

app = Flask(__name__)
api = Api(app)

api.add_resource(UploadData, '/')
api.add_resource(ViewData, '/data')

if __name__ == '__main__':
    app.run(debug=True)
