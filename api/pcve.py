from flask import Flask
from flask_restplus import Resource
from app import server

from model.pcve import POST_PCVE, GET_PCVE, PUT_FEEDBACK, parser
from src.ingestion import ingest_data_into_graph
from src.query_graph import query_graph
from src.feedback import feedback

app, api = server.app, server.api

@api.route('/api/v1/pcve')
class PCVE(Resource):

    @api.expect(parser)
    @api.marshal_list_with(GET_PCVE, skip_none=True)
    @api.doc("API to list probable CVEs")
    def get(self):
        return query_graph(parser.parse_args())

    @api.expect([POST_PCVE])
    @api.doc("API to ingest data into DB")
    def post(self):
        return ingest_data_into_graph(api.payload)

    @api.expect([PUT_FEEDBACK])
    @api.doc("API to update the feedback for probable cve. True/False")
    def put(self):
        return feedback(api.payload)
