from flask import Flask
from flask_restplus import Resource
from app import server
from flask_restplus import reqparse

from model.pcve import POST_PCVE, GET_PCVE, PUT_FEEDBACK
from src.ingestion import ingest_data_into_graph
from src.query_graph import query_graph

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
    @api.marshal_list_with(GET_PCVE)
    @api.doc("API to list probable CVEs")
    def get(self):
        return query_graph(parser.parse_args())

    @api.expect([POST_PCVE])
    @api.doc("API to ingest data into DB")
    def post(self):
        return ingest_data_into_graph(api.payload)

    @api.expect(PUT_FEEDBACK)
    @api.doc("API to update the feedback for probable cve. True/False")
    def put(self):
        # todo
        pass

