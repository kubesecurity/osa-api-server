from src.app import server

# import src/rest_api to register all endpoints with flask
import src.rest_api

if __name__ == '__main__':
    server.run()
