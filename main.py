"""Main module"""
from src.app import app
# to register routes to API endpoints
import src.rest_api # pylint: disable=unused-import

if __name__ == '__main__':
    app.run(port=5000)
