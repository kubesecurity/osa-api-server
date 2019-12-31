from app import server
import sys, os

# Need to import all resources
from api.cve import *

if __name__ == '__main__':
    server.run()