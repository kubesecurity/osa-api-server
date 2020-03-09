"""Abstracts REST end-point routers"""
from flask_restplus import Resource

from src.app import api
from src.feedback import feedback
from src.ingestion import ingest_data_into_graph
from src.query_graph import query_graph
from src.rest_model import POST_PCVE, GET_PCVE, POST_FEEDBACK, PARSER

@api.route('/api/v1/pcve')
class RestApi(Resource):
    """Abstracts REST end-point routers"""
    @api.expect(PARSER)
    @api.marshal_list_with(GET_PCVE, skip_none=True)
    @api.doc("API to list probable CVEs")
    def get(self): # pylint: disable=no-self-use
        """API to list probable CVEs"""
        return query_graph(PARSER.parse_args())

    @api.expect(POST_PCVE)
    @api.doc("API to ingest data into DB")
    def post(self): # pylint: disable=no-self-use
        """API to ingest data into DB"""
        return ingest_data_into_graph(api.payload)


@api.route('/api/v1/feedback')
class Feedback(Resource):
    """Abstracts REST end-point routers"""
    @api.expect(POST_FEEDBACK)
    @api.doc("API to post feedback for an event")
    def post(self): # pylint: disable=no-self-use
        """API to post feedback for an event"""
        return feedback(api.payload)
