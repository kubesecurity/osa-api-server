from src.app import server

# Need to import all resources
from src.rest_api import *

if __name__ == '__main__':
    server.run()
