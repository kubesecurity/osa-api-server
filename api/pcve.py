from flask import Flask
from flask_restplus import Api, Resource, fields
from app import server
from flask_restplus import reqparse

from model.pcve import pcve
from src.ingestion import ingest_data_into_graph

app, api = server.app, server.api

parser = reqparse.RequestParser()
parser.add_argument('ecosystem', type=str, help='Ecosystem')
parser.add_argument('is_cve', type=bool, help='Is actually a CVE ?')
parser.add_argument('feedback', type=bool, help='Feedback updated true/false')
parser.add_argument('from_date', type=str, help='From date')
parser.add_argument('to_date', type=str, help='To date')
parser.add_argument('repo', type=str, help='Repository name')
parser.add_argument('event_type', type=str, help='Event type')

@api.route('/api/v1/pcve')
class PCVE(Resource):

    @api.expect(parser)
    @api.marshal_list_with(pcve)
    @api.doc("API to list probable CVEs")
    def get(self):
        query_graph(parser.parse_args())

    @api.expect([pcve])
    @api.doc("API to ingest data into DB")
    def post(self):
        ingest_data_into_graph(api.payload)
        return { 'status': 'success' }

    @api.expect(pcve)
    @api.marshal_list_with(pcve)
    @api.doc("API to update the feedback for probable cve. True/False")
    def put(self):

        #update the feedback text
        return api.payload

