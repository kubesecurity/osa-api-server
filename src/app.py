"""Module that encapsulates flask app and flask_restplus api object creation."""
import sentry_sdk
from flask import Flask
from flask_restplus import Api
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.middleware.proxy_fix import ProxyFix

from src import config

# initialize sentry for error logging
sentry_sdk.init(
    dsn=config.SENTRY_DSN,
    integrations=[FlaskIntegration()]
)

app = Flask(__name__)  # pylint: disable=invalid-name

# fix for swagger.json to go over HTTP/HTTPS
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

api = Api(app,  # pylint: disable=invalid-name
          version='1.0',
          title='Probable CVE',
          description='Probable CVE Endpoints',
          doc="/api/swagger")
