"""Abstracts REST end-point routers."""
from flask_restplus import Resource

from src.app import api
from src.feedback import add_feedback, get_feedback
from src.ingestion import ingest_data_into_graph
from src.query_graph import query_graph
from src.rest_model import POST_PCVE, GET_PCVE, POST_FEEDBACK, PARSER, POST_GREMLIN, FEEDBACK_PARSER, GET_FEEDBACK
from src.utils import fetch_nodes

ns_pcve = api.namespace('Probable CVE', path='/')
ns_feedback = api.namespace('Feedback', path='/')


@ns_pcve.route('/api/v1/pcve')
class RestApi(Resource):
    """Abstracts REST end-point routers."""

    @ns_pcve.expect(PARSER)
    @ns_pcve.marshal_list_with(GET_PCVE, skip_none=True)
    @ns_pcve.doc("List probable CVEs")
    def get(self):  # pylint: disable=no-self-use
        """List probable CVEs."""
        return query_graph(PARSER.parse_args())

    @ns_pcve.expect(POST_PCVE)
    @ns_pcve.doc("Ingest data into DB")
    def post(self):  # pylint: disable=no-self-use
        """Ingest data into DB."""
        return ingest_data_into_graph(api.payload)


@ns_feedback.route('/api/v1/feedback')
class Feedback(Resource):
    """Abstracts REST end-point routers."""

    @ns_feedback.expect(POST_FEEDBACK)
    @ns_feedback.doc("Post feedback for an event")
    def post(self):  # pylint: disable=no-self-use
        """Post feedback for an event."""
        return add_feedback(api.payload)

    @ns_feedback.expect(FEEDBACK_PARSER)
    @ns_feedback.marshal_list_with(GET_FEEDBACK, skip_none=True)
    @ns_feedback.doc("Get feedback for a security event")
    def get(self):
        """List feedback for given security event."""
        return get_feedback(FEEDBACK_PARSER.parse_args())


@api.route('/api/v1/graph', methods=['POST'])
@api.doc(False)
class GraphQuery(Resource):
    """Abstracts REST end-point routers."""

    # @api.marshal_list_with(GET_PCVE, skip_none=True)
    @api.expect(POST_GREMLIN)
    def post(self):
        """Endpoint to query graph db properties."""
        return fetch_nodes(api.payload)['result']['data']
