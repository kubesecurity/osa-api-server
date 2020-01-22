from src.app import server

# import src/rest_api to register all endpoints with flask
from src.rest_api import app

if __name__ == '__main__':
    server.run()
