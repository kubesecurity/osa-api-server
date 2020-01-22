from flask import Flask
from flask_restplus import Api, Resource, fields

class Server(object):
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app,
            version='1.0',
            title='Probable CVE',
            description='Probable CVE Endpoints',
            doc = "/api/swagger"
        )

    def run(self):
        self.app.run(port = 5000)

server = Server()
