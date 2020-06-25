"""Module that encapsulates flask app and flask_restplus api object creation."""
from flask import Flask, url_for
from flask_restplus import Api

from src.config import SECURE_DEPLOYMENT

app = Flask(__name__)  # pylint: disable=invalid-name

if SECURE_DEPLOYMENT:
    @property
    def specs_url(self):
        """Create function to override http/https scheme via Api.specs_url ."""
        return url_for(self.endpoint('specs'), _external=True, _scheme='https')
    Api.specs_url = specs_url

api = Api(app,  # pylint: disable=invalid-name
          version='1.0',
          title='Probable CVE',
          description='Probable CVE Endpoints',
          doc="/api/swagger")
