"""Module that encapsulates flask app and flask_restplus api object creation."""
from flask import Flask
from flask_restplus import Api

from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)  # pylint: disable=invalid-name

# fix for swagger.json to go over HTTP/HTTPS
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

api = Api(app,  # pylint: disable=invalid-name
          version='1.0',
          title='Probable CVE',
          description='Probable CVE Endpoints',
          doc="/api/swagger")
