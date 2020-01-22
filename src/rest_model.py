from flask_restplus import fields, reqparse
from src.app import server

from src.graph_model import FeedBackType, EventType
from src.parse_datetime import to_date_str, from_date_str

POST_PCVE = server.api.model('PCVE', {
    'ecosystem': fields.String(description='Ecosystem'),
    'repo_name': fields.String(description='Repository Name'),
    'event_type': fields.String(description='Event Type'),
    'status': fields.String(description='Status'),
    'url': fields.Url(description='url'),
    'id': fields.String(description='Event Id'),
    'number': fields.Integer('PR/Issue number'),
    'api_url': fields.Url(description='Github API'),
    'created_at': fields.DateTime(dt_format='iso8601'),
    'updated_at': fields.DateTime(dt_format='iso8601'),
    'closed_at': fields.DateTime(dt_format='iso8601'),
    'creator_name': fields.String,
    'creator_url': fields.Url(description='Creator Url'),
})

class ISO8601Format(fields.Raw):
    def format(self, value):
        return to_date_str(value)

parser = reqparse.RequestParser()
parser.add_argument('ecosystem', type=str, help='Ecosystem')
parser.add_argument('is_probable_cve', type=bool, help='Manually triaged as probable vulnerability')
parser.add_argument('feedback', type=bool, help='Feedback updated true/false')
parser.add_argument('from_date', type=from_date_str, help='Updated range - from')
parser.add_argument('to_date', type=from_date_str, help='Updated range - to')
parser.add_argument('repo', type=str, help='Repository name')
parser.add_argument('event_type', type=str, choices=(EventType._member_names_), help='Event type')

GET_PCVE = server.api.model('GET_PCVE', {
    'ecosystem': fields.String(description='Ecosystem'),
    'repo_name': fields.String(attribute='dependency.dependency_name', description='Repository Name'),
    'event_type': fields.String(attribute='security_event.event_type', description='Event Type', enum=EventType._member_names_),
    'status': fields.String(attribute='security_event.status', description='Status'),
    'url': fields.String(attribute='security_event.url', description='url'),
    'event_id': fields.String(attribute='security_event.event_id', description='Event Id from Github'),
    'probable_vuln_id': fields.String(attribute='probable_vulnerability.probable_vuln_id', description='Probable vulnerability ID'),
    'created_at': ISO8601Format(attribute='security_event.created_at'),
    'updated_at': ISO8601Format(attribute='security_event.updated_at'),
    'closed_at': ISO8601Format(attribute='security_event.closed_at'),
})

PUT_FEEDBACK = server.api.model('FEEDBACK', {
    'author': fields.String(description='User id of the feedback provider', default='anonymous'),
    'comments': fields.String(description='Feedback text'),
    'url': fields.String(description='Github Issue/PR/Commit absolute(fully qualified) URL'),
    'feedback_type': fields.String(description='Feedback type', enum=FeedBackType._member_names_),
    'identified_cve': fields.String(description='Actual CVE details if exists')
})
