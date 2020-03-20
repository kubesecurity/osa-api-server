"""Module that encapsulates flask app and flask_restplus api object creation."""
from flask import Flask
from flask_restplus import Api

app = Flask(__name__)  # pylint: disable=invalid-name
api = Api(app,  # pylint: disable=invalid-name
          version='1.0',
          title='Probable CVE',
          description='Probable CVE Endpoints',
          doc="/api/swagger")
